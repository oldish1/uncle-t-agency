# CHALES Hair Boutique website

The live site at chaleshairboutique.co.za. Plain HTML, hosted on Netlify (site `chaleshairboutique`, id `ba8f5769-00ef-41c8-bf9a-0892e8ce14bc`). It is not connected to Git, so deploys are uploads through the Netlify API.

`site/` is the exact set of files to upload. Before 20 Nov 2026 the only copy lived on Netlify. It was pulled down and saved here so it can't get lost.

## What's where

- `index.html` homepage, `/prices/`, and four service pages (`/nanoplastia/`, `/keratin-brazilian-blowout/`, `/hair-botox-glowtox/`, `/hair-colour-highlights/`)
- `/review/` is the post-visit rating page (kept out of Google on purpose)
- `llms.txt` plain summary for AI assistants (ChatGPT, Perplexity, Claude, Gemini)
- `robots.txt` lets every search engine and AI crawler in
- `<key>.txt` the IndexNow key, for pinging Bing and others when pages change
- Photos are `.webp` with descriptive names. The old `IMG-2026...jpg` files stay so old links don't break.

## Changing the site

Edit files in `site/`, then deploy the whole folder through the Netlify API (file-digest deploy). Do a draft deploy first, check the preview link, then publish.

`fix.py` and `home.py` are the one-off scripts used for the 20 Nov SEO pass, kept for reference.
