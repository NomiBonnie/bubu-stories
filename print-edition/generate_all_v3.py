#!/usr/bin/env python3
"""Generate all print edition illustrations for Stories 1-4 (v3)."""

import json, os, time, subprocess, requests, sys

# API config
cfg = json.load(open(os.path.expanduser("~/.config/azure-openai/config.json")))
ENDPOINT = cfg["image2_eastus2_endpoint"].rstrip("/")
API_KEY = cfg["image2_eastus2_api_key"]
API_VERSION = "2025-04-01-preview"
URL = f"{ENDPOINT}?api-version={API_VERSION}"

HEADERS = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

WORKSPACE = "bubu-stories/print-edition"

# Character prompts
BUBU = "a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow. She has a small pink bow centered ON TOP OF HER HEAD between her two ears (not on left ear, not on right ear, not behind — exactly centered on top between the ears). She has a toddler-like round body proportion."

SAM_DAD = "Sam Dad who is a GOLDEN RETRIEVER DOG (NOT a human, NOT a person — he is an ANIMAL, a large golden-furred dog walking upright). He has warm golden fur all over his body, a dog snout/muzzle, floppy dog ears, and a wagging tail. He wears a dark navy jacket over a simple shirt. He has a warm gentle dog smile. IMPORTANT: Sam Dad must look like a golden retriever dog, not a human man."

TINA_MOM = "Tina Mom who is a BLACK-AND-WHITE COW (NOT a human, NOT a person — she is an ANIMAL, a cow walking upright). She has black and white spotted fur pattern all over, small curved horns, cow ears, and hooves. She wears an elegant cream knit cardigan over a floral skirt. She has a gentle warm cow smile. IMPORTANT: Tina Mom must look like a cow, not a human woman."

NOMI = "a raccoon (NOMI) with grey-brown fur, distinctive black eye mask markings, and a ringed bushy tail. She wears a blue-and-white horizontally striped sweater. She has clever bright eyes and nimble paws."

NONO = "a small red bird (NONO) with bright red feathers all over, round bright eyes, and an orange-yellow beak. He has exactly TWO wings and TWO small bird feet with talons. NO ARMS, NO HANDS — birds do not have arms or hands, only wings."

DOUDOU = "a small hedgehog (Doudou) with a brown body covered in dark brown spines/quills, small round shiny eyes, a tiny nose. He is small, round, and shy-looking."

MANMAN = "a small turtle (Manman) with a green shell with dark green hexagonal patterns, light green skin, small round eyes, and a gentle slow expression."

BOTTOM_DARK = "The bottom 20% of the image should be slightly darker/softer as a natural gradient for later text overlay."
STYLE_PREFIX = "Pixar 3D animation style, children's picture book illustration, vertical portrait composition 1024x1536. No text, no letters, no words, no numbers anywhere in the image."

def make_prompt(lighting, scene, characters):
    return f"""{STYLE_PREFIX} {lighting}

SCENE: {scene}

CHARACTERS: {characters}

The composition naturally centers characters in the middle-right area of the frame. {BOTTOM_DARK}

Professional children's picture book quality, warm and inviting atmosphere."""


