#!/usr/bin/env python3
"""Generate all 55 illustrations for Stories 14-18 (Book 4)."""

import json, os, sys, time, base64, subprocess, urllib.request, urllib.error

# Load API config
with open(os.path.expanduser("~/.config/azure-openai/config.json")) as f:
    cfg = json.load(f)

ENDPOINT = cfg["image2_eastus2_endpoint"]
API_KEY = cfg["image2_eastus2_api_key"]
API_VERSION = "2025-04-01-preview"
OUTPUT_BASE = os.path.expanduser("~/.openclaw/workspace/bubu-stories/print-edition")

# Character prompts
BUBU = "a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow. She has a small pink bow centered ON TOP OF HER HEAD between her two ears (not on left ear, not on right ear, not behind — exactly centered on top between the ears). She has a toddler-like round body proportion."

SAM_DAD = "Sam Dad who is a GOLDEN RETRIEVER DOG (NOT a human, NOT a person — he is an ANIMAL, a large golden-furred dog walking upright). He has warm golden fur all over his body, a dog snout/muzzle, floppy dog ears, and a wagging tail. He wears a dark navy jacket over a simple shirt. He has a warm gentle dog smile. IMPORTANT: Sam Dad must look like a golden retriever dog, not a human man."

TINA_MOM = "Tina Mom who is a BLACK-AND-WHITE COW (NOT a human, NOT a person — she is an ANIMAL, a cow walking upright). She has black and white spotted fur pattern all over, small curved horns, cow ears, and hooves. She wears an elegant cream knit cardigan over a floral skirt. She has a gentle warm cow smile. IMPORTANT: Tina Mom must look like a cow, not a human woman."

NOMI = "a raccoon (NOMI) with grey-brown fur, distinctive black eye mask markings, and a ringed bushy tail. She wears a blue-and-white horizontally striped sweater. She has clever bright eyes and nimble paws."

NONO = "a small red bird (NONO) with bright red feathers all over, round bright eyes, and an orange-yellow beak. He has exactly TWO wings and TWO small bird feet with talons. NO ARMS, NO HANDS — birds do not have arms or hands, only wings."

# All pages to generate: (story, page, scene, characters_list, lighting)
PAGES = []

# Story 14: 咘咘和爸爸妈妈一起做咖啡
# Dad pages: 3,4,5,8,9,11,12  Mom pages: 6,7,11,12
s14 = [
    (14, 2, "Early morning, a cozy kitchen with warm sunlight streaming through the window. Bubu is rubbing her eyes sleepily, walking toward the kitchen following a delicious smell. The kitchen has a warm, homey atmosphere with coffee-related items visible.", [BUBU], "warm golden morning light streaming through kitchen window"),
    (14, 3, "In a bright kitchen, Dad (golden retriever) is pouring coffee beans into a hand grinder on the counter. Bubu stands nearby watching curiously. The grinder is making grinding sounds.", [BUBU, SAM_DAD], "warm morning kitchen light"),
    (14, 4, "Close-up scene: Bubu runs up to Dad (golden retriever) curiously, looking up at him. Dad is holding coffee beans. Bubu looks excited and curious about the aromatic beans.", [BUBU, SAM_DAD], "warm indoor morning light"),
    (14, 5, "Dad (golden retriever) is smiling and holding out a handful of coffee beans for Bubu to smell. Bubu leans in close with her little nose, sniffing happily. A warm father-daughter moment.", [BUBU, SAM_DAD], "soft warm morning light"),
    (14, 6, "Mom (cow) is placing a kettle on the stove in the kitchen. The water is starting to boil with steam and bubbles rising. The kitchen scene is warm and cozy.", [BUBU, TINA_MOM], "warm kitchen light with steam effects"),
    (14, 7, "Bubu is reaching her small hand toward the hot kettle on the stove. Mom (cow) is gently holding Bubu's hand back with a caring, protective expression. A teaching moment about safety.", [BUBU, TINA_MOM], "warm kitchen light"),
    (14, 8, "Dad (golden retriever) is kneeling down to Bubu's eye level, explaining something gently. Bubu is listening attentively. They are a few steps back from the kitchen counter.", [BUBU, SAM_DAD], "soft warm indoor light"),
    (14, 9, "Dad (golden retriever) is carefully pouring hot water from a kettle over coffee grounds in a pour-over dripper. The coffee grounds are blooming and puffing up like a small hill. Bubu watches from a safe distance, fascinated.", [BUBU, SAM_DAD], "warm morning light with steam"),
    (14, 10, "Bubu standing a few steps away from the counter, scrunching her little nose and taking a big sniff of the coffee aroma filling the air. She looks delighted. Coffee brewing setup visible in background.", [BUBU], "warm golden morning light"),
    (14, 11, "Dad (golden retriever) is pouring freshly brewed coffee into a cup for Mom (cow). Mom takes a sip and looks delighted. Bubu watches happily. A warm family moment in the kitchen.", [BUBU, SAM_DAD, TINA_MOM], "warm morning kitchen light"),
    (14, 12, "A happy family scene: Mom (cow) is praising Bubu, Dad (golden retriever) is smiling proudly. Bubu is beaming with pride, hands clasped together happily. All three are together in the warm kitchen.", [BUBU, SAM_DAD, TINA_MOM], "warm golden morning light"),
]
PAGES.extend(s14)

