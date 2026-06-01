#!/usr/bin/env python3
"""Generate all illustrations for Stories 32-37 (Print Edition Volume 7)."""

import json, os, time, sys, base64, subprocess
import urllib.request, urllib.error

# API config
cfg = json.load(open(os.path.expanduser("~/.config/azure-openai/config.json")))
ENDPOINT = cfg["image2_eastus2_endpoint"].rstrip("/")
API_KEY = cfg["image2_eastus2_api_key"]
API_VERSION = "2025-04-01-preview"

# Character prompts
BUBU = "a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow. She has a small pink bow centered ON TOP OF HER HEAD between her two ears (not on left ear, not on right ear, not behind — exactly centered on top between the ears). She has a toddler-like round body proportion."

SAM_DAD = "Sam Dad who is a GOLDEN RETRIEVER DOG (NOT a human, NOT a person — he is an ANIMAL, a large golden-furred dog walking upright). He has warm golden fur all over his body, a dog snout/muzzle, floppy dog ears, and a wagging tail. He wears a dark navy jacket over a simple shirt. He has a warm gentle dog smile. IMPORTANT: Sam Dad must look like a golden retriever dog, not a human man."

TINA_MOM = "Tina Mom who is a BLACK-AND-WHITE COW (NOT a human, NOT a person — she is an ANIMAL, a cow walking upright). She has black and white spotted fur pattern all over, small curved horns, cow ears, and hooves. She wears an elegant cream knit cardigan over a floral skirt. She has a gentle warm cow smile. IMPORTANT: Tina Mom must look like a cow, not a human woman."

NOMI = "a raccoon (NOMI) with grey-brown fur, distinctive black eye mask markings, and a ringed bushy tail. She wears a blue-and-white horizontally striped sweater. She has clever bright eyes and nimble paws."

NONO = "a small red bird (NONO) with bright red feathers all over, round bright eyes, and an orange-yellow beak. He has exactly TWO wings and TWO small bird feet with talons. NO ARMS, NO HANDS — birds do not have arms or hands, only wings."

COCO = "a red panda (Coco) with reddish-brown fur, round face with white markings, big round shiny eyes, a bushy ringed tail, and wearing a small yellow scarf. She is slightly bigger than Bubu."

WAIPO = "Grandma (Waipo) who is a GOAT with light grey-white fur, small curved goat horns, warm brown eyes, short goat beard. She wears a floral blouse with light casual pants and a sun hat. She has a warm grandmotherly smile."

WAIGONG = "Grandpa (Waigong) who is a HORSE with dark brown fur, grey-white mane showing age, steady dark eyes. He wears a polo shirt with casual pants and a simple watch. He is tall and dignified."

STYLE_PREFIX = "Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition (1024x1536). Pure illustration with NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS anywhere in the image."
STYLE_SUFFIX = "The bottom 20% of the image gradually darkens naturally into a soft warm shadow/vignette. Natural composition, no forced blank spaces."

# All 68 pages
PAGES = []