# ============ STORY 1: 小兔子找月亮 ============
STORY1 = [
    # P2
    make_prompt("Golden sunset light, warm and soft.",
        "A lush green meadow stretching to the horizon, wildflowers dotting the grass, golden hour sky.",
        f"{BUBU} standing happily in the meadow, hopping with joy, ears bouncing."),
    # P3
    make_prompt("Warm afternoon light filtering through leaves.",
        "A lush green meadow with a large oak tree nearby.",
        f"{NOMI} waving happily on the meadow, looking friendly and clever."),
    # P4
    make_prompt("Bright blue sky with fluffy white clouds.",
        "Open sky above a green meadow, clouds scattered beautifully.",
        f"{NONO} flying cheerfully through the sky with wings spread wide."),
    # P5
    make_prompt("Peaceful moonlit night, soft blue tones.",
        "A small grassy hill under a dark blue night sky with a big bright full moon and twinkling stars.",
        f"{BUBU} sitting on the hilltop, looking up at the moon with wonder and a gentle smile."),
    # P6
    make_prompt("Dark night sky, slightly dramatic lighting.",
        "The same grassy hill but now the sky is completely dark — no moon visible, only a few faint stars. Eerie but not scary.",
        f"{BUBU} looking up at the empty sky with a worried, puzzled expression."),
    # P7
    make_prompt("Night scene, soft moonless darkness with distant warm light.",
        "A meadow at night, a cozy treehouse visible in the distance with warm light glowing from its windows.",
        f"{BUBU} running urgently across the meadow toward the treehouse, looking worried."),
    # P8
    make_prompt("Warm lamplight inside, dark night outside.",
        "Inside a cozy tree hollow with books on shelves, a warm lamp glowing. The entrance shows dark night outside.",
        f"{NOMI} sitting inside reading a book with tiny glasses on. {BUBU} at the entrance looking worried and calling out."),
    # P9
    make_prompt("Dark night sky with stars.",
        "Night sky over a meadow, stars twinkling. Ground visible below with grass.",
        f"{NONO} flying high in the dark sky, searching around with determined expression. Below on the ground, {BUBU} and {NOMI} looking up."),
    # P10
    make_prompt("Magical moonlit glow reflecting off water.",
        "A calm pond surrounded by reeds and grass at night. The full moon is perfectly reflected in the still water surface, creating a magical glow.",
        f"{NONO} hovering excitedly above the pond, pointing down with one wing at the moon reflection."),
    # P11
    make_prompt("Soft moonlight reflecting off crystal clear water, magical firefly lights.",
        "A beautiful calm pond at night with fireflies floating around. A perfect full moon reflection shimmers in the crystal clear water.",
        f"{BUBU} and {NOMI} kneeling at the pond edge, looking down at the moon reflection with wonder and amazement."),
    # P12
    make_prompt("Dynamic night scene with water splashing and light fragments.",
        "The pond at night. Water is splashing dramatically, the moon reflection is shattered into many shimmering light fragments across the rippling surface.",
        f"{BUBU} with one paw in the water, looking surprised. {NOMI} and {NONO} nearby getting splashed, with funny surprised expressions."),
    # P13
    make_prompt("Beautiful bright moonlight streaming down from above.",
        "Night meadow near the pond. The big beautiful full moon is now clearly visible high in the sky, bathing everything in magical silver moonlight.",
        f"{BUBU} looking up amazed at the moon with mouth open in wonder. {NOMI} pointing up at the sky and smiling. {NONO} perched on NOMI's head."),
    # P14
    make_prompt("Warm soft moonlight bathing three friends in gentle glow.",
        "A meadow at night under a beautiful full moon. Peaceful and heartwarming atmosphere.",
        f"{BUBU}, {NOMI}, and {NONO} all together, smiling happily under the moonlight. They look content and close."),
    # P15
    make_prompt("Warm cozy bedroom light, soft and sleepy.",
        "A cozy children's bedroom with a warm bed covered in soft blankets. A window shows the full moon outside. A warm bedside lamp glows softly. Stuffed animal toys on the pillow.",
        f"{BUBU} tucked into bed, looking out the window at the moon with a sleepy happy expression."),
    # P16
    make_prompt("Soft pastel moonlight, educational and warm.",
        "A hill at night with a calm pond below. The full moon is in the sky AND reflected in the pond, showing both the real moon and its reflection.",
        f"{BUBU}, {NOMI}, and {NONO} sitting together on the hill, looking at both the moon above and its reflection in the pond below."),
]

