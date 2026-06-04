#!/usr/bin/env python3
"""Generate Story 52 print-edition illustrations (P2-P15) + Volume 5B cover & TOC."""

import json, os, sys, time, base64, subprocess, requests

CONFIG = json.load(open(os.path.expanduser("~/.config/azure-openai/config.json")))
ENDPOINT = CONFIG["image2_eastus2_endpoint"]
API_KEY = CONFIG["image2_eastus2_api_key"]
API_VERSION = "2025-04-01-preview"

OUT_DIR = "/Users/samyuan/.openclaw/workspace/bubu-stories/print-edition/story52"
COVER_DIR = "/Users/samyuan/.openclaw/workspace/bubu-stories/print-edition"

BUBU = "a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a light pink summer dress with a small pink bow centered ON TOP OF HER HEAD between her two ears. Toddler-like round body."
NOMI = "a raccoon (NOMI) with grey-brown fur, black eye mask markings, ringed bushy tail, wearing a blue-and-white horizontally striped sweater, clever bright eyes, nimble paws."
NONO = "a small red bird (NONO) with bright red feathers, round bright eyes, orange-yellow beak. TWO wings, TWO small bird feet. NO ARMS NO HANDS — only wings."
YANYAN = "Teacher Yanyan, an orange tabby cat (warm orange fur with subtle stripes), kind green eyes, wearing a pink kindergarten apron over a light summer top. Adult-sized, much taller than the children."
FEIFEI = "Feifei, a grey-and-white tabby kitten with soft grey and white striped fur, big round eyes, wearing a pretty summer dress. Same size as Bubu."
SAM_DAD = "Sam Dad who is a GOLDEN RETRIEVER DOG (animal, not human). Golden fur all over, dog snout, floppy dog ears, wagging tail. Wears a casual summer polo shirt. Warm gentle dog smile."
TINA_MOM = "Tina Mom who is a BLACK-AND-WHITE COW (animal, not human). Black and white spotted fur, small curved horns, cow ears, hooves. Wears an elegant light summer dress. Gentle warm cow smile."
WAIPO = "Grandma (Waipo) who is a goat with light grey-white fur, small curved horns, kind brown eyes, wearing a floral summer blouse and light pants with a sun hat."
WAIGONG = "Grandpa (Waigong) who is a horse with dark brown fur, grey-white mane, steady deep eyes, wearing a polo shirt and casual summer pants."
BEAR_CLS = "a brown bear cub classmate in a summer T-shirt, round and chubby"
CORGI_CLS = "a corgi puppy classmate with brown-white fur, short legs, in a summer outfit"
CAT_CLS = "a grey-white tabby kitten classmate in summer clothes"
DEER_CLS = "a fawn classmate with white spots, slender legs, in summer clothes"

STYLE = "Pixar 3D animation style, warm soft lighting, children's picture book quality, vibrant colors. The bottom 20% of the image has a subtle dark gradient overlay (for text placement). NO TEXT, NO WORDS, NO LETTERS anywhere in the image. Pure illustration only."
SUMMER = "Setting: summer day in southern China, bright warm sunlight."

