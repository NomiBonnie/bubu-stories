#!/usr/bin/env python3
"""Generate Volume 1 PDF for 咘咘的故事书 - v2"""

from reportlab.lib.pagesizes import B5
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white, black
from PIL import Image as PILImage
import json, os

# Register fonts
pdfmetrics.registerFont(TTFont('HeitiSC', '/System/Library/Fonts/STHeiti Medium.ttc', subfontIndex=1))
pdfmetrics.registerFont(TTFont('SFNS', '/System/Library/Fonts/SFNS.ttf'))

W, H = B5
base = os.path.expanduser("~/.openclaw/workspace/bubu-stories")
compressed = "/tmp/bubu-compressed"
out_path = os.path.expanduser("~/Desktop/咘咘的故事书-第一册-认识世界.pdf")

# Load stories 1-8
stories = []
for ch in range(1, 9):
    with open(os.path.join(base, f"stories/story{ch}.json")) as f:
        s = json.load(f)
    s['chapter'] = ch
    stories.append(s)

c = canvas.Canvas(out_path, pagesize=B5)
c.setTitle("Bubu's Storybook · Volume 1 · Discovering the World")
c.setAuthor("Sam & NOMI")

margin = 12 * mm

def get_img(img_rel):
    """Get compressed image path, fallback to original."""
    if not img_rel:
        return ''
    comp = os.path.join(compressed, '/'.join(img_rel.split('/')[-2:]))
    if os.path.exists(comp):
        return comp
    orig = os.path.join(base, 'public', img_rel)
    return orig if os.path.exists(orig) else ''

def draw_image_fit(c, img_path, x, y, max_w, max_h):
    """Draw image centered within bounds. Returns (draw_x, draw_w, draw_h)."""
    if not img_path or not os.path.exists(img_path):
        return x, max_w, max_h
    pil = PILImage.open(img_path)
    iw, ih = pil.size
    pil.close()
    ratio = min(max_w / iw, max_h / ih)
    dw, dh = iw * ratio, ih * ratio
    cx = x + (max_w - dw) / 2
    c.drawImage(img_path, cx, y, dw, dh, preserveAspectRatio=True)
    return cx, dw, dh

def draw_wrapped(c, text, x, y, max_w, font, size, color=black, leading_mult=1.65):
    """Draw wrapped text respecting newlines. Returns final y."""
    if not text:
        return y
    leading = size * leading_mult
    c.setFont(font, size)
    c.setFillColor(color)
    for para in text.split('\n'):
        if not para.strip():
            y -= leading * 0.5
            continue
        # Estimate char width
        has_cjk = any(ord(ch) > 0x2E80 for ch in para[:10])
        avg_w = size * 0.52 if has_cjk else size * 0.48
        cpl = max(10, int(max_w / avg_w))
        while para:
            chunk = para[:cpl]
            para = para[cpl:]
            if y < 12 * mm:
                break
            c.drawString(x, y, chunk)
            y -= leading
    return y

# ============================================================
# PAGE 1: Volume Cover (full bleed)
# ============================================================
cover = os.path.join(compressed, "volume1-cover.jpg")
if os.path.exists(cover):
    c.drawImage(cover, 0, 0, W, H)
c.showPage()
print("✅ Cover")

# ============================================================
# PAGE 2: Title page — ALL ENGLISH
# ============================================================
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
print("✅ Title page (EN)")

# ============================================================
# PAGE 3: TOC — ALL ENGLISH
# ============================================================
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
    title_en = s.get('title_en', s['title'])
    c.drawString(margin + 5*mm, y_toc, f"Story {s['chapter']}    {title_en}")
    c.setFont('SFNS', 10)
    c.setFillColor(HexColor('#AAA'))
    c.drawRightString(W - margin - 5*mm, y_toc, str(pg))
    y_toc -= 14*mm
    pg += len(s.get('pages', []))
c.showPage()
print("✅ TOC (EN)")

# ============================================================
# STORY PAGES
# ============================================================
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
            # Story cover: FULL PAGE IMAGE ONLY, no overlay
            if img_path and os.path.exists(img_path):
                c.drawImage(img_path, 0, 0, W, H, preserveAspectRatio=False)
        else:
            # Content page: image top, text bottom
            c.setFillColor(white)
            c.rect(0, 0, W, H, fill=1, stroke=0)
            
            # Estimate text height
            zh_len = len(txt_zh) if txt_zh else 0
            en_len = len(txt_en) if txt_en else 0
            nl_zh = txt_zh.count('\n') if txt_zh else 0
            nl_en = txt_en.count('\n') if txt_en else 0
            zh_lines = max(1, zh_len // 22 + nl_zh + 1) if txt_zh else 0
            en_lines = max(1, en_len // 38 + nl_en + 1) if txt_en else 0
            text_h = zh_lines * 6.5*mm + en_lines * 5.5*mm + 15*mm
            text_h = max(38*mm, min(text_h, 90*mm))
            
            img_top = H - 3*mm
            img_h = H - text_h - 6*mm
            
            # Draw image and get its actual bounds
            img_x = margin / 2
            img_max_w = W - margin
            draw_x, draw_w, draw_h = img_x, img_max_w, img_h
            if img_path and os.path.exists(img_path):
                draw_x, draw_w, draw_h = draw_image_fit(c, img_path, img_x, text_h, img_max_w, img_h)
            
            # Text aligned to image edges
            text_left = draw_x
            text_width = draw_w
            
            y = text_h - 10*mm
            if txt_zh:
                y = draw_wrapped(c, txt_zh, text_left, y, text_width, 'HeitiSC', 10.5, black)
                y -= 3*mm
            if txt_en:
                y = draw_wrapped(c, txt_en, text_left, y, text_width, 'SFNS', 9, black)
            
            # Page number
            c.setFont('SFNS', 7)
            c.setFillColor(HexColor('#CCC'))
            c.drawCentredString(W/2, 4*mm, str(cur_pg))
        
        c.showPage()
        cur_pg += 1
    
    print(f"  ✅ Story {ch}: {story['title']} ({len(pages)}p)")

# ============================================================
# Back Cover
# ============================================================
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
