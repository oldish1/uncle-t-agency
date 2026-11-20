#!/usr/bin/env python3
"""Make a Google-review QR code and a printable A5 poster for a salon.

Usage:
    python3 scripts/review_qr.py "CHALES Hair Boutique" "https://g.page/r/XXXX/review" outputs/chales

The review link comes from the salon's verified Google Business Profile:
Profile > Get more reviews > Copy link. Until the profile exists there is no real link,
so do not print anything made with a placeholder.
"""
from __future__ import annotations

import sys
from pathlib import Path

import segno
from PIL import Image, ImageDraw, ImageFont

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def centre(draw: ImageDraw.ImageDraw, text: str, y: int, fnt, width: int, fill=(30, 30, 30)) -> int:
    box = draw.textbbox((0, 0), text, font=fnt)
    draw.text(((width - (box[2] - box[0])) // 2, y), text, font=fnt, fill=fill)
    return y + (box[3] - box[1])


def make(name: str, url: str, out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    qr_path = out_dir / "review-qr.png"
    segno.make(url, error="h").save(qr_path, scale=24, border=2, dark="#1a1a1a")

    w, h = 1240, 1748  # A5 at 213 dpi, prints well at A5 or A6
    poster = Image.new("RGB", (w, h), (252, 249, 244))
    d = ImageDraw.Draw(poster)
    d.rectangle([40, 40, w - 40, h - 40], outline=(40, 40, 40), width=6)
    y = 150
    y = centre(d, "Loved your hair today?", y, font(BOLD, 84), w) + 50
    y = centre(d, "A quick Google review", y, font(REG, 58), w) + 14
    y = centre(d, "helps us more than you know.", y, font(REG, 58), w) + 80
    qr = Image.open(qr_path).convert("RGB")
    qr = qr.resize((760, 760), Image.NEAREST)
    poster.paste(qr, ((w - 760) // 2, y))
    y += 760 + 60
    y = centre(d, "Scan with your phone camera", y, font(BOLD, 52), w) + 40
    y = centre(d, "Takes 30 seconds. Thank you!", y, font(REG, 46), w) + 120
    centre(d, name, h - 230, font(BOLD, 60), w)
    poster_path = out_dir / "review-poster-A5.png"
    poster.save(poster_path)
    return qr_path, poster_path


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    a, b = make(sys.argv[1], sys.argv[2], Path(sys.argv[3]))
    print(a)
    print(b)
