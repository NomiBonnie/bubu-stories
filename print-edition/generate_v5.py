#!/usr/bin/env python3
"""Generate print-edition illustrations for Stories 19-24 (Volume 5)."""

import json, os, sys, time, base64, subprocess, requests

# Load API config
with open(os.path.expanduser("~/.config/azure-openai/config.json")) as f:
    cfg = json.load(f)

ENDPOINT = cfg["image2_eastus2_endpoint"]
API_KEY = cfg["image2_eastus2_api_key"]
API_VERSION = "2025-04-01-preview"
URL = f"{ENDPOINT}?api-version={API_VERSION}"
HEADERS = {"api-key": API_KEY, "Content-Type": "application/json"}

WORKSPACE = os.path.expanduser("~/.openclaw/workspace/bubu-stories/print-edition")

# Character prompts
BUBU = "a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow. She has a small pink bow centered ON TOP OF HER HEAD between her two ears (not on left ear, not on right ear, not behind — exactly centered on top between the ears). She has a toddler-like round body proportion."

SAM_DAD = "Sam Dad who is a GOLDEN RETRIEVER DOG (NOT a human, NOT a person — he is an ANIMAL, a large golden-furred dog walking upright). He has warm golden fur all over his body, a dog snout/muzzle, floppy dog ears, and a wagging tail. He wears a dark navy jacket over a simple shirt. He has a warm gentle dog smile. IMPORTANT: Sam Dad must look like a golden retriever dog, not a human man."

TINA_MOM = "Tina Mom who is a BLACK-AND-WHITE COW (NOT a human, NOT a person — she is an ANIMAL, a cow walking upright). She has black and white spotted fur pattern all over, small curved horns, cow ears, and hooves. She wears an elegant cream knit cardigan over a floral skirt. She has a gentle warm cow smile. IMPORTANT: Tina Mom must look like a cow, not a human woman."

NOMI = "a raccoon (NOMI) with grey-brown fur, distinctive black eye mask markings, and a ringed bushy tail. She wears a blue-and-white horizontally striped sweater. She has clever bright eyes and nimble paws."

NONO = "a small red bird (NONO) with bright red feathers all over, round bright eyes, and an orange-yellow beak. He has exactly TWO wings and TWO small bird feet with talons. NO ARMS, NO HANDS — birds do not have arms or hands, only wings."

WAIPO = "Grandma (Waipo) who is a LIGHT GREY-WHITE GOAT (NOT a human — she is an ANIMAL, a goat walking upright). She has soft pale grey-white fur, small curved goat horns, gentle deep brown eyes, and a short goat beard. She wears a floral blouse with light-colored casual pants and a sun hat. She has a warm loving grandmother smile."

WAIGONG = "Grandpa (Waigong) who is a DARK BROWN HORSE (NOT a human — he is an ANIMAL, a horse walking upright). He has dark brown fur/coat, a grey-white mane showing his age, calm deep eyes. He wears a polo shirt with casual pants and a simple wristwatch. He is tall but not bulky, elderly but energetic. He has a steady gentle smile."

STYLE_BASE = "Pixar 3D animation style, warm soft lighting, children's picture book illustration. Pure illustration with NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS anywhere in the image. The bottom 20% of the image should have natural darkening/vignette gradient."

def build_prompt(scene_desc, characters):
    """Build full prompt with characters + scene + style."""
    char_block = "\n\nCharacters in this scene:\n" + "\n".join(f"- {c}" for c in characters)
    return f"{STYLE_BASE}\n\nScene: {scene_desc}{char_block}\n\nIMPORTANT: No text/words/letters anywhere. Natural composition. Bottom 20% natural darkening."

