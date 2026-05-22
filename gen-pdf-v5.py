#!/usr/bin/env python3
"""Generate Volume 1 PDF v5 — max image size, minimal margins"""

from reportlab.lib.pagesizes import B5
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase.pdfmetrics import stringWidth
from PIL import Image as PILImage
import json, os

pdfmetrics.registerFont(TTFont('HeitiSC', '/System/Library/Fonts/STHeiti Medium.ttc', subfontIndex=1))
pdfmetrics.registerFont(TTFont('SFNS', '/System/Library/Fonts/SFNS.ttf'))

W, H = B5  # 498.9 x 708.7 pts = 176 x 250 mm
base = os.path.expanduser("~/.openclaw/workspace/bubu-stories")
compressed = "/tmp/bubu-compressed"
out_path = os.path.expanduser("~/Desktop/咘咘的故事书-第一册-认识世界.pdf")

# Margins — left side has 12mm binding margin, right 3mm
BIND = 12 * mm
SIDE = 3 * mm
IMG_X = BIND
IMG_W = W - BIND - SIDE   # ~161mm wide
IMG_TOP_Y = H - 3 * mm     # 3mm from top
TEXT_BOTTOM = 10 * mm       # page number at 5mm, text stops at 10mm
PAGE_NUM_Y = 4 * mm

# Text area = same width as image
TEXT_X = IMG_X
TEXT_W = IMG_W

# Fixed text area height — must fit longest page (80zh + 252en)
# At 170mm wide: ZH 10.5pt ~28chars/line → 3 lines; EN 10pt ~50chars/line → 6 lines
# 3*5.5mm + 6*5mm + gaps = ~50mm. Use 55mm to be safe.
TEXT_AREA_H = 55 * mm
IMG_H = H - 3*mm - TEXT_AREA_H - 3*mm   # top margin - text - gap = ~189mm
IMG_Y = TEXT_AREA_H + 2*mm              # image bottom

stories = []
for ch in range(1, 9):
    with open(os.path.join(base, f"stories/story{ch}.json")) as f:
        s = json.load(f)
    s['chapter'] = ch
    stories.append(s)

c = canvas.Canvas(out_path, pagesize=B5)
c.setTitle("Bubu's Storybook · Volume 1 · Discovering the World")
c.setAuthor("Sam & NOMI")

def get_img(img_rel):
    if not img_rel: return ''
    comp = os.path.join(compressed, '/'.join(img_rel.split('/')[-2:]))
    if os.path.exists(comp): return comp
    orig = os.path.join(base, 'public', img_rel)
    return orig if os.path.exists(orig) else ''

# Pre-calc image bounds for 2:3 images
_ratio = min(IMG_W / 1024, IMG_H / 1536)
_IMG_DRAW_W = 1024 * _ratio
_IMG_DRAW_X = IMG_X + (IMG_W - _IMG_DRAW_W) / 2

def draw_image_fixed(c, img_path):
    """Draw image filling the fixed area as much as possible."""
    if not img_path or not os.path.exists(img_path): return
    pil = PILImage.open(img_path)
    iw, ih = pil.size
    pil.close()
    ratio = min(IMG_W / iw, IMG_H / ih)
    dw, dh = iw * ratio, ih * ratio
    cx = IMG_X + (IMG_W - dw) / 2
    cy = IMG_Y + (IMG_H - dh) / 2
    c.drawImage(img_path, cx, cy, dw, dh, preserveAspectRatio=True)

def wrap_text(text, font, size, max_w):
    if not text: return []
    lines = []
    for para in text.split('\n'):
        if not para.strip():
            lines.append('')
            continue
        cur = ''
        for ch in para:
            test = cur + ch
            if stringWidth(test, font, size) > max_w and cur:
                lines.append(cur)
                cur = ch
            else:
                cur = test
        if cur: lines.append(cur)
    return lines

def draw_text(c, text, x, y, max_w, font, size, color=black, leading_mult=1.55):
    if not text: return y
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap_text(text, font, size, max_w):
        if not line:
            y -= size * leading_mult * 0.4
            continue
        if y < TEXT_BOTTOM: break
        c.drawString(x, y, line)
        y -= size * leading_mult
    return y

# === P1: Cover ===
cover = os.path.join(compressed, "volume1-cover-en.jpg")
if not os.path.exists(cover):
    cover = os.path.join(compressed, "volume1-cover.jpg")
c.drawImage(cover, 0, 0, W, H)
c.showPage()
print("✅ Cover")

# === P2: TOC ===
c.setFillColor(HexColor('#FFF8E7'))
c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFont('SFNS', 20)
c.setFillColor(HexColor('#E8A87C'))
c.drawCentredString(W/2, H - 30*mm, "Contents")
y = H - 52*mm
pg = 3
for s in stories:
    c.setFont('SFNS', 12)
    c.setFillColor(HexColor('#555'))
    c.drawString(SIDE + 10*mm, y, f"Story {s['chapter']}    {s.get('title_en', s['title'])}")
    c.setFont('SFNS', 10)
    c.setFillColor(HexColor('#AAA'))
    c.drawRightString(W - SIDE - 10*mm, y, str(pg))
    y -= 14*mm
    pg += len(s.get('pages', []))
c.showPage()
print("✅ TOC")

# === Stories ===
cur_pg = 3
for story in stories:
    pages = story.get('pages', [])
    ch = story['chapter']
    for pi, page in enumerate(pages):
        txt_zh = page.get('text', '')
        txt_en = page.get('text_en', '')
        img_path = get_img(page.get('image', ''))
        
        if pi == 0:  # story cover
            if img_path: c.drawImage(img_path, 0, 0, W, H, preserveAspectRatio=False)
        else:
            c.setFillColor(white)
            c.rect(0, 0, W, H, fill=1, stroke=0)
            draw_image_fixed(c, img_path)
            y = TEXT_AREA_H - 8*mm
            if txt_zh:
                y = draw_text(c, txt_zh, _IMG_DRAW_X, y, _IMG_DRAW_W, 'HeitiSC', 10.5, black)
                y -= 2*mm
            if txt_en:
                y = draw_text(c, txt_en, _IMG_DRAW_X, y, _IMG_DRAW_W, 'SFNS', 10, black)
            c.setFont('SFNS', 7)
            c.setFillColor(black)
            c.drawCentredString(W/2, PAGE_NUM_Y, str(cur_pg))
        
        c.showPage()
        cur_pg += 1
    print(f"  ✅ Story {ch}: {story['title']} ({len(pages)}p)")

# No back cover

c.save()
sz = os.path.getsize(out_path)
print(f"\n✅ PDF: {out_path}")
print(f"   {cur_pg+1} pages, {sz/1024/1024:.1f} MB")
print(f"   Image area: {IMG_W/mm:.0f}x{IMG_H/mm:.0f}mm, Text area: {TEXT_AREA_H/mm:.0f}mm")