# ============ STORY 2: 咘咘找朋友 (rainbow) ============
STORY2 = [
    # P2
    make_prompt("Bright morning light after rain, rainbow in sky.",
        "View from inside a cozy room looking out a rain-speckled window. Outside, a huge beautiful rainbow arcs across the clearing sky after rain.",
        f"{BUBU} pressing her face against the window glass, staring at the rainbow with amazement and delight."),
    # P3
    make_prompt("Bright post-rain sunshine, vibrant rainbow.",
        "Outside a cozy cottage door, wet grass glistening, a grand rainbow stretching across the sky.",
        f"{BUBU} leaping excitedly out the door, running toward the rainbow with arms outstretched."),
    # P4
    make_prompt("Bright sunshine, rainbow in the distance.",
        "A green hill with wet grass. The rainbow is visible but far away in the sky.",
        f"{BUBU} standing on top of the hill, reaching toward the distant rainbow, looking determined but the rainbow seems so far."),
    # P5
    make_prompt("Warm morning light, post-rain freshness.",
        "A hillside with mushrooms growing after the rain. Some mushrooms in a basket.",
        f"{NOMI} holding a basket of mushrooms, looking curious. {BUBU} running up excitedly, looking eager."),
    # P6
    make_prompt("Dappled forest light, mysterious and inviting.",
        "Edge of a lush forest, trees dripping with raindrops, the rainbow visible through the canopy pointing beyond the forest.",
        f"{NOMI} and {BUBU} walking together toward the forest, looking determined and excited."),
    # P7
    make_prompt("Post-rain sunshine, water droplets sparkling on leaves.",
        "A tree branch with water droplets. Forest path visible behind.",
        f"{NONO} on a branch shaking water off his wings. {BUBU} and {NOMI} below looking up at him."),
    # P8
    make_prompt("Bright sky with clouds, aerial perspective feeling.",
        "High up near the clouds, looking down at a river winding through green landscape. Rainbow arcing toward the river.",
        f"{NONO} flying high near the clouds, looking down and pointing with a wing toward the river below."),
    # P9
    make_prompt("Sparkling riverside light.",
        "A beautiful river bank with rocks and flowing water. The rainbow appears to end just beyond the river, tantalizingly close but still out of reach.",
        f"{BUBU}, {NOMI}, and {NONO} at the riverside, looking disappointed as the rainbow seems to have moved further away."),
    # P10
    make_prompt("Warm afternoon light, gentle and tired.",
        "Riverside with smooth rocks for sitting. Calm flowing water.",
        f"{BUBU} sitting tiredly on a river rock, looking a bit sad. {NOMI} and {NONO} nearby, also resting."),
    # P11
    make_prompt("Brilliant sunshine hitting water spray, prismatic light effects.",
        "River surface with sunlight hitting water spray, creating many tiny rainbows dancing in the water mist.",
        f"{NOMI} pointing excitedly at the water surface. {BUBU} leaning forward to look, eyes wide with surprise."),
    # P12
    make_prompt("Magical prismatic light on water spray.",
        "Close-up view of water splashing, with a small rainbow visible in the water droplets catching sunlight.",
        f"{BUBU} with paws outstretched, water spray creating a tiny rainbow right in her palms. Her expression is pure joy and amazement."),
    # P13
    make_prompt("Misty waterfall spray with rainbow light.",
        "Near a small waterfall, mist and spray creating beautiful rainbow effects.",
        f"{NONO} flying through waterfall mist, his wings creating swirls in the spray, a rainbow appearing in the mist around him."),
    # P14
    make_prompt("Warm golden afternoon light, peaceful.",
        "Riverside with beautiful light, small rainbows visible in water spray in background.",
        f"{NOMI} smiling wisely. {BUBU} looking happy and enlightened. {NONO} perched nearby."),
    # P15
    make_prompt("Golden sunset light, puddles reflecting sky.",
        "A path home with rain puddles along the way, each puddle reflecting colorful sunset sky, tiny rainbows in each.",
        f"{BUBU} hopping joyfully through puddles, splashing, with a big happy smile. Small rainbows visible in the splashing water."),
    # P16
    make_prompt("Warm educational light, rainbow and water theme.",
        "A scene with sunlight shining through water droplets, creating a beautiful rainbow. The connection between light and water is visually shown.",
        f"{BUBU}, {NOMI}, and {NONO} together marveling at a rainbow forming in water spray, looking happy and amazed."),
]

