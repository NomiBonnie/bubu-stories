#!/usr/bin/env python3
"""Generate Story 54 illustrations."""
import json, os, time, subprocess, base64, sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError

CONFIG = json.load(open(os.path.expanduser("~/.config/azure-openai/config.json")))
ENDPOINT = CONFIG["image2_eastus2_endpoint"]
API_KEY = CONFIG["image2_eastus2_api_key"]
API_VERSION = "2025-04-01-preview"
OUT_DIR = os.path.expanduser("~/.openclaw/workspace/bubu-stories/public/images/story54")
os.makedirs(OUT_DIR, exist_ok=True)

# Character descriptions
BUBU = "a toddler white rabbit girl (100% snow-white fur, exactly TWO long ears with pink insides, big round brown eyes, small pink nose), wearing a light pink summer dress with thin straps and sandals, a small pink bow centered on top of her head BETWEEN her two ears"
NOMI = "a raccoon character (grey-brown fur with black eye mask markings, ringed tail) wearing a blue-and-white striped t-shirt (summer lightweight)"
NONO = "a small red bird (bright red feathers, round bright eyes, orange-yellow beak, NO hands — only wings)"
SAM_DAD = "a golden retriever father (golden fur, warm and big), wearing a casual summer polo shirt and shorts"
TINA_MOM = "a cow mother (black and white patches, gentle and elegant), wearing a light summer blouse and skirt"
OLIVER = "a realistic Border Collie dog (black and white fur, intelligent deep brown eyes, medium-sized, four legs, NO clothes, NOT anthropomorphized — a real dog walking on all fours)"

STYLE = "Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition 1024x1536."

prompts = {}

# Page 01 - Cover
prompts["page-01"] = f"""Pixar 3D animation style, cinematic children's picture book cover poster, warm golden summer sunset lighting, vertical portrait 1024x1536.

TOP: Elegant hand-lettered title "Bubu Misses Oliver" in warm golden embossed 3D letters with a gentle glow, positioned at the top. Small paw prints and hearts scattered around the letters. NO Chinese text, NO bubble letters.

CENTER: {BUBU} — she sits in a dreamy pose, hugging a stuffed Border Collie toy close to her chest, looking up at the sky with longing eyes.

LOWER CENTER: A semi-transparent dreamy vision of {OLIVER} running happily through a golden field, tail wagging, like a memory or dream floating in the air.

BOTTOM LEFT: {NOMI} sitting beside Bubu, one paw gently on her shoulder.
BOTTOM RIGHT: {NONO} perched on Bubu's ear, looking at the dream-Oliver.

BACKGROUND: Split scene — left side shows a Suzhou garden with traditional architecture, right side shows Shenzhen city skyline, connected by a warm golden light bridge. Summer evening sky with orange and pink clouds. Rich layered movie poster depth composition with bokeh effects."""

# Page 02
prompts["page-02"] = f"""{STYLE}

SCENE: A bright summer living room in Suzhou. Sunlight streams through large windows.

CENTER: {BUBU} sits on the wooden floor, hugging a fluffy stuffed toy dog that looks like a Border Collie (black and white plush). She looks at it with tender eyes.

BACKGROUND: A cozy modern Chinese apartment with light-colored furniture, a small fan on the table, summer decorations. Through the window, a sunny Suzhou cityscape is visible."""

# Page 03
prompts["page-03"] = f"""{STYLE}

SCENE: Same Suzhou living room, warm summer afternoon.

CENTER: {BUBU} looks up with questioning eyes, still holding the stuffed dog. {TINA_MOM} kneels down beside her, gently patting Bubu's head with a reassuring smile.

BACKGROUND: The living room with a phone on the coffee table showing a photo of a Border Collie (Oliver)."""

# Page 04
prompts["page-04"] = f"""{STYLE}

SCENE: A dreamy flashback memory scene with warm golden morning light, slightly soft-focus edges to indicate this is a memory. A bedroom door in a Shenzhen apartment.

CENTER: {OLIVER} stands at a closed bedroom door, nose pressed against the door crack, tail wagging enthusiastically. His ears are perked up with excitement.

FOREGROUND: The door is slightly ajar, and we can see a tiny white rabbit paw (Bubu's) reaching out from inside. Morning sunlight filters through a nearby window."""

