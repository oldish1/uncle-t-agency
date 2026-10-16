#!/usr/bin/env bash
# Deploy a built static site to Netlify through its REST API.
# Usage: scripts/deploy_netlify.sh <project-dir> [site-name]
# Auth: the environment's proxy secret adds the Netlify token to api.netlify.com requests,
# so no token is needed here. Builds the project if it has a package.json, zips dist/,
# creates the site on first run (needs a name) and stores its id in <project-dir>/.netlify-site-id.
set -euo pipefail
dir="${1:?usage: deploy_netlify.sh <project-dir> [site-name]}"
name="${2:-}"
api=https://api.netlify.com/api/v1
cd "$dir"
if [ -f package.json ]; then npm install --no-audit --no-fund >/dev/null && npm run build; fi
[ -d dist ] || { echo "No dist/ folder to deploy"; exit 1; }
if [ ! -f .netlify-site-id ]; then
  [ -n "$name" ] || { echo "First deploy needs a site name"; exit 1; }
  curl -fsS -X POST "$api/sites" -H 'Content-Type: application/json' -d "{\"name\":\"$name\"}" \
    | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])' > .netlify-site-id
fi
id=$(cat .netlify-site-id)
rm -f /tmp/site.zip && (cd dist && zip -qr /tmp/site.zip .)
curl -fsS -X POST "$api/sites/$id/deploys" -H 'Content-Type: application/zip' --data-binary @/tmp/site.zip \
  | python3 -c 'import sys,json;d=json.load(sys.stdin);print("state:",d.get("state"));print("url:",d.get("ssl_url") or d.get("url"))'