# Story 15: 咘咘去游乐场
# Dad pages: 2,5,6,9,11
s15 = [
    (15, 2, "A bright sunny day outdoors. Dad (golden retriever) and Bubu are walking out the front door together. Bubu is hopping and bouncing excitedly. Blue sky with fluffy clouds, sunshine everywhere.", [BUBU, SAM_DAD], "bright sunny outdoor daylight"),
    (15, 3, "Bubu is riding a colorful merry-go-round horse at an amusement park. She is laughing joyfully with her mouth wide open. The carousel is colorful with lights and decorations.", [BUBU], "bright colorful amusement park lights"),
    (15, 4, "Bubu is sitting in a small airplane ride at the amusement park, high up in the air. She has her arms spread wide, looking thrilled and free. The ground is visible below.", [BUBU], "bright sunny sky light"),
    (15, 5, "Bubu and Dad (golden retriever) are sitting together in a small colorful train ride. The train is going through a small tunnel. Bubu is waving her hand excitedly.", [BUBU, SAM_DAD], "mixed tunnel and outdoor light"),
    (15, 6, "Bubu and Dad (golden retriever) are looking up at a massive colorful rainbow slide. It is very tall and impressive. Bubu points up at it excitedly. Dad stands beside her.", [BUBU, SAM_DAD], "bright outdoor daylight"),
    (15, 7, "Bubu is standing next to a height measurement sign (120cm mark) beside the big slide. She is on her tippy-toes, stretching as tall as she can, but still a bit too short. A disappointed but determined expression.", [BUBU], "bright outdoor light"),
    (15, 8, "Bubu looking sad with her long floppy ears drooping down. She is standing near the big slide, looking dejected. A melancholy but cute moment.", [BUBU], "softer afternoon light, slightly muted"),
    (15, 9, "Dad (golden retriever) is kneeling down and hugging Bubu warmly. He has a reassuring, loving expression. Bubu is being comforted, starting to look hopeful again.", [BUBU, SAM_DAD], "warm golden afternoon light"),
    (15, 10, "Back at home, dining scene. Bubu has climbed into her high chair and is eating enthusiastically — big bites of rice and vegetables. She looks determined and happy.", [BUBU], "warm indoor dining light"),
    (15, 11, "Bubu has finished eating — her bowl is completely clean and empty. She looks proud. Dad (golden retriever) is giving a thumbs up with a big smile.", [BUBU, SAM_DAD], "warm indoor light"),
    (15, 12, "Bubu is patting her round tummy with one hand and raising her other hand high in the air triumphantly. She has a big determined smile. A motivational, uplifting moment.", [BUBU], "warm golden light, hopeful atmosphere"),
]
PAGES.extend(s15)