PAGES = [
    (2, f"{STYLE} {SUMMER} Scene: Early morning bedroom. {BUBU} bouncing excitedly on her bed, both ears standing tall with joy. {NOMI} standing beside the bed holding a pink bow ribbon, ready to help tie it. Sunlight streaming through curtains. Happy cheerful mood."),
    (3, f"{STYLE} {SUMMER} Scene: Kindergarten entrance gate, festive decorations with colorful banners and balloons. {YANYAN} wearing a big silly dinosaur headpiece/hat on her head (a plush dinosaur costume hood) while waving at children, laughing. {BUBU} at the gate laughing hard, nearly falling over with giggles. Other animal children arriving in background. Fun carnival atmosphere."),
    (4, f"{STYLE} {SUMMER} Scene: Kindergarten entrance path. {BUBU} and {FEIFEI} holding hands, walking happily into kindergarten together. {NONO} flying playfully above their heads. Festive decorations around. Both girls smiling brightly at each other."),
    (5, f"{STYLE} Scene: Kindergarten classroom transformed into a little theater. Colorful curtains drawn across the front. Lights dimmed, theatrical atmosphere. {YANYAN} by the curtain. {BUBU} and {FEIFEI} sitting right next to each other in the front row on small chairs, eyes wide with anticipation. Other animal children seated behind them. Stage lighting, cozy atmosphere."),
    (6, f"{STYLE} Scene: Puppet show stage viewed from audience perspective. On the puppet stage: a large scary MONSTER puppet (green/purple creature, big teeth, NOT a dinosaur) with mouth wide open, and a small panda puppet being gobbled up. In the foreground/audience: {BUBU} hugging {NOMI}'s arm tightly, eyes wide with scared excitement. Other children looking nervous and thrilled. Dramatic puppet show lighting."),
    (7, f"{STYLE} Scene: Puppet show stage. On the puppet stage: a brave PANDA DAD puppet (large panda with determined expression) chasing away the big monster puppet. The monster retreating. In the audience: {BUBU} clapping enthusiastically with big smile. {NONO} flying excited loops in the air above the children. All children clapping and cheering. Triumphant joyful mood."),
    (8, f"{STYLE} {SUMMER} Scene: A long kindergarten hallway/corridor. A very long row of small tables and chairs arranged in a single line stretching all the way down the hallway like a train. {YANYAN} gesturing at the setup with a big smile. Children including {BUBU} and {FEIFEI} looking amazed and surprised at the long 'train' of tables. Bright and cheerful."),
    (9, f"{STYLE} {SUMMER} Scene: The long hallway 'train breakfast'. Children sitting in a long single row at the connected tables like passengers on a train. {BUBU} sitting next to {FEIFEI}, {BEAR_CLS} across from them, {CORGI_CLS} behind. Tables have bread, milk cartons, and fruit. Everyone chatting happily. {NOMI} holding up a tiny camera taking a photo. Warm, joyful, communal eating scene."),
    (10, f"{STYLE} {SUMMER} Scene: The train breakfast hallway. {BUBU} holding a piece of bread like a steering wheel, pretending to drive a train, mouth open making 'choo choo' sounds. {FEIFEI} next to her also playing along. Other children laughing. {YANYAN} standing to the side, holding up a phone/camera taking photos with a warm smile. The long row of tables and children stretches into background. Playful and hilarious."),
    (11, f"{STYLE} {SUMMER} Scene: Kindergarten classroom. {YANYAN} standing by a large colorful box, pulling out bright gift bags with ribbons and handing them to excited children lined up. {BUBU} receiving her gift bag with sparkling excited eyes, reaching out eagerly. Other children around holding their bags. Festive gift-giving atmosphere."),
    (12, f"{STYLE} {SUMMER} Scene: {BUBU} cranking a small handheld hand-crank fan, cool breeze blowing her ears back slightly, delighted expression. {FEIFEI} next to her pressing buttons on a tiny handheld game console, focused and happy. They are about to swap toys — Bubu extending the fan toward Feifei. Gift bag wrapping on the ground. Bright, fun, sharing moment."),
    (13, f"{STYLE} {SUMMER} Scene: Kindergarten exit/gate area. {BUBU} running out excitedly holding gift bags, toward {WAIGONG} and {WAIPO} who are waiting with open arms and warm smiles. Bubu is animated, mouth open talking excitedly, showing them the hand-crank fan in one paw and the mini game console in the other. Warm golden afternoon light. Joyful reunion."),
    (14, f"{STYLE} Scene: Cozy bedroom at night, warm dim lamplight. {BUBU} lying in bed under a blanket, sleepy with a big yawn, still holding the small hand-crank fan. {NOMI} leaning against the pillow beside her, looking at Bubu warmly. {NONO} standing on the nightstand, eyes half-closed sleepily. Peaceful, dreamy, warm end-of-day feeling. Moonlight through window."),
    (15, f"{STYLE} {SUMMER} Scene: A joyful celebratory illustration. {BUBU} in the center, jumping with arms up in pure happiness, surrounded by floating colorful balloons, confetti, and streamers. {NOMI} and {NONO} celebrating beside her. Bright, festive, Children's Day party atmosphere. Radiating joy and childhood magic."),
]

