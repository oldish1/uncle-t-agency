"""Builds the CHALES treatment pages and price list from the data below.

Run from apps/chales-site:  python3 build_pages.py
Writes <slug>/index.html for each page, plus sitemap.xml and robots.txt.
Edit prices, answers or photos here, then run it again. Never edit the generated pages by hand.
"""
import html, json, os, urllib.parse

SITE = "https://chaleshairboutique.co.za"
LEXI = "https://wa.me/27714296057"
CHANTE_TEL = "+27814332756"
CHANTE_SHOW = "081 433 2756"
MAPS = "https://maps.google.com/?cid=13659620552899745009"
ADDRESS = "46 Alexandra Street, Oakdale, Bellville"
INSIDE = "Inside the Vodacom building"
UPDATED = "November 2026"

def lexi_link(text):
    return LEXI + "?text=" + urllib.parse.quote(text)

# ---------------------------------------------------------------- content
TREATMENTS = [
    {
        "slug": "nanoplastia",
        "nav": "Nanoplastia",
        "title": "Nanoplastia in Bellville, Cape Town | CHALES Hair Boutique",
        "desc": "Formaldehyde-free Nanoplastia smoothing in Oakdale, Bellville. R1 800 short to medium, R2 200 long. Book with Lexi on WhatsApp.",
        "h1": "Nanoplastia in Bellville",
        "lead": "Formaldehyde-free smoothing that leaves hair soft, glossy and easy to style for months. Done by Chanté at CHALES in Oakdale, Bellville.",
        "service": "Nanoplastia",
        "options": [("Short / medium", "R1 800"), ("Long", "R2 200")],
        "about": "Nanoplastia smooths frizz and calms volume using plant-based ingredients instead of formaldehyde. Hair dries faster, blow-dries in half the time and keeps a natural shine, without the flat, poker-straight look. It suits anyone who wants smoother hair but has been put off keratin by the fumes.",
        "facts": [
            ("In the chair", "About 2 to 3 hours"),
            ("How long it lasts", "Usually 3 to 5 months, with sulphate-free shampoo"),
            ("Formaldehyde", "None"),
            ("Price", "R1 800 short to medium, R2 200 long"),
        ],
        "photos": ["IMG-20260221-WA0108.jpg", "IMG-20260221-WA0111.jpg", "IMG-20260221-WA0112.jpg", "IMG-20260221-WA0109.jpg"],
        "hero": "IMG-20260221-WA0111.jpg",
        "hero_alt": "Long, smooth, glossy hair after a smoothing treatment at CHALES Hair Boutique, Bellville",
        "prices": [("Nanoplastia, short / medium", "R1 800"), ("Nanoplastia, long", "R2 200"), ("Extra length surcharge", "From R100")],
        "faq": [
            ("How much is Nanoplastia in Cape Town?", "At CHALES it's R1 800 for short to medium hair and R2 200 for long hair. Very long or very thick hair can carry a surcharge from R100. Chanté confirms your price before she starts."),
            ("How long does Nanoplastia last?", "Usually 3 to 5 months. It depends on your hair and how you look after it. Washing with a sulphate-free shampoo helps it last longer."),
            ("Nanoplastia or keratin, which is better?", "Both smooth frizz. Nanoplastia is formaldehyde-free and gives a softer, more natural finish. Keratin gives a sleeker, straighter result. Not sure which suits your hair? Ask Chanté for a consultation on WhatsApp."),
            ("Can I do Nanoplastia on coloured hair?", "In most cases, yes. Tell Chanté what's been done to your hair recently (colour, bleach, relaxer) so she can check it first."),
            ("How long does the appointment take?", "Plan for 2 to 3 hours, depending on the length and thickness of your hair."),
        ],
    },
    {
        "slug": "keratin-brazilian-blowout",
        "nav": "Keratin & Brazilian",
        "title": "Keratin & Brazilian Blowout in Bellville | CHALES Hair Boutique",
        "desc": "Keratin treatment and Brazilian blowout in Oakdale, Bellville, Cape Town. From R1 500. Smooth, frizz-free hair. Book with Lexi on WhatsApp.",
        "h1": "Keratin in Bellville",
        "lead": "Smooth, frizz-free hair that's quicker to style, for weeks at a time. Keratin and Brazilian blowout treatments at CHALES in Oakdale, Bellville.",
        "service": "Keratin or Brazilian blowout",
        "options": [("Short / medium", "R1 500"), ("Long", "R1 800")],
        "about": "Both treatments seal smoothness and shine into the hair. A Brazilian blowout softens frizz and adds gloss while keeping some movement. A keratin treatment gives a sleeker, straighter finish and suits thick or very frizzy hair. Either way, mornings get a lot shorter.",
        "facts": [
            ("In the chair", "About 2 to 3 hours"),
            ("How long it lasts", "Brazilian about 10 to 12 weeks, keratin up to 3 to 4 months"),
            ("Best for", "Frizz, humidity and hair that takes forever to blow dry"),
            ("Price", "R1 500 short to medium, R1 800 long"),
        ],
        "photos": ["IMG-20260221-WA0082.jpg", "IMG-20260221-WA0083.jpg", "IMG-20260221-WA0084.jpg", "IMG-20260221-WA0110.jpg"],
        "hero": "IMG-20260221-WA0082.jpg",
        "hero_alt": "Sleek, shiny bob after a smoothing treatment at CHALES Hair Boutique, Bellville",
        "prices": [("Keratin treatment, short / medium", "R1 500"), ("Keratin treatment, long", "R1 800"), ("Brazilian blowout, short / medium", "R1 500"), ("Brazilian blowout, long", "R1 800"), ("Extra length surcharge", "From R100")],
        "faq": [
            ("How much is a keratin treatment in Cape Town?", "At CHALES a keratin treatment or a Brazilian blowout is R1 500 for short to medium hair and R1 800 for long hair."),
            ("What's the difference between keratin and a Brazilian blowout?", "A Brazilian blowout keeps more movement and body. Keratin gives a straighter, sleeker result and lasts a bit longer. Chanté will recommend one once she's seen your hair."),
            ("How long does a keratin treatment last?", "Up to 3 to 4 months for keratin and about 10 to 12 weeks for a Brazilian blowout, depending on your hair and aftercare."),
            ("Should I colour before or after?", "Colour first, smooth after is the usual order. Mention it when you book and Chanté will plan the two appointments."),
            ("Is there a formaldehyde-free option?", "Yes. Nanoplastia is a formaldehyde-free smoothing treatment, also done at CHALES."),
        ],
    },
    {
        "slug": "hair-botox-glowtox",
        "nav": "Botox & Glowtox",
        "title": "Hair Botox & Glowtox in Bellville | CHALES Hair Boutique",
        "desc": "Hair botox and Glowtox deep repair treatments in Oakdale, Bellville, Cape Town. From R1 200. No needles. Book with Lexi on WhatsApp.",
        "h1": "Hair Botox in Bellville",
        "lead": "Deep repair for dry, damaged or over-coloured hair. No needles, just softness, body and shine. Hair botox and Glowtox at CHALES in Oakdale, Bellville.",
        "service": "Hair Botox",
        "options": [("Botox, short / medium", "R1 200"), ("Botox, long", "R1 500"), ("Glowtox", "R1 400")],
        "about": "Hair botox has nothing to do with injections. It's a deep-conditioning treatment that fills in damaged, porous strands so hair looks fuller, feels softer and shines again. Glowtox is the version built for maximum shine. Both keep more of your natural texture than a smoothing treatment does.",
        "facts": [
            ("In the chair", "About 1.5 to 2.5 hours"),
            ("How long it lasts", "Usually 2 to 3 months"),
            ("Best for", "Dry, brittle, bleached or heat-damaged hair"),
            ("Price", "Botox from R1 200, Glowtox R1 400"),
        ],
        "photos": ["IMG-20260221-WA0113.jpg", "IMG-20260221-WA0083.jpg", "IMG-20260221-WA0115.jpg", "IMG-20260221-WA0084.jpg"],
        "hero": "IMG-20260221-WA0113.jpg",
        "hero_alt": "Soft, healthy-looking brown hair after treatment at CHALES Hair Boutique, Bellville",
        "prices": [("Hair botox, short / medium", "R1 200"), ("Hair botox, long", "R1 500"), ("Glowtox", "R1 400"), ("Olaplex treatment", "R350"), ("Deep conditioning mask", "R200")],
        "faq": [
            ("Is hair botox the same as Botox injections?", "No. There are no needles and nothing goes into your skin. It's a conditioning treatment applied to the hair, named for the way it fills and plumps damaged strands."),
            ("How much is hair botox in Cape Town?", "At CHALES it's R1 200 for short to medium hair, R1 500 for long hair, and Glowtox is R1 400."),
            ("How long does hair botox last?", "Usually 2 to 3 months, depending on how often you wash and heat-style your hair."),
            ("Hair botox or keratin?", "Botox repairs and conditions while keeping your natural texture. Keratin is for smoothing and straightening. If your main problem is damage rather than frizz, botox is usually the place to start."),
            ("Can I have it on bleached hair?", "Yes, bleached and coloured hair is often where it helps most. Tell Chanté what's been done recently so she can check your hair first."),
        ],
    },
    {
        "slug": "hair-colour-highlights",
        "nav": "Colour & Highlights",
        "title": "Hair Colour, Highlights & Balayage in Bellville | CHALES",
        "desc": "Hair colour, highlights, balayage and root touch-ups in Oakdale, Bellville, Cape Town. Highlights from R650. Book with Lexi on WhatsApp.",
        "h1": "Hair Colour in Bellville",
        "lead": "Full colour, highlights, balayage and root touch-ups, matched to your skin tone and kept looking fresh between visits. At CHALES in Oakdale, Bellville.",
        "service": "Hair colour",
        "options": [("Root touch-up", "R450"), ("Half head highlights", "R650"), ("Full colour, short / medium", "R650"), ("Full head highlights", "R950"), ("Balayage", "R1 200")],
        "about": "Chanté mixes each colour for the person in the chair, from rich burgundies and warm browns to soft highlights and balayage. She'll tell you honestly what's possible in one sitting and what needs a second visit, so your hair stays healthy on the way there.",
        "facts": [
            ("In the chair", "From 1 hour for roots to about 3 hours for balayage"),
            ("Root touch-ups", "Every 4 to 6 weeks keeps it seamless"),
            ("Creative colour", "Priced on consultation"),
            ("Price", "Highlights from R650, full colour from R650"),
        ],
        "photos": ["IMG-20260221-WA0079.jpg", "IMG-20260221-WA0081.jpg", "chante-work.jpg", "IMG-20260221-WA0114.jpg"],
        "hero": "IMG-20260221-WA0080.jpg",
        "hero_alt": "Deep burgundy hair colour being finished in the chair at CHALES Hair Boutique, Bellville",
        "prices": [("Root touch-up", "R450"), ("Root touch-up + blow dry", "R650"), ("Toner", "R300"), ("Half head highlights", "R650"), ("Full head highlights", "R950"), ("Highlights + blow dry", "From R950"), ("Balayage", "R1 200"), ("Balayage & toner", "R1 500"), ("Full colour, short / medium", "R650"), ("Full colour, long", "R850"), ("Full colour + blow dry", "From R900"), ("Fashion / creative colour", "On consultation")],
        "faq": [
            ("How much are highlights in Cape Town?", "At CHALES half head highlights are R650, full head highlights R950, and balayage R1 200 (R1 500 with a toner)."),
            ("How often do I need a root touch-up?", "Every 4 to 6 weeks for most people. A root touch-up is R450, or R650 with a blow dry."),
            ("Balayage or highlights?", "Highlights are placed in fine, even sections for an all-over lift. Balayage is painted on by hand for a softer, grown-out look that needs fewer touch-ups."),
            ("Can I go much lighter in one visit?", "It depends on your starting colour and your hair's condition. Chanté will tell you straight at your consultation, and may split it over two visits to protect your hair."),
            ("Can I colour and smooth my hair?", "Yes. Colour first, then a smoothing treatment like Nanoplastia or keratin. Chanté can plan both."),
        ],
    },
]

