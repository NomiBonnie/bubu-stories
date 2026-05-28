#!/usr/bin/env python3
"""Generate all print-edition illustrations for Stories 5-8 (Book 2)."""

import json, os, sys, time, base64, subprocess, urllib.request, urllib.error

# Load API config
with open(os.path.expanduser("~/.config/azure-openai/config.json")) as f:
    cfg = json.load(f)

ENDPOINT = cfg["image2_eastus2_endpoint"]
API_KEY = cfg["image2_eastus2_api_key"]
API_VERSION = "2025-04-01-preview"
OUTPUT_BASE = os.path.dirname(os.path.abspath(__file__))

# Character prompts
BUBU = "a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow. She has a small pink bow centered ON TOP OF HER HEAD between her two ears (not on left ear, not on right ear, not behind — exactly centered on top between the ears). She has a toddler-like round body proportion."

SAM_DAD = "Sam Dad who is a GOLDEN RETRIEVER DOG (NOT a human, NOT a person — he is an ANIMAL, a large golden-furred dog walking upright). He has warm golden fur all over his body, a dog snout/muzzle, floppy dog ears, and a wagging tail. He wears a dark navy jacket over a simple shirt. He has a warm gentle dog smile. IMPORTANT: Sam Dad must look like a golden retriever dog, not a human man."

TINA_MOM = "Tina Mom who is a BLACK-AND-WHITE COW (NOT a human, NOT a person — she is an ANIMAL, a cow walking upright). She has black and white spotted fur pattern all over, small curved horns, cow ears, and hooves. She wears an elegant cream knit cardigan over a floral skirt. She has a gentle warm cow smile. IMPORTANT: Tina Mom must look like a cow, not a human woman."

NOMI = "a raccoon (NOMI) with grey-brown fur, distinctive black eye mask markings, and a ringed bushy tail. She wears a blue-and-white horizontally striped sweater. She has clever bright eyes and nimble paws."

NONO = "a small red bird (NONO) with bright red feathers all over, round bright eyes, and an orange-yellow beak. He has exactly TWO wings and TWO small bird feet with talons. NO ARMS, NO HANDS — birds do not have arms or hands, only wings."

DOUDOU = "a small hedgehog (Doudou) with a brown body covered in dark brown spines/quills, small round shiny eyes, a tiny nose. He is small, round, and shy-looking."

MANMAN = "a small turtle (Manman) with a green shell with dark green hexagonal patterns, light green skin, small round eyes, and a gentle slow expression."

ZHUZHU = "a white sheep (Zhuzhu, NOT a pig despite the name) with cloud-like curly white wool, light blue vest, brown little hooves, pink nose, about the same size as Bubu."

DR_GIRAFFE = "a tall giraffe doctor (Dr. Giraffe) with standard giraffe spots, wearing a white doctor coat and stethoscope, warm professional expression, bending down to talk to small children."

NURSE_SQUIRREL = "a squirrel nurse with reddish-brown fur, wearing a pink nurse uniform and white nurse cap, fluffy bushy tail, small and nimble."

YUANYUAN = "a giant panda (Yuanyuan) with classic black-and-white panda markings, round black ears, signature black eye patches, big round shiny brown eyes, wearing a yellow little dress, chubby and round, about the same size as Bubu."

TEMPLATE = "Pixar 3D animation style, {lighting}, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: {scene}\n\nCHARACTERS: {characters}\n\nThe composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality."

# All pages definition
PAGES = []