# ============ STORY 3: 小刺猬的新朋友 ============
STORY3 = [
    # P2
    make_prompt("Bright sunny day, warm and cheerful.",
        "A beautiful park with a playground — slides, swings, and a large sandbox visible. Trees and flowers around.",
        f"{SAM_DAD} walking with {BUBU} into the park. {BUBU} is excitedly looking around. Sam Dad holds her paw gently."),
    # P3
    make_prompt("Warm sunshine in sandbox area.",
        "A large sandbox in the park with a pretty sand castle being built. Playground equipment visible in background.",
        f"{DOUDOU} in the sandbox carefully building a sand castle with a small shovel. The castle looks detailed and pretty."),
    # P4
    make_prompt("Bright playground light.",
        "The sandbox area. The sand castle is visible.",
        f"{BUBU} running toward {DOUDOU} and grabbing the shovel from him, looking eager but thoughtless. {DOUDOU} looks startled."),
    # P5
    make_prompt("Tense moment lighting, slightly dramatic.",
        "The sandbox with a collapsed sand castle, sand scattered everywhere. The shovel lies on the ground.",
        f"{BUBU} and {DOUDOU} pushing and pulling, both looking upset. {DOUDOU} is crying with tears streaming down. The sand castle is ruined."),
    # P6
    make_prompt("Warm gentle light, parental guidance moment.",
        "The sandbox area. The ruined sand castle in background.",
        f"{SAM_DAD} kneeling down to {BUBU}'s eye level, looking at her gently but seriously. {BUBU} looking down, ashamed. {DOUDOU} crying in background."),
    # P7
    make_prompt("Warm patient light, teaching moment.",
        "Same sandbox scene, close-up feeling.",
        f"{SAM_DAD} gently holding {BUBU}'s paw, demonstrating how to ask nicely with a warm encouraging expression. {BUBU} looking up at him, listening carefully."),
    # P8
    make_prompt("Soft apologetic light, tender moment.",
        "The sandbox with the ruined castle.",
        f"{BUBU} standing in front of {DOUDOU}, head slightly bowed, looking sorry and shy. She is speaking softly to the crying hedgehog."),
    # P9
    make_prompt("Brightening light, hope returning.",
        "The sandbox, mood lifting.",
        f"{DOUDOU} wiping tears with one paw and nodding with a small smile. {BUBU} looking relieved and hopeful."),
    # P10
    make_prompt("Happy warm sunshine.",
        "The sandbox with a new, bigger, more beautiful sand castle being built.",
        f"{BUBU} using the shovel to build. {DOUDOU} patting sand with little paws. They are working together happily, both smiling."),
    # P11
    make_prompt("Cheerful afternoon light.",
        "The sandbox with the impressive new castle. Friends arriving.",
        f"{NOMI} arriving with a small bucket. {NONO} flying in carrying a tiny flag in his beak. {BUBU} and {DOUDOU} looking up happily. The sand castle is big and beautiful."),
    # P12
    make_prompt("Warm maternal glow, loving observation.",
        "Park bench near the sandbox, overlooking the children playing.",
        f"{TINA_MOM} sitting on a park bench, watching the children play with a warm loving smile. In the background, {BUBU}, {DOUDOU}, {NOMI}, and {NONO} are playing around the sand castle."),
    # P13
    make_prompt("Golden late afternoon light, friendship warmth.",
        "A park path leading home, trees lining the way, golden hour light.",
        f"{BUBU} carefully holding {DOUDOU}'s paw (holding the palm side without spines). Both smiling at each other, walking together. {SAM_DAD} walking behind them, smiling proudly."),
    # P14
    make_prompt("Warm educational light, friendship theme.",
        "The park sandbox with a beautiful completed sand castle, golden hour.",
        f"{BUBU} and {DOUDOU} standing proudly next to their sand castle, holding paws, smiling at each other. The castle has a little flag on top."),
]