# Story 16: 咘咘刷牙亮晶晶
# No dad, no mom
s16 = [
    (16, 2, "Morning scene in a bright bathroom. Sunlight comes through the window. Bubu is rubbing her eyes and yawning big. NOMI (raccoon) walks over carrying a small cup and a toothbrush.", [BUBU, NOMI], "bright morning bathroom light"),
    (16, 3, "Close-up: NOMI (raccoon) is carefully squeezing a tiny pea-sized amount of toothpaste onto a small pink toothbrush. Bubu watches with wide curious eyes. The toothpaste looks like a tiny white pearl.", [BUBU, NOMI], "bright clean bathroom light"),
    (16, 4, "Bubu is standing on a small step stool in front of a bathroom mirror, mouth wide open showing her little white teeth. NONO (red bird) is perched on the faucet, tilting his head curiously.", [BUBU, NONO], "bright bathroom mirror light"),
    (16, 5, "NOMI (raccoon) is demonstrating how to brush teeth, holding a toothbrush and showing the brushing motion. White foam bubbles are appearing. Bubu watches carefully, learning.", [BUBU, NOMI], "bright bathroom light"),
    (16, 6, "Bubu is brushing the right side of her teeth with her little toothbrush, doing back-and-forth motions. NOMI (raccoon) is beside her, clapping her paws happily and encouraging.", [BUBU, NOMI], "bright bathroom light"),
    (16, 7, "Bubu is now brushing the left side of her teeth. NONO (red bird) is standing nearby, his little head swaying left and right following the toothbrush motion, like he's dancing.", [BUBU, NONO], "bright bathroom light"),
    (16, 8, "Bubu has her mouth open wide in an 'eee' shape, brushing her front teeth up and down. She's concentrating hard. Toothpaste foam visible around her mouth.", [BUBU], "bright bathroom light"),
    (16, 9, "NOMI (raccoon) is holding up a small hourglass with sand flowing through it. Bubu is brushing diligently. The hourglass shows the passage of time.", [BUBU, NOMI], "bright bathroom light"),
    (16, 10, "Bubu is leaning over the bathroom sink, spitting out white toothpaste foam — 'ptoo!' NOMI (raccoon) is giving a thumbs up. The sink has foam in it.", [BUBU, NOMI], "bright bathroom light"),
    (16, 11, "Bubu is holding a small cup, cheeks puffed out like a chipmunk as she swishes water around in her mouth — 'gurgle gurgle'. She looks funny and cute with puffy cheeks.", [BUBU], "bright bathroom light"),
    (16, 12, "Bubu is grinning widely at the bathroom mirror, showing off her sparkly clean white teeth that seem to shine like stars. NOMI (raccoon) and NONO (red bird) are visible in the mirror reflection, all smiling together.", [BUBU, NOMI, NONO], "bright sparkling bathroom light with star-like gleams"),
]
PAGES.extend(s16)

