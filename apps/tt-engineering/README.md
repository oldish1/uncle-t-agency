# T & T Engineering: pitch mockup

Static site (no build step). Open `index.html`, or drag this whole folder onto Netlify (app.netlify.com/drop).

## What's in it
- Hero: "CUT [live machine strip] BEND." The strip loops a laser cutting a part, then a press brake bending it.
- Scroll section: scrolling runs the laser (holes, then outline, with sparks), then the press brake folds the part to 90 degrees. The two buttons jump between them.
- Work rows, stats, contact and a big phone-number footer.
- Fully responsive, respects reduced-motion settings, self-hosted font (Archivo, SIL OFL).

## Before this goes to the client as final
- **Real photos and footage.** All pictures are drawn in code. Swap in the shop's own photos, and a short phone clip of the laser and press brake, as the hero strip and the scroll section (see the comment at the top of `app.js`). Do not use YouTube clips on the live site: copyright. Use the shop's own footage.
- **Confirm facts with the client.** Business name ("T & T Engineering"), phone numbers, email and address were taken from their current site. Machine specs (laser power, bed size, press brake tonnage, materials and thicknesses) are deliberately not stated: add them once known.
- Page title and copy say "Lansdowne, Cape Town" (6 Windsor Road). Check that is right.


## v4 (17 Oct): real footage build
- Clips in `public/media/` (laser.mp4, brake.mp4, bend.mp4 plus poster jpgs) are cut from **JFY's own promo videos**, not TNT's machines. Fine for a mock-up. Before launch, get permission from JFY or their local dealer, or replace them with the shop's own footage (same file names, update `manifest.json`).
- Do not claim the clip's details (TruDisk, 16 mm mild steel) for TNT's machine. The site only states what Theo confirmed: 6 kW JFY laser, 150 ton 3 m JFY press brake.
- Hero plays the laser clip. The pinned machines section scrubs the laser then the press brake with scroll. Reduced-motion users get posters.
- Type: Inter 500, small and tight. Check at 390 and 1440 px before shipping.
- 17 Oct update: clips contain no people. Laser = cutting with sparks (9.5 to 19.5 s of the source). Brake = dark machine close-ups crossfading into a finished folded part (the source has no hands-free bend shot; the real bend only appears with hands). The folded sample part carries a small JFY etch.
