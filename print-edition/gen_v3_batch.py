#!/usr/bin/env python3
"""Generate all illustrations for Stories 9-13 (print edition v3)."""

import json, os, sys, time, base64, subprocess, requests
sys.stdout.reconfigure(line_buffering=True)

# Config
API_KEY = "G0XzcVpk6KUGX53HbGfW6nBFiU4yh4Wjfowo8BSseYoSL8HAL9E4JQQJ99CCACHYHv6XJ3w3AAAAACOGJIkM"
ENDPOINT = "https://kaixi-mmimphd8-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-image-2/images/generations"
API_VERSION = "2025-04-01-preview"
OUTPUT_BASE = os.path.dirname(os.path.abspath(__file__))
DELAY = 8
RETRY_WAIT = 45
MAX_RETRIES = 3

# Character prompts
BUBU = "a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow. She has a small pink bow centered ON TOP OF HER HEAD between her two ears (not on left ear, not on right ear, not behind — exactly centered on top between the ears). She has a toddler-like round body proportion."
SAM_DAD = "Sam Dad who is a GOLDEN RETRIEVER DOG (NOT a human, NOT a person — he is an ANIMAL, a large golden-furred dog walking upright). He has warm golden fur all over his body, a dog snout/muzzle, floppy dog ears, and a wagging tail. He wears a dark navy jacket over a simple shirt. He has a warm gentle dog smile. IMPORTANT: Sam Dad must look like a golden retriever dog, not a human man."
TINA_MOM = "Tina Mom who is a BLACK-AND-WHITE COW (NOT a human, NOT a person — she is an ANIMAL, a cow walking upright). She has black and white spotted fur pattern all over, small curved horns, cow ears, and hooves. She wears an elegant cream knit cardigan over a floral skirt. She has a gentle warm cow smile. IMPORTANT: Tina Mom must look like a cow, not a human woman."
NOMI = "a raccoon (NOMI) with grey-brown fur, distinctive black eye mask markings, and a ringed bushy tail. She wears a blue-and-white horizontally striped sweater. She has clever bright eyes and nimble paws."
NONO = "a small red bird (NONO) with bright red feathers all over, round bright eyes, and an orange-yellow beak. He has exactly TWO wings and TWO small bird feet with talons. NO ARMS, NO HANDS — birds do not have arms or hands, only wings."
DOUDOU = "a small hedgehog (Doudou) with a brown body covered in dark brown spines/quills, small round shiny eyes, a tiny nose. He is small, round, and shy-looking."
MANMAN = "a small turtle (Manman) with a green shell with dark green hexagonal patterns, light green skin, small round eyes, and a gentle slow expression."

def make_prompt(scene, characters_desc, lighting="warm soft evening light"):
    chars = "\n".join(f"- {c}" for c in characters_desc)
    return f"""Pixar 3D animation style, {lighting}, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.

SCENE: {scene}

CHARACTERS:
{chars}

The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality."""

# All pages definition: (story, page, scene, [characters], lighting)
PAGES = []

