#!/usr/bin/env python3
"""Generate Volume 1A & 1B PDFs — split into two thinner books"""

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

# Margins
BIND = 15 * mm
RIGHT = 5 * mm
IMG_X = BIND
IMG_W = W - BIND - RIGHT
IMG_TOP_Y = H - 3 * mm

# TEXT_AREA_H, IMG_H, IMG_Y, _ratio, _IMG_DRAW_W, _IMG_DRAW_X
# are calculated dynamically per volume in generate_volume()

def get_img(img_rel):
    if not img_rel: return ''
    comp = os.path.join(compressed, '/'.join(img_rel.split('/')[-2:]))
    if os.path.exists(comp): return comp
    orig = os.path.join(base, 'public', img_rel)
    return orig if os.path.exists(orig) else ''

def draw_image_fixed(c, img_path, IMG_H, IMG_Y):
    if not img_path or not os.path.exists(img_path): return
    pil = PILImage.open(img_path)
    iw, ih = pil.size
    pil.close()
    ratio = min(IMG_W / iw, IMG_H / ih)
    dw, dh = iw * ratio, ih * ratio
    cx = IMG_X + (IMG_W - dw) / 2
    cy = IMG_Y + (IMG_H - dh) / 2
    c.drawImage(img_path, cx, cy, dw, dh, preserveAspectRatio=True)

import re

# Punctuation that must not start a line
NO_START = set('，。！？、；：）】」』》〉…—～·.,!?;:)]}\'"\'\u201D\u2019')

def strip_emoji(text):
    """Remove emoji characters that render as bars in PDF fonts."""
    return re.sub(r'[\U0001F300-\U0001FAFF\U00002702-\U000027B0]', '', text).lstrip()

def wrap_text_zh(text, font, size, max_w):
    """Wrap Chinese text: no punctuation at line start."""
    if not text: return []
    text = strip_emoji(text)
    lines = []
    for para in text.split('\n'):
        if not para.strip():
            lines.append('')
            continue
        cur = ''
        for ch in para:
            test = cur + ch
            if stringWidth(test, font, size) > max_w and cur:
                # Don't break if next char is punctuation
                if ch in NO_START and cur:
                    cur += ch
                    continue
                lines.append(cur)
                cur = ch
            else:
                cur = test
        if cur: lines.append(cur)
    return lines

def wrap_text_en(text, font, size, max_w):
    """Wrap English text by words: never split a word."""
    if not text: return []
    text = strip_emoji(text)
    lines = []
    for para in text.split('\n'):
        if not para.strip():
            lines.append('')
            continue
        words = para.split(' ')
        cur = ''
        for word in words:
            test = (cur + ' ' + word).strip() if cur else word
            if stringWidth(test, font, size) > max_w and cur:
                lines.append(cur)
                cur = word
            else:
                cur = test
        if cur: lines.append(cur)
    return lines

def draw_text(c, text, x, y, max_w, font, size, color=black, leading_mult=1.55, lang='zh'):
    if not text: return y
    c.setFont(font, size)
    c.setFillColor(color)
    wrapped = wrap_text_zh(text, font, size, max_w) if lang == 'zh' else wrap_text_en(text, font, size, max_w)
    for line in wrapped:
        if not line:
            y -= size * leading_mult * 0.4
            continue
        if y < 10 * mm: break
        c.drawString(x, y, line)
        y -= size * leading_mult
    return y