# Story 32: 咘咘学说Hello (P2-P12 = pages[1]-pages[11])
s32 = [
    (2, f"{STYLE_PREFIX} A beautiful spring park with cherry blossoms and green grass. {BUBU} is walking happily holding hands with {NOMI}. {NONO} is perched on NOMI's head. Butterflies flutter around them. Warm spring sunshine. {STYLE_SUFFIX}"),
    (3, f"{STYLE_PREFIX} In a spring park, {COCO} runs up to {BUBU} with a friendly wave. Bubu looks surprised and curious, tilting her head. {NOMI} stands beside Bubu watching. Cherry blossom petals fall gently. {STYLE_SUFFIX}"),
    (4, f"{STYLE_PREFIX} {NOMI} crouches down next to {BUBU}, gently explaining something with a warm smile. Bubu listens attentively with curious big eyes. {COCO} stands nearby waiting patiently. Spring park background with flowers. {STYLE_SUFFIX}"),
    (5, f"{STYLE_PREFIX} {BUBU} bravely speaks to {COCO}, looking a bit shy but determined. Coco smiles happily back at her. They are becoming friends. {NOMI} watches proudly from behind. Spring park with warm sunlight. {STYLE_SUFFIX}"),
    (6, f"{STYLE_PREFIX} {COCO} offers a pretty little flower to {BUBU}. Bubu reaches out to take it with delight. {NOMI} leans in and whispers a reminder to Bubu. Colorful spring flowers in the background. {STYLE_SUFFIX}"),
    (7, f"{STYLE_PREFIX} {BUBU} happily holds the flower and speaks cheerfully. {COCO} claps her paws happily. Both are smiling brightly. {NOMI} and {NONO} watch with warm smiles. Spring park setting. {STYLE_SUFFIX}"),
    (8, f"{STYLE_PREFIX} {TINA_MOM} arrives at the park to pick up Bubu. {BUBU} runs towards her mom with arms open. {NOMI} stands nearby smiling. {COCO} and {NONO} watch. Warm afternoon light in the spring park. {STYLE_SUFFIX}"),
    (9, f"{STYLE_PREFIX} {BUBU} hugs {TINA_MOM} tightly, nuzzling into her. Mom is moved, kissing Bubu's forehead tenderly. Warm golden afternoon light. {NOMI} and {NONO} stand nearby, touched by the scene. Spring park. {STYLE_SUFFIX}"),
    (10, f"{STYLE_PREFIX} {BUBU} runs back to {COCO} and waves goodbye. Coco waves back with a warm smile. {NOMI} teaches Bubu, gesturing. The setting sun casts golden light. Spring park. {STYLE_SUFFIX}"),
    (11, f"{STYLE_PREFIX} {BUBU} walks on a path going home, happily reciting words she learned. {NONO} flies around her head cheerfully. {TINA_MOM} walks beside her smiling. {NOMI} walks alongside. Beautiful spring sunset, cherry blossom petals on the path. {STYLE_SUFFIX}"),
    (12, f"{STYLE_PREFIX} {BUBU} sits on her bed at home in pajamas, hugging a stuffed toy, looking thoughtful and happy. She imagines playing with {COCO} again tomorrow. Warm bedroom with a nightlight. Dreamy atmosphere. {NOMI} sits beside the bed. {STYLE_SUFFIX}"),
]
for p, prompt in s32:
    PAGES.append(("story32", p, prompt))

# Story 33: 咘咘的科技馆大冒险 (P2-P9 = pages[1]-pages[8])
s33 = [
    (2, f"{STYLE_PREFIX} Outside a grand, colorful science museum entrance. {SAM_DAD} holds {BUBU}'s hand. {COCO} waves excitedly at the entrance. The building has a futuristic dome shape with bright colors. Spring day. {STYLE_SUFFIX}"),
    (3, f"{STYLE_PREFIX} Inside a science museum, a rolling ball exhibit with ramps and tracks. {BUBU} watches in amazement as colorful balls roll down slopes. {COCO} stands next to her pointing at the balls. {SAM_DAD} watches from behind. Bright interior lighting. {STYLE_SUFFIX}"),
    (4, f"{STYLE_PREFIX} {BUBU} and {COCO} at a magnet exhibit in a science museum. They hold colorful horseshoe magnets, trying to push them together. Bubu looks puzzled and curious. Coco flips a magnet and they snap together. Interactive exhibit setting. {STYLE_SUFFIX}"),
    (5, f"{STYLE_PREFIX} {BUBU} and {COCO} stand in front of colorful light projectors, their shadows cast in rainbow colors on a white wall. Bubu giggles seeing her pink shadow. Coco points at her orange shadow. Bright playful museum exhibit. {STYLE_SUFFIX}"),
    (6, f"{STYLE_PREFIX} Inside a science museum, {BUBU} and {COCO} at opposite ends of a speaking tube exhibit — large curved pipes on a wall. Bubu speaks into one end with wide eyes. Coco listens at the other end with excitement. Fun museum interior. {STYLE_SUFFIX}"),
    (7, f"{STYLE_PREFIX} {BUBU} stands inside a giant soap bubble in a museum bubble exhibit. She looks amazed with arms spread. {COCO} watches from outside the bubble with excitement. Iridescent rainbow colors on the bubble surface. Magical lighting. {STYLE_SUFFIX}"),
    (8, f"{STYLE_PREFIX} Outside the science museum at sunset. {BUBU} waves goodbye to {COCO}. {SAM_DAD} stands behind Bubu. Coco waves back warmly. Golden sunset light. Spring flowers near the entrance. {STYLE_SUFFIX}"),
    (9, f"{STYLE_PREFIX} {BUBU}'s bedroom at night. She sits on the floor in pajamas, building a small ball-rolling track with colorful wooden blocks. {NOMI} sits nearby watching with interest. A small nightlight glows warmly. Bubu looks proud and happy. {STYLE_SUFFIX}"),
]
for p, prompt in s33:
    PAGES.append(("story33", p, prompt))