# ===== STORY 9: 咘咘早点睡 =====
s9 = [
    (2, "A moonlit forest clearing at night. The moon hangs above the treetops, casting silvery light. Small forest animals are yawning in the background. Fireflies twinkle softly.", [BUBU], "soft moonlight with warm undertones"),
    (3, "A cozy little burrow entrance in the forest at night. A small hedgehog rubbing his eyes sleepily, about to walk into his tiny hole home. Moonlight filtering through trees.", [DOUDOU], "gentle moonlight"),
    (4, "A small turtle pulling her head into her shell on a mossy log at night. The forest is quiet and peaceful. A few stars visible through the canopy.", [MANMAN], "soft starlight and moonlight"),
    (5, "A small red bird nestled in a cozy nest on a tree branch at night. The bird has tucked his wings over his face like a blanket. Leaves gently surround the nest.", [NONO], "warm moonlight filtering through leaves"),
    (6, "A raccoon in a blue-white striped sweater hugging a white rabbit girl, then turning to walk toward her treehouse home. Night forest, warm lamplight from the treehouse window.", [NOMI, BUBU], "warm lamplight mixed with moonlight"),
    (7, "A white rabbit toddler alone in a moonlit forest clearing, stomping her foot stubbornly, looking a little pouty. All other animals have gone home. The forest is empty and quiet.", [BUBU], "cool moonlight, slightly lonely atmosphere"),
    (8, "A black-and-white cow mother gently holding the hand of a white rabbit toddler, walking together on a moonlit forest path toward home. Warm and tender moment.", [TINA_MOM, BUBU], "warm moonlight"),
    (9, "A cozy bathroom at home. A golden retriever dad standing next to a warm bubbly bathtub, inviting a white rabbit toddler to take a bath. Warm steam rising, rubber ducks floating.", [SAM_DAD, BUBU], "warm bathroom light"),
    (10, "A bathroom scene. A cow mother holding a toothbrush, showing a white rabbit toddler how to brush teeth. The toddler has her mouth open wide. Toothpaste foam visible.", [TINA_MOM, BUBU], "warm bathroom light"),
    (11, "A white rabbit toddler standing on a step stool at the bathroom mirror, brushing teeth with foam all around her mouth like a white beard, laughing at her own reflection. Cute and funny.", [BUBU], "warm bathroom light"),
    (12, "A golden retriever dad helping a white rabbit toddler put on soft pink star-patterned pajamas. The rabbit is twirling happily. Cozy bedroom setting.", [SAM_DAD, BUBU], "warm bedroom lamplight"),
    (13, "A cow mother using a hairdryer to dry a white rabbit toddler's ears. The warm air makes the rabbit squint her eyes in comfort. Cozy bedroom.", [TINA_MOM, BUBU], "warm golden hairdryer glow and bedroom light"),
    (14, "A white rabbit toddler in pink star pajamas tucked into a small bed. A cow mother tucking in the blanket, a golden retriever dad sitting on the bed edge, both looking at her lovingly.", [BUBU, TINA_MOM, SAM_DAD], "soft warm nightlight glow"),
    (15, "A dreamlike scene: the moon sleeping on a cloud, stars with closed eyes, and small silhouettes of a hedgehog, turtle, red bird, and raccoon all sleeping peacefully. Dreamy and magical.", [BUBU], "dreamy moonlight blue-purple tones"),
    (16, "A white rabbit toddler peacefully asleep in her small bed, eyes closed, a gentle smile. A golden retriever dad and cow mother standing by the bedside, gazing lovingly. A nightlight glows softly. Window shows the moon outside.", [BUBU, SAM_DAD, TINA_MOM], "soft warm nightlight, moonlight through window"),
]
for i, (pg, scene, chars, light) in enumerate(s9):
    PAGES.append((9, pg, scene, chars, light))