# Story 17: 咘咘的午觉超能力
# Mom pages: 2,7
s17 = [
    (17, 2, "Noon time, bright living room with sun overhead visible through windows. Mom (cow) is gently suggesting nap time. Bubu is on the floor building with colorful blocks, shaking her head stubbornly. A half-built block castle is in front of her.", [BUBU, TINA_MOM], "bright noon sunlight"),
    (17, 3, "Bubu is sitting with building blocks, mid-yawn with her mouth wide open. NOMI (raccoon) is laughing and pointing at Bubu's yawn. The block castle is partially built.", [BUBU, NOMI], "warm afternoon indoor light"),
    (17, 4, "Bubu is rubbing her eyes with her small hands while saying she's not sleepy. NONO (red bird) is perched on Bubu's shoulder, tilting his head. Bubu looks drowsy despite protesting.", [BUBU, NONO], "warm afternoon light"),
    (17, 5, "NOMI (raccoon) is holding up an open picture book showing illustrations: on one page a tired child's blocks falling (2 layers), on the other page an energized child's tall castle (5 layers). Bubu is looking at the book with interest.", [BUBU, NOMI], "warm indoor light"),
    (17, 6, "NONO (red bird) is yawning with his little beak open, tucking his head under his wing to sleep. He looks round and fluffy. Bubu is giggling at NONO's cute appearance.", [BUBU, NONO], "warm soft afternoon light"),
    (17, 7, "A cozy bedroom scene. Mom (cow) is pulling curtains closed, creating a warm orange glow in the room. Bubu is on the bed hugging a small bunny-shaped blanket. NOMI (raccoon) is whispering softly nearby.", [BUBU, TINA_MOM, NOMI], "warm orange-tinted light through curtains"),
    (17, 8, "Bubu is lying in her small bed with eyes closed, looking peaceful. NOMI (raccoon) is sitting beside the bed, whispering. Small glowing stars float gently above Bubu in a dreamy atmosphere.", [BUBU, NOMI], "warm dim orange bedroom light with soft star glow"),
    (17, 9, "A magical dream scene: Bubu is bouncing happily on fluffy white clouds in a starry sky. Glowing stars dance around her. Everything is soft, dreamy, and magical. Bubu looks joyful and free.", [BUBU], "magical dreamy starlit glow"),
    (17, 10, "Bubu is waking up in her bed, stretching big with a happy refreshed expression. Golden sunlight streams through the opening curtains. NOMI (raccoon) is smiling nearby.", [BUBU, NOMI], "warm golden afternoon sunlight streaming in"),
    (17, 11, "Bubu is back at the building blocks, energetically and skillfully stacking a tall 5-layer castle. Her hands are steady and fast. She looks triumphant and full of energy.", [BUBU], "bright warm afternoon light"),
    (17, 12, "A happy concluding scene: Bubu is in bed with curtains drawn (warm orange light), hugging her bunny blanket, looking content and ready for nap. Small stars float above. A peaceful, warm ending.", [BUBU], "warm orange glow with soft starlight"),
]
PAGES.extend(s17)

# Story 18: 咘咘坐好吃饭饭
# Mom pages: 2,3,5,10
s18 = [
    (18, 2, "A dining room and living room scene. Mom (cow) is carrying steaming delicious food to the dining table. Bubu is running around the living room — touching the sofa, kicking a ball, being restless and not coming to eat.", [BUBU, TINA_MOM], "warm indoor evening dinner light"),
    (18, 3, "Mom (cow) is chasing after Bubu with a bowl of food, trying to feed her a spoonful. Bubu is running away mid-chew. Rice grains are scattered on the floor and vegetables are on her clothes. NOMI (raccoon) looks at the mess on the floor, frowning.", [BUBU, TINA_MOM, NOMI], "warm indoor light"),
    (18, 4, "NOMI (raccoon) is patting a cute toddler high chair that has a name sticker and bunny sticker on it. NOMI looks excited, presenting the chair as a 'special throne'. Bubu looks curious and interested.", [BUBU, NOMI], "warm indoor light"),
    (18, 5, "Bubu has climbed onto her special high chair (throne). NOMI (raccoon) sits beside her, NONO (red bird) stands on a cup on the table. Mom (cow) is clapping and smiling in the background. All three friends are shouting 'dinner time!' together.", [BUBU, NOMI, NONO, TINA_MOM], "warm dinner table light"),
    (18, 6, "Bubu is sitting properly in her high chair, using a small spoon to eat rice. The spoonful goes perfectly into her mouth. She looks focused and happy. NONO (red bird) is watching approvingly.", [BUBU, NONO], "warm dinner light"),
    (18, 7, "Bubu is chewing a piece of carrot slowly with a surprised, delighted expression — discovering it's sweet! NOMI (raccoon) is beside her, smiling knowingly.", [BUBU, NOMI], "warm dinner table light"),
    (18, 8, "NOMI (raccoon) places a small hourglass on the dining table. Bubu's eyes go wide with excitement, picking up her spoon determinedly. Food is on the table.", [BUBU, NOMI], "warm indoor dinner light"),
    (18, 9, "Bubu is eating enthusiastically, bowl nearly empty. Vegetables gone, carrots gone, rice almost finished. She glances at the hourglass which still has lots of sand. She looks proud of being fast.", [BUBU], "warm dinner light"),
    (18, 10, "Bubu is holding up her completely empty, clean bowl triumphantly. Mom (cow) is giving a thumbs up. NONO (red bird) is flapping his wings like clapping. Everyone looks happy and proud.", [BUBU, TINA_MOM, NONO], "warm celebratory dinner light"),
    (18, 11, "After dinner scene in the living room. Bubu is energetically building blocks — a 3-layer tower. She looks full of energy and happy, patting her full tummy with one hand.", [BUBU], "warm evening indoor light"),
    (18, 12, "A happy concluding scene: Bubu is sitting in her special throne/high chair at the dining table, looking content. A clean sparkly empty bowl in front of her. She's smiling proudly. NOMI (raccoon) and NONO (red bird) are beside her.", [BUBU, NOMI, NONO], "warm golden dinner light"),
]
PAGES.extend(s18)