def generate_volume(chapters, vol_label, vol_subtitle, out_filename, use_compressed=True):
    stories = []
    for ch in chapters:
        with open(os.path.join(base, f"stories/story{ch}.json")) as f:
            s = json.load(f)
        s['chapter'] = ch
        stories.append(s)
    
    # === Dynamic layout: scan all pages to find max text height ===
    # First pass with a rough IMG_DRAW_W estimate (2:3 image in full area)
    _rough_ratio = min(IMG_W / 1024, (H - 60*mm) / 1536)
    _rough_draw_w = 1024 * _rough_ratio
    
    max_text_h = 0
    for story in stories:
        for pi, page in enumerate(story.get('pages', [])):
            if pi == 0: continue  # skip covers
            txt_zh = strip_emoji(page.get('text', ''))
            txt_en = strip_emoji(page.get('text_en', ''))
            zh_lines = len(wrap_text_zh(txt_zh, 'HeitiSC', 10.5, _rough_draw_w))
            en_lines = len(wrap_text_en(txt_en, 'SFNS', 10, _rough_draw_w))
            th = zh_lines * 10.5 * 1.55 + en_lines * 10 * 1.55 + 5*mm  # gap between zh/en
            if th > max_text_h:
                max_text_h = th
    
    TEXT_AREA_H = max_text_h + 12*mm  # safety margin for padding
    TEXT_AREA_H = max(TEXT_AREA_H, 35*mm)  # minimum
    IMG_H = H - 3*mm - TEXT_AREA_H - 3*mm
    IMG_Y = TEXT_AREA_H + 2*mm
    
    # Final image bounds
    _ratio = min(IMG_W / 1024, IMG_H / 1536)
    _IMG_DRAW_W = 1024 * _ratio
    _IMG_DRAW_X = IMG_X + (IMG_W - _IMG_DRAW_W) / 2
    
    print(f"  Layout: text_area={TEXT_AREA_H/mm:.0f}mm, img_h={IMG_H/mm:.0f}mm, img_w={_IMG_DRAW_W/mm:.0f}mm")
    
    out_path = os.path.expanduser(f"~/Desktop/{out_filename}")
    c = canvas.Canvas(out_path, pagesize=B5)
    c.setTitle(f"Bubu's Storybook · {vol_label}")
    c.setAuthor("Sam & NOMI")
    
    # Cover — use volume-specific cover
    cover_map = {
        '1A': 'volume1a-cover',
        '1B': 'volume1b-cover',
        '2A': 'volume2a-cover',
        '2B': 'volume2b-cover',
    }
    cover_key = vol_label.split()[-1]  # e.g. 'Volume 1A' -> '1A'
    cover_name = cover_map.get(cover_key, 'volume1-cover-en')
    if use_compressed:
        cover = os.path.join(compressed, f'{cover_name}.jpg')
    else:
        cover = os.path.join(base, f'{cover_name}.jpg')
    if not os.path.exists(cover):
        cover = os.path.join(compressed, f'{cover_name}.jpg')
    if not os.path.exists(cover):
        cover = os.path.join(compressed, 'volume1-cover-en.jpg')
    c.drawImage(cover, 0, 0, W, H)
    c.showPage()
    print(f"  ✅ Cover")
    
    # TOC
    c.setFillColor(HexColor('#FFF8E7'))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFont('SFNS', 18)
    c.setFillColor(HexColor('#E8A87C'))
    c.drawCentredString(W/2, H - 28*mm, vol_subtitle)
    c.setFont('SFNS', 11)
    c.setFillColor(HexColor('#BBB'))
    c.drawCentredString(W/2, H - 38*mm, "Contents")
    
    y = H - 55*mm
    pg = 3
    for s in stories:
        c.setFont('SFNS', 12)
        c.setFillColor(HexColor('#555'))
        c.drawString(BIND + 5*mm, y, f"Story {s['chapter']}    {s.get('title_en', s['title'])}")
        c.setFont('SFNS', 10)
        c.setFillColor(HexColor('#AAA'))
        c.drawRightString(W - RIGHT - 5*mm, y, str(pg))
        y -= 14*mm
        pg += len(s.get('pages', []))
    c.showPage()
    print(f"  ✅ TOC")
    
    # Stories
    cur_pg = 3
    for story in stories:
        pages = story.get('pages', [])
        ch = story['chapter']
        for pi, page in enumerate(pages):
            txt_zh = page.get('text', '')
            txt_en = page.get('text_en', '')
            img_rel = page.get('image', '')
            if use_compressed:
                img_path = get_img(img_rel)
            else:
                img_path = os.path.join(base, 'public', img_rel) if img_rel else ''
                if not os.path.exists(img_path):
                    img_path = get_img(img_rel)  # fallback
            
            if pi == 0:
                if img_path: c.drawImage(img_path, 0, 0, W, H, preserveAspectRatio=False)
            else:
                c.setFillColor(white)
                c.rect(0, 0, W, H, fill=1, stroke=0)
                draw_image_fixed(c, img_path, IMG_H, IMG_Y)
                y = TEXT_AREA_H - 8*mm
                if txt_zh:
                    y = draw_text(c, txt_zh, _IMG_DRAW_X, y, _IMG_DRAW_W, 'HeitiSC', 10.5, black, lang='zh')
                    y -= 2*mm
                if txt_en:
                    y = draw_text(c, txt_en, _IMG_DRAW_X, y, _IMG_DRAW_W, 'SFNS', 10, black, lang='en')
                c.setFont('SFNS', 7)
                c.setFillColor(black)
                c.drawCentredString(W/2, 4*mm, str(cur_pg))
            
            c.showPage()
            cur_pg += 1
        print(f"  ✅ Story {ch}: {story['title']} ({len(pages)}p)")
    
    c.save()
    sz = os.path.getsize(out_path)
    total = cur_pg
    print(f"  📄 {total} pages, {sz/1024/1024:.1f} MB → {out_path}")
    return out_path

# All volumes to generate
volumes = [
    ([19,20,21,22,23,24], "Volume 3A", "Outdoor Adventures", "咘咘的故事书-3A-户外探索"),
    ([25,26,28,29,30,31], "Volume 3B", "Feelings & Friends", "咘咘的故事书-3B-情感与友谊"),
]

for chs, label, subtitle, name in volumes:
    print(f"\n📕 {label}: {subtitle}")
    # HD version (original images) → Desktop
    generate_volume(chs, label, subtitle, f"{name}.pdf", use_compressed=False)
    # Compressed version → Desktop subfolder
    generate_volume(chs, label, subtitle, f"咘咘故事书-压缩版/{name}-压缩.pdf", use_compressed=True)