def generate_image(prompt, output_path, retry=0):
    """Call Azure API, save as JPG."""
    if os.path.exists(output_path):
        sz = os.path.getsize(output_path)
        if sz > 50000:
            print(f"  SKIP (exists {sz//1024}KB): {output_path}")
            return True

    body = {"prompt": prompt, "n": 1, "size": "1024x1536", "quality": "medium", "output_format": "png"}
    try:
        r = requests.post(URL, headers=HEADERS, json=body, timeout=120)
        if r.status_code == 429:
            if retry < 3:
                wait = 45
                print(f"  429 rate limit, waiting {wait}s (retry {retry+1}/3)")
                time.sleep(wait)
                return generate_image(prompt, output_path, retry+1)
            print(f"  FAIL 429 after 3 retries: {output_path}")
            return False
        if r.status_code != 200:
            print(f"  FAIL {r.status_code}: {r.text[:200]}")
            return False

        data = r.json()
        b64 = data["data"][0]["b64_json"]
        png_path = output_path.replace(".jpg", ".png")
        with open(png_path, "wb") as f:
            f.write(base64.b64decode(b64))

        # Convert to JPG
        subprocess.run(["ffmpeg", "-y", "-i", png_path, "-q:v", "2", output_path],
                      capture_output=True, timeout=30)
        os.remove(png_path)
        sz = os.path.getsize(output_path)
        print(f"  OK {sz//1024}KB: {output_path}")
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

