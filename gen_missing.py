#!/usr/bin/env python3
"""Regenerate missing pages for Story 58"""
import json, time, base64, urllib.request, urllib.error, os

API_KEY = "G0XzcVpk6KUGX53HbGfW6nBFiU4yh4Wjfowo8BSseYoSL8HAL9E4JQQJ99CCACHYHv6XJ3w3AAAAACOGJIkM"
ENDPOINT = "https://kaixi-mmimphd8-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-image-2/images/generations?api-version=2025-04-01-preview"
OUT_DIR = "/Users/samyuan/.openclaw/workspace/bubu-stories/public/images/story58"

BUBU = "a small white rabbit toddler (snow-white fur, exactly TWO long ears with pink inner sides, large round brown eyes, small pink nose) wearing a pink summer dress with a pink bow centered ON TOP OF HER HEAD between her two ears, toddler proportions"
TEACHER_KATE = "a red fox (reddish-brown fur, white belly, amber eyes, fluffy tail) wearing a light yellow top with white apron, slender and lively"
TEACHER_YANZI = "a swallow bird (black back, white belly, distinctive forked swallow tail, small and agile) wearing a light blue apron"
GRANDPA = "an elderly horse (dark brown fur, grey-white mane) wearing a summer polo shirt and light pants"
GRANDMA = "an elderly goat (light grey-white fur, small curved horns) wearing a summer floral blouse with sun hat"
NOMI = "a raccoon (grey-brown fur with black eye mask markings, ringed tail) wearing a blue-and-white striped sweater"
NONO = "a small red bird (bright red feathers, round body, orange-yellow beak, NO ARMS NO HANDS only wings and bird feet)"
PREFIX = "Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition 1024x1536. Summer day in Shenzhen, China."

pages = {
    "page-05.jpg": f"{PREFIX} In a bright classroom, {TEACHER_KATE} walking toward {BUBU} with a friendly smile, holding a small colorful ukulele. The fox's fluffy tail sways gently. Bubu looks up with curious big eyes and a smile. A colorful alphabet poster on the wall behind them. Other animal toddlers watching nearby. Bottom 20% naturally darkened.",
    "page-12.jpg": f"{PREFIX} Outdoor playground in bright summer sunshine. {BUBU} going down a colorful slide with arms up, laughing joyfully. Other animal toddlers (a small brown bear on swings, a corgi puppy running) playing around. {TEACHER_YANZI} flying overhead watching the children with a smile. Green trees, blue sky, modern playground equipment. Bottom 20% naturally darkened.",
    "page-13.jpg": f"{PREFIX} Warm evening living room scene. {BUBU} sitting on a cozy couch, hugging {NOMI} on her left side while {NONO} is perched on her right shoulder. Bubu's mouth is open excitedly telling them about her day, eyes sparkling. In the background through a window, golden evening light. A framed family photo on the wall. Cozy warm home atmosphere. Bottom 20% naturally darkened.",
}

def generate_image(prompt, filename, attempt=1):
    data = json.dumps({"prompt": prompt, "n": 1, "size": "1024x1536", "quality": "medium", "output_format": "png"}).encode()
    req = urllib.request.Request(ENDPOINT, data=data, headers={"Content-Type": "application/json", "api-key": API_KEY})
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        result = json.loads(resp.read())
        img_b64 = result["data"][0]["b64_json"]
        png_path = os.path.join(OUT_DIR, filename.replace('.jpg', '.png'))
        with open(png_path, 'wb') as f:
            f.write(base64.b64decode(img_b64))
        jpg_path = os.path.join(OUT_DIR, filename)
        os.system(f'ffmpeg -y -i "{png_path}" -q:v 4 "{jpg_path}" 2>/dev/null')
        os.remove(png_path)
        size = os.path.getsize(jpg_path)
        print(f"OK {filename}: {size/1024:.0f}KB", flush=True)
        return True
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.readable() else ""
        if e.code == 429 and attempt <= 3:
            print(f"429 on {filename}, waiting 45s...", flush=True)
            time.sleep(45)
            return generate_image(prompt, filename, attempt+1)
        print(f"FAIL {filename}: HTTP {e.code} - {body[:200]}", flush=True)
        return False
    except Exception as e:
        print(f"FAIL {filename}: {e}", flush=True)
        return False

for filename, prompt in pages.items():
    print(f"Generating {filename}...", flush=True)
    generate_image(prompt, filename)
    time.sleep(8)
print("Done!", flush=True)