# Story 5 - 咘咘学会说你好 (P2-P16, Dad: P2,3,4,5,15, Mom: P12)
s5 = [
    (2, "warm morning sunlight", "A bright sunny forest path. Sam Dad is taking Bubu to a little market in the forest. Dad kneels down asking Bubu what to do when meeting someone. Bubu blinks curiously.", f"{BUBU}; {SAM_DAD}"),
    (3, "warm golden sunlight", "Forest path. Sam Dad smiling warmly, explaining to Bubu that she should smile and say 'hello' when meeting someone. Bubu listens attentively looking up at Dad.", f"{BUBU}; {SAM_DAD}"),
    (4, "dappled forest light", "Forest roadside with berry bushes. Doudou the hedgehog picks berries. Bubu hides shyly behind Sam Dad, peeking out. Dad gently encourages her.", f"{BUBU}; {SAM_DAD}; {DOUDOU}"),
    (5, "warm dappled sunlight", "Forest path. Sam Dad gently nudges Bubu forward. Bubu shyly whispers hello to Doudou who is nearby. A tentative first greeting.", f"{BUBU}; {SAM_DAD}; {DOUDOU}"),
    (6, "bright cheerful daylight", "Forest roadside. Doudou happily turns around smiling at Bubu, offering her a plump red berry. Bubu reaches out to take it, both smiling.", f"{BUBU}; {DOUDOU}"),
    (7, "bright sunny light", "Forest path. Bubu hopping along happily by herself, feeling confident after making a friend. Birds in trees, flowers along the path. Joyful bouncy energy.", f"{BUBU}"),
    (8, "sparkling river light", "A peaceful riverbank. Manman the turtle basks in sunshine on a rock. Bubu confidently calls out hello to Manman, waving enthusiastically. No shyness this time.", f"{BUBU}; {MANMAN}"),
    (9, "warm golden river light", "Riverbank. Manman slowly raises head with a big smile, inviting Bubu to bask in the sun together. Both look happy and friendly.", f"{BUBU}; {MANMAN}"),
    (10, "lively market light", "A bustling forest market with stalls and lanterns. Bubu greets a large friendly brown bear (Uncle Bear) selling honey jars at his stall. Bubu waves and smiles.", f"{BUBU}; a large friendly brown bear (Uncle Bear) wearing an apron, standing behind a market stall with honey jars, warm smile"),
    (11, "warm market glow", "Forest market. Uncle Bear laughs heartily and hands Bubu a small jar of golden honey. Bubu receives it with delight.", f"{BUBU}; a large friendly brown bear (Uncle Bear) wearing an apron, laughing, handing a small honey jar"),
    (12, "soft warm market light", "Forest market flower stall. A rabbit mama (Tina Mom) sells beautiful flowers. Bubu admires the flowers and receives a small daisy. Both smile warmly.", f"{BUBU}; {TINA_MOM} — here acting as a flower seller at the market stall with bouquets of colorful flowers"),
    (13, "warm afternoon light", "Forest market. NOMI is at a workbench fixing something with her nimble paws. Bubu runs over to greet her. NOMI looks up and smiles proudly at how polite Bubu is.", f"{BUBU}; {NOMI}"),
    (14, "bright blue sky light", "Open sky above the market. NONO flies down from the sky toward Bubu, laughing. Bubu looks up happily. Blue sky with fluffy clouds.", f"{BUBU}; {NONO}"),
    (15, "golden sunset light", "A forest path at sunset. Bubu walks home with Sam Dad, her little hands full of berries, a honey jar, and a daisy. Dad asks if she had fun. Bubu nods enthusiastically. Warm father-daughter moment.", f"{BUBU}; {SAM_DAD}"),
    (16, "warm dreamy glow", "A warm montage-feel scene: Bubu standing in center smiling brightly, surrounded by soft glowing vignettes of her greeting friends today. Warm golden tones, storybook ending feeling.", f"{BUBU}"),
]
for p, light, scene, chars in s5:
    PAGES.append(("story5", p, light, scene, chars))