# ===== STORY 10: 咘咘不害怕 =====
s10 = [
    (2, "Close-up of a white rabbit toddler biting her lips nervously, big worried eyes. Simple soft background.", [BUBU], "soft diffused light"),
    (3, "Three vignettes: a white rabbit toddler biting her lips during thunder (lightning flash in window), in the dark (shadow-filled room), and when strangers approach (tall blurry figures). Montage style.", [BUBU], "dramatic varied lighting"),
    (4, "A forest clearing decorated with colorful bunting and a small wooden stage for a music concert. A raccoon inviting a white rabbit toddler to sing. Forest animals setting up chairs.", [NOMI, BUBU], "cheerful afternoon sunlight"),
    (5, "A white rabbit toddler biting her lips hard, shaking her head, looking scared. A raccoon looking at her with gentle concern. Concert stage visible in background.", [BUBU, NOMI], "afternoon light"),
    (6, "A raccoon crouching down to a white rabbit toddler's level, gently holding her small hand. Warm and reassuring moment. Forest concert area in soft focus behind.", [NOMI, BUBU], "warm golden afternoon light"),
    (7, "A white rabbit toddler and a raccoon doing breathing exercises together. The rabbit inhaling deeply (like smelling a flower), imaginary flower petals floating. Peaceful forest setting.", [BUBU, NOMI], "soft dreamy afternoon light"),
    (8, "A white rabbit toddler doing breathing exercises — exhaling slowly with puffed cheeks (like blowing a bubble), an imaginary soap bubble floating from her mouth. She looks calmer. Peaceful forest.", [BUBU], "warm soft light"),
    (9, "A golden retriever dad kneeling beside a white rabbit toddler, telling her a story. He gestures as if describing his own nervous childhood. Warm father-daughter moment.", [SAM_DAD, BUBU], "warm afternoon golden light"),
    (10, "A white rabbit toddler looking up at a golden retriever dad with wide surprised eyes, mouth slightly open in amazement. 'Daddy gets scared too?' moment.", [BUBU, SAM_DAD], "warm golden light"),
    (11, "A cow mother talking to a white rabbit toddler, gesturing as if baking a cake, showing shaky hands. A dreamy thought bubble showing a big beautiful cake. Warm kitchen-like feeling.", [TINA_MOM, BUBU], "warm soft light"),
    (12, "A cow mother kissing a white rabbit toddler's forehead gently. The toddler's eyes are closed, peaceful expression. Tender mother-daughter moment.", [TINA_MOM, BUBU], "warm golden intimate light"),
    (13, "A forest concert stage. A small hedgehog on stage blowing a tune on a large leaf, looking proud and happy. Animal audience watching and clapping. Bunting decorations.", [DOUDOU], "cheerful stage lighting"),
    (14, "A small turtle on stage singing very slowly, mouth wide open. The animal audience laughing warmly. Cute and funny moment.", [MANMAN], "cheerful stage lighting"),
    (15, "A white rabbit toddler standing below the stage, trembling slightly, hands shaking, about to bite her lips again. Spotlight from stage visible. Nervous moment.", [BUBU], "dramatic stage light from above"),
    (16, "A raccoon whispering encouragingly to a white rabbit toddler from the side of the stage. The rabbit taking a deep breath. 'Smell the flower, blow the bubble.' moment.", [NOMI, BUBU], "warm side lighting"),
    (17, "A white rabbit toddler standing center stage, mouth open singing, tiny voice coming out. She looks nervous but brave. Soft spotlight on her. Audience silhouettes visible.", [BUBU], "warm spotlight center stage"),
    (18, "A white rabbit toddler on stage smiling broadly as the whole animal audience claps. Hedgehog, turtle, raccoon, red bird all cheering. Confetti or flower petals falling. Triumphant joyful moment.", [BUBU, DOUDOU, MANMAN, NOMI, NONO], "warm celebratory golden light"),
]
for pg, scene, chars, light in s10:
    PAGES.append((10, pg, scene, chars, light))

# ===== STORY 11: 咘咘坐小马桶 =====
s11 = [
    (2, "A cow mother gesturing toward a small pink potty with bunny patterns. A white rabbit toddler shaking her head stubbornly, wearing a diaper. Cozy bathroom setting.", [TINA_MOM, BUBU], "warm bathroom light"),
    (3, "A cute pink potty with bunny decorations sitting alone on a bathroom floor. A white rabbit toddler peeking at it suspiciously from behind a door. The potty looks friendly but the rabbit is uncertain.", [BUBU], "soft bathroom light"),
    (4, "A small hedgehog visiting, proudly telling a white rabbit toddler about not wearing diapers anymore. The hedgehog stands tall and proud. The rabbit looks impressed but unsure.", [DOUDOU, BUBU], "cheerful indoor light"),
    (5, "A small turtle also proudly sharing that she can use the potty. She demonstrates walking slowly toward an imaginary potty. The white rabbit watches thoughtfully.", [MANMAN, BUBU], "warm indoor light"),
    (6, "A white rabbit toddler looking worried, holding her hands together. She seems unsure about when she needs to go. Thought bubble with question marks.", [BUBU], "soft warm light"),
    (7, "A golden retriever dad smiling warmly, kneeling next to a white rabbit toddler beside the pink potty. He's explaining gently, pointing at the potty. Encouraging and patient.", [SAM_DAD, BUBU], "warm bathroom light"),
    (8, "A white rabbit toddler just looking at the pink potty from a small distance. A golden retriever dad giving a thumbs up encouragingly. 'Even looking is progress!' moment.", [BUBU, SAM_DAD], "warm bathroom light"),
    (9, "A white rabbit toddler cautiously touching the pink potty with one hand. A cow mother smiling encouragingly beside her. 'Even touching is progress!' moment.", [BUBU, TINA_MOM], "warm bathroom light"),
    (10, "A white rabbit toddler sitting on the pink potty for the first time, looking surprised and proud! Arms raised in celebration. Big happy moment.", [BUBU], "warm celebratory light"),
    (11, "A raccoon holding up a colorful sticker chart with star stickers. A white rabbit toddler looking excited, reaching for a gold star sticker. Craft supplies around.", [NOMI, BUBU], "cheerful indoor light"),
    (12, "Three small vignettes showing a white rabbit toddler sitting on the pink potty: morning (sunrise through window), after meal (empty bowl nearby), before going out (wearing shoes). Routine montage.", [BUBU], "varied warm daylight"),
    (13, "A white rabbit toddler sitting on the pink potty but nothing happening. She looks a little disappointed. A golden retriever dad patting her head gently, saying 'next time'. Patient encouraging moment.", [BUBU, SAM_DAD], "soft warm light"),
    (14, "A white rabbit toddler jumping up from the potty with the biggest most joyful expression — SUCCESS! Arms up, eyes sparkling, jumping with pure joy. Sparkle effects around.", [BUBU], "bright celebratory light"),
    (15, "Close-up of a colorful sticker chart almost full of gold star stickers. A white rabbit toddler's hand placing another star. Many stars already there — nearly complete!", [BUBU], "warm indoor light"),
    (16, "A white rabbit toddler confidently walking toward the pink potty by herself, announcing 'I need to use the potty!' with a determined expression. Independent and proud.", [BUBU], "warm confident lighting"),
    (17, "A cow mother helping a white rabbit toddler put on cute pink star-patterned underwear. The rabbit looks SO proud and grown-up. No more diapers! Celebratory moment.", [TINA_MOM, BUBU], "warm joyful light"),
    (18, "A white rabbit toddler standing tall and proud, wearing her new underwear (visible under her pink dress hem), surrounded by all friends — raccoon, hedgehog, turtle, red bird — all celebrating. Sticker chart fully complete on the wall behind. 'Growing up!' moment.", [BUBU, NOMI, DOUDOU, MANMAN, NONO], "warm golden celebratory light"),
]
for pg, scene, chars, light in s11:
    PAGES.append((11, pg, scene, chars, light))

