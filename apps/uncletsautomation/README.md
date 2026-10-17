# uncletsautomation (site)

Svelte site for uncletsautomation.co.za. Three views (Home dark, Studio light, Proof dark) swapped with a GSAP rolling transition, hash-linked (#home, #studio, #proof), plus a /privacy page.

- Run: `npm install`, then `npm run dev`
- Build: `npm run build` (static output in `dist/`)
- Deploy a preview: from the repo root, `bash scripts/deploy_netlify.sh apps/uncletsautomation`
- Text, prices and chat scripts: `src/lib/content.js`
- Motion helpers (reveals, parallax, reduced motion): `src/lib/motion.js`
- Views: `src/lib/views/`, page shell and transition: `src/routes/+page.svelte`
- Before launch: delete `static/_headers` (it hides the preview from Google), fill the yellow email and address placeholders in `ProofView.svelte` and `routes/privacy/+page.svelte`.