# Define all pages with scenes and characters
PAGES = {
    "story19": {
        2: ("Bubu sitting excitedly in the back seat of a car, kicking her little feet. NOMI sits next to her giggling. Through the car window, spring countryside scenery. Qingming Festival spring outing atmosphere.",
            [BUBU, SAM_DAD, NOMI]),
        3: ("A vast green strawberry field stretching out. Bubu stands looking around confused, searching for strawberry trees. Sam Dad kneels down beside her laughing. Bright spring sunshine, green strawberry leaves everywhere.",
            [BUBU, SAM_DAD]),
        4: ("Close-up: Sam Dad gently lifts green strawberry leaves to reveal a big red strawberry underneath. Bubu's eyes are wide with amazement. NONO flies down low to look. Strawberry field setting.",
            [BUBU, SAM_DAD, NONO]),
        5: ("Tina Mom pointing at strawberries on the ground, teaching Bubu. There are red ripe strawberries and green unripe ones visible. Bubu nods attentively. Sunny strawberry field.",
            [BUBU, TINA_MOM]),
        6: ("NOMI demonstrating to Bubu how to pick strawberries with two fingers, giving a gentle twist. Bubu carefully copies the motion. Close-up of their hands/paws near strawberry plants.",
            [BUBU, NOMI]),
        7: ("Bubu proudly showing Sam Dad a small basket full of red strawberries. Dad gives thumbs up. Strawberry field background, warm sunshine.",
            [BUBU, SAM_DAD]),
        8: ("Tina Mom handing a washed strawberry to Bubu. Bubu takes a big bite with a delighted expression, juice on her face. NOMI watches nearby smiling. Outdoor picnic-like setting near the field.",
            [BUBU, TINA_MOM, NOMI]),
        9: ("Bubu discovering a tomato patch — red, green, and yellow tomatoes growing on vines. Bubu reaches to pick a red tomato. Tina Mom standing nearby smiling. Garden/farm setting.",
            [BUBU, TINA_MOM]),
        10: ("The whole family standing together at the edge of the field, posing for a photo. Bubu holds a basket full of strawberries and tomatoes. Tina Mom wipes sweat from Bubu's face. Warm golden hour light.",
             [BUBU, TINA_MOM, NOMI, NONO]),
        11: ("Inside a car, Bubu has fallen asleep holding her basket of strawberries. Strawberry juice stains on her fingers. NOMI gently covers her with a small blanket. Soft evening light through car window.",
             [BUBU, NOMI]),
        12: ("Bubu standing happily in a strawberry field, holding up a big red strawberry triumphantly. NOMI and NONO beside her. Green strawberry plants all around, bright cheerful atmosphere. Summary/ending scene.",
             [BUBU, NOMI, NONO]),
    },
    "story20": {
        2: ("Bubu pressing her face against a window, looking out at cherry blossom trees in full bloom. Pink petals visible through the glass. Spring morning light, cozy indoor-outdoor scene.",
            [BUBU]),
        3: ("Sam Dad and Tina Mom standing at the doorway, inviting Bubu to go out. Bubu's rabbit ears perk up with excitement. Tina Mom holds Bubu's hand. Cherry blossoms visible outside.",
            [BUBU, SAM_DAD, TINA_MOM]),
        4: ("A large three-seat tandem bike with a canopy in a park. Bubu sits in the middle seat, Sam Dad on left, Tina Mom on right. Cherry blossom trees line the path. Spring park setting.",
            [BUBU, SAM_DAD, TINA_MOM]),
        5: ("The family riding the big tandem bike along a cherry blossom-lined path. Pink petals floating down like snow. Wind blowing gently. Bubu shouting happily. Beautiful spring scenery.",
            [BUBU, NOMI, NONO]),
        6: ("A cherry blossom petal landing on Bubu's nose. Bubu giggles with squinty eyes. NOMI waves from the path below. NONO perches on a cherry blossom branch singing. Whimsical spring scene.",
            [BUBU, NOMI, NONO]),
        7: ("Bubu running and spinning in circles under a giant cherry blossom tree. Ground covered in pink petals like a carpet. Joyful, magical atmosphere. Petals swirling around her.",
            [BUBU]),
        8: ("Picnic scene under cherry blossoms. Tina Mom spreads a blanket with bread and juice. Bubu leans against Sam Dad holding a juice box, looking up at the flowers. Warm family moment.",
            [BUBU, SAM_DAD, TINA_MOM]),
        9: ("A cute red toy train on a track in the park. Bubu pulling Sam Dad's hand excitedly, running toward the train. Cherry blossom park setting.",
            [BUBU, SAM_DAD]),
        10: ("Bubu sitting in a small toy train, gripping the handle. The train passes through a tunnel of cherry blossom branches with petals showering down. Magical, dreamy atmosphere.",
             [BUBU]),
        11: ("Sunset scene — orange-red sky. Bubu asleep on Sam Dad's back, arms around his neck. Sam Dad walking along a cherry blossom path. Warm, tender father-daughter moment.",
             [BUBU, SAM_DAD]),
        12: ("Dreamy ending scene: the family silhouetted or softly lit under cherry blossom trees at dusk. Bubu between Sam Dad and Tina Mom, holding their hands. Petals floating. Warm, magical atmosphere.",
             [BUBU, SAM_DAD, TINA_MOM]),
    },
    "story21": {
        2: ("Warm spring morning. Bubu reaching up with arms extended toward Tina Mom, wanting to be carried. Front door/entrance area of a home. Tina Mom looking down with a gentle smile.",
            [BUBU, TINA_MOM]),
        3: ("Tina Mom patting a cute baby stroller, introducing it to Bubu. Bubu looking at the stroller curiously. Indoor/doorway setting, spring light coming in.",
            [BUBU, TINA_MOM]),
        4: ("Bubu sitting happily in the stroller, swinging her little feet. The stroller has a cute sunshade canopy. Outdoor sidewalk/park path. Spring sunshine.",
            [BUBU]),
        5: ("Bubu in the stroller kicking her legs happily, enjoying the breeze. Trees and spring flowers along the path. Peaceful, comfortable atmosphere.",
            [BUBU]),
        6: ("Bubu in the stroller, looking at a small friendly dog (not a character, just a pet dog) walking by wagging its tail. Street/park scene. Bubu pointing excitedly.",
            [BUBU]),
        7: ("Bubu in stroller pointing at colorful butterflies flying past flower bushes. Tina Mom walking beside the stroller. Vibrant spring flowers and butterflies. Bubu's eyes sparkling with wonder.",
            [BUBU, TINA_MOM]),
        8: ("NOMI walking up to Bubu in the stroller, admiring it. NONO flying around nearby chirping. Park/sidewalk setting. Bubu looking proud in her stroller.",
            [BUBU, NOMI, NONO]),
        9: ("Bubu sitting proudly in the stroller with a small bunny plush toy placed next to her. She declares it her 'adventure car'. Fun, imaginative atmosphere.",
            [BUBU]),
        10: ("Bubu in stroller eating a small cake, parked outside a cute bakery/shop. Tina Mom handing her the cake. Cozy street scene. Bubu enjoying the treat.",
             [BUBU, TINA_MOM]),
        11: ("Sam Dad pushing the stroller from behind, Tina Mom walking alongside. Bubu eating and looking at scenery, swinging feet. Tree-lined spring street. Warm family outing.",
             [BUBU, SAM_DAD, TINA_MOM]),
        12: ("Wide shot of Bubu in her stroller on a beautiful spring path, looking out at the big world. NOMI and NONO accompanying her. Bright, cheerful, open scenery. Ending/summary feel.",
             [BUBU, NOMI, NONO]),
    },
    "story22": {
        2: ("Beautiful sunny day. Bubu standing excitedly between Grandma Goat (Waipo) and Grandpa Horse (Waigong), ready to go out. Residential neighborhood setting.",
            [BUBU, WAIPO, WAIGONG, NOMI]),
        3: ("Inside a bus. Bubu sitting next to Grandma Goat, looking out the window at city scenery. Grandpa Horse sits nearby. Cozy public transport scene.",
            [BUBU, WAIPO, WAIGONG]),
        4: ("A big beautiful city square with flowers, trees, and a large fountain. Bubu looking around in awe. Grandpa and Grandma walking with her. Bright sunny day.",
            [BUBU, WAIPO, WAIGONG]),
        5: ("Grandma Goat holding up a phone to take Bubu's photo. Bubu turning to face the camera with a big smile. Square/park background with flowers.",
            [BUBU, WAIPO]),
        6: ("Close-up of Bubu posing for a photo, looking directly at the viewer/camera with a sweet smile. Fountain and flowers in the background. Photo-within-a-scene feel.",
            [BUBU]),
        7: ("Grandpa Horse holding up a phone to photograph Bubu. Bubu looking at the camera with a squinty happy smile. Park/square setting.",
            [BUBU, WAIGONG]),
        8: ("Another photo moment — Bubu posing confidently for the camera, looking at the lens. She's learned to look at the camera! Bright, cheerful setting.",
            [BUBU]),
        9: ("Grandma Goat and Bubu sitting on a bench, Bubu eating a plum blossom cake (梅花糕). The cake looks delicious. Park/square setting. Happy snack time.",
            [BUBU, WAIPO]),
        10: ("Bubu posing for yet another photo after eating, with crumbs/sweet smile on her face. Looking at camera. Park with flowers and greenery behind.",
             [BUBU, WAIPO, WAIGONG]),
        11: ("Evening bus ride home. Bubu dozing off in Grandma Goat's arms. Soft evening light through bus windows. Grandpa Horse sitting nearby watching tenderly.",
             [BUBU, WAIPO, WAIGONG]),
        12: ("Bubu lying in her little bed after a bath, sleepy and content. Dreaming of all the photos she took today. Soft nightlight ambiance. Cozy bedroom scene.",
             [BUBU]),
    },
    "story23": {
        2: ("Large museum entrance/lobby. Bubu holding Sam Dad's hand tightly, looking a bit scared by the grand space. High ceilings, grand architecture. Museum interior.",
            [BUBU, SAM_DAD]),
        3: ("Sam Dad and Tina Mom reassuring Bubu. NOMI also holding Bubu's hand/paw. Museum hallway. Bubu looking less scared with her family around her.",
            [BUBU, SAM_DAD, TINA_MOM, NOMI]),
        4: ("Bubu looking up in amazement at a large model of a Chinese ancient palace/building in a museum display. Grand, impressive exhibit. Museum interior with display lighting.",
            [BUBU, NOMI]),
        5: ("Bubu pointing at a beautiful traditional Chinese painting on a museum wall, eyes sparkling with wonder. Museum gallery with proper lighting.",
            [BUBU]),
        6: ("Bubu looking curiously at various ancient artifacts/treasures in glass display cases. Museum exhibition hall. Curious, engaged expression.",
            [BUBU, NOMI]),
        7: ("Tina Mom bending down to tell Bubu about an exhibit — a model of an ancient house. Bubu listening attentively. Museum setting with historical displays.",
            [BUBU, TINA_MOM]),
        8: ("Bubu and friends sitting in a museum café/rest area, having snacks. Taking a break. Museum interior with comfortable seating.",
            [BUBU, NOMI, NONO]),
        9: ("Bubu jumping up energetically, ready to explore more of the museum. Excited expression. Museum corridor with interesting exhibits visible.",
            [BUBU]),
        10: ("Bubu reaching up to spin a large globe in the museum. Fascinated expression. Museum education/interactive area.",
             [BUBU, NOMI]),
        11: ("Wide shot of Bubu walking confidently through the museum, no longer scared. She looks amazed and happy. Beautiful museum interior with exhibits.",
             [BUBU, NOMI, NONO]),
        12: ("Bubu outside the museum entrance, waving goodbye to the building. Sunset light. She looks happy and fulfilled. NOMI and NONO with her. Ending scene.",
             [BUBU, NOMI, NONO]),
    },
    "story24": {
        2: ("Family arriving at a campsite. Sam Dad just finished setting up a tent. Bubu jumping with excitement. Green meadow, trees, outdoor camping gear. Bright day.",
            [BUBU, SAM_DAD, NOMI]),
        3: ("Bubu discovering wildflowers on the meadow — red, yellow, purple flowers dotted across green grass. Bubu bending down to look closely. Beautiful natural setting.",
            [BUBU]),
        4: ("Bubu reaching out to pick a flower, but NOMI gently holds her hand to stop her. Teaching moment — 'look but don't touch'. Meadow with wildflowers.",
            [BUBU, NOMI]),
        5: ("Bubu finding a dandelion — a perfect round white fluffy seed head. She holds it up, amazed. Green meadow background. Close-up magical moment.",
            [BUBU]),
        6: ("The family blowing a dandelion together — seeds flying into the air like tiny parachutes. Bubu clapping her hands. Magical, whimsical scene. Sunny meadow.",
            [BUBU, NOMI, NONO]),
        7: ("Bubu crouching down to watch a bee collecting nectar from a flower. Curious expression. Close-up nature observation. Meadow with flowers.",
            [BUBU]),
        8: ("NOMI explaining to Bubu about bees — gesturing to keep distance. Bubu and NOMI standing a few steps back from flowers where a bee is working. Educational moment.",
            [BUBU, NOMI]),
        9: ("Bubu squatting down, watching a line of ants carrying food on the ground. Fascinated expression. Close-up ground-level perspective. Grass and soil visible.",
            [BUBU]),
        10: ("Bubu standing up proudly, declaring 'look with eyes, don't touch!' NOMI and NONO nearby looking proud of her. Meadow setting, warm light.",
             [BUBU, NOMI, NONO]),
        11: ("Sunset scene at the campsite. Family sitting in front of the tent. Orange-red sky. NOMI pouring hot cocoa for Bubu. Warm, cozy camping evening atmosphere.",
             [BUBU, NOMI, NONO]),
        12: ("Bubu sitting contentedly at the campsite at dusk, surrounded by nature — flowers, dandelion seeds floating, fireflies beginning to appear. Peaceful, magical ending. NOMI and NONO with her.",
             [BUBU, NOMI, NONO]),
    },
}