PRICE_GROUPS = [
    ("Hair care", None, [("Wash & blow dry, short / medium", "R250 to R300"), ("Wash & blow dry, long", "R350"), ("Trim", "R200"), ("Fringe trim", "R80"), ("Precision cut", "R350"), ("Cut & blow dry", "R450"), ("Basin treatment", "R150")]),
    ("Colour & highlights", "hair-colour-highlights", [("Root touch-up", "R450"), ("Root touch-up + blow dry", "R650"), ("Toner", "R300"), ("Half head highlights", "R650"), ("Full head highlights", "R950"), ("Highlights + blow dry", "From R950"), ("Balayage", "R1 200"), ("Balayage & toner", "R1 500"), ("Full colour, short / medium", "R650"), ("Full colour, long", "R850"), ("Full colour + blow dry", "From R900"), ("Fashion / creative colour", "On consultation")]),
    ("Smoothing", "nanoplastia", [("Nanoplastia, short / medium", "R1 800"), ("Nanoplastia, long", "R2 200"), ("Keratin treatment, short / medium", "R1 500"), ("Keratin treatment, long", "R1 800"), ("Brazilian blowout, short / medium", "R1 500"), ("Brazilian blowout, long", "R1 800")]),
    ("Repair treatments", "hair-botox-glowtox", [("Hair botox, short / medium", "R1 200"), ("Hair botox, long", "R1 500"), ("Glowtox", "R1 400"), ("Olaplex treatment", "R350"), ("Deep conditioning mask", "R200"), ("Scalp treatment", "R250"), ("Gloss / glaze", "R350")]),
    ("Monthly contracts", None, [("Wash & blow dry contract, 4 visits a month", "R900"), ("Cut & style contract, monthly", "R550"), ("Colour maintenance contract, root + blow dry", "R1 100"), ("Treatment contract, monthly deep treatment", "R400"), ("VIP full package, colour + cut + blow dry", "From R1 500"), ("Extra length surcharge (any service)", "From R100")]),
]