# Story 6 - 咘咘学会等一等 (P2-P16, Dad: P4,5,7,8,9,10, Mom: P11,12,13)
s6 = [
    (2, "warm kitchen light", "A cozy kitchen. Bubu stands impatiently tugging at her skirt, asking 'is it ready yet?' while looking at the stove. She looks restless and hungry. Warm homey kitchen with pots on stove.", f"{BUBU}"),
    (3, "bright doorway light", "A cottage doorway. Bubu peeks out impatiently, looking down a sunny path, tapping her foot. She's waiting for NOMI to arrive. Sunny day outside.", f"{BUBU}"),
    (4, "calm morning river light", "A peaceful riverbank. Sam Dad and Bubu sit together with fishing rods by a calm river. Dad looks calm and patient, Bubu looks excited and eager.", f"{BUBU}; {SAM_DAD}"),
    (5, "soft river light", "Riverbank. Bubu stands up impatiently leaning over the water to check the fishing line. Sam Dad gently gestures for her to sit down. Fish shadows visible under water.", f"{BUBU}; {SAM_DAD}"),
    (6, "dreamy afternoon light", "Riverbank. Bubu sits holding fishing rod lazily, looking up at fluffy clouds in a beautiful sky. Peaceful dreamy scene.", f"{BUBU}"),
    (7, "warm golden afternoon", "Riverbank. Sam Dad and Bubu both looking up at the sky, pointing at clouds. One cloud shaped like a bunny, another like a fish. Joyful bonding moment.", f"{BUBU}; {SAM_DAD}"),
    (8, "exciting golden light", "Riverbank. Bubu excitedly points at her fishing rod which is bending with a fish pulling. Eyes wide with excitement. Sam Dad smiling beside her. River splashing.", f"{BUBU}; {SAM_DAD}"),
    (9, "triumphant golden light", "Riverbank. Sam Dad helps Bubu pull up the fishing rod with a shiny silver fish on the line. Water splashing, both overjoyed. Golden river light.", f"{BUBU}; {SAM_DAD}"),
    (10, "warm sunset river light", "Riverbank at sunset. Sam Dad kneels next to proud Bubu who holds a small bucket with a silver fish. Dad explains the lesson about patience wisely.", f"{BUBU}; {SAM_DAD}"),
    (11, "warm kitchen glow", "Cozy kitchen. Tina Mom puts a cake in the oven. Bubu watches, mouth open about to complain but stopping herself, remembering the fishing lesson. A small thought bubble with a fish.", f"{BUBU}; {TINA_MOM}"),
    (12, "cozy kitchen light", "Kitchen. Bubu sits patiently on a small stool, drawing with crayons on paper. Tina Mom checks the oven in the background. Peaceful patient scene.", f"{BUBU}; {TINA_MOM}"),
    (13, "warm golden kitchen light", "Kitchen. Tina Mom takes a golden brown cake out of the oven, delicious steam rising. Bubu claps her hands excitedly. Warm celebration moment.", f"{BUBU}; {TINA_MOM}"),
    (14, "starlit night", "Outside a cozy cottage at night. Bubu stands peacefully looking up at a beautiful starry sky, waiting calmly. A small path leads to the cottage. Serene nighttime.", f"{BUBU}"),
    (15, "warm starlit night", "Under a starry night sky outside the cottage. NOMI in blue striped sweater runs up apologetically. Bubu smiles calmly and points up at the stars. Warm friendship.", f"{BUBU}; {NOMI}"),
    (16, "warm dreamy golden glow", "A dreamy montage scene: Bubu in center smiling, surrounded by soft vignettes of fishing patiently, waiting for cake, watching stars. 'Good things are worth waiting for' feeling. Storybook ending.", f"{BUBU}"),
]
for p, light, scene, chars in s6:
    PAGES.append(("story6", p, light, scene, chars))

