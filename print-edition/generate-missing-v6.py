#!/usr/bin/env python3
"""Generate missing print-edition pages for Volume 6 (Stories 53-57)"""
import json, os, sys, time, base64, subprocess, urllib.request, urllib.error
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Load API config
with open(os.path.expanduser("~/.config/azure-openai/config.json")) as f:
    cfg = json.load(f)

ENDPOINT = cfg["image2_eastus2_endpoint"]
API_KEY = cfg["image2_eastus2_api_key"]
API_VERSION = "2025-04-01-preview"
URL = f"{ENDPOINT}?api-version={API_VERSION}"

OUT_DIR = os.path.expanduser("~/.openclaw/workspace/bubu-stories/print-edition")

# Character prompts
BUBU = """a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow. She has a small pink bow centered ON TOP OF HER HEAD between her two ears (not on left ear, not on right ear, not behind — exactly centered on top between the ears). She has a toddler-like round body proportion."""

SAM_DAD = """Sam Dad who is a GOLDEN RETRIEVER DOG (NOT a human, NOT a person — he is an ANIMAL, a large golden-furred dog walking upright). He has warm golden fur all over his body, a dog snout/muzzle, floppy dog ears, and a wagging tail. He wears a dark navy jacket over a simple shirt. He has a warm gentle dog smile. IMPORTANT: Sam Dad must look like a golden retriever dog, not a human man."""

TINA_MOM = """Tina Mom who is a BLACK-AND-WHITE COW (NOT a human, NOT a person — she is an ANIMAL, a cow walking upright). She has black and white spotted fur pattern all over, small curved horns, cow ears, and hooves. She wears an elegant cream knit cardigan over a floral skirt. She has a gentle warm cow smile. IMPORTANT: Tina Mom must look like a cow, not a human woman."""

NOMI = """a raccoon (NOMI) with grey-brown fur, distinctive black eye mask markings, and a ringed bushy tail. She wears a blue-and-white horizontally striped sweater. She has clever bright eyes and nimble paws."""

NONO = """a small red bird (NONO) with bright red feathers all over, round bright eyes, and an orange-yellow beak. He has exactly TWO wings and TWO small bird feet with talons. NO ARMS, NO HANDS — birds do not have arms or hands, only wings."""

STYLE = "Pixar 3D animation style, warm soft lighting, children's picture book illustration quality. The bottom 20% of the image should have a subtle dark gradient overlay for text placement."

# All tasks: (story_num, page_num, prompt)
TASKS = []

# === Story 55 Page 13 ===
TASKS.append(("story55", 13, f"""
{STYLE}
Scene: A cozy hotel room at night in Anji (bamboo countryside resort). {BUBU} lies on a big comfortable bed, eyes half-closed, a sweet sleepy smile on her face. She is being tucked in under a soft blanket. {SAM_DAD} sits on one side of the bed, looking down at her lovingly. {TINA_MOM} sits on the other side, also gazing gently. {NOMI} stands beside the bed, gently pulling the blanket up over Bubu. Through the window, we can see a moonlit bamboo forest and a starry night sky. The room is warmly lit with a soft bedside lamp. A peaceful, sleepy atmosphere. NO TEXT anywhere in the image. Pure illustration only.
"""))

# === Story 57 Pages ===
# Page 3: Dad asks to play his song, Bubu pouts
TASKS.append(("story57", 3, f"""
{STYLE}
Scene: Inside a car during a family road trip to the beach. {BUBU} is sitting in a child car seat in the back, pouting with her little mouth pushed out and arms crossed, looking upset. {SAM_DAD} is in the driver's seat, turned slightly to look back at Bubu with a gentle, patient smile. The car interior is warm and sunny. Through the windows, a beach road landscape is visible. Bubu is refusing to let Dad change the music. A playful father-daughter moment. NO TEXT anywhere in the image. Pure illustration only.
"""))

# Page 5: At beach, Bubu tugs Mom's hand
TASKS.append(("story57", 5, f"""
{STYLE}
Scene: A beautiful sandy beach on a sunny summer day. {TINA_MOM} and {SAM_DAD} sit together on a beach blanket, chatting. {BUBU} runs over excitedly and tugs on Mom's hand/hoof, pointing towards the shore with her other paw. She has a bright excited expression, clearly wanting attention. In the background, gentle ocean waves and a blue sky. A seashell is visible near the water's edge. NO TEXT anywhere in the image. Pure illustration only.
"""))

# Page 6: Mom interrupted, parents exchange a look
TASKS.append(("story57", 6, f"""
{STYLE}
Scene: Same beach setting. {BUBU} is pulling on {TINA_MOM}'s arm/hoof urgently, mouth open calling out. {TINA_MOM} and {SAM_DAD} are exchanging a knowing glance at each other, smiling with a gentle sigh — a classic parental "here we go again" look, but affectionate not annoyed. The beach blanket and picnic items are visible. Warm golden sunlight. NO TEXT anywhere in the image. Pure illustration only.
"""))