# Story 34: 妈妈生日快乐 (P2-P13 = pages[1]-pages[12])
s34 = [
    (2, f"{STYLE_PREFIX} Early morning in Bubu's bedroom. {SAM_DAD} gently wakes {BUBU} with a finger to his lips (shh gesture). Bubu sits up in bed looking sleepy but curious. {COCO} peeks through the window with an excited expression. Soft morning light streams in. {STYLE_SUFFIX}"),
    (3, f"{STYLE_PREFIX} In a warm kitchen, {BUBU} stands on a stool stirring cake batter in a big bowl, flour on her face. {SAM_DAD} stands behind her helping. {COCO} holds out a strawberry. Baking supplies scattered on the counter. Warm cozy kitchen. {STYLE_SUFFIX}"),
    (4, f"{STYLE_PREFIX} {BUBU} lies on the table drawing a birthday card with crayons. She concentrates hard, tongue sticking out. {COCO} leans over helping guide the writing. Colorful crayons scattered around. Warm lighting. {STYLE_SUFFIX}"),
    (5, f"{STYLE_PREFIX} {SAM_DAD} blows up colorful balloons while {BUBU} hangs streamers on furniture. {COCO} stands on a chair putting paper stars on the wall. The living room is being transformed into a party space. Festive atmosphere. {STYLE_SUFFIX}"),
    (6, f"{STYLE_PREFIX} {TINA_MOM} opens the front door and sees the decorated room. {BUBU}, {SAM_DAD}, and {COCO} shout surprise together with arms raised. Mom covers her mouth with hooves, eyes sparkling with joy and tears. Colorful balloons and streamers everywhere. {STYLE_SUFFIX}"),
    (7, f"{STYLE_PREFIX} A beautiful birthday cake with colorful candles on a table. {BUBU} helps count the candles, pointing at each one. {COCO} stands beside her. {SAM_DAD} and {TINA_MOM} watch warmly. Festive living room. {STYLE_SUFFIX}"),
    (8, f"{STYLE_PREFIX} All candles are lit on the cake, glowing beautifully. {BUBU}, {SAM_DAD}, {COCO}, {NOMI}, and {NONO} gather around the cake singing. {TINA_MOM} sits behind the cake, touched and happy. Warm candlelight illuminates their faces. {STYLE_SUFFIX}"),
    (9, f"{STYLE_PREFIX} {TINA_MOM} closes her eyes with hooves together, making a wish over the birthday cake. {BUBU} watches quietly with wonder. The candle glow is warm and magical. Everyone is silent and respectful. Intimate atmosphere. {STYLE_SUFFIX}"),
    (10, f"{STYLE_PREFIX} {TINA_MOM} blows out all the candles on the cake in one breath! {BUBU} claps and cheers excitedly. {COCO} jumps with joy. {SAM_DAD} smiles proudly. Wisps of candle smoke curl upward. Festive moment. {STYLE_SUFFIX}"),
    (11, f"{STYLE_PREFIX} {SAM_DAD} cuts the birthday cake. {BUBU} carefully carries the first slice to {TINA_MOM} with both paws. Mom is deeply moved, bending down to kiss Bubu. Warm family scene. {STYLE_SUFFIX}"),
    (12, f"{STYLE_PREFIX} Everyone happily eating cake around the table. {BUBU} has cream all over her nose and cheeks, looking adorable and clueless. {COCO} laughs pointing at Bubu's creamy face. {SAM_DAD} and {TINA_MOM} laugh warmly. Festive party scene. {STYLE_SUFFIX}"),
    (13, f"{STYLE_PREFIX} Bedtime scene. {BUBU} hugs {TINA_MOM} tightly on the bed. {COCO} sits beside them smiling softly. Warm bedroom with soft nightlight glow. Bubu looks up at Mom with pure love. Tender, emotional moment. {STYLE_SUFFIX}"),
]
for p, prompt in s34:
    PAGES.append(("story34", p, prompt))