# Page 05
prompts["page-05"] = f"""{STYLE}

SCENE: Dreamy memory scene, a kitchen in a Shenzhen home with warm golden light.

CENTER: {BUBU} squats on the kitchen floor next to {OLIVER}. She holds a small bowl and carefully drops kibble pieces one by one into Oliver's big food bowl. Oliver sits patiently, head tilted, watching her with adoring eyes and a slightly open mouth.

DETAILS: Dog food bag visible nearby, a water bowl next to the food bowl. The kitchen is bright and clean."""

# Page 06
prompts["page-06"] = f"""{STYLE}

SCENE: Dreamy memory scene. A Shenzhen neighborhood park at summer evening, golden hour light, trees and a walking path.

CENTER: {SAM_DAD} walks casually while {BUBU} holds a red leash attached to {OLIVER} who is running ahead eagerly. Bubu is being pulled forward, laughing with her mouth wide open, her ears flying back from the speed.

OLIVER runs with all four legs in motion, tongue out, tail streaming behind. The leash is taut between Bubu and Oliver.

BACKGROUND: A leafy park path with evening golden light filtering through trees, other families visible in the distance."""

# Page 07
prompts["page-07"] = f"""{STYLE}

SCENE: Dreamy memory scene. Same park, close-up moment.

CENTER: {OLIVER} has turned around and is licking {BUBU}'s face. Bubu squeezes her eyes shut and laughs, her hands up trying to gently push Oliver away but clearly enjoying it. Oliver's tail is a blur of wagging.

COMPOSITION: Close-up shot, warm golden backlight creating a halo effect around both characters. Very tender and joyful moment."""

# Page 08
prompts["page-08"] = f"""{STYLE}

SCENE: A split composition showing distance and separation. Summer day.

LEFT SIDE: A Suzhou apartment window. {BUBU} looks out the window with a slightly sad expression, her stuffed dog toy on the windowsill.

RIGHT SIDE (smaller, like a thought bubble or distant view): A pet hotel building in Shenzhen with {OLIVER} visible through a window, lying on a bed.

BETWEEN: A subtle airplane silhouette in the sky connecting the two cities. The overall mood is bittersweet — bright summer day but emotional separation."""

# Page 09
prompts["page-09"] = f"""{STYLE}

SCENE: Bubu alone at a window, looking out at the Suzhou summer sky with fluffy white clouds.

CENTER: {BUBU} stands on tiptoes at a large window, her small paws on the windowsill, looking up at the sky. Her expression is wistful and thoughtful. The stuffed Oliver toy sits beside her on the windowsill.

BACKGROUND: A beautiful Suzhou summer sky with big fluffy clouds, one cloud subtly shaped like a running dog. Warm afternoon light bathes the scene."""

# Page 10
prompts["page-10"] = f"""{STYLE}

SCENE: A clean, comfortable pet hotel room in Shenzhen. Warm but slightly lonely atmosphere.

CENTER: {OLIVER} lies on a cushioned dog bed, his nose resting on his front paws. His ears are perked up, his deep brown eyes looking hopefully toward the door. His tail is still.

DETAILS: A food bowl and water bowl nearby (both full), a chew toy untouched, a small window showing Shenzhen city lights in the evening. The room is clean but Oliver looks like he's waiting for someone specific."""

# Page 11
prompts["page-11"] = f"""{STYLE}

SCENE: Bubu's bedroom in Suzhou at night. Soft warm lamplight. Bedtime atmosphere.

CENTER: {NOMI} sits on the bed holding {BUBU} gently in a comforting hug. Bubu leans against NOMI, listening with wide eyes. {NONO} perches on the bedpost nearby.

DETAILS: The stuffed Oliver toy is on the pillow. A small night light glows. Through the window, a crescent moon and stars are visible in the summer night sky."""