# Page 7: NOMI arrives with beach ball, proposes game
TASKS.append(("story57", 7, f"""
{STYLE}
Scene: On the sandy beach. {NOMI} walks toward {BUBU} carrying a colorful beach ball (red, yellow, blue stripes), with a cheerful smile. {BUBU} looks up at NOMI with curiosity and excitement. In the background, {SAM_DAD} and {TINA_MOM} watch from the beach blanket. {NONO} perches on a nearby beach umbrella pole. The beach is bright and inviting. NO TEXT anywhere in the image. Pure illustration only.
"""))

# Page 8: NOMI explains rules, NONO flaps wings excitedly
TASKS.append(("story57", 8, f"""
{STYLE}
Scene: On the beach. {NOMI} stands in the center, holding up one paw as if explaining rules, looking enthusiastic and teacher-like. {BUBU} sits cross-legged on the sand, listening with interest. {NONO} is beside them, flapping his two wings excitedly, beak open as if calling out eagerly. {SAM_DAD} and {TINA_MOM} are sitting nearby, smiling and watching. The beach ball rests on the sand between them. NO TEXT anywhere in the image. Pure illustration only.
"""))

# Page 9: Everyone sits in circle, NONO sings off-key
TASKS.append(("story57", 9, f"""
{STYLE}
Scene: On the beach, everyone sits in a circle on the sand. {NONO} stands in the middle of the circle, wings spread wide, beak open wide, clearly singing enthusiastically (and off-key — show wavy music note effects around him). {BUBU}, {SAM_DAD}, {TINA_MOM}, and {NOMI} sit around the circle, all laughing and clapping. The beach ball and a few seashells are scattered around. Warm sunset beginning. NO TEXT anywhere in the image. Pure illustration only.
"""))

# Page 10: Dad hums guitar song, Bubu restrains herself with NOMI's help
TASKS.append(("story57", 10, f"""
{STYLE}
Scene: On the beach, golden hour light. {SAM_DAD} sits in the circle, eyes half-closed, gently humming along to music (show a few soft music notes near him). He looks peaceful and happy. {BUBU} sits across from him, mouth slightly open as if about to speak, but she notices {NOMI} beside her holding one paw finger to her lips in a quiet "shh" gesture. Bubu's expression shows she's trying hard to stay quiet. {TINA_MOM} sits nearby, listening peacefully. {NONO} perches on the beach umbrella. NO TEXT anywhere in the image. Pure illustration only.
"""))

# Page 11: Mom shares memory, Bubu's eyes go wide
TASKS.append(("story57", 11, f"""
{STYLE}
Scene: On the beach at sunset. {TINA_MOM} is speaking, gesturing with her hooves, looking nostalgic and happy, telling a story about her childhood at the beach. {BUBU} is leaning forward with her eyes wide open in wonder and surprise, mouth slightly open, fascinated by Mom's story. {SAM_DAD} listens warmly beside them. {NOMI} sits nearby, also listening intently. Scattered seashells on the sand around them. Warm orange-pink sunset sky. NO TEXT anywhere in the image. Pure illustration only.
"""))

# Page 12: Bubu's turn — she shows pink shell and sings
TASKS.append(("story57", 12, f"""
{STYLE}
Scene: On the beach at sunset. {BUBU} stands proudly in the center of the circle, holding up a beautiful pink seashell in one paw, mouth open wide as she sings her favorite song happily. She looks absolutely delighted and confident. Around her, {SAM_DAD}, {TINA_MOM}, {NOMI}, and {NONO} are all clapping and smiling, giving her their full attention. The sunset casts a warm golden glow over everyone. It's a heartwarming moment of being truly heard. NO TEXT anywhere in the image. Pure illustration only.
"""))

# Page 13: In car going home, Bubu quietly listens to Dad's song
TASKS.append(("story57", 13, f"""
{STYLE}
Scene: Inside a car at sunset/twilight. {BUBU} sits quietly in her car seat, looking peaceful and content with a gentle smile, leaning slightly against the seat. Golden sunset light streams through the car window onto her face. In the front, {SAM_DAD} drives, visible from behind. In the back seat next to Bubu, {NOMI} and {NONO} exchange a warm knowing smile at each other, pleased that Bubu has learned patience. The sky through the windows shows beautiful sunset colors — orange, pink, and purple. A serene, warm ending scene. NO TEXT anywhere in the image. Pure illustration only.
"""))

