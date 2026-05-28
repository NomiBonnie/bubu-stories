#!/usr/bin/env python3
"""Generate missing print-edition pages for Stories 5-8."""

import json, os, sys, time, base64, subprocess, urllib.request

# Load API config
with open(os.path.expanduser("~/.config/azure-openai/config.json")) as f:
    cfg = json.load(f)

ENDPOINT = cfg["image2_eastus2_endpoint"]
API_KEY = cfg["image2_eastus2_api_key"]
API_VERSION = "2025-04-01-preview"
WORKSPACE = os.path.expanduser("~/.openclaw/workspace/bubu-stories/print-edition")

# Character prompts
BUBU = "a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow. She has a small pink bow centered ON TOP OF HER HEAD between her two ears. She has a toddler-like round body proportion."

SAM_DAD = "Sam Dad who is a GOLDEN RETRIEVER DOG (NOT a human — he is an ANIMAL, a large golden-furred dog walking upright). He has warm golden fur, a dog snout/muzzle, floppy dog ears, and a wagging tail. He wears a dark navy jacket over a simple shirt. He has a warm gentle dog smile. IMPORTANT: Sam Dad must look like a golden retriever dog, not a human man."

TINA_MOM = "Tina Mom who is a BLACK-AND-WHITE COW (NOT a human — she is an ANIMAL, a cow walking upright). She has black and white spotted fur pattern, small curved horns, cow ears, and hooves. She wears an elegant cream knit cardigan over a floral skirt. She has a gentle warm cow smile. IMPORTANT: Tina Mom must look like a cow, not a human woman."

NOMI = "a raccoon (NOMI) with grey-brown fur, distinctive black eye mask markings, and a ringed bushy tail. She wears a blue-and-white horizontally striped sweater. She has clever bright eyes and nimble paws."

NONO = "a small red bird (NONO) with bright red feathers all over, round bright eyes, and an orange-yellow beak. He has exactly TWO wings and TWO small bird feet with talons. NO ARMS, NO HANDS — birds do not have arms or hands, only wings."

DOUDOU = "a small hedgehog (Doudou) with a brown body covered in dark brown spines/quills, small round shiny eyes, a tiny nose. He is small, round, and shy-looking."

MANMAN = "a small turtle (Manman) with a green shell with dark green hexagonal patterns, light green skin, small round eyes, and a gentle slow expression."

ZHUZHU = "a white sheep (Zhuzhu, NOT a pig) with cloud-like curly white wool, light blue vest, brown little hooves, pink nose, about the same size as Bubu"

DR_GIRAFFE = "a tall giraffe doctor (Dr. Giraffe) with standard giraffe spots, wearing a white doctor coat and stethoscope, warm professional expression, bending down to talk to small children"

NURSE_SQUIRREL = "a small squirrel nurse with reddish-brown fur, fluffy bushy tail, wearing a pink nurse uniform and white nurse cap with red cross symbol"

YUANYUAN = "a giant panda (Yuanyuan) with classic black and white panda coloring, round black ears, black eye patches, big round dark brown shiny eyes, wearing a yellow little dress, chubby and round, about the same size as Bubu"

STYLE = "Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition (1024x1536). Pure illustration, NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS anywhere in the image. The bottom 20% of the image should have natural darkening/vignette."

# All pages to generate: (story, page, prompt)
PAGES = []

# Story 5, P14: NONO flies down, Bubu looking up, outdoor market
PAGES.append((5, 14, f"{STYLE} Outdoor forest market scene. {NONO} flying down from the sky with wings spread wide, landing near {BUBU} who is looking up happily with arms raised. The market stalls are in the background with colorful awnings. Bright sunny day, dappled forest light."))

# Story 6
PAGES.append((6, 2, f"{STYLE} Cozy kitchen scene. {BUBU} standing impatiently next to {TINA_MOM} who is cooking at the stove. Bubu is tugging at mom's apron, looking restless and hungry. Warm kitchen with pots on stove, steam rising."))

PAGES.append((6, 3, f"{STYLE} {BUBU} peeking out of a wooden cottage door repeatedly, looking down a path impatiently, tapping her foot. Sunny day outside, a winding path leading away from the cozy cottage. She's waiting for someone to arrive, looking eager."))

PAGES.append((6, 5, f"{STYLE} Riverside scene. {BUBU} standing up impatiently from her spot, leaning over the water to check the fishing line. {SAM_DAD} sitting calmly beside her, gently gesturing for her to sit back down. Calm river with fish shadows beneath the surface, green grass bank."))