# Page 12
prompts["page-12"] = f"""{STYLE}

SCENE: Same bedroom, a moment of joy and hope.

CENTER: {BUBU}'s eyes are sparkling with excitement. She holds up the stuffed Border Collie toy and kisses it on the forehead, her expression full of love and determination.

{NOMI} watches with a warm smile. {NONO} flutters nearby with wings spread happily.

MOOD: The lighting shifts from soft night to a warm hopeful glow, representing Bubu's renewed optimism."""

# Page 13
prompts["page-13"] = f"""{STYLE}

SCENE: A dreamy, magical closing scene. Bubu is asleep in bed, and above her floats a beautiful dream cloud.

BOTTOM: {BUBU} lies sleeping peacefully in bed with a smile on her face, hugging the stuffed Oliver. {NOMI} is curled up nearby, also drowsy. {NONO} is tucked under a wing on the bedpost.

TOP (DREAM CLOUD): Inside a glowing warm dream bubble, {BUBU} pushes open a door and {OLIVER} leaps toward her with tail wagging wildly, about to lick her face. The dream is full of golden light, flower petals, and joy.

MOOD: Warm, hopeful, the promise of reunion. Soft starlight from the window mingles with the golden dream light."""


def generate_image(prompt, filename):
    """Generate image via Azure OpenAI API."""
    png_path = os.path.join(OUT_DIR, filename.replace('.jpg', '.png'))
    jpg_path = os.path.join(OUT_DIR, filename)
    
    if os.path.exists(jpg_path):
        print(f"  SKIP {filename} (exists)")
        return True

    url = f"{ENDPOINT}?api-version={API_VERSION}"
    body = json.dumps({
        "prompt": prompt,
        "n": 1,
        "size": "1024x1536",
        "quality": "medium",
        "output_format": "png"
    }).encode()

    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }

    for attempt in range(4):
        try:
            req = Request(url, data=body, headers=headers, method="POST")
            resp = urlopen(req, timeout=120)
            result = json.loads(resp.read())
            
            img_b64 = result["data"][0]["b64_json"]
            with open(png_path, "wb") as f:
                f.write(base64.b64decode(img_b64))
            
            # Convert to JPG
            subprocess.run([
                "ffmpeg", "-y", "-i", png_path, "-q:v", "4", jpg_path
            ], capture_output=True)
            os.remove(png_path)
            
            size_kb = os.path.getsize(jpg_path) / 1024
            print(f"  OK {filename} ({size_kb:.0f} KB)")
            return True
            
        except HTTPError as e:
            if e.code == 429:
                print(f"  429 rate limit, waiting 30s... (attempt {attempt+1})")
                time.sleep(30)
            elif e.code == 400:
                body_text = e.read().decode()
                print(f"  400 error: {body_text[:200]}")
                if "content_policy" in body_text.lower() or "safety" in body_text.lower():
                    print(f"  SAFETY FILTER on {filename}, will retry with simplified prompt")
                    return False
                return False
            else:
                print(f"  HTTP {e.code}: {e.read().decode()[:200]}")
                if attempt < 3:
                    time.sleep(10)
                else:
                    return False
        except Exception as e:
            print(f"  Error: {e}")
            if attempt < 3:
                time.sleep(10)
            else:
                return False
    return False


# Generate all pages
pages = sorted(prompts.keys())
for i, page in enumerate(pages):
    print(f"[{i+1}/{len(pages)}] Generating {page}...")
    success = generate_image(prompts[page], f"{page}.jpg")
    if not success:
        print(f"  FAILED {page}")
    if i < len(pages) - 1:
        time.sleep(7)

print("\nDone! Checking files:")
for page in pages:
    path = os.path.join(OUT_DIR, f"{page}.jpg")
    if os.path.exists(path):
        size_kb = os.path.getsize(path) / 1024
        print(f"  {page}.jpg: {size_kb:.0f} KB")
    else:
        print(f"  {page}.jpg: MISSING")
