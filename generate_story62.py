#!/usr/bin/env python3
"""Generate all images for Story 62: Typhoon Hongxia Is Coming!"""
import json, requests, time, base64, subprocess, os

CONFIG = json.load(open(os.path.expanduser("~/.config/azure-openai/config.json")))
ENDPOINT = CONFIG["image2_eastus2_endpoint"]
API_KEY = CONFIG["image2_eastus2_api_key"]
OUT_DIR = "/Users/samyuan/.openclaw/workspace/bubu-stories/public/images/story62"
os.makedirs(OUT_DIR, exist_ok=True)

# Character descriptions
BUBU = "a small white rabbit toddler (100% snow-white fur, two long ears with pink insides, big brown eyes, small pink nose) wearing a light pink summer dress and a pink bow on top of her head between her ears"
NOMI = "a raccoon (grey-brown fur with black eye mask markings and ringed tail) wearing a blue-and-white striped sweater, big clever eyes, dexterous paws"
NONO = "a small red bird (bright red feathers, round body, tiny orange-yellow beak, round bright eyes)"
COCO = "a red panda (reddish-brown fur, round face, big bright eyes) wearing a yellow scarf"
MAMA = "a cow mother (black and white patches, elegant) wearing a casual summer blouse and light pants"
NAINAI = "a small monkey grandmother (light brown soft fur, warm peach-colored face, kind big eyes) wearing a Chinese floral blouse"

PREFIX = "Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition 1024x1536. DAYTIME scene with natural daylight."

prompts = [
    # Page 01 - Cover
    f"""Pixar 3D animation style, cinematic children's picture book cover poster, dramatic stormy daylight, vertical portrait 1024x1536.

TOP: Large 3D weathered metallic silver letters spelling "Typhoon Hongxia Is Coming!" in a bold cinematic font with wind streaks and rain droplets on the letters, slightly tilted as if blown by wind.

CENTER: {BUBU} standing by a large window looking out at heavy rain and wind (DAYTIME, grey stormy sky), her ears blowing slightly. Next to her, {NOMI} holding a colorful picture book titled "台风小百科" with cute cloud illustrations on the cover.

RIGHT SIDE: {NONO} being blown sideways by the wind near the window, wings spread, looking comically windswept.

BACKGROUND: Through the window, visible stormy grey daytime sky, trees bending dramatically in wind, heavy rain sheets. Inside is warm and cozy with soft interior lighting. Rich layered movie poster depth composition.""",

    # Page 02 - Grey morning
    f"""{PREFIX} A bedroom scene in early morning with grey overcast daylight coming through the window. {BUBU} sitting up in her small bed, looking toward the window with curious eyes. Outside the window: grey cloudy sky, trees swaying dramatically in strong wind, leaves flying. The room is cozy with stuffed animals on the bed. Summer morning, natural grey daylight fills the room.""",

    # Page 03 - Mama explains
    f"""{PREFIX} A living room scene. {MAMA} kneeling down talking to {BUBU} who looks up with big curious eyes and tilted head. Mama has a gentle expression. Through the window behind them: grey windy sky, trees swaying. The room is bright with daylight. Summer casual home clothing.""",

    # Page 04 - NOMI explains typhoon formation
    f"""{PREFIX} {NOMI} sitting on a couch holding open a colorful children's picture book showing a cute illustrated diagram of typhoon formation: warm blue ocean at bottom with steam rising, white clouds forming in a spiral pattern with cute arrow indicators, a big friendly swirl at the top. {BUBU} leaning in close looking at the book with amazement. The illustration in the book is simple, colorful, child-friendly. Living room with grey daylight from window.""",

    # Page 05 - Coco arrives
    f"""{PREFIX} Front door of the apartment. {COCO} standing at the doorway with a big smile, slightly wet from rain, shaking off water droplets. {BUBU} at the door greeting Coco excitedly. Behind Coco through the open door: a hallway. Bright indoor lighting, cheerful atmosphere. Both wearing summer casual clothes.""",

    # Page 06 - NONO at window
    f"""{PREFIX} {NONO} perched on a windowsill, pressed against the glass, watching outside with excited round eyes. {BUBU} standing next to the window looking out too. Through the window: trees bending dramatically in strong wind, green leaves flying through the air, grey stormy daytime sky. The wind is visible through the bending trees and flying debris. Indoor warm lighting contrasts with grey outdoor scene.""",

    # Page 07 - NOMI explains consequences
    f"""{PREFIX} {NOMI} standing and gesturing with paws while explaining something serious but gentle. {BUBU} sitting on the floor looking up attentively. Behind them a window showing: heavy rain, a tree partially bent, wind blowing. NOMI has a thoughtful teaching expression. Cozy living room, grey daylight through window, summer.""",

    # Page 08 - Family prepares
    f"""{PREFIX} A busy home preparation scene. {MAMA} checking a window latch. {NAINAI} arranging water bottles and snacks on a table. {BUBU} carrying a small flower pot from the balcony direction, talking to the plant lovingly. The balcony door is open showing grey rainy sky. Warm indoor scene, everyone working together happily. Summer casual home clothes.""",

    # Page 09 - Watching rain
    f"""{PREFIX} {BUBU} and {COCO} both pressing their faces against a large window, looking out with wide amazed eyes. Outside: dramatic heavy rain pouring down, raindrops visible hitting the glass, grey stormy daytime sky, everything blurry through the rain. The two friends are close together, pointing at the rain. Cozy indoor scene with warm lighting. Rain streaks visible on the window glass.""",

    # Page 10 - Bubu recites rules
    f"""{PREFIX} {BUBU} standing proudly, holding up three fingers on one paw, reciting with a confident expression. {NOMI} sitting nearby giving a thumbs up with a proud smile. {NONO} on NOMI's shoulder looking impressed. Living room with cozy interior. Grey daylight from window. A small whiteboard or paper on the wall behind them showing three simple icons: a house (stay inside), a window (close it), a water bottle (prepare supplies).""",

    # Page 11 - Typhoon will pass
    f"""{PREFIX} {COCO} speaking cheerfully with a reassuring smile. {NOMI} nodding in agreement. {BUBU} listening with a relieved expression. They are all sitting together on a couch with cushions. Through the window behind them: still rainy but the grey sky seems slightly lighter. Warm cozy indoor atmosphere, summer afternoon daylight.""",

    # Page 12 - Wind dying down
    f"""{PREFIX} {BUBU} running excitedly toward a window, paws on the glass. {MAMA} standing behind with a gentle smile. Through the window: the rain is now just a light drizzle, sky slightly brighter grey, trees still but no longer bending wildly. Late afternoon daylight starting to peek through clouds. Hopeful atmosphere. Indoor living room scene.""",

    # Page 13 - Splashing in puddles
    f"""{PREFIX} OUTDOOR scene, bright sunny morning after the storm. Brilliant blue sky with a few white fluffy clouds. {BUBU} wearing yellow rain boots, jumping joyfully into a puddle with water splashing everywhere. Fallen green leaves scattered on the wet ground. Trees look fresh and clean. Everything sparkles with residual water droplets catching sunlight. Vibrant colors, happy energetic scene. {NOMI} and {NONO} watching nearby, NOMI smiling, NONO flying happily.""",

    # Page 14 - Ending
    f"""{PREFIX} OUTDOOR scene, beautiful clear blue sky. {BUBU} standing looking up at the bright blue sky with a proud confident smile, arms slightly spread. {NOMI} standing beside her with a warm proud smile. {NONO} perched on NOMI's head cheerfully. Behind them: a clean street with a few scattered leaves, a rainbow faintly visible in the sky, sparkling clean world after rain. Bright warm sunlight, hopeful triumphant atmosphere. Summer morning."""
]

