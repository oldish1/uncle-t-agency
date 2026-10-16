#!/usr/bin/env bash
# Deploy a built static site to Netlify.
# Usage: scripts/deploy_netlify.sh <project-dir> [site-name]
# Needs NETLIFY_AUTH_TOKEN in the environment. Builds the project if it has a package.json,
# then deploys <project-dir>/dist. First run creates the site; later runs update it.
set -euo pipefail
dir="${1:?usage: deploy_netlify.sh <project-dir> [site-name]}"
name="${2:-}"
: "${NETLIFY_AUTH_TOKEN:?NETLIFY_AUTH_TOKEN is not set (see reference/ or ask Theo)}"
cd "$dir"
if [ -f package.json ]; then npm install --no-audit --no-fund >/dev/null && npm run build; fi
state=".netlify/state.json"
if [ ! -f "$state" ]; then
  [ -n "$name" ] || { echo "First deploy needs a site name"; exit 1; }
  npx --yes netlify-cli sites:create --name "$name" >/dev/null
  npx --yes netlify-cli link --name "$name" >/dev/null
fi
npx --yes netlify-cli deploy --dir=dist --prod