# === Cover ===
TASKS.append(("cover", 0, f"""
{STYLE.replace("The bottom 20% of the image should have a subtle dark gradient overlay for text placement.", "")}
A cinematic movie-poster style children's book cover. Split-screen concept: LEFT HALF shows a warm nostalgic scene of Suzhou (traditional Chinese garden with moon gate, canal, gentle willow trees) in autumn golden tones. RIGHT HALF shows a vibrant modern scene of Shenzhen (futuristic skyline, palm trees, ocean view) in bright hopeful blue-green tones. In the center where the two halves merge, {BUBU} stands looking forward with determination and a gentle smile, holding a small suitcase. {NOMI} stands beside her. {NONO} flies above. The transition between the two cities is seamless and artistic. At the top in elegant white serif font: "GROWING & GOODBYE". At the bottom in smaller font: "BUBU'S STORIES • VOLUME SIX". The overall mood is bittersweet but hopeful — about change and new beginnings. Cinematic lighting with lens flare.
"""))

# === TOC ===
TASKS.append(("toc", 0, f"""
{STYLE.replace("The bottom 20% of the image should have a subtle dark gradient overlay for text placement.", "")}
A warm cozy scene for a table of contents page. {BUBU} sits on a big cushion in a sunlit reading nook, with {NOMI} beside her and {NONO} perched on a shelf above. They are surrounded by soft golden light. On the wall behind them, five framed pictures show tiny vignettes of each story: friends playing at kindergarten, a dog (Border Collie), bamboo forest holiday, moving boxes with city skyline, and a beach scene. In clean elegant white text, centered and easy to read:

"TABLE OF CONTENTS

53  Kindergarten Friends
54  Bubu Misses Oliver
55  Holiday in Anji
56  Goodbye Suzhou Hello Shenzhen
57  Bubu Learns to Wait"

The text should be clear, properly spaced, and readable. Warm illustration style with a scrapbook/memory wall feeling.
"""))


def generate_image(prompt: str, out_path: str, max_retries: int = 3):
    """Generate a single image via Azure API"""
    body = json.dumps({
        "prompt": prompt.strip(),
        "n": 1,
        "size": "1024x1536",
        "quality": "medium",
        "output_format": "png"
    }).encode()

    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(URL, data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())

            b64 = data["data"][0]["b64_json"]
            png_path = out_path.replace(".jpg", ".png")
            with open(png_path, "wb") as f:
                f.write(base64.b64decode(b64))

            # Convert PNG -> JPG with ffmpeg
            subprocess.run([
                "ffmpeg", "-y", "-i", png_path, "-q:v", "2", out_path
            ], capture_output=True, check=True)
            os.remove(png_path)

            size_kb = os.path.getsize(out_path) / 1024
            print(f"  ✅ Generated: {os.path.basename(out_path)} ({size_kb:.0f} KB)")
            return True

        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 45
                print(f"  ⚠️ Rate limited (429), waiting {wait}s... (attempt {attempt+1}/{max_retries})")
                time.sleep(wait)
            else:
                err_body = e.read().decode() if e.fp else "no body"
                print(f"  ❌ HTTP {e.code}: {err_body[:200]}")
                if attempt < max_retries - 1:
                    time.sleep(15)
                else:
                    return False
        except Exception as e:
            print(f"  ❌ Error: {e}")
            if attempt < max_retries - 1:
                time.sleep(15)
            else:
                return False

    return False


def main():
    start_idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    results = []

    for i, (story_id, page_num, prompt) in enumerate(TASKS):
        if i < start_idx:
            continue

        if story_id == "cover":
            out_path = os.path.join(OUT_DIR, "volume6-print-cover.jpg")
            label = "Volume 6 Cover"
        elif story_id == "toc":
            out_path = os.path.join(OUT_DIR, "volume6-print-toc.jpg")
            label = "Volume 6 TOC"
        else:
            story_dir = os.path.join(OUT_DIR, story_id)
            os.makedirs(story_dir, exist_ok=True)
            out_path = os.path.join(story_dir, f"page-{page_num:02d}.jpg")
            label = f"{story_id}/page-{page_num:02d}"

        print(f"\n[{i+1}/{len(TASKS)}] Generating {label}...")
        ok = generate_image(prompt, out_path)
        results.append((label, ok))

        # Wait between requests
        if i < len(TASKS) - 1:
            time.sleep(8)

    print("\n" + "="*50)
    print("RESULTS:")
    for label, ok in results:
        status = "✅" if ok else "❌"
        print(f"  {status} {label}")

    failed = [r for r in results if not r[1]]
    if failed:
        print(f"\n⚠️ {len(failed)} failed. Rerun with start_idx to retry.")
    else:
        print(f"\n🎉 All {len(results)} images generated successfully!")

if __name__ == "__main__":
    main()