# Story 7 - 猪猪不怕打针 (P2-P17, Dad: none, Mom: P3,4)
s7 = [
    (2, "warm sunny meadow light", "A green meadow with flowers. Bubu and Zhuzhu play together on the grass, laughing. Zhuzhu's wool is soft like a cloud. Sunny happy day.", f"{BUBU}; {ZHUZHU}"),
    (3, "warm indoor light", "Cozy home interior. Zhuzhu looks unwell with a red nose, sneezing. A sheep mother (white wool, gentle, wearing a cream cardigan) feels Zhuzhu's forehead with concern. Warm soft lighting.", f"{ZHUZHU}; a sheep mother with white wool, gentle expression, wearing a cream cardigan, feeling her child's forehead with concern"),
    (4, "soft worried light", "Home interior. Zhuzhu hides behind his sheep mother looking scared and worried. A thought bubble shows a scary imagined hospital. Nervous expression.", f"{ZHUZHU}; a sheep mother with white wool, gentle expression, wearing a cream cardigan"),
    (5, "bright encouraging light", "Outdoor path. Bubu holds Zhuzhu's hand firmly, looking determined and encouraging. 'Don't be scared, I'll go with you!' Bright outdoor setting, path ahead.", f"{BUBU}; {ZHUZHU}"),
    (6, "bright welcoming sunshine", "A bright, warm, friendly animal hospital exterior. A big tree with colorful lanterns at the entrance. Everything bright and welcoming. Bubu and Zhuzhu arriving, looking around with curiosity. Sunshine, flowers.", f"{BUBU}; {ZHUZHU}"),
    (7, "bright clean hospital light", "Inside the hospital. Dr. Giraffe bends down with a warm smile, holding a stethoscope. Zhuzhu looks up at the tall gentle giraffe doctor. Cheerful hospital with colorful decorations.", f"{ZHUZHU}; {DR_GIRAFFE}"),
    (8, "warm medical room light", "Hospital room. Dr. Giraffe places stethoscope on Zhuzhu's tummy. Zhuzhu flinches slightly at the cool touch but starts relaxing. Bubu watches nearby encouragingly.", f"{BUBU}; {ZHUZHU}; {DR_GIRAFFE}"),
    (9, "gentle hospital light", "Hospital room. Dr. Giraffe explains kindly that Zhuzhu needs a shot. Zhuzhu looks worried. Doctor holds up a tiny syringe showing it's small. Reassuring atmosphere.", f"{ZHUZHU}; {DR_GIRAFFE}"),
    (10, "soft emotional light", "Close-up of Zhuzhu with teary red eyes, looking scared. Small voice asking 'will it hurt?' Emotional sympathetic scene.", f"{ZHUZHU}"),
    (11, "warm encouraging light", "Hospital room. Bubu grips Zhuzhu's hand tightly, looking into his eyes with a brave encouraging smile. 'Look at me! Let's count 1, 2, 3 together!' Friendship and courage.", f"{BUBU}; {ZHUZHU}"),
    (12, "bright hospital light", "The shot moment. A squirrel nurse gently wipes Zhuzhu's arm. Bubu and Zhuzhu count together '1, 2, 3!' with determined brave expressions. Quick moment, not scary.", f"{BUBU}; {ZHUZHU}; {NURSE_SQUIRREL}"),
    (13, "sparkling relief light", "Hospital room. Zhuzhu looks at a star-shaped bandaid on his arm with wonder and delight. The squirrel nurse smiles. It's done! Relief and happiness. Sparkle effect around the star.", f"{ZHUZHU}; {NURSE_SQUIRREL}"),
    (14, "cheerful bright light", "Hospital corridor. Zhuzhu laughs happily, proudly showing his star bandaid arm to Bubu. Both smiling brightly. 'It wasn't scary at all!'", f"{BUBU}; {ZHUZHU}"),
    (15, "warm proud light", "Hospital. Dr. Giraffe pats Zhuzhu's head gently, praising his bravery. Zhuzhu beams with pride. Bubu claps beside them.", f"{BUBU}; {ZHUZHU}; {DR_GIRAFFE}"),
    (16, "golden sunset light", "A sunset path home. Zhuzhu bounces happily alongside Bubu. 'We're the brave team!' Golden light, trees and flowers along the road. Happy confident mood.", f"{BUBU}; {ZHUZHU}"),
    (17, "warm dreamy glow", "Dreamy ending scene. Zhuzhu and Bubu showing their star bandaids like medals, standing proudly. A friendly hospital with a rainbow in the background. Warm uplifting storybook ending.", f"{BUBU}; {ZHUZHU}"),
]
for p, light, scene, chars in s7:
    PAGES.append(("story7", p, light, scene, chars))