# Track results
results = []
total = sum(len(pages) for pages in PAGES.values())
done = 0

for story_key in sorted(PAGES.keys()):
    pages = PAGES[story_key]
    story_dir = os.path.join(WORKSPACE, story_key)
    os.makedirs(story_dir, exist_ok=True)

    for page_num in sorted(pages.keys()):
        scene_desc, characters = pages[page_num]
        prompt = build_prompt(scene_desc, characters)
        output_path = os.path.join(story_dir, f"page-{page_num:02d}.jpg")

        done += 1
        print(f"\n[{done}/{total}] {story_key}/page-{page_num:02d}")

        ok = generate_image(prompt, output_path)
        sz = os.path.getsize(output_path) if os.path.exists(output_path) else 0
        results.append({"story": story_key, "page": page_num, "ok": ok, "size_kb": sz // 1024, "path": output_path})

        if done < total:
            time.sleep(8)

# Summary
print("\n\n=== GENERATION SUMMARY ===")
for r in results:
    status = "✅" if r["ok"] else "❌"
    print(f"{status} {r['story']}/page-{r['page']:02d} — {r['size_kb']}KB")

failed = [r for r in results if not r["ok"]]
print(f"\nTotal: {len(results)}, Success: {len(results)-len(failed)}, Failed: {len(failed)}")
if failed:
    print("Failed pages:", [f"{r['story']}/p{r['page']}" for r in failed])
