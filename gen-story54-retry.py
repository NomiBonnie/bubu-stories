#!/usr/bin/env python3
"""Retry failed pages with simplified prompts."""
import json, os, time, subprocess, base64
from urllib.request import Request, urlopen
from urllib.error import HTTPError

CONFIG = json.load(open(os.path.expanduser("~/.config/azure-openai/config.json")))
ENDPOINT = CONFIG["image2_eastus2_endpoint"]
API_KEY = CONFIG["image2_eastus2_api_key"]
API_VERSION = "2025-04-01-preview"
OUT_DIR = os.path.expanduser("~/.openclaw/workspace/bubu-stories/public/images/story54")

BUBU = "a toddler white rabbit girl (snow-white fur, TWO long ears with pink insides, big brown eyes, pink nose), wearing a light pink summer dress with sandals, a small pink bow between her ears on top of her head"
OLIVER = "a realistic Border Collie dog (black and white fur, brown eyes, medium-sized, four legs, a real dog)"
STYLE = "Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition 1024x1536."

prompts = {
    "page-05": f"""{STYLE}

A warm kitchen scene. {BUBU} kneels on the floor next to {OLIVER}. She holds a small cup and pours dog food into a big bowl on the floor. Oliver sits patiently beside the bowl, watching her with a tilted head and happy expression. 

The kitchen is bright and cheerful with morning sunlight. A dreamy soft-focus border indicates this is a happy memory.""",

    "page-07": f"""{STYLE}

An outdoor park scene at golden hour. {OLIVER} faces {BUBU} and gently nuzzles her cheek with his nose. Bubu giggles with eyes closed and a big smile, holding her hands up playfully. Oliver's tail wags behind him.

Warm golden backlight creates a glowing halo around both characters. Green trees and a walking path in the background. A dreamy soft-focus border indicates this is a happy memory."""
}

def generate_image(prompt, filename):
    png_path = os.path.join(OUT_DIR, filename.replace('.jpg', '.png'))
    jpg_path = os.path.join(OUT_DIR, filename)
    
    url = f"{ENDPOINT}?api-version={API_VERSION}"
    body = json.dumps({
        "prompt": prompt, "n": 1, "size": "1024x1536",
        "quality": "medium", "output_format": "png"
    }).encode()
    headers = {"Content-Type": "application/json", "api-key": API_KEY}

    for attempt in range(3):
        try:
            req = Request(url, data=body, headers=headers, method="POST")
            resp = urlopen(req, timeout=120)
            result = json.loads(resp.read())
            img_b64 = result["data"][0]["b64_json"]
            with open(png_path, "wb") as f:
                f.write(base64.b64decode(img_b64))
            subprocess.run(["ffmpeg", "-y", "-i", png_path, "-q:v", "4", jpg_path], capture_output=True)
            os.remove(png_path)
            size_kb = os.path.getsize(jpg_path) / 1024
            print(f"  OK {filename} ({size_kb:.0f} KB)")
            return True
        except HTTPError as e:
            err = e.read().decode()[:200]
            print(f"  Attempt {attempt+1} failed: HTTP {e.code} - {err}")
            if e.code == 429:
                time.sleep(30)
            else:
                time.sleep(10)
    return False

for page, prompt in prompts.items():
    print(f"Generating {page}...")
    if not generate_image(prompt, f"{page}.jpg"):
        print(f"  FAILED {page}")
    time.sleep(7)
