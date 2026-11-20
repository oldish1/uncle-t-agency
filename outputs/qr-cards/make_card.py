"""Builds the Chales QR business card (front + back) as chales-card.html and chales-qr.svg."""
import qrcode

URL = "https://chaleshairboutique.co.za/?utm_source=qr&utm_medium=card&utm_campaign=chales-card-1"
q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, border=0, box_size=10)
q.add_data(URL)
q.make(fit=True)
m = q.get_matrix()
n = len(m)
rects = "".join(
    f'<rect x="{x}" y="{y}" width="1.02" height="1.02"/>'
    for y, r in enumerate(m) for x, v in enumerate(r) if v
)
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}" '
       f'shape-rendering="crispEdges" fill="#252522">{rects}</svg>')
open("chales-qr.svg", "w").write(svg)

html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Chales QR card</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Montserrat:wght@400;500;600&display=swap" rel="stylesheet">
<style>
@page {{ size: 90mm 55mm; margin: 0 }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
html, body {{ background: #fff }}
.card {{ width: 90mm; height: 55mm; position: relative; overflow: hidden; page-break-after: always;
  background: #252522; color: #F5F0E8; font-family: 'Montserrat', sans-serif }}
.frame {{ position: absolute; inset: 2.4mm; border: 0.25mm solid #C9A84C }}
.front {{ display: flex; align-items: center; justify-content: space-between; padding: 0 8mm 0 9mm }}
.l {{ display: flex; flex-direction: column; gap: 2.2mm; max-width: 42mm }}
.brand {{ font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 600; font-size: 7.4mm;
  letter-spacing: .35mm; color: #E8C96A; line-height: .95 }}
.sub {{ font-size: 1.9mm; letter-spacing: .55mm; text-transform: uppercase; color: #C9A84C }}
.scan {{ font-family: 'Cormorant Garamond', Georgia, serif; font-style: italic; font-size: 4.6mm;
  line-height: 1.05; color: #F5F0E8; margin-top: 1.5mm }}
.tile {{ background: #F5F0E8; padding: 2.6mm; border-radius: 1.6mm; width: 30mm; height: 30mm; flex: none }}
.tile svg {{ width: 100%; height: 100%; display: block }}
.back {{ display: flex; flex-direction: column; justify-content: center; align-items: center;
  text-align: center; gap: 2.4mm }}
.back .brand {{ font-size: 6.4mm }}
.rule {{ width: 14mm; height: .25mm; background: #C9A84C }}
.line {{ font-size: 2.2mm; letter-spacing: .3mm; color: #F5F0E8; line-height: 1.5 }}
.gold {{ color: #E8C96A }}
.tiny {{ font-size: 1.8mm; letter-spacing: .45mm; text-transform: uppercase; color: #C9A84C }}
</style></head><body>
<div class="card front"><div class="frame"></div>
  <div class="l"><div class="brand">CHALES<br>HAIR BOUTIQUE</div>
    <div class="sub">Bellville · Cape Town</div>
    <div class="scan">Scan to see<br>our work &amp; book</div></div>
  <div class="tile">{svg}</div></div>
<div class="card back"><div class="frame"></div>
  <div class="brand">CHALES</div><div class="rule"></div>
  <div class="line">Nanoplastia · Keratin · Colour<br>Braids · Wash &amp; blow-dry</div>
  <div class="line gold">46 Alexandra Street, Oakdale, Bellville</div>
  <div class="line">chaleshairboutique.co.za</div>
  <div class="tiny">@chaleshairboutique &nbsp;·&nbsp; @Chales418</div></div>
</body></html>"""
open("chales-card.html", "w").write(html)
print(n, "modules")