# Story 35: 咘咘说话算数 (P2-P14 = pages[1]-pages[13])
s35 = [
    (2, f"{STYLE_PREFIX} Bedtime in Bubu's cozy bedroom. {SAM_DAD} sits on the bed reading a storybook. {BUBU} sits next to him in pajamas, hugging the book eagerly, wanting more stories. Warm nightlight glow. Stuffed animals on the bed. {STYLE_SUFFIX}"),
    (3, f"{STYLE_PREFIX} {SAM_DAD} points at a clock on the wall with one paw while looking at {BUBU} warmly. He holds up one finger (one more story). Bubu nods eagerly. Cozy bedroom, warm lamp light. {STYLE_SUFFIX}"),
    (4, f"{STYLE_PREFIX} Close-up of {BUBU}'s tiny pink paw and {SAM_DAD}'s large golden paw doing a pinky promise. Both look at each other with warm smiles. Bubu nods seriously. Cozy bedroom background slightly blurred. {STYLE_SUFFIX}"),
    (5, f"{STYLE_PREFIX} {SAM_DAD} finishes reading the story, closing the book. {BUBU} sneakily reaches for another book on the nightstand with a hopeful expression. Cozy bedroom, warm lighting. {STYLE_SUFFIX}"),
    (6, f"{STYLE_PREFIX} {SAM_DAD} gently shakes his head with a kind but firm expression, one paw raised. {BUBU} looks a bit disappointed but understanding. He reminds her of their pinky promise. Warm bedroom. {STYLE_SUFFIX}"),
    (7, f"{STYLE_PREFIX} {BUBU} sits on the bed with a little pout, putting the book back. She looks at her own little pinky finger, remembering the promise. Cute contemplative expression. Soft bedroom lighting. {STYLE_SUFFIX}"),
    (8, f"{STYLE_PREFIX} Next morning, bright and cheerful living room. {NOMI} arrives to play. {BUBU} in a pink dress holds up her pinky to NOMI, proposing a promise. Bright spring sunlight through windows. {STYLE_SUFFIX}"),
    (9, f"{STYLE_PREFIX} {BUBU} and {NOMI} do a pinky promise together — Bubu's small white paw linked with NOMI's grey raccoon paw. Both smile at each other. Cheerful living room, morning light. {STYLE_SUFFIX}"),
    (10, f"{STYLE_PREFIX} {BUBU} and {NOMI} play with colorful building blocks on the floor. Bubu has built a tall tower and looks proud. Blocks scattered around. Bright cheerful room. {STYLE_SUFFIX}"),
    (11, f"{STYLE_PREFIX} {BUBU} looks longingly at the block tower, wanting to keep playing. But she remembers the pinky promise — a small thought bubble or visual hint of the linked pinkies. She hesitates. Bright room. {STYLE_SUFFIX}"),
    (12, f"{STYLE_PREFIX} {BUBU} takes a deep breath, stands up with determination. She looks resolved and proud of herself. {NOMI} looks at her with admiration. Building blocks on the floor. Bright cheerful room. {STYLE_SUFFIX}"),
    (13, f"{STYLE_PREFIX} {NOMI} pats {BUBU} on the head affectionately. Bubu beams with pride. Both look happy. Warm sunlit room. A feeling of accomplishment and growth. {STYLE_SUFFIX}"),
    (14, f"{STYLE_PREFIX} That night, {BUBU} and {SAM_DAD} on the bed again. They do another pinky promise. This time Bubu looks confident and determined. After the story, Bubu closes her eyes peacefully to sleep. Warm cozy bedroom with nightlight. {STYLE_SUFFIX}"),
]
for p, prompt in s35:
    PAGES.append(("story35", p, prompt))

