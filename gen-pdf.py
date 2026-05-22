#!/usr/bin/env python3
"""Generate Volume 1 PDF for 咘咘的故事书"""

from reportlab.lib.pagesizes import B5
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white, black
import json, os

# Register Chinese font
pdfmetrics.registerFont(TTFont('Heiti', '/System/Library/Fonts/STHeiti Medium.ttc', subfontIndex=0))

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
c.setTitle("咘咘的故事书 · 第一册 · 认识世界")
c.setAuthor("Sam & NOMI")

margin = 12 * mm

def draw_wrapped(c, text, x, y, max_w, font, size, color=black, leading_mult=1.6):
    if not text:
        return y
    leading = size * leading_mult
    c.setFont(font, size)
    c.setFillColor(color)
    for para in text.split('\n'):
        if not para.strip():
            y -= leading * 0.5
            continue
        # char width estimate
        avg_w = size * 0.52 if any(ord(ch) > 127 for ch in para[:5]) else size * 0.48
        cpl = max(10, int(max_w / avg_w))
        while para:
            chunk = para[:cpl]
            para = para[cpl:]
            if y < 15 * mm:
                break
            c.drawString(x, y, chunk)
            y -= leading
    return y

# --- Volume Cover ---
cover = os.path.join(compressed, "volume1-cover.jpg")
if os.path.exists(cover):
    c.drawImage(cover, 0, 0, W, H)
c.showPage()
print("✅ Cover")

# --- Title Page ---
c.setFillColor(HexColor('#FFF8E7'))
c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFont('Heiti', 26)
c.setFillColor(HexColor('#E8A87C'))
c.drawCentredString(W/2, H - 60*mm, "咘咘的故事书")
c.setFont('Heiti', 15)
c.setFillColor(HexColor('#C0785C'))
c.drawCentredString(W/2, H - 75*mm, "第一册 · 认识世界")
c.setFont('Heiti', 11)
c.setFillColor(HexColor('#999'))
c.drawCentredString(W/2, H - 87*mm, "Volume 1 · Discovering the World")
c.setFont('Heiti', 10)
c.setFillColor(HexColor('#AAA'))
c.drawCentredString(W/2, H - 105*mm, "收录故事 1-8 · Stories 1-8")
c.setFont('Heiti', 9)
c.setFillColor(HexColor('#BBB'))
c.drawCentredString(W/2, 28*mm, "文字 · Sam & NOMI")
c.drawCentredString(W/2, 20*mm, "插画 · AI (gpt-image-2)")
c.drawCentredString(W/2, 12*mm, "2026")
c.showPage()
print("✅ Title page")

# --- TOC ---
c.setFillColor(HexColor('#FFF8E7'))
c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFont('Heiti', 18)
c.setFillColor(HexColor('#E8A87C'))
c.drawCentredString(W/2, H - 35*mm, "目 录")
c.setFont('Heiti', 9)
c.setFillColor(HexColor('#999'))
c.drawCentredString(W/2, H - 44*mm, "Contents")

y_toc = H - 62*mm
pg = 4
for s in stories:
    c.setFont('Heiti', 12)
    c.setFillColor(HexColor('#555'))
    c.drawString(margin + 5*mm, y_toc, f"故事 {s['chapter']}　{s['title']}")
    c.setFont('Heiti', 8)
    c.setFillColor(HexColor('#999'))
    c.drawString(margin + 5*mm, y_toc - 5*mm, s.get('title_en', ''))
    c.setFont('Heiti', 10)
    c.setFillColor(HexColor('#AAA'))
    c.drawRightString(W - margin - 5*mm, y_toc, str(pg))
    y_toc -= 18*mm
    pg += len(s.get('pages', []))
c.showPage()
print("✅ TOC")

