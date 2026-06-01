#!/usr/bin/env python3
"""Retry failed pages for Volume 5."""
import json, os, base64, subprocess, requests, time

with open(os.path.expanduser("~/.config/azure-openai/config.json")) as f:
    cfg = json.load(f)

ENDPOINT = cfg["image2_eastus2_endpoint"]
API_KEY = cfg["image2_eastus2_api_key"]
URL = f"{ENDPOINT}?api-version=2025-04-01-preview"
HEADERS = {"api-key": API_KEY, "Content-Type": "application/json"}
WS = os.path.expanduser("~/.openclaw/workspace/bubu-stories/print-edition")

BUBU = "a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow. She has a small pink bow centered ON TOP OF HER HEAD between her two ears. She has a toddler-like round body proportion."
NOMI = "a raccoon (NOMI) with grey-brown fur, distinctive black eye mask markings, and a ringed bushy tail. She wears a blue-and-white horizontally striped sweater."
NONO = "a small red bird (NONO) with bright red feathers, round bright eyes, orange-yellow beak. TWO wings, TWO bird feet. NO ARMS NO HANDS."
STYLE = "Pixar 3D animation style, warm soft lighting, children's picture book illustration. Pure illustration with NO TEXT anywhere. Bottom 20% natural darkening."

retries = [
    {
        "path": f"{WS}/story22/page-08.jpg",
        "prompt": f"""{STYLE}

Scene: A cheerful photo moment at a city square park. Bubu the rabbit posing happily for a photograph, looking directly at the viewer with a sweet confident smile. Colorful flowers and park greenery in the background. Bright sunny day.

Characters:
- {BUBU}

IMPORTANT: No text/words. Natural composition. Bottom 20% darkening."""
    },
    {
        "path": f"{WS}/story24/page-10.jpg",
        "prompt": f"""{STYLE}

Scene: Bubu standing proudly on a green meadow near a campsite, announcing that she learned to observe nature without touching. NOMI and NONO nearby, looking proud of her. Warm afternoon sunlight, wildflowers around.

Characters:
- {BUBU}
- {NOMI}
- {NONO}

IMPORTANT: No text/words. Natural composition. Bottom 20% darkening."""
    },
]

for item in retries:
    path = item["path"]
    print(f"Retrying: {path}")
    body = {"prompt": item["prompt"], "n": 1, "size": "1024x1536", "quality": "medium", "output_format": "png"}
    for attempt in range(3):
        try:
            r = requests.post(URL, headers=HEADERS, json=body, timeout=180)
            if r.status_code == 429:
                print(f"  429, waiting 45s...")
                time.sleep(45)
                continue
            if r.status_code != 200:
                print(f"  {r.status_code}: {r.text[:200]}")
                time.sleep(10)
                continue
            b64 = r.json()["data"][0]["b64_json"]
            png = path.replace(".jpg", ".png")
            with open(png, "wb") as f:
                f.write(base64.b64decode(b64))
            subprocess.run(["ffmpeg", "-y", "-i", png, "-q:v", "2", path], capture_output=True, timeout=30)
            os.remove(png)
            print(f"  OK {os.path.getsize(path)//1024}KB")
            break
        except Exception as e:
            print(f"  Error: {e}")
            time.sleep(10)
    time.sleep(8)
print("Done")