PAGES.append((6, 9, f"{STYLE} Exciting river scene. {SAM_DAD} helping {BUBU} pull up a fishing rod together. A shiny silver little fish on the line, water splashing. Both looking overjoyed and excited. Golden river light, afternoon sun."))

PAGES.append((6, 13, f"{STYLE} Warm kitchen scene. {TINA_MOM} taking a golden brown cake out of the oven with oven mitts. {BUBU} clapping her hands excitedly nearby. Delicious steam rising from the cake. Warm golden kitchen light, cozy atmosphere."))

PAGES.append((6, 14, f"{STYLE} Nighttime scene. {BUBU} standing outside a cottage looking up at a starry sky peacefully while waiting. Beautiful night sky full of twinkling stars, calm and patient expression. A small garden path leading to the cottage door. Gentle moonlight."))

# Story 7
PAGES.append((7, 6, f"{STYLE} A bright, warm, friendly animal hospital exterior. A big tree with colorful little lanterns at the entrance. Everything is bright and welcoming, not scary at all. {BUBU} and {ZHUZHU} arriving at the entrance, looking around with curiosity. Sunshine, flowers around the entrance, cheerful atmosphere."))

PAGES.append((7, 12, f"{STYLE} Hospital room shot moment. {NURSE_SQUIRREL} gently wiping Zhuzhu's arm with cotton. {BUBU} and {ZHUZHU} counting together '1, 2, 3!' with determined brave expressions, eyes squeezed shut. Quick moment, bright cheerful hospital room with colorful wall decorations."))

PAGES.append((7, 13, f"{STYLE} Hospital room. {ZHUZHU} looking at a star-shaped bandaid on his arm with wonder and delight, eyes sparkling. {NURSE_SQUIRREL} smiling beside him. It's already done! Relief and happiness. Sparkle effect around the star bandaid. Bright cheerful room."))

PAGES.append((7, 14, f"{STYLE} Cheerful hospital corridor. {ZHUZHU} laughing happily, proudly showing his star bandaid arm raised up to {BUBU}. Both smiling brightly, celebrating. 'It wasn't scary at all!' energy. Bright sunlit corridor with colorful decorations."))

PAGES.append((7, 15, f"{STYLE} Inside the hospital. {DR_GIRAFFE} patting {ZHUZHU}'s head gently with a warm smile. Zhuzhu beaming with pride. {BUBU} clapping beside them. Warm, proud, encouraging moment. Bright clean hospital interior."))

PAGES.append((7, 16, f"{STYLE} Beautiful sunset walking path scene. {ZHUZHU} bouncing happily alongside {BUBU}, both walking home together. 'We are the brave team!' energy. Golden sunset light, trees and wildflowers along a winding path. Joyful, triumphant mood."))

PAGES.append((7, 17, f"{STYLE} Dreamy storybook ending scene. {ZHUZHU} and {BUBU} standing together showing their star bandaids like medals, both looking proud and brave. A friendly colorful hospital building in the soft background with a rainbow arching over it. Warm golden glow, uplifting atmosphere."))

# Story 8
PAGES.append((8, 2, f"{STYLE} Cozy home interior in morning light. {BUBU} jumping with excitement wearing a small backpack. {SAM_DAD} and {TINA_MOM} smiling beside her, holding suitcases. Through the window, a bright sunny day. Warm morning light, travel excitement."))

PAGES.append((8, 3, f"{STYLE} A huge bustling airport terminal with high ceilings and many animal passengers in the background. {BUBU} holding tightly onto {TINA_MOM}'s hand, eyes wide with wonder, looking around at the enormous space. Long queues, departure boards, bright lights overhead."))

PAGES.append((8, 4, f"{STYLE} Airport check-in area. {TINA_MOM} handing a boarding pass to {BUBU}. Bubu hugging the boarding pass to her chest proudly, looking very grown-up and important. Airport counter in the background."))

PAGES.append((8, 5, f"{STYLE} Inside a large airplane cabin. {BUBU} touching the soft airplane seat curiously, looking at the round airplane window with wonder. {TINA_MOM} sitting in the next seat smiling. Warm cabin lighting, rows of seats visible."))

PAGES.append((8, 6, f"{STYLE} Dramatic scene inside airplane during takeoff. {BUBU} gripping {TINA_MOM}'s hand tightly, her tummy feeling ticklish, giggling with a mix of excitement and nervousness. Motion blur visible outside the window showing acceleration. Dynamic angle."))