# ===== STORY 12: 咘咘自己走 =====
s12 = [
    (2, "A golden retriever dad carrying a white rabbit toddler who clings saying 'carry me!'. A cow mother watching with a concerned smile. At a sunny spring park entrance. The rabbit is getting big — dad is straining a little.", [SAM_DAD, BUBU, TINA_MOM], "bright spring morning light"),
    (3, "A small hedgehog with a tiny backpack bouncing happily far ahead on a flower-lined spring path. A white rabbit toddler watching from a golden retriever's arms in the background.", [DOUDOU, BUBU, SAM_DAD], "cheerful spring sunlight"),
    (4, "A small turtle walking slowly but steadily along a spring path, tiny footprints stretching behind her. A white rabbit in a golden retriever's arms watching with impressed curious eyes.", [MANMAN, BUBU, SAM_DAD], "warm spring light"),
    (5, "A small red bird perched on a cherry blossom branch, calling down to a white rabbit toddler being carried by a golden retriever. Spring park with flowers and butterflies.", [NONO, BUBU, SAM_DAD], "bright spring daylight"),
    (6, "A raccoon pointing at a turtle walking in the distance, then pointing at a white rabbit toddler's feet dangling from a golden retriever's arms. The rabbit looking down at her own feet with a realization moment.", [NOMI, BUBU, SAM_DAD, MANMAN], "spring afternoon light"),
    (7, "Close-up of a white rabbit toddler looking down comparing her feet to a small turtle's tiny legs nearby. Lightbulb realization moment. A golden retriever gently lowering her to the spring grass.", [BUBU, MANMAN, SAM_DAD], "warm spring light"),
    (8, "A white rabbit toddler taking a wobbly first step on soft spring grass, bare feet on grass. A cow mother walking alongside with arms ready to catch but not touching. Warm encouraging scene with spring flowers.", [BUBU, TINA_MOM], "warm spring sunshine"),
    (9, "A white rabbit toddler taking confident steps on spring grass. A hedgehog running back excitedly cheering. A raccoon and turtle clapping in background. Spring park with colorful flowers.", [BUBU, DOUDOU, NOMI, MANMAN], "cheerful spring light"),
    (10, "A white rabbit toddler running on spring grass chasing a laughing hedgehog, steps a bit clumsy but joyful. A golden retriever and cow watching from a bench with proud tearful expressions.", [BUBU, DOUDOU, SAM_DAD, TINA_MOM], "warm spring golden hour"),
    (11, "A white rabbit toddler sliding down a colorful playground slide with arms up, laughing. A hedgehog and turtle cheering at the bottom. A raccoon at the top of the slide. A red bird flying around. Spring park playground.", [BUBU, DOUDOU, MANMAN, NOMI, NONO, SAM_DAD], "bright playground light"),
    (12, "A white rabbit toddler sitting on a park bench next to a golden retriever dad, both drinking from juice boxes. The rabbit swinging her tired little legs happily. Spring trees and flowers around. Peaceful resting moment.", [BUBU, SAM_DAD], "warm spring afternoon light"),
    (13, "A white rabbit toddler and a small turtle standing up together, ready to go. The rabbit looks energized and determined. Spring park sunset beginning. A hedgehog, raccoon, and red bird joining them.", [BUBU, MANMAN, DOUDOU, NOMI, NONO], "spring sunset light"),
    (14, "A white rabbit toddler walking confidently ahead on a spring sunset path, looking back and waving at a golden retriever and cow who follow behind with proud happy expressions. Friends walking together. Cherry blossom petals falling.", [BUBU, SAM_DAD, TINA_MOM, DOUDOU, MANMAN, NOMI, NONO], "golden hour spring sunset"),
    (15, "A golden retriever dad kneeling at the front door of a cozy house, opening arms to offer a carry. A white rabbit toddler standing and looking at him thoughtfully. Spring evening warm light.", [SAM_DAD, BUBU], "warm spring evening light"),
    (16, "A white rabbit toddler walking through the front door of a cozy home by herself with the most proud determined expression. A golden retriever and cow standing behind with the proudest loving smiles. Warm spring evening light streaming through the door.", [BUBU, SAM_DAD, TINA_MOM], "warm evening doorway light"),
    (17, "A white rabbit toddler standing tall and proud in the center, surrounded by all friends — golden retriever, cow, raccoon, hedgehog, turtle, and red bird on her head. Spring flower petals falling. A winding path behind representing her journey. Warm triumphant celebratory scene.", [BUBU, SAM_DAD, TINA_MOM, NOMI, DOUDOU, MANMAN, NONO], "golden spring sunset celebratory light"),
]
for pg, scene, chars, light in s12:
    PAGES.append((12, pg, scene, chars, light))