def generate_image(prompt, output_path, retries=3):
    """Call Azure OpenAI image generation API."""
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
    
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read())
            
            b64 = result["data"][0]["b64_json"]
            png_path = output_path.replace(".jpg", ".png")
            with open(png_path, "wb") as f:
                f.write(base64.b64decode(b64))
            
            # Convert to JPG
            subprocess.run([
                "ffmpeg", "-y", "-i", png_path, "-q:v", "2", output_path
            ], capture_output=True, check=True)
            os.remove(png_path)
            
            size = os.path.getsize(output_path)
            return size
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 45
                print(f"  429 rate limit, waiting {wait}s (attempt {attempt+1}/{retries})")
                time.sleep(wait)
            else:
                body_text = e.read().decode() if e.fp else ""
                print(f"  HTTP {e.code}: {body_text[:200]}")
                if attempt < retries - 1:
                    time.sleep(15)
                else:
                    raise
        except Exception as e:
            print(f"  Error: {e}")
            if attempt < retries - 1:
                time.sleep(15)
            else:
                raise
    return 0


def build_prompt(scene, characters, lighting):
    chars = "\n".join([f"- {c}" for c in characters])
    return f"""Pixar 3D animation style, {lighting}, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.

SCENE: {scene}

CHARACTERS:
{chars}

The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality."""


# Track progress
start_idx = 0
# Check for resume
if os.path.exists(f"{OUTPUT_BASE}/progress.txt"):
    with open(f"{OUTPUT_BASE}/progress.txt") as f:
        start_idx = int(f.read().strip())
    print(f"Resuming from index {start_idx}")

total = len(PAGES)
print(f"Total pages to generate: {total}")

for i, (story, page, scene, chars, lighting) in enumerate(PAGES):
    if i < start_idx:
        continue
    
    output_path = f"{OUTPUT_BASE}/story{story}/page-{page:02d}.jpg"
    
    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print(f"[{i+1}/{total}] story{story}/page-{page:02d}.jpg EXISTS ({size:,} bytes)")
        continue
    
    prompt = build_prompt(scene, chars, lighting)
    print(f"[{i+1}/{total}] Generating story{story}/page-{page:02d}.jpg ...", flush=True)
    
    size = generate_image(prompt, output_path)
    print(f"  → {size:,} bytes")
    
    # Save progress
    with open(f"{OUTPUT_BASE}/progress.txt", "w") as f:
        f.write(str(i + 1))
    
    if i < total - 1:
        time.sleep(8)

print("\n✅ All done!")