# ============ STORY 4: 咘咘学会说对不起 ============
STORY4 = [
    # P2
    make_prompt("Beautiful sunny day, sparkles on water.",
        "A riverside with sand. Calm water flowing gently. Lush green banks. A nice day for playing outside.",
        f"{BUBU} and {MANMAN} playing together in the sand by the river. {MANMAN} carefully building a sand castle."),
    # P3
    make_prompt("Warm admiring light.",
        "Riverside sand area. A beautiful detailed sand castle made by the turtle.",
        f"{BUBU} looking at {MANMAN}'s impressive sand castle with admiration. {MANMAN} carefully adding details to the castle."),
    # P4
    make_prompt("Sudden dramatic moment, dust/sand flying.",
        "Riverside sand area. The sand castle is collapsing as it gets accidentally knocked.",
        f"{BUBU} accidentally bumping into {MANMAN}'s sand castle, looking shocked. The castle is crumbling. Sand flying."),
    # P5
    make_prompt("Sad emotional light, blue tones.",
        "Riverside sand area. The collapsed sand castle is now just a pile of sand.",
        f"{MANMAN} looking at the ruined castle with tears flowing from her eyes. Looking devastated and sad."),
    # P6
    make_prompt("Isolated feeling, guilt and sadness.",
        "A cozy room with a bed and window. Curtains partially drawn, subdued light.",
        f"{BUBU} sitting alone on her bed, hugging her knees, looking guilty and sad. She's hiding from the world."),
    # P7
    make_prompt("Warm comforting light, paternal tenderness.",
        "Bubu's cozy bedroom. Warm light from window.",
        f"{SAM_DAD} sitting on the bed beside {BUBU}, looking at her with gentle understanding. {BUBU} looking up at him, about to explain what happened."),
    # P8
    make_prompt("Thoughtful warm light, reflection moment.",
        "Same bedroom, close emotional moment.",
        f"{SAM_DAD} speaking gently to {BUBU}. {BUBU} thinking deeply, looking contemplative and starting to understand, a little sad but growing."),
    # P9
    make_prompt("Warm kitchen light, smell of fresh cookies.",
        "A cozy kitchen with an oven. A tray of fresh cookies on the counter, steam rising.",
        f"{TINA_MOM} handing a plate of warm cookies to {BUBU}. {TINA_MOM} smiling encouragingly. {BUBU} taking the plate with a determined but nervous expression."),
    # P10
    make_prompt("Afternoon riverside light, vulnerable moment.",
        "Back at the riverside. The ruined sand castle area. A half-rebuilt castle shows Manman has been working alone.",
        f"{BUBU} approaching {MANMAN} carrying the plate of cookies, looking nervous but brave. {MANMAN} looking up from her rebuilding, surprised to see Bubu."),
    # P11
    make_prompt("Quiet tender moment, hope emerging.",
        "Riverside sand area. The plate of cookies between them.",
        f"{BUBU} placing cookies in front of {MANMAN}, looking sincere and apologetic. {MANMAN} looking at the cookies, then at {BUBU}, expression softening."),
    # P12
    make_prompt("Warming light, forgiveness dawning.",
        "Riverside sand area. Cookies being shared.",
        f"{MANMAN} smiling slowly, forgiving. {BUBU} looking relieved and grateful. They start to reconnect."),
    # P13
    make_prompt("Joyful bright light, achievement and teamwork.",
        "Riverside sand area with an even bigger, more magnificent sand castle than before.",
        f"{BUBU} and {MANMAN} proudly standing next to their new bigger castle. {NOMI} passing by, looking amazed at the castle."),
    # P14
    make_prompt("Happy celebratory light.",
        "The magnificent sand castle with a small flag on top. All friends gathered.",
        f"{BUBU} and {MANMAN} laughing together by the castle. {NONO} placing a tiny flag on the very top of the castle. Everyone happy."),
    # P15
    make_prompt("Golden sunset light, walking home.",
        "A path along the river heading home, beautiful golden sunset sky.",
        f"{SAM_DAD} walking with {BUBU}, holding her paw. {BUBU} looking up at him, speaking proudly. Sam Dad looking down at her with a warm proud smile, patting her head."),
    # P16
    make_prompt("Warm educational light, cooperation theme.",
        "Riverside with the beautiful sand castle, golden hour. Peaceful and inspiring.",
        f"{BUBU} and {MANMAN} together by their castle, looking at each other with friendship and trust. The castle stands tall and proud between them."),
]