# ===== STORY 13: 咘咘再来一次 =====
s13 = [
    (2, "A beautiful spring garden with blooming flowers. A white rabbit toddler and a raccoon running happily on green grass. Colorful butterflies and petals in the air.", [BUBU, NOMI], "bright cheerful spring sunlight"),
    (3, "A white rabbit toddler tripping over a small rock and landing on her bottom with a surprised expression — plop! A raccoon nearby looking startled. Spring garden.", [BUBU, NOMI], "bright spring light"),
    (4, "A raccoon rushing over to a white rabbit toddler who is sitting on the ground after falling. The raccoon looks worried, reaching out. Spring garden.", [NOMI, BUBU], "warm spring light"),
    (5, "A white rabbit toddler standing up, patting her pink dress, then deliberately sitting back down on the grass on purpose with a mischievous grin! A raccoon looking confused. Spring garden.", [BUBU, NOMI], "cheerful spring sunlight"),
    (6, "A white rabbit toddler sitting on the grass with a big determined grin, announcing she wants to fall again! A raccoon standing nearby with a surprised but amused expression. Spring garden.", [BUBU, NOMI], "bright fun spring light"),
    (7, "A raccoon tilting her head thoughtfully, looking at a white rabbit toddler sitting on the grass. The raccoon has a knowing smile — she understands what the rabbit wants. Spring garden.", [NOMI, BUBU], "warm soft spring light"),
    (8, "A white rabbit toddler nodding vigorously with sparkling determined eyes, fists clenched in excitement. 'I want to try it myself!' Energetic and brave. Spring garden.", [BUBU], "bright encouraging spring light"),
    (9, "A raccoon plopping down on the grass right next to a white rabbit toddler, both sitting together. The raccoon laughing, the rabbit delighted. Spring garden flowers around them.", [NOMI, BUBU], "warm joyful spring light"),
    (10, "A raccoon and a white rabbit toddler sitting on the grass together, both laughing hysterically. A small red bird landing on the grass nearby, curious. Spring garden, flower petals floating.", [NOMI, BUBU, NONO], "bright cheerful spring light"),
    (11, "A raccoon asking a white rabbit toddler 'how does it feel?'. The rabbit rubbing her bottom with one hand, making a funny half-grimace half-smile face. 'A little sore but fun!' Spring garden.", [NOMI, BUBU], "warm spring afternoon light"),
    (12, "A raccoon making a wise teacher-like pose, explaining to a white rabbit toddler. Both sitting on the grass. The rabbit listening and nodding. 'Now we know!' moment. Spring garden.", [NOMI, BUBU], "warm golden spring light"),
    (13, "A white rabbit toddler standing up from the grass, patting her pink dress clean, looking confident and happy. A raccoon standing up beside her. Ready to play again! Spring garden.", [BUBU, NOMI], "bright spring light"),
    (14, "Three friends — a white rabbit toddler, a raccoon, and a small red bird — running happily through a beautiful spring flower garden. The rabbit runs in front, leading the way. Petals and butterflies everywhere. The most joyful and free scene. Cherry blossoms overhead.", [BUBU, NOMI, NONO], "golden spring afternoon celebratory light"),
]
for pg, scene, chars, light in s13:
    PAGES.append((13, pg, scene, chars, light))