# Story 8 - 咘咘坐飞机 (P2-P11, Dad: P2,10,11, Mom: P2,3,4,5,6,7,11)
s8 = [
    (2, "warm morning light", "A cozy home interior in the morning. Bubu jumps with excitement wearing a small backpack. Tina Mom smiles beside her holding suitcases. Sam Dad waves goodbye from the doorway. Through the window, a bright sunny day.", f"{BUBU}; {TINA_MOM}; {SAM_DAD}"),
    (3, "bright airport light", "A huge bustling airport terminal with high ceilings and many animal passengers. Bubu holds tightly onto Tina Mom's hand, eyes wide with wonder at the enormous space. Long queues, departure boards.", f"{BUBU}; {TINA_MOM}"),
    (4, "warm airport light", "Airport check-in counter. Tina Mom hands a boarding pass to Bubu. Bubu hugs the boarding pass to her chest proudly, looking very grown-up.", f"{BUBU}; {TINA_MOM}"),
    (5, "warm cabin light", "Inside airplane cabin. Bubu touches the soft airplane seat curiously, looking at the round window with wonder. Tina Mom sits in the next seat smiling. Rows of seats.", f"{BUBU}; {TINA_MOM}"),
    (6, "dramatic takeoff light", "Inside airplane during takeoff. Bubu grips Tina Mom's hand tightly, her tummy feeling ticklish, giggling with excitement and nervousness. Motion blur outside the window.", f"{BUBU}; {TINA_MOM}"),
    (7, "magical golden sunlight through clouds", "Bubu pressing her face against the airplane window, looking down at tiny houses like building blocks and a river like a ribbon far below. Fluffy clouds beside the window. Tina Mom leans over to look too. Magical aerial view.", f"{BUBU}; {TINA_MOM}"),
    (8, "warm cabin glow", "Inside airplane. A kind deer flight attendant in uniform brings a tray with juice and cookies to Bubu. Bubu says thank you politely. Warm cabin scene.", f"{BUBU}; a kind female deer flight attendant in airline uniform with a serving tray"),
    (9, "bright landing light", "Inside airplane during landing. Bubu claps her little hands with joy, looking out the window at the runway. Expression of triumph and pride. Bright scene.", f"{BUBU}"),
    (10, "golden sunset light", "Emotional reunion outside airport exit. Sam Dad with open arms as Bubu runs and leaps toward him. Dad catching and hugging Bubu, kissing her forehead. Tina Mom walks behind with luggage smiling. Sunset golden light. Heartwarming.", f"{BUBU}; {SAM_DAD}; {TINA_MOM}"),
    (11, "warm moonlight and lamplight", "Cozy nighttime bedroom scene. Bubu in pajamas in bed, looking out window at starry sky with an airplane silhouette. A toy airplane on nightstand. Sam Dad and Tina Mom tucking her in together. Dreamy peaceful.", f"{BUBU}; {SAM_DAD}; {TINA_MOM}"),
]
for p, light, scene, chars in s8:
    PAGES.append(("story8", p, light, scene, chars))

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
            req = urllib.request.Request(url, data=body, headers=headers)
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())
            b64 = data["data"][0]["b64_json"]
            png_path = output_path.replace(".jpg", ".png")
            with open(png_path, "wb") as f:
                f.write(base64.b64decode(b64))
            # Convert to JPG
            subprocess.run(["ffmpeg", "-y", "-i", png_path, "-q:v", "2", output_path],
                          capture_output=True, check=True)
            os.remove(png_path)
            size_kb = os.path.getsize(output_path) / 1024
            return size_kb
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                print(f"  429 rate limit, waiting 45s... (attempt {attempt+1})")
                time.sleep(45)
            else:
                raise
    return 0

def main():
    # Check for resume point
    start_idx = 0
    if len(sys.argv) > 1:
        start_idx = int(sys.argv[1])
        print(f"Resuming from index {start_idx}")

    total = len(PAGES)
    print(f"Total pages to generate: {total}")

    results = []
    for i, (story, page, lighting, scene, characters) in enumerate(PAGES):
        if i < start_idx:
            continue

        output_path = os.path.join(OUTPUT_BASE, story, f"page-{page:02d}.jpg")

        # Skip if already exists
        if os.path.exists(output_path):
            size_kb = os.path.getsize(output_path) / 1024
            print(f"[{i+1}/{total}] {story}/page-{page:02d}.jpg SKIP (exists, {size_kb:.0f}KB)")
            results.append((story, page, size_kb, "skipped"))
            continue

        prompt = TEMPLATE.format(lighting=lighting, scene=scene, characters=characters)
        print(f"[{i+1}/{total}] Generating {story}/page-{page:02d}.jpg ...")

        try:
            size_kb = generate_image(prompt, output_path)
            print(f"  ✅ {size_kb:.0f}KB")
            results.append((story, page, size_kb, "ok"))
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            results.append((story, page, 0, f"error: {e}"))

        # Wait between requests
        if i < total - 1:
            time.sleep(8)

    # Summary
    print("\n" + "="*60)
    print("GENERATION SUMMARY")
    print("="*60)
    for story, page, size_kb, status in results:
        flag = ""
        # Mark dad/mom pages
        dad_pages = {
            "story5": [2,3,4,5,15],
            "story6": [4,5,7,8,9,10],
            "story8": [2,10,11],
        }
        mom_pages = {
            "story5": [12],
            "story6": [11,12,13],
            "story7": [3,4],
            "story8": [2,3,4,5,6,7,11],
        }
        if page in dad_pages.get(story, []):
            flag += " 🐕Dad"
        if page in mom_pages.get(story, []):
            flag += " 🐄Mom"
        print(f"  {story}/page-{page:02d}.jpg  {size_kb:6.0f}KB  {status}{flag}")

    ok = sum(1 for _,_,_,s in results if s in ("ok","skipped"))
    err = sum(1 for _,_,_,s in results if s.startswith("error"))
    print(f"\nTotal: {ok} ok, {err} errors out of {len(results)}")

if __name__ == "__main__":
    main()