# Story 36: 咘咘送爸爸妈妈上班 (P2-P13 = pages[1]-pages[12])
s36 = [
    (2, f"{STYLE_PREFIX} Spring morning, warm sunlight streams through a bedroom window. {BUBU} opens her eyes in bed and sees {SAM_DAD} and {TINA_MOM} already dressed in nice clothes, ready for work. Cozy bedroom. {STYLE_SUFFIX}"),
    (3, f"{STYLE_PREFIX} {BUBU} rubs her eyes and looks up at {SAM_DAD} and {TINA_MOM} who are dressed for work. Bubu looks confused and a bit worried. Warm bedroom, morning light. {STYLE_SUFFIX}"),
    (4, f"{STYLE_PREFIX} {BUBU}'s lip trembles as she wraps her arms tightly around {SAM_DAD}'s leg, not wanting him to leave. She looks up with pleading eyes. {TINA_MOM} watches with a gentle expression. Warm morning light. {STYLE_SUFFIX}"),
    (5, f"{STYLE_PREFIX} {TINA_MOM} crouches down and hugs {BUBU} warmly. Mom points toward the window where golden sunlight pours in. Bubu looks up at the window. Tender moment, warm morning light. {STYLE_SUFFIX}"),
    (6, f"{STYLE_PREFIX} Through the window, beautiful golden sunshine floods in. {BUBU} and {TINA_MOM} look out the window together at the bright spring sky. The sun appears warm and friendly. A comforting, hopeful scene. {STYLE_SUFFIX}"),
    (7, f"{STYLE_PREFIX} Close-up: {SAM_DAD} gently kisses {BUBU}'s open palm. Bubu watches with wide eyes, fascinated. His golden paw holds her tiny white paw carefully. Warm, intimate moment. Soft focus background. {STYLE_SUFFIX}"),
    (8, f"{STYLE_PREFIX} {BUBU} clenches her little fist tight, looking determined and brave. She tiptoes up to kiss {SAM_DAD} and {TINA_MOM} on their cheeks. Both parents look touched. Warm morning light in the hallway. {STYLE_SUFFIX}"),
    (9, f"{STYLE_PREFIX} {SAM_DAD} and {TINA_MOM} walk out the front door, turning to wave. {BUBU} stands at the doorway waving bravely. {NOMI} stands beside Bubu. {NONO} perches on NOMI's shoulder. Spring morning, trees with new leaves. {STYLE_SUFFIX}"),
    (10, f"{STYLE_PREFIX} {WAIPO} holds {BUBU}'s hand, leading her to a table with art supplies. Bubu draws a picture showing: the sun, her parents at work, and herself waving at home. Crayons and paper everywhere. Warm domestic scene. {STYLE_SUFFIX}"),
    (11, f"{STYLE_PREFIX} Afternoon scene. {BUBU} and {NOMI} build with colorful blocks on the living room floor. {NONO} playfully hops on top of the blocks. {WAIPO} sits in an armchair watching with a warm smile. Bubu builds a castle shape. Bright afternoon light. {STYLE_SUFFIX}"),
    (12, f"{STYLE_PREFIX} The doorbell rings! {BUBU} runs excitedly toward the front door with arms wide open. {SAM_DAD} and {TINA_MOM} are at the door, arms outstretched. Golden evening light. A joyful reunion moment. {STYLE_SUFFIX}"),
    (13, f"{STYLE_PREFIX} The whole family sits together on a cozy sofa. {BUBU} shows {SAM_DAD} and {TINA_MOM} her drawing and block castle. Parents hug her tightly. {NOMI} and {NONO} sit nearby. {WAIPO} watches from an armchair. Warm evening light, family togetherness. {STYLE_SUFFIX}"),
]
for p, prompt in s36:
    PAGES.append(("story36", p, prompt))