ALL_STORIES = [
    ("story1", STORY1, 15),
    ("story2", STORY2, 15),
    ("story3", STORY3, 13),
    ("story4", STORY4, 15),
]

def generate_image(prompt, output_path, retry=0):
    """Generate one image via Azure OpenAI API."""
    body = {
        "prompt": prompt,
        "n": 1,
        "size": "1024x1536",
        "quality": "medium",
        "output_format": "png",
    }
    try:
        resp = requests.post(URL, headers=HEADERS, json=body, timeout=120)
        if resp.status_code == 429:
            if retry < 3:
                wait = 45
                print(f"  429 rate limit, waiting {wait}s (retry {retry+1}/3)...")
                time.sleep(wait)
                return generate_image(prompt, output_path, retry + 1)
            else:
                print(f"  ❌ 429 after 3 retries, skipping")
                return False
        if resp.status_code != 200:
            print(f"  ❌ HTTP {resp.status_code}: {resp.text[:200]}")
            if retry < 3:
                time.sleep(15)
                return generate_image(prompt, output_path, retry + 1)
            return False
        
        data = resp.json()
        # Extract base64 image
        import base64
        b64 = data["data"][0]["b64_json"]
        png_path = output_path.replace(".jpg", ".png")
        with open(png_path, "wb") as f:
            f.write(base64.b64decode(b64))
        
        # Convert PNG to JPG with ffmpeg
        subprocess.run([
            "ffmpeg", "-y", "-i", png_path, "-q:v", "2", output_path
        ], capture_output=True)
        
        # Remove PNG
        if os.path.exists(output_path):
            os.remove(png_path)
            size_kb = os.path.getsize(output_path) / 1024
            print(f"  ✅ {output_path} ({size_kb:.0f} KB)")
            return True
        else:
            print(f"  ⚠️ ffmpeg failed, keeping PNG")
            os.rename(png_path, output_path)
            return True
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        if retry < 3:
            time.sleep(15)
            return generate_image(prompt, output_path, retry + 1)
        return False

def main():
    # Check if we should resume from a specific point
    start_story = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    start_page = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    
    total = 0
    failed = []
    parent_chars = {}  # Track which pages have parents
    
    for story_name, prompts, num_pages in ALL_STORIES:
        story_num = int(story_name.replace("story", ""))
        if story_num < start_story:
            continue
            
        out_dir = f"{WORKSPACE}/{story_name}"
        os.makedirs(out_dir, exist_ok=True)
        
        print(f"\n{'='*50}")
        print(f"  STORY {story_num}: Generating {num_pages} pages")
        print(f"{'='*50}")
        
        for i, prompt in enumerate(prompts):
            page_num = i + 2  # Pages start at P2
            if story_num == start_story and page_num < start_page:
                continue
            
            output_path = f"{out_dir}/page-{page_num:02d}.jpg"
            print(f"\n[Story {story_num} P{page_num}]")
            
            # Track parent characters
            has_dad = "SAM_DAD" in prompt or "Sam Dad" in prompt or "golden retriever" in prompt.lower()
            has_mom = "TINA_MOM" in prompt or "Tina Mom" in prompt or "cow" in prompt.lower()
            if has_dad or has_mom:
                key = f"Story {story_num} P{page_num}"
                chars = []
                if has_dad: chars.append("爸爸")
                if has_mom: chars.append("妈妈")
                parent_chars[key] = chars
            
            success = generate_image(prompt, output_path)
            if success:
                total += 1
            else:
                failed.append(f"Story {story_num} P{page_num}")
            
            time.sleep(8)  # Rate limit spacing
    
    # Summary
    print(f"\n{'='*50}")
    print(f"  COMPLETE: {total} images generated")
    if failed:
        print(f"  FAILED: {failed}")
    print(f"\n  Pages with parents:")
    for k, v in parent_chars.items():
        print(f"    {k}: {', '.join(v)}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
