#!/usr/bin/env python3
"""Generate remaining pages 12-14 for Story 62"""
import json, requests, time, base64, subprocess, os

CONFIG = json.load(open(os.path.expanduser("~/.config/azure-openai/config.json")))
ENDPOINT = CONFIG["image2_eastus2_endpoint"]
API_KEY = CONFIG["image2_eastus2_api_key"]
OUT_DIR = "/Users/samyuan/.openclaw/workspace/bubu-stories/public/images/story62"

BUBU = "a small white rabbit toddler (100% snow-white fur, two long ears with pink insides, big brown eyes, small pink nose) wearing a light pink summer dress and a pink bow on top of her head between her ears"
NOMI = "a raccoon (grey-brown fur with black eye mask markings and ringed tail) wearing a blue-and-white striped sweater, big clever eyes, dexterous paws"
NONO = "a small red bird (bright red feathers, round body, tiny orange-yellow beak, round bright eyes)"
MAMA = "a cow mother (black and white patches, elegant) wearing a casual summer blouse and light pants"

PREFIX = "Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition 1024x1536. DAYTIME scene with natural daylight."

remaining = [
    (12, f"""{PREFIX} {BUBU} running excitedly toward a window, paws on the glass. {MAMA} standing behind with a gentle smile. Through the window: the rain is now just a light drizzle, sky slightly brighter grey, trees still but no longer bending wildly. Late afternoon daylight starting to peek through clouds. Hopeful atmosphere. Indoor living room scene."""),
    (13, f"""{PREFIX} OUTDOOR scene, bright sunny morning after the storm. Brilliant blue sky with a few white fluffy clouds. {BUBU} wearing yellow rain boots, jumping joyfully into a puddle with water splashing everywhere. Fallen green leaves scattered on the wet ground. Trees look fresh and clean. Everything sparkles with residual water droplets catching sunlight. Vibrant colors, happy energetic scene. {NOMI} and {NONO} watching nearby, NOMI smiling, NONO flying happily."""),
    (14, f"""{PREFIX} OUTDOOR scene, beautiful clear blue sky. {BUBU} standing looking up at the bright blue sky with a proud confident smile, arms slightly spread. {NOMI} standing beside her with a warm proud smile. {NONO} perched on NOMI's head cheerfully. Behind them: a clean street with a few scattered leaves, a rainbow faintly visible in the sky, sparkling clean world after rain. Bright warm sunlight, hopeful triumphant atmosphere. Summer morning.""")
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
            print(f"⏳ Rate limited, waiting {wait}s...")
            time.sleep(wait)
        else:
            print(f"❌ Page {page_num:02d} attempt {attempt+1}: {resp.status_code} - {resp.text[:200]}")
            time.sleep(5)
    return False

for page_num, prompt in remaining:
    print(f"--- Generating Page {page_num:02d} ---")
    generate_image(prompt, page_num)
    if page_num < 14:
        time.sleep(8)

print("\nDone!")