def generate_image(prompt, page_num):
    url = f"{ENDPOINT}?api-version=2025-04-01-preview"
    headers = {"api-key": API_KEY, "Content-Type": "application/json"}
    body = {"prompt": prompt, "n": 1, "size": "1024x1536", "quality": "medium", "output_format": "png"}
    
    for attempt in range(3):
        resp = requests.post(url, headers=headers, json=body, timeout=120)
        if resp.status_code == 200:
            data = resp.json()
            img_b64 = data["data"][0]["b64_json"]
            png_path = f"{OUT_DIR}/page-{page_num:02d}.png"
            jpg_path = f"{OUT_DIR}/page-{page_num:02d}.jpg"
            with open(png_path, "wb") as f:
                f.write(base64.b64decode(img_b64))
            subprocess.run(["ffmpeg", "-y", "-i", png_path, "-q:v", "4", jpg_path], capture_output=True)
            os.remove(png_path)
            size = os.path.getsize(jpg_path)
            print(f"✅ Page {page_num:02d}: {size//1024}KB")
            return True
        elif resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", 15))
            print(f"⏳ Page {page_num:02d}: Rate limited, waiting {wait}s...")
            time.sleep(wait)
        else:
            print(f"❌ Page {page_num:02d} attempt {attempt+1}: {resp.status_code} - {resp.text[:200]}")
            if "content_policy" in resp.text.lower():
                print("   Safety filter triggered, simplifying prompt...")
                prompt = prompt.replace("dramatic", "gentle").replace("stormy", "cloudy")
            time.sleep(5)
    return False

print(f"Generating {len(prompts)} images for Story 62...")
for i, prompt in enumerate(prompts):
    page = i + 1
    print(f"\n--- Generating Page {page:02d} ---")
    success = generate_image(prompt, page)
    if not success:
        print(f"⚠️ FAILED Page {page:02d} after 3 attempts")
    if i < len(prompts) - 1:
        time.sleep(8)

print("\n🎉 Done! Checking files...")
for i in range(1, 15):
    path = f"{OUT_DIR}/page-{i:02d}.jpg"
    if os.path.exists(path):
        print(f"  {path}: {os.path.getsize(path)//1024}KB")
    else:
        print(f"  ⚠️ MISSING: {path}")
