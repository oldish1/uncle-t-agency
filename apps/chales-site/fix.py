import re, json, glob, os, sys
from PIL import Image
root = sys.argv[1]; os.chdir(root)
B = "https://chaleshairboutique.co.za"
# descriptive names + alt text from looking at each photo
P = {
 "IMG-20260221-WA0079.jpg": ("burgundy-hair-colour-bellville", "Client with fresh burgundy red hair colour at CHALES Hair Boutique, Bellville"),
 "IMG-20260221-WA0080.jpg": ("burgundy-colour-precision-trim", "Stylist trimming freshly coloured burgundy hair at CHALES, Oakdale"),
 "IMG-20260221-WA0081.jpg": ("burgundy-colour-blow-dry", "Chanté blow-drying a burgundy colour straight at CHALES Hair Boutique"),
 "IMG-20260221-WA0082.jpg": ("sleek-dark-bob-keratin", "Sleek dark brown bob with a glossy keratin smooth finish, Bellville"),
 "IMG-20260221-WA0083.jpg": ("smooth-bob-blow-dry", "Smooth, frizz-free bob after a blow dry at CHALES, Cape Town"),
 "IMG-20260221-WA0084.jpg": ("blunt-bob-cut-bellville", "Blunt shoulder-length bob cut at CHALES Hair Boutique, Bellville"),
 "IMG-20260221-WA0108.jpg": ("nanoplastia-long-straight-hair", "Long, straight, shiny hair after Nanoplastia at CHALES, Bellville"),
 "IMG-20260221-WA0109.jpg": ("nanoplastia-smoothing-result", "Nanoplastia smoothing result on long dark hair, CHALES Hair Boutique"),
 "IMG-20260221-WA0110.jpg": ("layered-cut-smooth-finish", "Layered cut with a smooth straight finish at CHALES, Oakdale Bellville"),
 "IMG-20260221-WA0111.jpg": ("long-silky-straight-hair", "Long silky straight hair after a smoothing treatment at CHALES"),
 "IMG-20260221-WA0112.jpg": ("silky-straight-shoulder-length", "Silky straight shoulder-length hair, smoothing treatment in Bellville"),
 "IMG-20260221-WA0113.jpg": ("chestnut-brown-hair-colour", "Rich chestnut brown hair colour with a sleek blow dry at CHALES"),
 "IMG-20260221-WA0114.jpg": ("auburn-hair-colour-blow-dry", "Auburn brown hair colour and blow dry at CHALES Hair Boutique, Cape Town"),
 "IMG-20260221-WA0115.jpg": ("brown-colour-angled-cut", "Warm brown colour with an angled cut at CHALES Hair Boutique, Bellville"),
 "chante-work.jpg":         ("burgundy-layered-colour", "Burgundy colour with soft layers by Chanté at CHALES Hair Boutique"),
 "Lexi.jpg":                ("lexi-whatsapp-booking", "Lexi, the CHALES WhatsApp booking assistant"),
}
low = {k.lower(): k for k in P}
for k, (name, _) in P.items():
    src = k.lower() if os.path.exists(k.lower()) else k
    im = Image.open(src).convert("RGB")
    if max(im.size) > 1200: im.thumbnail((1200, 1200))
    im.save(f"{name}.webp", "WEBP", quality=74, method=6)

def swap_imgs(s):
    # <img ... src="X.jpg" ... alt="..."> : swap src, and set alt if generic
    def rep(m):
        tag = m.group(0)
        mm = re.search(r'src="([^"]+)"', tag)
        if not mm: return tag
        src = mm.group(1)
        key = low.get(src.lower())
        if not key: return tag
        name, alt = P[key]
        tag = tag.replace(f'src="{src}"', f'src="/{name}.webp"')
        a = re.search(r'alt="([^"]*)"', tag)
        if a and a.group(1).strip() in ("", "CHALES Hair Boutique", "Hair styling at CHALES Hair Boutique, Bellville", "Lexi"):
            tag = tag.replace(a.group(0), f'alt="{alt}"')
        elif not a:
            tag = tag.replace("<img", f'<img alt="{alt}"', 1)
        return tag
    s = re.sub(r'<img\b[^>]*>', rep, s)
    # CSS / JS references (background-image, data-src) but NOT og:image / JSON-LD absolute URLs
    def rep2(m):
        key = low.get(m.group(2).lower())
        return m.group(1) + "/" + P[key][0] + ".webp" if key else m.group(0)
    s = re.sub(r'([\'"(]\s*)/?((?:IMG-2026[^\'")]+|chante-work|Lexi)\.jpg)(?=[\'")])', lambda m: rep2(m) if not m.string[max(0,m.start()-40):m.start()].count(B) else m.group(0), s, flags=re.I)
    return s

pages = ["index.html"] + glob.glob("*/index.html")
for p in pages:
    s = open(p, encoding="utf-8").read(); o = s
    s = swap_imgs(s)
    # og:image: keep a JPG (WhatsApp/Facebook previews) but give it a clean name
    s = re.sub(r'(og:image" content=")[^"]+(")', r'\1' + B + r'/chales-hair-boutique-bellville.jpg\2', s)
    s = s.replace(f'"image": "{B}/IMG-20260221-WA0079.jpg"', f'"image": "{B}/chales-hair-boutique-bellville.jpg"')
    open(p, "w", encoding="utf-8").write(s)
    print(p, "changed" if s != o else "same", len(re.findall(r'\.jpg', s, re.I)), "jpg refs left")
# a clean-named, lighter JPG for social previews / schema
im = Image.open("img-20260221-wa0079.jpg").convert("RGB"); im.thumbnail((1200,1200)); im.save("chales-hair-boutique-bellville.jpg", quality=82, optimize=True, progressive=True)