PAGES.append((8, 7, f"{STYLE} {BUBU} pressing her face against the airplane window, looking down at tiny houses like building blocks and a river like a shiny ribbon far below. Fluffy white clouds right beside the window. {TINA_MOM} leaning over to look too, smiling. Magical aerial view, golden sunlight through clouds."))

PAGES.append((8, 8, f"{STYLE} Inside the airplane. A kind deer flight attendant in uniform bringing a tray with juice and cookies to {BUBU} who is saying thank you politely with a happy smile. Warm cabin lighting, friendly service scene."))

PAGES.append((8, 9, f"{STYLE} Airplane landing scene viewed from inside. {BUBU} clapping her little hands with joy, looking out the window at the runway. Expression of triumph and pride. Afternoon light coming through the windows."))

PAGES.append((8, 10, f"{STYLE} Emotional reunion scene outside airport exit. {SAM_DAD} with open arms as {BUBU} runs and leaps toward him. Dad catching and hugging Bubu, kissing her forehead. {TINA_MOM} walking behind with luggage, smiling warmly. Sunset golden light, airport exit in background. Heartwarming family moment."))

PAGES.append((8, 11, f"{STYLE} Cozy nighttime bedroom scene. {BUBU} in pajamas lying in bed, looking out the window at a starry sky with a tiny airplane silhouette. A toy airplane on her nightstand. Dreamy, peaceful atmosphere. Moonlight and warm bedside lamp glow. {SAM_DAD} and {TINA_MOM} tucking her in together, all three looking happy and warm."))


def generate_image(prompt, output_path, retries=3):
    """Call Azure OpenAI image generation API."""
    url = f"{ENDPOINT}?api-version={API_VERSION}"
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }
    body = json.dumps({
        "prompt": prompt,
        "n": 1,
        "size": "1024x1536",
        "quality": "medium",
        "output_format": "png",
    }).encode()

    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=180) as resp:
                result = json.loads(resp.read())
            b64 = result["data"][0]["b64_json"]
            png_path = output_path.replace(".jpg", ".png")
            with open(png_path, "wb") as f:
                f.write(base64.b64decode(b64))
            # Convert to JPG
            subprocess.run([
                "ffmpeg", "-y", "-i", png_path, "-q:v", "2", output_path
            ], capture_output=True)
            os.remove(png_path)
            size = os.path.getsize(output_path)
            print(f"  ✅ {output_path} ({size/1024:.0f} KB)")
            return True
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"  ⚠️ 429 rate limited, waiting 45s (attempt {attempt+1}/{retries})")
                time.sleep(45)
            else:
                body_err = e.read().decode() if hasattr(e, 'read') else str(e)
                print(f"  ❌ HTTP {e.code}: {body_err[:200]}")
                if attempt < retries - 1:
                    time.sleep(10)
        except Exception as e:
            print(f"  ❌ Error: {e}")
            if attempt < retries - 1:
                time.sleep(10)
    return False


def main():
    total = len(PAGES)
    success = 0
    failed = []

    for i, (story, page, prompt) in enumerate(PAGES):
        outdir = os.path.join(WORKSPACE, f"story{story}")
        os.makedirs(outdir, exist_ok=True)
        outpath = os.path.join(outdir, f"page-{page:02d}.jpg")

        if os.path.exists(outpath):
            print(f"[{i+1}/{total}] Story {story} P{page} — already exists, skipping")
            success += 1
            continue

        print(f"[{i+1}/{total}] Story {story} P{page} — generating...")
        if generate_image(prompt, outpath):
            success += 1
        else:
            failed.append(f"Story {story} P{page}")

        if i < total - 1:
            time.sleep(8)

    print(f"\n{'='*40}")
    print(f"Done: {success}/{total} succeeded")
    if failed:
        print(f"Failed: {', '.join(failed)}")

    # Report file sizes
    print(f"\n📁 File sizes:")
    for story in [5, 6, 7, 8]:
        d = os.path.join(WORKSPACE, f"story{story}")
        if os.path.isdir(d):
            files = sorted(os.listdir(d))
            for fn in files:
                fp = os.path.join(d, fn)
                sz = os.path.getsize(fp)
                print(f"  story{story}/{fn}: {sz/1024:.0f} KB")


if __name__ == "__main__":
    main()