def generate_image(prompt, size="1024x1536", quality="medium"):
    url = f"{ENDPOINT}?api-version={API_VERSION}"
    headers = {"api-key": API_KEY, "Content-Type": "application/json"}
    body = {"prompt": prompt, "n": 1, "size": size, "quality": quality, "output_format": "png"}
    
    for attempt in range(4):
        try:
            r = requests.post(url, headers=headers, json=body, timeout=120)
            if r.status_code == 429:
                wait = 45
                print(f"  429 rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            if r.status_code != 200:
                print(f"  Error {r.status_code}: {r.text[:200]}")
                if attempt < 3:
                    time.sleep(15)
                    continue
                return None
            data = r.json()
            b64 = data["data"][0]["b64_json"]
            return base64.b64decode(b64)
        except Exception as e:
            print(f"  Exception: {e}")
            if attempt < 3:
                time.sleep(15)
                continue
            return None
    return None

def save_as_jpg(png_bytes, jpg_path):
    tmp = jpg_path.replace(".jpg", "_tmp.png")
    with open(tmp, "wb") as f:
        f.write(png_bytes)
    subprocess.run(["ffmpeg", "-y", "-i", tmp, "-q:v", "2", jpg_path], 
                   capture_output=True, timeout=30)
    os.remove(tmp)

# --- Task 1: Story 52 pages ---
print("=== Task 1: Story 52 Illustrations ===")
for page_num, prompt in PAGES:
    jpg_path = os.path.join(OUT_DIR, f"page-{page_num:02d}.jpg")
    if os.path.exists(jpg_path):
        print(f"P{page_num}: already exists, skipping")
        continue
    print(f"P{page_num}: generating...")
    img = generate_image(prompt)
    if img:
        save_as_jpg(img, jpg_path)
        sz = os.path.getsize(jpg_path)
        print(f"  P{page_num}: saved ({sz//1024}KB)")
    else:
        print(f"  P{page_num}: FAILED")
    time.sleep(8)

# --- Task 2: Volume 5B Cover and TOC ---
print("\n=== Task 2: Volume 5B Cover & TOC ===")

COVER_PROMPT = f"""Pixar 3D animation movie poster style, cinematic lighting, warm golden tones. A kindergarten classroom scene with a sense of GROWTH and confidence. {BUBU} walking confidently through a bright kindergarten classroom, looking forward with determination and a warm smile. Sunlight streaming through large windows. Subtle details: small backpack, colorful artwork on walls. The composition is like a movie poster — dramatic perspective, the character walking toward the viewer. English title "Growing Every Day" in elegant modern serif typography (NOT bubble letters, NOT cartoon font — sophisticated, like an indie film poster). Subtitle below: "Volume 9B". Warm, inspiring, hopeful mood. NO Chinese text."""

TOC_PROMPT = f"""Pixar 3D animation style, warm soft lighting. A cozy scene: {BUBU} sitting on a soft rug in a kindergarten reading corner, surrounded by picture books and plush toys, {NOMI} beside her, {NONO} perched on a nearby shelf. Warm afternoon light. On the image, elegantly laid out like a book's table of contents page in clean modern typography (NOT bubble font): 

"Table of Contents"
"Story 49 — Bubu Didn't Cry Today"
"Story 50 — Bubu Learns to Sit Still" 
"Story 51 — Bubu Can Ask for the Potty Now!"
"Story 52 — Bubu's Children's Day"

ALL TEXT IN ENGLISH. Clean, warm, inviting book interior design feel."""

cover_path = os.path.join(COVER_DIR, "volume5b-print-cover.jpg")
toc_path = os.path.join(COVER_DIR, "volume5b-print-toc.jpg")

if not os.path.exists(cover_path):
    print("Generating cover...")
    img = generate_image(COVER_PROMPT, size="1024x1536", quality="medium")
    if img:
        save_as_jpg(img, cover_path)
        print(f"  Cover saved ({os.path.getsize(cover_path)//1024}KB)")
    else:
        print("  Cover FAILED")
    time.sleep(8)

if not os.path.exists(toc_path):
    print("Generating TOC...")
    img = generate_image(TOC_PROMPT, size="1024x1536", quality="medium")
    if img:
        save_as_jpg(img, toc_path)
        print(f"  TOC saved ({os.path.getsize(toc_path)//1024}KB)")
    else:
        print("  TOC FAILED")

# --- Summary ---
print("\n=== Final Summary ===")
for page_num, _ in PAGES:
    p = os.path.join(OUT_DIR, f"page-{page_num:02d}.jpg")
    if os.path.exists(p):
        print(f"  story52/page-{page_num:02d}.jpg: {os.path.getsize(p)//1024}KB")
    else:
        print(f"  story52/page-{page_num:02d}.jpg: MISSING")

for name in ["volume5b-print-cover.jpg", "volume5b-print-toc.jpg"]:
    p = os.path.join(COVER_DIR, name)
    if os.path.exists(p):
        print(f"  {name}: {os.path.getsize(p)//1024}KB")
    else:
        print(f"  {name}: MISSING")
