# Plan: Nita's cleaning website (Rags To Riches Cleaning)

Status: planned, not built. Waiting on Nita's facts and photos (list at the bottom).

## What the reference reel shows (starry.intoai_, 24 Oct 2026, "Client paid $2000 for the website")

Brand shown: CLEARY, a cleaning company. Read from 17 seconds of screen recording:
1. **Hero:** a full-screen video of a cleaner in a bright high-rise flat, headline "Making Every Space Spotless", small nav, yellow call-to-action button.
2. **Scroll transition:** as you scroll, the video plays a foam burst that fills the whole screen, then clears to a new line over the same woman ("Professional Care. Visible Results.").
3. **Light airy sections:** "A little more clean. A lot more comfort." with three photo cards (Recurring Home Cleaning, Deep Cleaning, Move In / Move Out), then "Good cleaning is in the details", then "Results you can see. Comfort you can feel." with one photo that expands to full width.
4. **Close:** "A cleaner home in three easy steps" (Tell us what you need, Plan your cleaning, Enjoy a fresh start), an FAQ ("Your questions, answered"), and a contact form headed "A fresh home starts here".
Look: white and pale blue, one yellow accent, soft rounded cards, small clean type, generous space. The magic is the scroll-scrubbed hero video, not the layout.

## What we build for Nita (same feel, her brand, honest content)
- Brand: her pink and red (#c1185a) with white, pale blush and one dark ink. Light background, dark text (Theo's rule).
- **Hero:** scroll-driven. A foam and bubble burst drawn on a canvas (no video needed) that fills the screen as you scroll and clears to the next line. If Nita gives us a real before and after video or photos, they replace the drawn scene.
- Sections: services as three cards, "good cleaning is in the details" with her real photos, one image that expands on scroll, three steps, FAQ, and a "Book on WhatsApp" contact that opens Luna (her booking bot) with a pre-written message.
- Prices: Basic Clean R420 and Linen change R196 are the only real ones. Anything else stays out until Nita confirms.
- Stack: same as uncletsautomation (SvelteKit, GSAP, Lenis), own folder `apps/nitas-cleaning`, own Netlify preview, reduced-motion and no-script fallbacks.
- No fake testimonials, before-and-after claims or numbers.

## Research step (before building)
Mobbin public pages and Awwwards for cleaning, home-service and "fresh, clean" light sites. Save findings in `reference/research/`.

## What I need from Theo and Nita
1. Business name exactly as she wants it, and the suburbs she serves.
2. Her services and any prices beyond Basic Clean R420 and Linen R196.
3. Luna's WhatsApp number for the book button (never put Nita's personal number on the site).
4. 6 to 10 real photos (her team at work, results, before and after) with her permission, and a logo if she has one.
5. Anything she dislikes (colours, words).
