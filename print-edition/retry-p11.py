#!/usr/bin/env python3
"""Retry story48 page-11 with safer prompt."""
import json, os, base64, subprocess, urllib.request, urllib.error

with open(os.path.expanduser("~/.config/azure-openai/config.json")) as f:
    cfg = json.load(f)
URL = f"{cfg['image2_eastus2_endpoint']}?api-version=2025-04-01-preview"

BUBU = "a cute snow-white rabbit girl with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose, pink dress with pink bow centered on top of head between ears, toddler body."
STYLE = "Pixar 3D animated style, warm soft lighting, children's picture book. Vertical 2:3. Pure illustration NO text. Bottom 20% darkened gradient."

prompt = f"{STYLE} Summer clothing. Scene: A joyful kindergarten playground. A beautiful rainbow-colored blanket with stripes of red, orange, yellow, green and blue is spread across the ground like a colorful path. {BUBU} stands at the start of the colorful path, looking excited and ready for a fun race. A kind orange tabby cat teacher cheers nearby. Other young animal friends (a bear cub, a corgi puppy, a kitten, a fawn) watch and clap. Bright sunny day, festive atmosphere."

outpath = "bubu-stories/print-edition/story48/page-11.jpg"
body = json.dumps({"prompt": prompt, "n": 1, "size": "1024x1536", "quality": "medium"}).encode()
req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json", "api-key": cfg["image2_eastus2_api_key"]})
try:
    resp = urllib.request.urlopen(req, timeout=120)
    data = json.loads(resp.read())
    png = outpath.replace(".jpg", ".png")
    with open(png, "wb") as f:
        f.write(base64.b64decode(data["data"][0]["b64_json"]))
    subprocess.run(["ffmpeg", "-y", "-i", png, "-q:v", "2", outpath], capture_output=True)
    os.remove(png)
    print(f"OK {outpath} ({os.path.getsize(outpath)} bytes)")
except urllib.error.HTTPError as e:
    print(f"ERROR {e.code}: {e.read().decode()[:300]}")
except Exception as e:
    print(f"ERROR: {e}")