# ---------------------------------------------------------------- shared pieces
CSS = """
:root{--ground:#252522;--ground-2:#2e2e2b;--ground-3:#363633;--ink:#F5F0E8;--ink-2:#cfc8bb;--gold:#C9A84C;--gold-hi:#E8C96A;--on-gold:#1d1d1a;
--serif:'Cormorant Garamond',Georgia,serif;--sans:'Montserrat',system-ui,sans-serif;--edge:clamp(16px,4vw,48px);--gap:clamp(88px,10vw,150px)}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{background:var(--ground);color:var(--ink);font-family:var(--sans);font-size:17px;line-height:1.55;overflow-x:hidden}
img{display:block;max-width:100%}
a{color:inherit}
:focus-visible{outline:2px solid var(--gold-hi);outline-offset:3px}
.bar{position:sticky;top:0;z-index:20;background:var(--ground);display:flex;align-items:center;justify-content:space-between;gap:24px;padding:14px var(--edge)}
.mark{font-family:var(--serif);font-weight:600;font-size:1.7rem;letter-spacing:.28em;color:var(--gold);text-decoration:none}
.bar nav{display:flex;gap:28px;align-items:center}
.bar nav a{text-decoration:none;font-size:15px;color:var(--ink-2);transition:color .2s}
.bar nav a:hover{color:var(--gold)}
.bar nav a.btn{color:var(--on-gold)}
.bar nav a.btn:hover{color:var(--on-gold)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;background:var(--gold);color:var(--on-gold);font-family:var(--sans);font-weight:600;font-size:15px;text-decoration:none;padding:16px 26px;border:0;cursor:pointer;transition:background .2s,transform .15s}
.btn:hover{background:var(--gold-hi)}
.btn:active{transform:scale(.97)}
.btn.small{padding:11px 18px;font-size:15px}
.btn.dark{background:var(--ground);color:var(--ink)}
.btn.dark:hover{background:var(--ground-3)}
h1,h2{font-family:var(--serif);font-weight:400;letter-spacing:-.02em;line-height:.98}
h1{font-size:clamp(3.1rem,8.2vw,7.6rem)}
h2{font-size:clamp(2.4rem,5vw,4.6rem)}
.hero{display:grid;grid-template-columns:1.15fr .85fr;min-height:calc(100vh - 70px)}
.hero-text{padding:clamp(40px,7vw,110px) var(--edge) 64px;display:flex;flex-direction:column;justify-content:center;gap:28px}
.hero-text h1{color:var(--gold);max-width:11em}
.lead{font-size:clamp(1.1rem,1.6vw,1.35rem);max-width:34em}
.hero-pic{position:relative;overflow:hidden;min-height:60vh}
.hero-pic img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform-origin:50% 40%}
.picker{display:flex;flex-direction:column;gap:14px}
.picker p{font-size:15px;color:var(--ink-2)}
.choices{display:flex;flex-wrap:wrap;gap:8px}
.choices label{cursor:pointer}
.choices input{position:absolute;opacity:0;pointer-events:none}
.choices span{display:inline-block;padding:10px 16px;background:var(--ground-3);font-size:15px;transition:background .2s,color .2s}
.choices input:checked+span{background:var(--ink);color:var(--ground)}
.choices input:focus-visible+span{outline:2px solid var(--gold-hi);outline-offset:2px}
.choices label:hover span{background:#45453f}
.choices input:checked+span:hover{background:var(--ink)}
.quote{display:flex;flex-wrap:wrap;align-items:center;gap:20px 28px}
.price{font-family:var(--serif);font-size:clamp(3rem,5vw,4.4rem);line-height:1;color:var(--ink)}
.aside{font-size:15px;color:var(--ink-2)}
.aside a{color:var(--ink)}
.about{background:var(--ground-2);padding:var(--gap) var(--edge);display:grid;grid-template-columns:1.2fr .8fr;gap:clamp(40px,7vw,120px);align-items:start;margin-top:0}
.about .body{margin-top:24px;max-width:36em;font-size:17px}
.statement{font-family:var(--serif);font-size:clamp(1.4rem,2.6vw,2.25rem);line-height:1.25;max-width:22em}
.facts{display:grid;gap:26px}
.facts dt{font-size:15px;color:var(--gold)}
.facts dd{font-size:clamp(1.1rem,1.4vw,1.25rem)}
.work{padding:var(--gap) 0 0}
.work h2{padding:0 var(--edge);margin-bottom:40px}
.strip{display:grid;grid-template-columns:repeat(5,1fr);gap:6px}
.strip img,.strip video{width:100%;height:clamp(280px,30vw,460px);object-fit:cover;display:block}
.work .note{padding:18px var(--edge) 0;font-size:15px;color:var(--ink-2)}
.prices{padding:var(--gap) var(--edge);display:grid;grid-template-columns:.8fr 1.2fr;gap:clamp(40px,6vw,100px)}
table{width:100%;border-collapse:collapse;font-size:clamp(1.1rem,1.4vw,1.25rem)}
td{padding:16px 0;border-bottom:1px solid #45453f;vertical-align:top}
td:last-child{text-align:right;white-space:nowrap;padding-left:20px;color:var(--gold);font-variant-numeric:tabular-nums}
.prices .aside{margin-top:22px}
.faq{background:var(--ground-2);padding:var(--gap) var(--edge);display:grid;grid-template-columns:.8fr 1.2fr;gap:clamp(40px,6vw,100px)}
details{background:var(--ground-3);margin-bottom:8px}
summary{cursor:pointer;list-style:none;padding:22px 24px;font-size:clamp(1.1rem,1.4vw,1.25rem);font-weight:500;display:flex;justify-content:space-between;gap:16px;transition:color .2s}
summary::-webkit-details-marker{display:none}
summary::after{content:'+';color:var(--gold);font-size:1.4em;line-height:1}
details[open] summary::after{content:'\\2212'}
summary:hover{color:var(--gold-hi)}
details p{padding:0 24px 24px;max-width:40em}
.visit{background:var(--gold);color:var(--on-gold);padding:var(--gap) var(--edge);display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:end}
.visit h2{color:var(--on-gold)}
.visit .addr{font-family:var(--serif);font-size:clamp(1.35rem,2.4vw,2.25rem);line-height:1.2;margin-top:24px}
.visit .hours{font-size:17px;margin-top:18px;line-height:1.6}
.visit .inside{font-size:17px;font-weight:600;margin-top:10px}
.visit .acts{display:flex;flex-wrap:wrap;gap:12px;justify-self:end}
.visit .acts a.plain{padding:16px 6px;font-weight:600;text-decoration:underline;text-underline-offset:4px}
.more{padding:var(--gap) var(--edge) 40px}
.more h2{margin-bottom:28px}
.more ul{list-style:none}
.more li a{display:flex;justify-content:space-between;align-items:baseline;gap:20px;text-decoration:none;font-family:var(--serif);font-size:clamp(2rem,4.4vw,3.8rem);line-height:1.15;padding:10px 0;transition:color .2s,transform .25s}
.more li a:hover{color:var(--gold);transform:translateX(8px)}
footer{padding:60px var(--edge) 28px}
footer .big{font-family:var(--serif);color:var(--gold);font-size:clamp(4.5rem,19vw,17rem);letter-spacing:.12em;line-height:.85;font-weight:300}
footer .line{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px 30px;margin-top:28px;font-size:15px;color:var(--ink-2)}
footer .line a{text-decoration:none}
footer .line a:hover{color:var(--gold)}
.cats{display:flex;flex-wrap:wrap;gap:8px}
.cats a{padding:10px 16px;background:var(--ground-3);text-decoration:none;font-size:15px;transition:background .2s}
.cats a:hover{background:#45453f}
.group{padding:var(--gap) var(--edge) 0;display:grid;grid-template-columns:.8fr 1.2fr;gap:clamp(40px,6vw,100px)}
.group:nth-of-type(even){background:var(--ground-2);padding-bottom:var(--gap)}
.group .aside{margin-top:18px}
.list-hero{padding:clamp(56px,9vw,140px) var(--edge) 40px;display:grid;grid-template-columns:1.2fr .8fr;gap:40px;align-items:end}
.list-hero h1{color:var(--gold)}
.list-hero .side{display:flex;flex-direction:column;gap:22px}
.list-pics{display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:6px;margin-top:20px}
.list-pics img,.list-pics video{display:block;width:100%;height:clamp(240px,34vw,520px);object-fit:cover}
.js .rise{opacity:0;transform:translateY(24px);transition:opacity .7s cubic-bezier(.2,.7,.2,1),transform .7s cubic-bezier(.2,.7,.2,1)}
.js .rise.in{opacity:1;transform:none}
.js .hero-pic img{animation:drift 18s ease-out both}
@keyframes drift{from{transform:scale(1.12)}to{transform:scale(1)}}
@media (prefers-reduced-motion:reduce){.js .rise{opacity:1;transform:none;transition:none}.js .hero-pic img{animation:none}.more li a:hover{transform:none}}
@media (max-width:900px){
 .bar nav a.hide-s{display:none}
 .hero{grid-template-columns:1fr;min-height:0}
 .hero-pic{order:-1;min-height:40vh}
 .hero-text{padding-top:40px}
 .about,.prices,.faq,.group,.list-hero{grid-template-columns:1fr}
 .visit{grid-template-columns:1fr}.visit .acts{justify-self:start}
 .strip{grid-template-columns:1fr 1fr}.strip video{grid-column:1/-1}
 .list-pics{grid-template-columns:1fr 1fr}.list-pics img:first-child{grid-column:1/-1}
}
@media (max-width:520px){.bar nav{gap:14px}.bar nav a{font-size:14px}.mark{font-size:1.35rem}.btn.small{padding:10px 14px}}
"""

