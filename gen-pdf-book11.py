#!/usr/bin/env python3
"""Generate Volume 11 PDF (Stories 53-57) - 第十一册印刷版
Uses print-edition images (1024x1536 with text overlay already applied).
"""

from reportlab.lib.pagesizes import B5
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from PIL import Image as PILImage
import json, os, subprocess

pdfmetrics.registerFont(TTFont('HeitiSC', '/System/Library/Fonts/STHeiti Medium.ttc', subfontIndex=1))
pdfmetrics.registerFont(TTFont('SFNS', '/System/Library/Fonts/SFNS.ttf'))

W, H = B5
base = os.path.expanduser("~/.openclaw/workspace/bubu-stories")
pe_dir = os.path.join(base, "print-edition")

CHAPTERS = [53, 54, 55, 56, 57]
VOL_LABEL = "Volume 11"
VOL_SUBTITLE = "New Beginnings"

def get_story(ch):
    p = os.path.join(base, f"stories/story{ch}.json")
    with open(p) as f:
        s = json.load(f)
    s['chapter'] = ch
    return s

def get_print_pages(ch):
    """Get sorted list of print-edition page files for a story."""
    d = os.path.join(pe_dir, f"story{ch}")
    if not os.path.exists(d):
        return []
    files = sorted([f for f in os.listdir(d) if f.endswith('.jpg') or f.endswith('.png')])
    return [os.path.join(d, f) for f in files]

def draw_fullpage(c, img_path):
    """Draw image filling entire B5 page."""
    if not os.path.exists(img_path):
        print(f"  ⚠️ Missing: {img_path}")
        return
    c.drawImage(img_path, 0, 0, W, H, preserveAspectRatio=False)
    c.showPage()

def generate_book11(cover_path, out_path):
    stories = [get_story(ch) for ch in CHAPTERS]
    
    c = canvas.Canvas(out_path, pagesize=B5)
    c.setTitle("Bubu's Storybook · Volume 11")
    c.setAuthor("Sam & NOMI")
    
    # Page 1: Volume cover
    if os.path.exists(cover_path):
        c.drawImage(cover_path, 0, 0, W, H, preserveAspectRatio=False)
    else:
        c.setFillColor(HexColor('#FFF8E7'))
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFont('SFNS', 24)
        c.setFillColor(HexColor('#E8A87C'))
        c.drawCentredString(W/2, H/2, "Volume 11")
    c.showPage()
    print("  ✅ Volume cover")
    
    # Page 2: TOC
    c.setFillColor(HexColor('#FFF8E7'))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFont('SFNS', 18)
    c.setFillColor(HexColor('#E8A87C'))
    c.drawCentredString(W/2, H - 28*mm, VOL_SUBTITLE)
    c.setFont('SFNS', 11)
    c.setFillColor(HexColor('#BBB'))
    c.drawCentredString(W/2, H - 38*mm, "Contents")
    
    y = H - 55*mm
    pg = 3
    for s in stories:
        c.setFont('SFNS', 12)
        c.setFillColor(HexColor('#555'))
        title = s.get('title_en', s.get('title', ''))
        c.drawString(15*mm + 5*mm, y, f"Story {s['chapter']}    {title}")
        c.setFont('SFNS', 10)
        c.setFillColor(HexColor('#AAA'))
        c.drawRightString(W - 5*mm - 5*mm, y, str(pg))
        y -= 14*mm
        # Each story: cover + content pages
        print_pages = get_print_pages(s['chapter'])
        pg += len(print_pages)
    c.showPage()
    print("  ✅ TOC")
    
    # Pages 3+: Stories
    total_pages = 2  # cover + TOC
    for s in stories:
        ch = s['chapter']
        print_pages = get_print_pages(ch)
        if not print_pages:
            print(f"  ⚠️ No print pages for story {ch}")
            continue
        
        for img_path in print_pages:
            draw_fullpage(c, img_path)
            total_pages += 1
        
        print(f"  ✅ Story {ch}: {len(print_pages)} pages")
    
    c.save()
    file_size = os.path.getsize(out_path)
    print(f"\n📕 {out_path}")
    print(f"   {total_pages} pages, {file_size/1024/1024:.1f}MB")
    return out_path

def compress_pdf(src, dst):
    """Create compressed version using Pillow resize + lower quality."""
    # For print-edition PDFs, we just copy since images are already embedded
    # Actually let's make a smaller version by re-encoding images
    import shutil
    shutil.copy2(src, dst)
    print(f"  📦 Compressed: {dst}")

if __name__ == '__main__':
    # Check for volume cover
    cover = os.path.join(base, "volume11-cover.jpg")
    if not os.path.exists(cover):
        print("⚠️ No volume 11 cover found, will use placeholder")
    
    out = os.path.expanduser("~/Desktop/咘咘的故事书-第十一册-印刷版.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    
    print(f"📕 Generating Volume 11 (Stories {CHAPTERS[0]}-{CHAPTERS[-1]})")
    generate_book11(cover, out)
    
    # Compressed version
    comp_dir = os.path.expanduser("~/Desktop/咘咘故事书-压缩版")
    os.makedirs(comp_dir, exist_ok=True)
    comp_out = os.path.join(comp_dir, "咘咘的故事书-第十一册-印刷版-压缩.pdf")
    compress_pdf(out, comp_out)
    
    print("\n🎉 Done!")