# --- Story Pages ---
cur_pg = 4
for story in stories:
    pages = story.get('pages', [])
    ch = story['chapter']
    
    for pi, page in enumerate(pages):
        txt_zh = page.get('text', '')
        txt_en = page.get('text_en', '')
        img_rel = page.get('image', '')
        img_path_orig = os.path.join(base, 'public', img_rel) if img_rel else ''
        # Use compressed version
        img_path = os.path.join(compressed, '/'.join(img_rel.split('/')[-2:])) if img_rel else ''
        if not os.path.exists(img_path):
            img_path = img_path_orig
        is_cover = (pi == 0)
        
        if is_cover:
            # Full bleed story cover
            if img_path and os.path.exists(img_path):
                c.drawImage(img_path, 0, 0, W, H, preserveAspectRatio=False)
            # Overlay bar
            c.setFillColor(HexColor('#00000077'))
            c.rect(0, 0, W, 24*mm, fill=1, stroke=0)
            c.setFont('Heiti', 13)
            c.setFillColor(white)
            c.drawCentredString(W/2, 14*mm, f"故事 {ch}　{story['title']}")
            c.setFont('Heiti', 8)
            c.drawCentredString(W/2, 7*mm, story.get('title_en', ''))
        else:
            # White page: image top, text bottom
            c.setFillColor(white)
            c.rect(0, 0, W, H, fill=1, stroke=0)
            
            # Estimate text height
            zh_len = len(txt_zh) if txt_zh else 0
            en_len = len(txt_en) if txt_en else 0
            nl_zh = txt_zh.count('\n') if txt_zh else 0
            nl_en = txt_en.count('\n') if txt_en else 0
            zh_lines = max(1, zh_len // 24 + nl_zh + 1) if txt_zh else 0
            en_lines = max(1, en_len // 45 + nl_en + 1) if txt_en else 0
            text_h = zh_lines * 6*mm + en_lines * 4.5*mm + 12*mm
            text_h = max(35*mm, min(text_h, 85*mm))
            
            img_h = H - text_h - 5*mm
            
            if img_path and os.path.exists(img_path):
                # Fit image
                from PIL import Image as PILImage
                pil = PILImage.open(img_path)
                iw, ih = pil.size
                pil.close()
                img_draw_w = W - margin
                img_draw_h = img_h
                ratio = min(img_draw_w / iw, img_draw_h / ih)
                dw, dh = iw * ratio, ih * ratio
                cx = (W - dw) / 2
                c.drawImage(img_path, cx, text_h, dw, dh, preserveAspectRatio=True)
            
            # Text
            y = text_h - 10*mm
            if txt_zh:
                y = draw_wrapped(c, txt_zh, margin, y, W - 2*margin, 'Heiti', 10.5, HexColor('#333'))
                y -= 2*mm
            if txt_en:
                y = draw_wrapped(c, txt_en, margin, y, W - 2*margin, 'Heiti', 7.5, HexColor('#999'))
            
            # Page number
            c.setFont('Heiti', 7)
            c.setFillColor(HexColor('#CCC'))
            c.drawCentredString(W/2, 4*mm, str(cur_pg))
        
        c.showPage()
        cur_pg += 1
    
    print(f"  ✅ Story {ch}: {story['title']} ({len(pages)}p)")

# --- Back Cover ---
c.setFillColor(HexColor('#FFF8E7'))
c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFont('Heiti', 13)
c.setFillColor(HexColor('#E8A87C'))
c.drawCentredString(W/2, H/2 + 8*mm, "咘咘的故事书")
c.setFont('Heiti', 9)
c.setFillColor(HexColor('#BBB'))
c.drawCentredString(W/2, H/2 - 6*mm, "每一个故事，都是咘咘成长的脚印")
c.drawCentredString(W/2, H/2 - 16*mm, "Every story is a footprint of Bubu's growth")
c.setFont('Heiti', 7)
c.setFillColor(HexColor('#CCC'))
c.drawCentredString(W/2, 18*mm, "Made with ❤ by Sam & NOMI · 2026")
c.showPage()

c.save()
sz = os.path.getsize(out_path)
print(f"\n✅ PDF saved: {out_path}")
print(f"   Pages: {cur_pg + 1}, Size: {sz/1024/1024:.1f} MB")