def generate_image(prompt, output_path):
    """Call Azure OpenAI image API and save as JPG."""
    url = f"{ENDPOINT}?api-version={API_VERSION}"
    headers = {"api-key": API_KEY, "Content-Type": "application/json"}
    body = {
        "prompt": prompt,
        "n": 1,
        "size": "1024x1536",
        "quality": "medium",
        "output_format": "png"
    }
    
    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = requests.post(url, headers=headers, json=body, timeout=120)
            if resp.status_code == 429:
                wait = RETRY_WAIT * (attempt + 1)
                print(f"  429 rate limited, waiting {wait}s (attempt {attempt+1}/{MAX_RETRIES})")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            data = resp.json()
            b64 = data["data"][0]["b64_json"]
            
            # Save PNG temp then convert to JPG
            png_path = output_path.replace(".jpg", ".png")
            with open(png_path, "wb") as f:
                f.write(base64.b64decode(b64))
            
            # Convert to JPG with ffmpeg
            subprocess.run([
                "ffmpeg", "-y", "-i", png_path, "-q:v", "2", output_path
            ], capture_output=True, check=True)
            os.remove(png_path)
            
            size = os.path.getsize(output_path)
            return size
        except requests.exceptions.HTTPError as e:
            if resp.status_code == 429 and attempt < MAX_RETRIES:
                wait = RETRY_WAIT * (attempt + 1)
                print(f"  429 rate limited, waiting {wait}s (attempt {attempt+1}/{MAX_RETRIES})")
                time.sleep(wait)
                continue
            raise
    raise Exception("Max retries exceeded")

def main():
    # Check for resume
    start_idx = 0
    if len(sys.argv) > 1:
        start_idx = int(sys.argv[1])
        print(f"Resuming from index {start_idx}")
    
    total = len(PAGES)
    print(f"Total pages to generate: {total}")
    
    results = []
    for idx, (story, page, scene, chars, light) in enumerate(PAGES):
        if idx < start_idx:
            continue
        
        output_dir = os.path.join(OUTPUT_BASE, f"story{story}")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"page-{page:02d}.jpg")
        
        # Skip if already exists
        if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
            size = os.path.getsize(output_path)
            print(f"[{idx+1}/{total}] SKIP story{story}/page-{page:02d}.jpg ({size//1024}KB)")
            results.append((story, page, size))
            continue
        
        prompt = make_prompt(scene, chars, light)
        print(f"[{idx+1}/{total}] Generating story{story}/page-{page:02d}.jpg ...")
        
        try:
            size = generate_image(prompt, output_path)
            print(f"  ✅ {size//1024}KB")
            results.append((story, page, size))
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            results.append((story, page, -1))
        
        if idx < total - 1:
            time.sleep(DELAY)
    
    # Summary
    print("\n===== SUMMARY =====")
    for story in [9, 10, 11, 12, 13]:
        pages = [(p, s) for st, p, s in results if st == story]
        ok = sum(1 for _, s in pages if s > 0)
        fail = sum(1 for _, s in pages if s <= 0)
        print(f"Story {story}: {ok} ok, {fail} failed")
        for p, s in pages:
            status = f"{s//1024}KB" if s > 0 else "FAILED"
            print(f"  page-{p:02d}: {status}")

if __name__ == "__main__":
    main()
