#!/usr/bin/env python3
"""Overlay text panels on pure illustrations - v2 with proper typesetting"""

from PIL import Image, ImageDraw, ImageFont
import json, os, re

base = os.path.expanduser('~/.openclaw/workspace/bubu-stories')
story_json = os.path.join(base, 'stories/story1.json')

# Will be called with img_dir and out_dir as arguments
import sys
img_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base, 'print-edition/story1')
out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(base, 'print-edition/story1-final-v2')
os.makedirs(out_dir, exist_ok=True)

with open(story_json) as f:
    story = json.load(f)

FONT_ZH = '/System/Library/Fonts/STHeiti Medium.ttc'
FONT_EN = '/System/Library/Fonts/SFNS.ttf'
ZH_SIZE = 28
EN_SIZE = 22

font_zh = ImageFont.truetype(FONT_ZH, ZH_SIZE, index=1)
font_en = ImageFont.truetype(FONT_EN, EN_SIZE)

W, H = 1024, 1536
LEFT_MARGIN = int(W * 0.10)
RIGHT_MARGIN = int(W * 0.05)
TEXT_LEFT = LEFT_MARGIN + 15
TEXT_RIGHT = W - RIGHT_MARGIN - 15
TEXT_WIDTH = TEXT_RIGHT - TEXT_LEFT
BOTTOM_PAD = int(H * 0.02)

zh_line_h = ZH_SIZE + 8
en_line_h = EN_SIZE + 6

# Punctuation that must NOT start a line (Chinese typesetting rule)
NO_LINE_START = set('，。！？、；：）】」』》〉…—～·,!?;:)]\'"')

def strip_emoji(text):
    return re.sub(r'[\U0001F300-\U0001FAFF\U00002702-\U000027B0]', '', text).strip()

def wrap_zh_proper(text, font, max_w, draw):
    """Wrap Chinese text with proper punctuation avoidance at line start."""
    if not text:
        return []
    lines = []
    for para in text.split('\n'):
        if not para.strip():
            lines.append('')
            continue
        chars = list(para)
        cur = ''
        i = 0
        while i < len(chars):
            ch = chars[i]
            test = cur + ch
            bbox = draw.textbbox((0, 0), test, font=font)
            tw = bbox[2] - bbox[0]
            
            if tw > max_w and cur:
                # Before breaking, check if next char is punctuation
                next_ch = chars[i] if i < len(chars) else ''
                if next_ch in NO_LINE_START:
                    # Pull the punctuation back to current line
                    cur += next_ch
                    i += 1
                    # Keep pulling if there are consecutive punctuation
                    while i < len(chars) and chars[i] in NO_LINE_START:
                        cur += chars[i]
                        i += 1
                    lines.append(cur)
                    cur = ''
                else:
                    lines.append(cur)
                    cur = ch
                    i += 1
            else:
                cur = test
                i += 1
        if cur:
            lines.append(cur)
    return lines

def wrap_en_proper(text, font, max_w, draw):
    """Wrap English text by word boundaries."""
    if not text:
        return []
    lines = []
    for para in text.split('\n'):
        if not para.strip():
            lines.append('')
            continue
        words = para.split(' ')
        cur = ''
        for word in words:
            test = (cur + ' ' + word).strip() if cur else word
            bbox = draw.textbbox((0, 0), test, font=font)
            tw = bbox[2] - bbox[0]
            if tw > max_w and cur:
                lines.append(cur)
                cur = word
            else:
                cur = test
        if cur:
            lines.append(cur)
    return lines

def process_page(page_num, page_data, draw_dummy):
    img_path = os.path.join(img_dir, f'page-{page_num:02d}.jpg')
    if not os.path.exists(img_path):
        print(f'  ⚠️ Missing {img_path}')
        return
    
    img = Image.open(img_path).convert('RGBA')
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    
    txt_zh = strip_emoji(page_data.get('text', ''))
    txt_en = strip_emoji(page_data.get('text_en', ''))
    
    if page_num == 1:
        # Cover: use as-is (original cover)
        pass
    elif txt_zh or txt_en:
        overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        zh_lines = wrap_zh_proper(txt_zh, font_zh, TEXT_WIDTH, draw) if txt_zh else []
        en_lines = wrap_en_proper(txt_en, font_en, TEXT_WIDTH, draw) if txt_en else []
        
        gap = 10
        padding_top = 15
        padding_bottom = 15
        total_text_h = len(zh_lines) * zh_line_h + len(en_lines) * en_line_h + gap + padding_top + padding_bottom
        
        panel_bottom = H - BOTTOM_PAD
        panel_top = panel_bottom - total_text_h
        panel_left = LEFT_MARGIN
        panel_right = W - RIGHT_MARGIN
        
        # Draw panel
        draw.rounded_rectangle(
            [panel_left, panel_top, panel_right, panel_bottom],
            radius=12,
            fill=(15, 25, 60, 170)
        )
        
        # Draw Chinese
        y = panel_top + padding_top
        for line in zh_lines:
            draw.text((TEXT_LEFT, y), line, font=font_zh, fill=(255, 255, 255, 240))
            y += zh_line_h
        
        y += gap
        
        # Draw English
        for line in en_lines:
            draw.text((TEXT_LEFT, y), line, font=font_en, fill=(255, 245, 220, 200))
            y += en_line_h
        
        # Verify text doesn't overflow
        if y > panel_bottom - 5:
            print(f'  ⚠️ P{page_num}: text might overflow (y={y}, bottom={panel_bottom})')
        
        img = Image.alpha_composite(img, overlay)
    
    # Add page number (bottom right, outside panel) for all pages except cover
    if page_num > 1:
        pg_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        pg_draw = ImageDraw.Draw(pg_overlay)
        font_pg = ImageFont.truetype(FONT_EN, 16)
        pg_text = str(page_num)
        bbox = pg_draw.textbbox((0, 0), pg_text, font=font_pg)
        pg_w = bbox[2] - bbox[0]
        pg_x = W - RIGHT_MARGIN - pg_w - 5
        pg_y = H - 25
        pg_draw.text((pg_x, pg_y), pg_text, font=font_pg, fill=(80, 80, 80, 200))
        img = Image.alpha_composite(img, pg_overlay)
    
    img_rgb = img.convert('RGB')
    out_path = os.path.join(out_dir, f'page-{page_num:02d}.png')
    img_rgb.save(out_path, 'PNG')
    sz = os.path.getsize(out_path)
    print(f'  ✅ page-{page_num:02d}.png ({sz//1024}KB)')

# Verify wrapping first
dummy_img = Image.new('RGB', (W, H))
dummy_draw = ImageDraw.Draw(dummy_img)
print('=== Verifying text wrapping ===')
all_ok = True
for i, page in enumerate(story['pages']):
    if i == 0:
        continue
    txt_zh = strip_emoji(page.get('text', ''))
    zh_lines = wrap_zh_proper(txt_zh, font_zh, TEXT_WIDTH, dummy_draw)
    for li, line in enumerate(zh_lines):
        if line and line[0] in NO_LINE_START:
            print(f'❌ P{i+1} line {li+1}: starts with "{line[0]}"')
            all_ok = False

if all_ok:
    print('✅ All wrapping rules verified')
else:
    print('⚠️ Some issues found but proceeding')

print('\n=== Processing pages ===')
for i, page in enumerate(story['pages']):
    process_page(i + 1, page, dummy_draw)

print('\nDone!')
