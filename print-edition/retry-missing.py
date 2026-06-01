#!/usr/bin/env python3
"""Retry missing pages."""
import json, os, time, base64, subprocess, urllib.request, urllib.error

with open(os.path.expanduser("~/.config/azure-openai/config.json")) as f:
    cfg = json.load(f)
ENDPOINT = cfg["image2_eastus2_endpoint"]
API_KEY = cfg["image2_eastus2_api_key"]
URL = f"{ENDPOINT}?api-version=2025-04-01-preview"

BUBU = "a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow centered ON TOP OF HER HEAD between her two ears. Toddler-like round body."
NOMI = "a raccoon (NOMI) with grey-brown fur, black eye mask markings, ringed bushy tail, blue-and-white striped sweater."
NONO = "a small red bird (NONO) with bright red feathers, orange-yellow beak. TWO wings, NO ARMS NO HANDS."
TINA_MOM = "Tina Mom who is a BLACK-AND-WHITE COW walking upright, spotted fur, small horns, cow ears, hooves, cream cardigan over floral skirt."
STYLE = "Pixar 3D animated style, warm soft lighting, children's picture book quality. Vertical 2:3. Pure illustration NO text NO words NO letters. Bottom 20% subtly darkened gradient."
SUMMER = "Summer clothing."

tasks = [
    ("bubu-stories/print-edition/story48/page-11.jpg",
     f"{STYLE} {SUMMER} Scene: A colorful activity on a kindergarten playground. A large multi-colored striped mat (red, orange, yellow, green, blue — like a rainbow) is laid out on the ground. {BUBU} is on all fours at the start of the mat, ready to move across it playfully. A teacher encourages from the side. Other animal children watch excitedly. Fun outdoor activity atmosphere."),
    ("bubu-stories/print-edition/story51/page-02.jpg",
     f"{STYLE} {SUMMER} Scene: {BUBU} stands proudly with hands on hips in a bright living room. She looks confident and growing up. {NOMI} and {NONO} nearby looking proud of her. Warm cheerful atmosphere showing a toddler learning new skills."),
    ("bubu-stories/print-edition/story51/page-13.jpg",
     f"{STYLE} {SUMMER} Scene: Evening time. {BUBU} walks proudly around the living room in clean pajamas, chin up, confident stride. {NOMI} and {NONO} watch admiringly. Warm evening light. Bubu looks like she's grown up a little. Peaceful, proud ending scene."),
]

for outpath, prompt in tasks:
    if os.path.exists(outpath) and os.path.getsize(outpath) > 50000:
        print(f"SKIP {outpath}")
        continue
    print(f"Generating {outpath}...")
    body = json.dumps({"prompt": prompt, "n": 1, "size": "1024x1536", "quality": "medium"}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json", "api-key": API_KEY})
    for attempt in range(3):
        try:
            resp = urllib.request.urlopen(req, timeout=120)
            data = json.loads(resp.read())
            b64 = data["data"][0]["b64_json"]
            png = outpath.replace(".jpg", ".png")
            with open(png, "wb") as f:
                f.write(base64.b64decode(b64))
            subprocess.run(["ffmpeg", "-y", "-i", png, "-q:v", "2", outpath], capture_output=True)
            os.remove(png)
            print(f"  OK {outpath} ({os.path.getsize(outpath)} bytes)")
            break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"  429, waiting 45s...")
                time.sleep(45)
            else:
                print(f"  ERROR {e.code}: {e.read().decode()[:200]}")
                break
        except Exception as e:
            print(f"  ERROR: {e}")
            break
    time.sleep(8)

print("DONE")