JS = """
document.documentElement.classList.add('js');
addEventListener('DOMContentLoaded',()=>{
  const els=[...document.querySelectorAll('.rise')];
  if(!('IntersectionObserver' in window)){els.forEach(e=>e.classList.add('in'));return}
  const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
  els.forEach((e,i)=>{e.style.transitionDelay=((+e.dataset.d||0)*75)+'ms';io.observe(e)});
  const pk=document.querySelector('[data-picker]');
  if(pk){const out=document.querySelector('[data-price]'),bk=document.querySelector('[data-book]'),svc=pk.dataset.service;
    pk.addEventListener('change',ev=>{const i=ev.target;out.textContent=i.dataset.price;
      bk.href='https://wa.me/27714296057?text='+encodeURIComponent("Hi Lexi! I'd like to book "+svc+" ("+i.value+") at CHALES Hair Boutique.");});}
});
"""

def esc(s): return html.escape(s, quote=True)

def head(title, desc, path, schema):
    url = SITE + path
    return f"""<!DOCTYPE html>
<html lang="en-ZA">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/IMG-20260221-WA0079.jpg">
<meta name="geo.region" content="ZA-WC"><meta name="geo.placename" content="Bellville, Cape Town">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Montserrat:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script>{JS}</script>
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body>
<header class="bar">
  <a class="mark" href="/" aria-label="CHALES Hair Boutique home">CHALES</a>
  <nav aria-label="Main">
    <a class="hide-s" href="/#services">Treatments</a>
    <a href="/prices/">Prices</a>
    <a class="hide-s" href="#find-us">Find us</a>
    <a class="btn small" href="{lexi_link("Hi Lexi! I'd like to book an appointment at CHALES Hair Boutique.")}">Book with Lexi</a>
  </nav>
</header>
<main>
"""

