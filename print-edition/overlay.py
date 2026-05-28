#!/usr/bin/env python3
"""Overlay text panels on pure illustrations for Story 1 print edition"""

from PIL import Image, ImageDraw, ImageFont
import json, os, re

base = os.path.expanduser('~/.openclaw/workspace/bubu-stories')
img_dir = os.path.join(base, 'print-edition/story1')
out_dir = os.path.join(base, 'print-edition/story1-final')
os.makedirs(out_dir, exist_ok=True)

# Load story
with open(os.path.join(base, 'stories/story1.json')) as f:
    story = json.load(f)

# Fonts
FONT_ZH = '/System/Library/Fonts/STHeiti Medium.ttc'
FONT_EN = '/System/Library/Fonts/SFNS.ttf'
ZH_SIZE = 28  # at 1024px width this is readable
EN_SIZE = 22

font_zh = ImageFont.truetype(FONT_ZH, ZH_SIZE, index=1)
font_en = ImageFont.truetype(FONT_EN, EN_SIZE)
font_zh_title = ImageFont.truetype(FONT_ZH, 52, index=1)
font_en_title = ImageFont.truetype(FONT_EN, 36)

# Layout constants (in pixels, image is 1024x1536)
W, H = 1024, 1536
LEFT_MARGIN = int(W * 0.10)   # 10% binding
RIGHT_MARGIN = int(W * 0.05)  # 5% right
BOTTOM_PAD = int(H * 0.02)    # 2% bottom padding
TEXT_LEFT = LEFT_MARGIN + 15
TEXT_RIGHT = W - RIGHT_MARGIN - 15
TEXT_WIDTH = TEXT_RIGHT - TEXT_LEFT

def strip_emoji(text):
    return re.sub(r'[\U0001F300-\U0001FAFF\U00002702-\U000027B0]', '', text).strip()

def wrap_text(text, font, max_width, draw):
    """Wrap text to fit within max_width pixels."""
    if not text:
        return []
    lines = []
    for para in text.split('\n'):
        if not para.strip():
            lines.append('')
            continue
        words_or_chars = list(para) if any(ord(c) > 0x2E80 for c in para[:5]) else para.split(' ')
        current = ''
        for item in words_or_chars:
            test = current + item if any(ord(c) > 0x2E80 for c in para[:5]) else (current + ' ' + item).strip() if current else item
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] > max_width and current:
                lines.append(current)
                current = item
            else:
                current = test
        if current:
            lines.append(current)
    return lines

def process_page(page_num, page_data):
    img_path = os.path.join(img_dir, f'page-{page_num:02d}.jpg')
    if not os.path.exists(img_path):
        print(f'  ⚠️ Missing {img_path}')
        return
    
    img = Image.open(img_path).convert('RGBA')
    # Resize to exact 1024x1536 if needed
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    
    txt_zh = strip_emoji(page_data.get('text', ''))
    txt_en = strip_emoji(page_data.get('text_en', ''))
    
    if page_num == 1:
        # COVER: title centered in upper area, no panel
        overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        title_zh = story['title']
        title_en = story['title_en']
        
        # Semi-transparent dark band at top
        draw.rectangle([0, 0, W, 200], fill=(0, 0, 0, 100))
        
        # Chinese title centered
        bbox = draw.textbbox((0, 0), title_zh, font=font_zh_title)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, 50), title_zh, font=font_zh_title, fill=(255, 255, 255, 240))
        
        # English title centered below
        bbox = draw.textbbox((0, 0), title_en, font=font_en_title)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, 120), title_en, font=font_en_title, fill=(255, 245, 220, 220))
        
        img = Image.alpha_composite(img, overlay)
    
    elif txt_zh or txt_en:
        # CONTENT PAGE: panel at bottom
        overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Calculate text height needed
        zh_lines = wrap_text(txt_zh, font_zh, TEXT_WIDTH, draw) if txt_zh else []
        en_lines = wrap_text(txt_en, font_en, TEXT_WIDTH, draw) if txt_en else []
        
        zh_line_h = ZH_SIZE + 8
        en_line_h = EN_SIZE + 6
        gap = 10  # gap between zh and en
        
        total_text_h = len(zh_lines) * zh_line_h + len(en_lines) * en_line_h + gap + 30  # 30 = top+bottom padding
        
        # Panel position: fixed left, right, bottom; top varies
        panel_bottom = H - BOTTOM_PAD
        panel_top = panel_bottom - total_text_h
        panel_left = LEFT_MARGIN
        panel_right = W - RIGHT_MARGIN
        
        # Draw semi-transparent panel
        draw.rounded_rectangle(
            [panel_left, panel_top, panel_right, panel_bottom],
            radius=12,
            fill=(15, 25, 60, 170)  # dark navy, ~67% opacity
        )
        
        # Draw Chinese text
        y = panel_top + 15
        for line in zh_lines:
            draw.text((TEXT_LEFT, y), line, font=font_zh, fill=(255, 255, 255, 240))
            y += zh_line_h
        
        y += gap
        
        # Draw English text
        for line in en_lines:
            draw.text((TEXT_LEFT, y), line, font=font_en, fill=(255, 245, 220, 200))
            y += en_line_h
        
        img = Image.alpha_composite(img, overlay)
    
    # Save as RGB JPG
    img_rgb = img.convert('RGB')
    out_path = os.path.join(out_dir, f'page-{page_num:02d}.jpg')
    img_rgb.save(out_path, 'JPEG', quality=95)
    sz = os.path.getsize(out_path)
    print(f'  ✅ page-{page_num:02d}.jpg ({sz//1024}KB)')

# Process all pages
print('Overlaying text on illustrations...')
for i, page in enumerate(story['pages']):
    process_page(i + 1, page)

print('\nDone! All pages in print-edition/story1-final/')
