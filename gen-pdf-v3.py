#!/usr/bin/env python3
"""Generate Volume 1 PDF v3 — fixed wrapping, uniform images, EN cover"""

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

W, H = B5
base = os.path.expanduser("~/.openclaw/workspace/bubu-stories")
compressed = "/tmp/bubu-compressed"
out_path = os.path.expanduser("~/Desktop/咘咘的故事书-第一册-认识世界.pdf")

margin = 12 * mm

# FIXED image area for ALL content pages (not covers)
IMG_X = margin / 2
IMG_W = W - margin          # full width minus margin
IMG_TOP = H - 5 * mm        # top edge
IMG_H = 165 * mm            # fixed height for image area
IMG_Y = IMG_TOP - IMG_H     # bottom edge of image area
TEXT_LEFT = IMG_X
TEXT_WIDTH = IMG_W

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
    if not img_rel:
        return ''
    comp = os.path.join(compressed, '/'.join(img_rel.split('/')[-2:]))
    if os.path.exists(comp):
        return comp
    orig = os.path.join(base, 'public', img_rel)
    return orig if os.path.exists(orig) else ''

def draw_image_fixed(c, img_path):
    """Draw image in the FIXED image area, centered, preserving aspect ratio."""
    if not img_path or not os.path.exists(img_path):
        return
    pil = PILImage.open(img_path)
    iw, ih = pil.size
    pil.close()
    ratio = min(IMG_W / iw, IMG_H / ih)
    dw, dh = iw * ratio, ih * ratio
    cx = IMG_X + (IMG_W - dw) / 2
    cy = IMG_Y + (IMG_H - dh) / 2
    c.drawImage(img_path, cx, cy, dw, dh, preserveAspectRatio=True)

def wrap_text_precise(text, font, size, max_w):
    """Wrap text using actual glyph widths from reportlab."""
    if not text:
        return []
    lines = []
    for para in text.split('\n'):
        if not para.strip():
            lines.append('')
            continue
        current = ''
        for ch in para:
            test = current + ch
            w = stringWidth(test, font, size)
            if w > max_w and current:
                lines.append(current)
                current = ch
            else:
                current = test
        if current:
            lines.append(current)
    return lines

def draw_text_precise(c, text, x, y, max_w, font, size, color=black, leading_mult=1.65):
    """Draw text with precise wrapping. Returns final y."""
    if not text:
        return y
    leading = size * leading_mult
    c.setFont(font, size)
    c.setFillColor(color)
    lines = wrap_text_precise(text, font, size, max_w)
    for line in lines:
        if not line:
            y -= leading * 0.5
            continue
        if y < 10 * mm:
            break
        c.drawString(x, y, line)
        y -= leading
    return y

# === Volume Cover (EN) ===
cover = os.path.join(compressed, "volume1-cover-en.jpg")
if not os.path.exists(cover):
    cover = os.path.join(compressed, "volume1-cover.jpg")
if os.path.exists(cover):
    c.drawImage(cover, 0, 0, W, H)
c.showPage()
print("✅ Cover (EN)")

# === Title Page (EN) ===
c.setFillColor(HexColor('#FFF8E7'))
c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFont('SFNS', 28)
c.setFillColor(HexColor('#E8A87C'))
c.drawCentredString(W/2, H - 60*mm, "Bubu's Storybook")
c.setFont('SFNS', 16)
c.setFillColor(HexColor('#C0785C'))
c.drawCentredString(W/2, H - 78*mm, "Volume 1 · Discovering the World")
c.setFont('SFNS', 11)
c.setFillColor(HexColor('#AAA'))
c.drawCentredString(W/2, H - 95*mm, "Stories 1–8")
c.setFont('SFNS', 9)
c.setFillColor(HexColor('#BBB'))
c.drawCentredString(W/2, 28*mm, "Words · Sam & NOMI")
c.drawCentredString(W/2, 20*mm, "Illustrations · AI (gpt-image-2)")
c.drawCentredString(W/2, 12*mm, "2026")
c.showPage()
print("✅ Title page")

# === TOC (EN) ===
c.setFillColor(HexColor('#FFF8E7'))
c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFont('SFNS', 20)
c.setFillColor(HexColor('#E8A87C'))
c.drawCentredString(W/2, H - 35*mm, "Contents")
y_toc = H - 60*mm
pg = 4
for s in stories:
    c.setFont('SFNS', 12)
    c.setFillColor(HexColor('#555'))
    c.drawString(margin + 5*mm, y_toc, f"Story {s['chapter']}    {s.get('title_en', s['title'])}")
    c.setFont('SFNS', 10)
    c.setFillColor(HexColor('#AAA'))
    c.drawRightString(W - margin - 5*mm, y_toc, str(pg))
    y_toc -= 14*mm
    pg += len(s.get('pages', []))
c.showPage()
print("✅ TOC")

# === Story Pages ===
cur_pg = 4
for story in stories:
    pages = story.get('pages', [])
    ch = story['chapter']
    
    for pi, page in enumerate(pages):
        txt_zh = page.get('text', '')
        txt_en = page.get('text_en', '')
        img_rel = page.get('image', '')
        img_path = get_img(img_rel)
        is_cover = (pi == 0)
        
        if is_cover:
            # Story cover: full page, no overlay
            if img_path and os.path.exists(img_path):
                c.drawImage(img_path, 0, 0, W, H, preserveAspectRatio=False)
        else:
            c.setFillColor(white)
            c.rect(0, 0, W, H, fill=1, stroke=0)
            
            # Fixed image area
            draw_image_fixed(c, img_path)
            
            # Text below image, aligned to image area edges
            y = IMG_Y - 8 * mm
            if txt_zh:
                y = draw_text_precise(c, txt_zh, TEXT_LEFT, y, TEXT_WIDTH, 'HeitiSC', 10.5, black)
                y -= 3 * mm
            if txt_en:
                y = draw_text_precise(c, txt_en, TEXT_LEFT, y, TEXT_WIDTH, 'SFNS', 10, black)
            
            # Page number
            c.setFont('SFNS', 7)
            c.setFillColor(HexColor('#CCC'))
            c.drawCentredString(W/2, 4*mm, str(cur_pg))
        
        c.showPage()
        cur_pg += 1
    
    print(f"  ✅ Story {ch}: {story['title']} ({len(pages)}p)")

# === Back Cover ===
c.setFillColor(HexColor('#FFF8E7'))
c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFont('SFNS', 14)
c.setFillColor(HexColor('#E8A87C'))
c.drawCentredString(W/2, H/2 + 8*mm, "Bubu's Storybook")
c.setFont('SFNS', 9)
c.setFillColor(HexColor('#BBB'))
c.drawCentredString(W/2, H/2 - 8*mm, "Every story is a footprint of Bubu's growth")
c.setFont('SFNS', 7)
c.setFillColor(HexColor('#CCC'))
c.drawCentredString(W/2, 18*mm, "Made with love by Sam & NOMI · 2026")
c.showPage()

c.save()
sz = os.path.getsize(out_path)
print(f"\n✅ PDF saved: {out_path}")
print(f"   Pages: {cur_pg + 1}, Size: {sz/1024/1024:.1f} MB")