SALON = {
    "@type": "HairSalon", "@id": SITE + "/#salon", "name": "CHALES Hair Boutique", "url": SITE,
    "telephone": "+27 81 433 2756", "email": "info@chaleshairboutique.co.za", "priceRange": "R80 - R2200",
    "image": SITE + "/IMG-20260221-WA0079.jpg",
    "address": {"@type": "PostalAddress", "streetAddress": "46 Alexandra Street (inside the Vodacom building)", "addressLocality": "Bellville", "addressRegion": "Western Cape", "postalCode": "7530", "addressCountry": "ZA"},
    "geo": {"@type": "GeoCoordinates", "latitude": -33.8940119, "longitude": 18.6294225},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "16:30"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "15:00"}],
    "hasMap": MAPS, "areaServed": ["Bellville", "Oakdale", "Parow", "Goodwood", "Durbanville", "Cape Town"],
    "sameAs": ["https://www.tiktok.com/@chales418", "https://www.instagram.com/chaleshairboutique", "https://www.facebook.com/chaleshairboutique"],
}

def visit_block():
    return f"""
<section class="visit" id="find-us">
  <div>
    <h2 class="rise">Find CHALES</h2>
    <p class="addr rise" data-d="1">{ADDRESS},<br>Cape Town 7530</p>
    <p class="inside rise" data-d="2">{INSIDE}. Look for the Vodacom sign, CHALES is inside.</p>
    <p class="hours rise" data-d="3">Tuesday to Friday 08:00 to 16:30<br>Saturday 09:00 to 15:00<br>Sunday and Monday closed</p>
  </div>
  <div class="acts rise" data-d="4">
    <a class="btn dark" href="{lexi_link("Hi Lexi! I'd like to book an appointment at CHALES Hair Boutique.")}">Book with Lexi</a>
    <a class="plain" href="{MAPS}">Get directions</a>
    <a class="plain" href="tel:{CHANTE_TEL}">Call Chanté</a>
  </div>
</section>"""