# Story 37: 咘咘吃冰淇淋 (P2-P13 = pages[1]-pages[12])
s37 = [
    (2, f"{STYLE_PREFIX} A warm spring afternoon. {BUBU} walks between {SAM_DAD} and {TINA_MOM}, holding their hands. {NOMI} walks alongside carrying a small backpack. {NONO} stands on NOMI's head facing the breeze. A tree-lined path with spring flowers. {STYLE_SUFFIX}"),
    (3, f"{STYLE_PREFIX} A flower-lined path with butterflies fluttering among the blossoms. {BUBU} skips happily, her pink dress flowing like a flower petal. {SAM_DAD} and {TINA_MOM} walk behind her smiling. Spring sunshine. {STYLE_SUFFIX}"),
    (4, f"{STYLE_PREFIX} {BUBU} stops in front of a charming colorful ice cream shop with a bright sign showing various ice cream flavors. Her eyes light up with excitement, ears perked up. She points at the shop eagerly. {SAM_DAD} and {TINA_MOM} smile behind her. {STYLE_SUFFIX}"),
    (5, f"{STYLE_PREFIX} {SAM_DAD} crouches down smiling, patting {BUBU}'s head. Bubu nods eagerly with her ears standing up straight with excitement. The ice cream shop is in the background. Spring day. {STYLE_SUFFIX}"),
    (6, f"{STYLE_PREFIX} {SAM_DAD} holds a magnificent tall ice cream cone with multiple scoops — strawberry pink, chocolate brown, vanilla white — towering like a colorful mountain. {BUBU}, {NOMI}, and {NONO} all stare at it with wide amazed eyes and open mouths. {STYLE_SUFFIX}"),
    (7, f"{STYLE_PREFIX} {TINA_MOM} sits at a park bench, using a spoon to scoop ice cream into five small colorful bowls. A pink bowl for Bubu, blue for NOMI, red for NONO, brown for Dad, white for Mom. {BUBU} watches eagerly. Warm afternoon. {STYLE_SUFFIX}"),
    (8, f"{STYLE_PREFIX} {BUBU} sits holding her pink bowl, carefully taking a spoonful of strawberry ice cream. She closes her eyes in bliss, her little feet swinging happily. Park bench setting, spring afternoon. {STYLE_SUFFIX}"),
    (9, f"{STYLE_PREFIX} The whole family eating ice cream at a park. {SAM_DAD} eats chocolate ice cream happily from a brown bowl. {TINA_MOM} elegantly enjoys vanilla from a white bowl. {NOMI} holds a blue bowl with nimble paws. Everyone looks content. Spring park. {STYLE_SUFFIX}"),
    (10, f"{STYLE_PREFIX} {NONO} stands on the rim of a small red bowl, dipping his beak into the ice cream, then lifting his head up. Adorable and funny pose. Other characters watch and laugh in the background. Park setting. {STYLE_SUFFIX}"),
    (11, f"{STYLE_PREFIX} {BUBU} has a big blob of pink strawberry ice cream on her nose! She tilts her head confused, not knowing why everyone is laughing. {SAM_DAD}, {TINA_MOM}, {NOMI} all laugh warmly around her. Adorable funny moment. Park. {STYLE_SUFFIX}"),
    (12, f"{STYLE_PREFIX} {TINA_MOM} gently wipes the ice cream off {BUBU}'s nose with a tissue, then kisses her forehead. Bubu finally realizes and laughs too, a joyful giggling expression. Warm tender moment. Park bench. {STYLE_SUFFIX}"),
    (13, f"{STYLE_PREFIX} Sunset scene, orange-red sky. The family walks home hand in hand on a path. {BUBU} in the center holding {SAM_DAD}'s hand (left) and {TINA_MOM}'s hand (right). {NOMI} walks beside them. {NONO} perches on Dad's shoulder. Beautiful golden hour light, silhouette-like warmth. {STYLE_SUFFIX}"),
]
for p, prompt in s37:
    PAGES.append(("story37", p, prompt))

print(f"Total pages to generate: {len(PAGES)}")

def generate_image(prompt, output_path, retries=3):
    """Generate image via Azure OpenAI API."""
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
            
            # Convert PNG to JPG with ffmpeg
            subprocess.run(
                ["ffmpeg", "-y", "-i", png_path, "-q:v", "2", output_path],
                capture_output=True, timeout=30
            )
            os.remove(png_path)
            
            size = os.path.getsize(output_path)
            return size
            
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 45
                print(f"  429 rate limit, waiting {wait}s (attempt {attempt+1}/{retries})")
                time.sleep(wait)
            else:
                body_text = e.read().decode() if hasattr(e, 'read') else ''
                print(f"  HTTP {e.code}: {body_text[:200]}")
                if attempt < retries - 1:
                    time.sleep(10)
                else:
                    raise
        except Exception as e:
            print(f"  Error: {e}")
            if attempt < retries - 1:
                time.sleep(10)
            else:
                raise
    return 0

# Check what's already done
start_idx = 0
if len(sys.argv) > 1:
    start_idx = int(sys.argv[1])

base_dir = "bubu-stories/print-edition"
results = []

for idx, (story, page, prompt) in enumerate(PAGES):
    if idx < start_idx:
        continue
    
    output_path = f"{base_dir}/{story}/page-{page:02d}.jpg"
    
    # Skip if already exists
    if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
        size = os.path.getsize(output_path)
        print(f"[{idx+1}/{len(PAGES)}] {story}/page-{page:02d}.jpg EXISTS ({size//1024}KB)")
        results.append((story, page, size))
        continue
    
    print(f"[{idx+1}/{len(PAGES)}] Generating {story}/page-{page:02d}.jpg ...")
    size = generate_image(prompt, output_path)
    print(f"  Done: {size//1024}KB")
    results.append((story, page, size))
    
    # Wait between requests
    if idx < len(PAGES) - 1:
        time.sleep(8)

print("\n=== SUMMARY ===")
for story, page, size in results:
    print(f"  {story}/page-{page:02d}.jpg: {size//1024}KB")
print(f"\nTotal: {len(results)} images")