def footer(current):
    links = "".join(f'<a href="/{t["slug"]}/">{esc(t["nav"])}</a>' for t in TREATMENTS if t["slug"] != current)
    return f"""
</main>
<footer>
  <p class="big" aria-hidden="true">CHALES</p>
  <div class="line">
    <span>CHALES Hair Boutique, {ADDRESS}. {INSIDE}.</span>
    <span>{links}<a href="/prices/">Prices</a></span>
    <span><a href="https://www.tiktok.com/@chales418">TikTok</a> &nbsp; <a href="https://www.facebook.com/chaleshairboutique">Facebook</a></span>
  </div>
</footer>
</body>
</html>
"""

def treatment_page(t):
    path = f"/{t['slug']}/"
    first_label, first_price = t["options"][0]
    schema = {"@context": "https://schema.org", "@graph": [
        SALON,
        {"@type": "Service", "name": t["nav"], "serviceType": t["nav"], "provider": {"@id": SALON["@id"]},
         "areaServed": "Bellville, Cape Town", "url": SITE + path, "description": t["desc"],
         "offers": [{"@type": "Offer", "name": n, "priceCurrency": "ZAR", "price": p.replace("From ", "").replace("R", "").replace(" ", "")} for n, p in t["prices"] if p[0] in "RF" and "R" in p]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "CHALES Hair Boutique", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": t["nav"], "item": SITE + path}]},
    ]}
    radios = "".join(
        f'<label><input type="radio" name="opt" value="{esc(l)}" data-price="{esc(p)}"{" checked" if i == 0 else ""}><span>{esc(l)}</span></label>'
        for i, (l, p) in enumerate(t["options"]))
    facts = "".join(f'<div class="rise" data-d="{i}"><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for i, (a, b) in enumerate(t["facts"]))
    strip = "".join(f'<img class="rise" data-d="{i}" src="/{p}" alt="Hair by Chanté at CHALES Hair Boutique, Bellville" loading="lazy" width="1200" height="1600">' for i, p in enumerate(t["photos"]))
    rows = "".join(f"<tr><td>{esc(n)}</td><td>{esc(p)}</td></tr>" for n, p in t["prices"])
    faq = "".join(f'<details class="rise" data-d="{i}"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for i, (q, a) in enumerate(t["faq"]))
    others = [x for x in TREATMENTS if x["slug"] != t["slug"]]
    more = "".join(f'<li class="rise" data-d="{i}"><a href="/{o["slug"]}/">{esc(o["nav"])}</a></li>' for i, o in enumerate(others))
    book_text = f"Hi Lexi! I'd like to book {t['service']} ({first_label}) at CHALES Hair Boutique."
    body = f"""
<section class="hero">
  <div class="hero-text">
    <h1 class="rise">{esc(t['h1'])}</h1>
    <p class="lead rise" data-d="1">{esc(t['lead'])}</p>
    <div class="picker rise" data-d="2" data-picker data-service="{esc(t['service'])}">
      <div class="quote">
        <span class="price" data-price aria-live="polite">{esc(first_price)}</span>
        <a class="btn" data-book href="{lexi_link(book_text)}">Book this with Lexi</a>
      </div>
      <div class="choices" role="radiogroup" aria-label="Pick an option to see its price">{radios}</div>
    </div>
    <p class="aside rise" data-d="3">Lexi books you in on WhatsApp, day or night. Questions first? WhatsApp Chanté on <a href="https://wa.me/27814332756">{CHANTE_SHOW}</a>.</p>
  </div>
  <div class="hero-pic"><img src="/{t['hero']}" alt="{esc(t['hero_alt'])}" width="1200" height="1600" fetchpriority="high"></div>
</section>

<section class="about">
  <div><p class="statement rise">{esc(t['about'].split('. ',1)[0])}.</p>
  <p class="body rise" data-d="1">{esc(t['about'].split('. ',1)[1])}</p></div>
  <dl class="facts">{facts}</dl>
</section>

<section class="work">
  <h2 class="rise">From Chanté's chair</h2>
  <div class="strip">{strip}<video class="rise" data-d="4" src="/WhatsApp%20Video%202026-06-29%20at%2008.17.17.mp4" poster="/{t['photos'][0]}" muted loop playsinline autoplay preload="metadata" aria-label="Inside CHALES Hair Boutique"></video></div>
  <p class="note">Real clients at CHALES, Oakdale, Bellville.</p>
</section>

<section class="prices">
  <div>
    <h2 class="rise">{esc(t['nav'])} prices</h2>
    <p class="aside rise" data-d="1">Prices in rand, updated {UPDATED}. Card, cash and EFT. <a href="/prices/">See every price</a>.</p>
  </div>
  <table class="rise" data-d="1"><tbody>{rows}</tbody></table>
</section>

<section class="faq">
  <h2 class="rise">Questions people ask</h2>
  <div>{faq}</div>
</section>
{visit_block()}
<section class="more">
  <h2 class="rise">Other treatments</h2>
  <ul>{more}<li class="rise" data-d="4"><a href="/prices/">Full price list</a></li></ul>
</section>
"""
    return head(t["title"], t["desc"], path, schema) + body + footer(t["slug"])

def prices_page():
    path = "/prices/"
    schema = {"@context": "https://schema.org", "@graph": [
        SALON,
        {"@type": "OfferCatalog", "name": "CHALES Hair Boutique price list", "url": SITE + path,
         "itemListElement": [{"@type": "Offer", "name": n, "priceCurrency": "ZAR", "price": p.replace("From ", "").replace("R", "").replace(" ", "").split("to")[0]} for _, _, rows in PRICE_GROUPS for n, p in rows if p.startswith(("R", "From R"))]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "CHALES Hair Boutique", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Prices", "item": SITE + path}]},
    ]}
    def gid(name): return name.lower().replace(" & ", "-").replace(" ", "-")
    cats = "".join(f'<a href="#{gid(g)}">{esc(g)}</a>' for g, _, _ in PRICE_GROUPS)
    groups = ""
    for g, link, rows in PRICE_GROUPS:
        trs = "".join(f"<tr><td>{esc(n)}</td><td>{esc(p)}</td></tr>" for n, p in rows)
        extra = ""
        if link:
            names = {"hair-colour-highlights": "colour and highlights", "nanoplastia": "Nanoplastia", "hair-botox-glowtox": "hair botox and Glowtox"}
            extra = f'<p class="aside rise" data-d="1"><a href="/{link}/">All about {names[link]}</a>'
            if link == "nanoplastia":
                extra += ' &middot; <a href="/keratin-brazilian-blowout/">Keratin &amp; Brazilian</a>'
            extra += "</p>"
        if g == "Monthly contracts":
            extra = '<p class="aside rise" data-d="1">For regulars. Ask Chanté for a package built around how often you come in.</p>'
        groups += f'<section class="group" id="{gid(g)}"><div><h2 class="rise">{esc(g)}</h2>{extra}</div><table class="rise" data-d="1"><tbody>{trs}</tbody></table></section>'
    body = f"""
<section class="list-hero">
  <div>
    <h1 class="rise">CHALES price list</h1>
  </div>
  <div class="side">
    <p class="lead rise" data-d="1">Every service at CHALES Hair Boutique in Oakdale, Bellville, in rand. Updated {UPDATED}. Card, cash and EFT.</p>
    <div class="cats rise" data-d="2">{cats}</div>
    <div class="rise" data-d="3"><a class="btn" href="{lexi_link("Hi Lexi! I'd like to book an appointment at CHALES Hair Boutique.")}">Book with Lexi</a></div>
  </div>
</section>
<div class="list-pics">
  <img src="/IMG-20260221-WA0080.jpg" alt="Burgundy colour finished at CHALES Hair Boutique, Bellville" width="1200" height="1600">
  <img src="/IMG-20260221-WA0108.jpg" alt="Long smooth hair after a smoothing treatment at CHALES" width="1200" height="1600" loading="lazy">
  <img src="/IMG-20260221-WA0083.jpg" alt="Sleek bob at CHALES Hair Boutique" width="1200" height="1600" loading="lazy">
  <img src="/IMG-20260221-WA0114.jpg" alt="Warm brown colour at CHALES Hair Boutique" width="1200" height="1600" loading="lazy">
  <video src="/WhatsApp%20Video%202026-06-29%20at%2008.17.17.mp4" poster="/IMG-20260221-WA0079.jpg" muted loop playsinline autoplay preload="metadata" aria-label="Inside CHALES Hair Boutique"></video>
</div>
{groups}
{visit_block()}
"""
    return head("Prices | CHALES Hair Boutique, Bellville, Cape Town", "Full price list for CHALES Hair Boutique in Oakdale, Bellville: colour, highlights, balayage, Nanoplastia, keratin, Brazilian, hair botox, cuts and blow dries.", path, schema) + body + footer("prices")

# ---------------------------------------------------------------- review page
# Until Theo sends Chanté's g.page/r/... review link, this opens her Google listing,
# where "Write a review" is one tap away. Swap it here and rebuild.
GOOGLE_REVIEW = "https://g.page/r/CfHUNmaFuJC9EBM/review"
FEEDBACK_HOOK = "https://hook.eu1.make.com/nf6ksj2psx35bu5aqo3c3nqgairov2tc"

REVIEW_CSS = """
.rv{display:grid;grid-template-columns:1.1fr .9fr;min-height:calc(100vh - 70px)}
.rv-main{padding:clamp(40px,7vw,100px) var(--edge) 72px;display:flex;flex-direction:column;gap:26px;max-width:760px}
.rv-main h1{color:var(--gold);font-size:clamp(3rem,7vw,6.4rem)}
.rv-pic{position:relative;overflow:hidden;min-height:50vh}
.rv-pic img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.stars{display:flex;gap:6px}
.stars button{background:none;border:0;cursor:pointer;padding:6px;line-height:0;transition:transform .15s}
.stars button:hover{transform:scale(1.08)}
.stars button:active{transform:scale(.94)}
.stars svg{width:clamp(48px,9vw,64px);height:auto;fill:#6a6a62;transition:fill .2s}
.stars button.on svg{fill:var(--gold)}
.scale{display:flex;justify-content:space-between;max-width:360px;font-size:15px;color:var(--ink-2)}
.panel{display:none;flex-direction:column;gap:18px;background:var(--ground-2);padding:28px clamp(20px,3vw,32px)}
.panel.show{display:flex}
.panel h2{font-size:clamp(2rem,3.6vw,3rem)}
.panel label{font-size:15px;color:var(--ink-2);display:flex;flex-direction:column;gap:8px}
.panel textarea,.panel input{font:inherit;font-size:17px;color:var(--ink);background:var(--ground-3);border:1px solid #4a4a44;padding:14px;width:100%}
.panel textarea{min-height:110px;resize:vertical}
.panel .row{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.panel .small a{color:var(--ink)}
.sent{color:var(--gold-hi);font-weight:600}
.btn.ghost{background:var(--ground-3);color:var(--ink)}
.btn.ghost:hover{background:#45453f}
@media (max-width:900px){.rv{grid-template-columns:1fr}.rv-pic{order:-1;min-height:28vh}}
"""

STAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.3 1.3-6.6-4.9-4.6 6.6-.8z"/></svg>'

REVIEW_JS = """
(function(){
var HOOK='%s';
var q=new URLSearchParams(location.search),name=(q.get('n')||'').slice(0,40),phone=(q.get('p')||'').replace(/[^0-9+]/g,'').slice(0,15),src=q.get('s')||(name?'whatsapp':'card');
var rating=0;
function send(extra){var b=new URLSearchParams({rating:String(rating),name:extra.name||name,phone:extra.phone||phone,message:extra.message||'',source:src,page:'review'});
 try{fetch(HOOK+'?'+b.toString(),{method:'POST',mode:'no-cors'})}catch(e){}}
addEventListener('DOMContentLoaded',function(){
 if(name){document.getElementById('hi').textContent='Hi '+name+', thanks for coming in to CHALES.';}
 var lowName=document.getElementById('low-name'),lowPhone=document.getElementById('low-phone');
 if(name)lowName.value=name; if(phone)lowPhone.value=phone;
 var btns=[].slice.call(document.querySelectorAll('.stars button'));
 btns.forEach(function(b){b.addEventListener('click',function(){
   rating=+b.dataset.v; btns.forEach(function(x){x.classList.toggle('on',+x.dataset.v<=rating);x.setAttribute('aria-pressed',+x.dataset.v<=rating)});
   var low=rating<=3;
   document.getElementById('after').classList.add('show');
   document.getElementById('after-title').textContent=low?'Thanks for being straight with me':'Thanks, that means a lot';
   document.getElementById('after-text').innerHTML=low?"I'm sorry it wasn't right. I'd like to call you before you leave a review, so I get the chance to make it right. Or WhatsApp me now on <a href='https://wa.me/27814332756'>081 433 2756</a>.":'A Google review helps a small salon like CHALES more than anything.';
   document.getElementById('who').hidden=!low;
   send({});
   var p=document.getElementById('after'); if(p.scrollIntoView)p.scrollIntoView({behavior:'smooth',block:'nearest'});
 });});
 document.getElementById('send').addEventListener('click',function(){
   var m=document.getElementById('msg').value.trim(); if(!m){document.getElementById('msg').focus();return}
   var low=rating<=3;
   send({message:m,name:low?document.getElementById('low-name').value.trim():'',phone:low?document.getElementById('low-phone').value.trim():''});
   document.querySelector('#after .sent').hidden=false; this.disabled=true; this.textContent='Sent';
 });
});
})();
""" % FEEDBACK_HOOK

def review_page():
    path = "/review/"
    schema = {"@context": "https://schema.org", "@graph": [SALON]}
    stars = "".join(f'<button type="button" data-v="{i}" aria-label="{i} star{"s" if i>1 else ""}" aria-pressed="false">{STAR}</button>' for i in range(1, 6))
    body = f"""
<section class="rv">
  <div class="rv-main">
    <p class="lead" id="hi">Thanks for visiting CHALES Hair Boutique in Oakdale, Bellville.</p>
    <h1>How did Chanté do?</h1>
    <div>
      <div class="stars" role="group" aria-label="Rate your visit">{stars}</div>
      <div class="scale"><span>1 is bad</span><span>5 is great</span></div>
    </div>
    <noscript><p class="aside">Happy with your visit? <a href="{GOOGLE_REVIEW}">Leave a Google review</a>. Something not right? <a href="https://wa.me/27814332756">WhatsApp Chanté</a>.</p></noscript>

    <div class="panel" id="after" aria-live="polite">
      <h2 id="after-title">Thanks, that means a lot</h2>
      <p id="after-text">A Google review helps a small salon like CHALES more than anything.</p>
      <div class="row"><a class="btn" href="{GOOGLE_REVIEW}" target="_blank" rel="noopener">Leave a review on Google</a></div>
      <p class="aside">Takes about 30 seconds. Say whatever's true for you.</p>
      <label>Anything you want me to know? (optional)<textarea id="msg" maxlength="600"></textarea></label>
      <div id="who" hidden>
        <label>Your name<input id="low-name" autocomplete="name" maxlength="40"></label>
        <label style="margin-top:14px">Your WhatsApp number, so I can call you back<input id="low-phone" type="tel" autocomplete="tel" maxlength="15"></label>
      </div>
      <div class="row"><button class="btn ghost" type="button" id="send">Send to Chanté</button><span class="sent" hidden>Thank you, Chanté will see it.</span></div>
    </div>
  </div>
  <div class="rv-pic"><img src="/IMG-20260221-WA0080.jpg" alt="Colour being finished in the chair at CHALES Hair Boutique, Bellville" width="1200" height="1600"></div>
</section>
"""
    page = head("Rate your visit | CHALES Hair Boutique", "How did Chanté do? Rate your visit to CHALES Hair Boutique in Oakdale, Bellville.", path, schema) + body + footer("review")
    page = page.replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1)
    page = page.replace("</style>", REVIEW_CSS + "</style>", 1)
    page = page.replace("</head>", "<script>" + REVIEW_JS + "</script>\n</head>", 1)
    return page

def main():
    for t in TREATMENTS:
        os.makedirs(t["slug"], exist_ok=True)
        open(os.path.join(t["slug"], "index.html"), "w").write(treatment_page(t))
    os.makedirs("prices", exist_ok=True)
    open("prices/index.html", "w").write(prices_page())
    os.makedirs("review", exist_ok=True)
    open("review/index.html", "w").write(review_page())
    urls = ["/"] + [f"/{t['slug']}/" for t in TREATMENTS] + ["/prices/"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{SITE}{u}</loc><lastmod>2026-11-04</lastmod></url>\n" for u in urls) + "</urlset>\n"
    open("sitemap.xml", "w").write(sm)
    open("robots.txt", "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print("built", len(urls) - 1, "pages")

if __name__ == "__main__":
    main()
