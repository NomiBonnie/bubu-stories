#!/usr/bin/env python3
"""Generate all illustrations for print edition Book 6 (Stories 25,26,28,29,30,31)."""

import json, os, time, sys, subprocess, requests, base64

# API config
with open(os.path.expanduser("~/.config/azure-openai/config.json")) as f:
    cfg = json.load(f)

API_KEY = cfg["image2_eastus2_api_key"]
ENDPOINT = cfg["image2_eastus2_endpoint"]
API_VERSION = "2025-04-01-preview"

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# Character prompts
BUBU = "a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow. She has a small pink bow centered ON TOP OF HER HEAD between her two ears (not on left ear, not on right ear, not behind — exactly centered on top between the ears). She has a toddler-like round body proportion."

SAM_DAD = "Sam Dad who is a GOLDEN RETRIEVER DOG (NOT a human, NOT a person — he is an ANIMAL, a large golden-furred dog walking upright). He has warm golden fur all over his body, a dog snout/muzzle, floppy dog ears, and a wagging tail. He wears a dark navy jacket over a simple shirt. He has a warm gentle dog smile. IMPORTANT: Sam Dad must look like a golden retriever dog, not a human man."

TINA_MOM = "Tina Mom who is a BLACK-AND-WHITE COW (NOT a human, NOT a person — she is an ANIMAL, a cow walking upright). She has black and white spotted fur pattern all over, small curved horns, cow ears, and hooves. She wears an elegant cream knit cardigan over a floral skirt. She has a gentle warm cow smile. IMPORTANT: Tina Mom must look like a cow, not a human woman."

NOMI = "a raccoon (NOMI) with grey-brown fur, distinctive black eye mask markings, and a ringed bushy tail. She wears a blue-and-white horizontally striped sweater. She has clever bright eyes and nimble paws."

NONO = "a small red bird (NONO) with bright red feathers all over, round bright eyes, and an orange-yellow beak. He has exactly TWO wings and TWO small bird feet with talons. NO ARMS, NO HANDS — birds do not have arms or hands, only wings."

DOUDOU = "a small hedgehog (Doudou) with a brown body covered in dark brown spines/quills, small round shiny eyes, a tiny nose. He is small, round, and shy-looking."

SHUISHUI = "a snow-white rabbit girl (Shuishui, slightly taller than Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes. She wears a lavender/light purple dress with a purple headband/hair clip. She has a toddler-like body, cheerful and outgoing."

SHUISHUI_DAD = "Shuishui's Dad who is a SIBERIAN HUSKY DOG (NOT a human — he is an ANIMAL, a black-and-white husky walking upright). He has black fur on his back and white on his face and belly, ice-blue eyes (husky signature), black-rimmed glasses, and wears a dark blue polo shirt. He has a hearty friendly smile. IMPORTANT: must look like a husky dog, not a human."

SHUISHUI_MOM = "Shuishui's Mom who is a BROWN-AND-WHITE COW (NOT a human — she is an ANIMAL, a cow walking upright). She has brown and white spotted fur pattern (NOT black-and-white, different from Tina). She wears a white blouse with wide-leg pants and a silk scarf, and pearl earrings. IMPORTANT: must look like a cow, not a human woman."

STYLE_PREFIX = "Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition (1024x1536). Pure illustration, NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS anywhere in the image."
STYLE_SUFFIX = "The bottom 20% of the image gradually darkens naturally (subtle vignette). Natural composition, no forced blank margins."

# All pages to generate
PAGES = []

# Story 25 - 咘咘荡秋千 (summer)
s25_scenes = {
    2: f"A colorful children's playground with slides, swings, and seesaws. {BUBU} walks in holding the paw of {SAM_DAD}. Bright summer day, lush green trees. Bubu looks excited, pointing at the playground equipment.",
    3: f"{NOMI} helps {BUBU} sit on a swing in the playground. NOMI stands behind the swing, gently pushing. Bubu grips the swing chains with her small paws, smiling with anticipation. Summer sunshine, playground background.",
    4: f"{BUBU} swinging high on a swing, eyes closed with joy, ears fluttering in the wind. Her pink dress flows. Summer breeze, blue sky with fluffy clouds. Dynamic swinging motion, joyful expression.",
    5: f"Drama moment: {DOUDOU} accidentally bumps into the swing. {BUBU} loses her grip and is tumbling off the swing mid-air, surprised expression. The swing swings wildly. Playground setting, summer day.",
    6: f"{BUBU} sitting on the ground near the swing, looking down at her slightly scraped knee. Tears well up in her big brown eyes, pouty lips. She looks frustrated and sad. Playground ground with wood chips, summer light.",
    7: f"{NOMI} kneeling down next to {BUBU} who sits on the ground, gently patting Bubu's back with her nimble paw. NOMI has a warm, comforting expression. Bubu looks up at NOMI with teary eyes. Playground, soft summer light.",
    8: f"{NONO} flying toward {BUBU} who sits on the ground, wings spread wide, chirping cheerfully with beak open. NONO hovers at Bubu's eye level. Bubu's tears start to dry, a small smile forming. Playground, summer afternoon.",
    9: f"{DOUDOU} standing in front of {BUBU}, looking apologetic with downcast eyes. Bubu sits on the ground wiping her tears with one paw, smiling forgivingly at Doudou. Playground, warm summer light.",
    10: f"{BUBU} climbing back onto the swing by herself, determined expression, gripping the chains firmly. She takes a deep breath, showing courage. The swing is ready. Playground, summer afternoon golden light.",
    11: f"{BUBU} swinging very high on the swing, much higher than before, gripping tightly with both paws. Her ears stream behind her in the wind. Expression of pure exhilaration and triumph. Blue sky, summer clouds, dynamic motion.",
    12: f"{BUBU} swinging high with a huge joyful shout, arms (one paw) raised in triumph. Below the swing, {NOMI} and {SAM_DAD} stand together clapping and cheering. {NONO} flies around excitedly. Playground, golden summer light, triumphant finale scene.",
}

for p, scene in s25_scenes.items():
    PAGES.append(("story25", p, scene))

# Story 26 - 咘咘的小脚踩到了水 (evening/night scene at a mall)
s26_scenes = {
    2: f"A spectacular modern shopping mall at night, with a shallow decorative water pool in the center filled with illuminated fountains. {SAM_DAD} and {TINA_MOM} walk with {BUBU} between them, holding her paws. Bubu looks around in wonder at the sparkling fountains. Evening/night lighting, modern architecture.",
    3: f"The shallow fountain pool in the mall, surrounded by decorative pebble stepping stones like little islands. In the center of the pool stands a giant apple-shaped structure (an Apple Store). {BUBU} stands at the edge looking at it with wide curious eyes. Water sparkles, evening mall lighting.",
    4: f"Close-up of {BUBU} looking up excitedly at the giant apple-shaped Apple Store in the center of the fountain pool, her big brown eyes wide with curiosity and desire, pointing at it with one paw. {SAM_DAD} stands behind her, smiling. Mall interior, evening lights reflecting on water.",
    5: f"{SAM_DAD} crouching down to Bubu's level, smiling encouragingly and gesturing toward the stepping stones across the water. {BUBU} looks at the stepping stones with a brave, excited expression. The fountain pool and Apple Store visible in background. Evening mall lighting.",
    6: f"{BUBU} hopping from one pebble stepping stone to another across the shallow fountain pool, arms out for balance, big happy smile. {NOMI} stands at the edge clapping and cheering. Water splashes gently around the stones. Evening mall lighting, colorful fountain lights.",
    7: f"Drama moment: {BUBU} mid-slip on a wet stepping stone, one foot splashing into the cold water. Surprised expression, mouth open. Water splashes up around her pink shoe. The fountain pool, evening mall lighting. Dynamic action shot.",
    8: f"{BUBU} standing still on a stepping stone, looking down at her one wet shoe with a pouty expression, lower lip trembling, tears about to fall. Her ears droop slightly. Water drips from the shoe. Evening mall lighting, reflections on water.",
    9: f"{TINA_MOM} kneeling at the edge of the fountain pool, giving {BUBU} a big warm hug. Bubu's face is pressed against Tina's chest, looking comforted. Tina has a gentle, reassuring cow smile. Evening mall lighting, warm embrace scene.",
    10: f"{SAM_DAD} standing next to {BUBU} and {TINA_MOM}, gently patting Bubu's shoulder. Both parents look lovingly at Bubu. Bubu looks up at Sam Dad with trusting eyes, tears drying. The fountain pool and Apple Store in soft-focus background. Evening mall lighting.",
    11: f"{BUBU} starting to smile again, looking up hopefully. The Apple Store glows invitingly in the background across the water. Bubu's expression changes from sad to hopeful and eager. Evening mall lighting, warm atmosphere.",
    12: f"{BUBU} walking confidently across the stepping stones, holding {SAM_DAD}'s paw on one side and {TINA_MOM}'s hoof on the other. All three heading toward the glowing Apple Store. Bubu smiles bravely. Evening mall lighting, triumphant family scene, warm golden glow from the store.",
}

for p, scene in s26_scenes.items():
    PAGES.append(("story26", p, scene))

# Story 28 - 咘咘在床上蹦蹦跳 (indoor, summer)
s28_scenes = {
    2: f"A cozy bedroom with a large bed with a headboard/railing. {BUBU} stands on the big soft bed, giving a small experimental bounce, eyes lighting up with delight. The bed dips under her feet. Warm bedroom lighting, summer afternoon, curtains gently moving.",
    3: f"{BUBU} bouncing high on the bed, mid-air, arms spread wide, laughing with pure joy. Her pink dress poofs out. Bedsheets and pillows bounce around her. Energetic, dynamic pose. Bedroom, summer afternoon light.",
    4: f"{BUBU} bouncing too close to the edge of the bed near a windowsill, startled expression, one paw reaching out to catch herself. She's about to bump into the windowsill. Dangerous moment, summer light from window. Bedroom setting.",
    5: f"{BUBU} sitting on the bed after slipping, one paw on her chest feeling her racing heart, wide eyes, slightly scared expression. She sits near the bed edge. The floor visible below. Bedroom, summer afternoon.",
    6: f"{SAM_DAD} rushing into the bedroom doorway, concerned expression, one paw raised. He looks at {BUBU} on the bed with gentle worry. Bedroom, summer afternoon light streaming in.",
    7: f"{TINA_MOM} standing beside the bed, speaking gently to {BUBU} who sits on the bed listening. Tina points at the bed railing with one hoof, demonstrating. Warm bedroom scene, summer afternoon.",
    8: f"{SAM_DAD} and {TINA_MOM} on either side of the bed, teaching {BUBU} to hold onto the bed railing. Sam Dad guides Bubu's small paw to grip the railing. Bubu watches attentively. Warm family teaching moment, bedroom, summer light.",
    9: f"{BUBU} bouncing happily on the bed while holding firmly onto the bed railing with both paws. Safe and fun! Big smile, controlled bouncing. Bedroom, warm summer light. Energetic but safe pose.",
    10: f"{BUBU} bouncing joyfully on the bed holding the railing, while {SAM_DAD} and {TINA_MOM} sit nearby on the bed edge, watching with warm proud smiles. {NONO} perches on the headboard. Warm, cozy bedroom, golden summer evening light. Happy ending scene.",
}

for p, scene in s28_scenes.items():
    PAGES.append(("story28", p, scene))

# Story 29 - 咘咘等水水姐姐来玩 (spring, Suzhou)
s29_scenes = {
    2: f"Split scene: On the left, {BUBU} waves from a Suzhou garden with traditional white-walled buildings and a canal. On the right, {SHUISHUI} waves from in front of simplified colorful Beijing landmarks. A dotted line with hearts connects the two cities across the sky. Spring weather, bright cheerful scene.",
    3: f"{SAM_DAD} crouching to eye level with {BUBU} in a modern Suzhou apartment living room, gesturing excitedly with a warm smile. Bubu's eyes are wide open with pure joy, mouth in a big O of surprise, ears perked straight up. Spring light streaming in.",
    4: f"{BUBU} jumping joyfully in the air with arms raised, big sparkling eyes full of excitement. Star and heart sparkles around her. {NOMI} watches happily from a shelf. {NONO} flutters nearby. Cozy living room, spring afternoon light.",
    5: f"{BUBU} walking between {SAM_DAD} and {TINA_MOM}, holding both their paws, pulling them forward eagerly. A charming Suzhou street with traditional architecture, spring trees with fresh green leaves, morning golden light. Heading toward shops.",
    6: f"Inside a colorful gift shop. {BUBU} stands surrounded by shelves full of cute toys, stuffed animals, colorful hair accessories, stickers. Her eyes dart excitedly between items, paws reaching toward a purple stuffed animal and a sparkly hair clip simultaneously. Warm interior, spring display.",
    7: f"Close-up of {BUBU} holding up a delicate purple beaded bracelet with both paws, examining it with a proud satisfied smile. Her eyes sparkle with love. The bracelet catches the light. Gift shop counter in background. {TINA_MOM} smiles approvingly behind her.",
    8: f"{BUBU} sitting at a small desk, drawing on colorful paper with crayons. The card shows two rabbit figures holding hands with hearts and stars. Crayon supplies scattered on desk. {NOMI} helps hold the paper steady. Afternoon light through window.",
    9: f"{BUBU} standing on tiptoes at the front door of a Suzhou apartment, one paw shading her eyes as she peers eagerly down the path. She holds a small gift bag in her other paw. Spring flowers bloom by the doorstep. Late morning light, anticipation on her face.",
    10: f"Two rabbit girls running toward each other on a tree-lined Suzhou path with arms wide open. Left: {BUBU}. Right: {SHUISHUI} running joyfully. Behind Shuishui: {SHUISHUI_DAD} and {SHUISHUI_MOM}. Spring cherry blossom petals floating in the air. Emotional reunion scene.",
    11: f"Close-up of {BUBU} and {SHUISHUI} hugging warmly, eyes closed, big happy smiles. Little hearts float around them. Behind them: {SAM_DAD}, {TINA_MOM}, {SHUISHUI_DAD}, {SHUISHUI_MOM} all watching and smiling. Spring afternoon, cherry blossom petals.",
    12: f"{BUBU} proudly presenting a purple beaded bracelet and a handmade colorful card to {SHUISHUI}. Shuishui looks at the gifts with wide sparkling eyes and amazed smile. The card shows two rabbits holding hands. Warm indoor lighting, cozy apartment.",
    13: f"{SHUISHUI} now wearing the purple bracelet on her wrist, holding out a cute red box decorated with Beijing tanghulu designs. {BUBU} reaches for the box with delighted eyes. Both rabbits beam at each other. Living room, soft lighting.",
    14: f"Final scene: {BUBU} and {SHUISHUI} sitting side by side on a bench in a beautiful Suzhou garden with canal and arched stone bridge. Sharing Beijing candy, legs swinging happily. {NOMI} and {NONO} perch nearby. Their families chat in background. Golden sunset, spring warmth, friendship and joy.",
}

for p, scene in s29_scenes.items():
    PAGES.append(("story29", p, scene))

# Story 30 - 咘咘追萤火虫 (summer evening/night, Suzhou garden)
s30_scenes = {
    2: f"A beautiful Suzhou classical garden at golden hour, with white walls, moon gate, green bamboo. Sky painted in warm orange and pink sunset. Gentle summer breeze rustles willow trees and lotus flowers in a small pond. No characters, just the serene garden. Warm, peaceful atmosphere.",
    3: f"{BUBU} wearing a light pink summer dress running happily on a stone path in a Suzhou garden. Behind her: {SAM_DAD} in casual linen shirt, {TINA_MOM} in elegant summer blouse, {NOMI} in blue-and-white striped summer t-shirt, and {NONO} perched on NOMI's shoulder. Summer evening, warm golden light.",
    4: f"{BUBU} in light pink summer dress crouching near a bush in the garden, peering at a single warm yellow-green glowing firefly hovering above the grass. Her eyes are wide with wonder, ears perked forward. Dusky Suzhou garden, soft purple twilight. The firefly's glow illuminates Bubu's face.",
    5: f"{NOMI} in blue-and-white striped summer t-shirt kneeling beside {BUBU} in light pink summer dress. NOMI points gently toward a glowing firefly with one paw. Both look at the firefly with soft smiles. Dusky garden, more fireflies appearing in distance. Warm magical lighting.",
    6: f"{BUBU} in light pink summer dress stretching both paws up eagerly trying to catch a glowing yellow-green firefly hovering just out of reach above her. Determined excited expression. The firefly glows against dusky purple-blue sky. More fireflies in background. Dynamic playful pose.",
    7: f"{BUBU} in light pink summer dress running and leaping through a Suzhou garden at twilight, chasing several glowing yellow-green fireflies that scatter away. Motion blur on running feet, arms outstretched. Fireflies leave trails of light. Garden path between rocks and bamboo. Playful energetic scene.",
    8: f"{BUBU} in light pink summer dress sitting on a large garden stone, cheeks puffed out in a pout, paws on knees. Tired and frustrated. Fireflies glow far away in distance. Dusky garden, blue-purple evening light. {NONO} perched on stone next to her, tilting head sympathetically.",
    9: f"{NOMI} in blue-and-white striped summer t-shirt sitting on a garden stone, one arm gently around {BUBU}'s shoulder in light pink summer dress. NOMI speaks softly with a wise tender expression. Bubu looks up at NOMI. Fireflies glow in background. Intimate warm moment, dusky garden.",
    10: f"Close-up of {BUBU} in light pink summer dress looking down at her empty cupped paws. Expression of gentle sadness mixed with longing. Big round brown eyes glisten with wistfulness. A single firefly glows in blurred background. Soft bokeh with warm yellow-green firefly lights. Intimate emotional shot.",
    11: f"{NOMI} in blue-and-white striped summer t-shirt smiling warmly, holding up one finger as if sharing a secret, sitting next to {BUBU} in light pink summer dress who looks curious and hopeful. Both on a stone in the garden. Distant fireflies glow. Encouraging mood.",
    12: f"{BUBU} in light pink summer dress sitting very still on a garden stone, hands folded in lap, eyes wide and watchful. Background: {SAM_DAD} in casual linen shirt and {TINA_MOM} in summer blouse sit together on a garden bench, smiling tenderly. {NOMI} beside Bubu. Twilight, fireflies drifting closer.",
    13: f"MAGICAL CLIMAX: {BUBU} in light pink summer dress sitting still on a garden stone, beaming with the most beautiful smile. One glowing warm yellow-green firefly sits on her pink nose. Many more fireflies surround her — on her ears, shoulders, paws, floating everywhere. The entire Suzhou garden illuminated by hundreds of firefly lights. {NOMI} watches with proud tender smile. {NONO} on a branch above. Breathtaking magical scene.",
    14: f"DREAM SEQUENCE: {BUBU} in light pink summer dress floating and flying through a fantastical starry night garden, with tiny translucent golden wings like a firefly on her back, her belly glowing warm yellow-green. Arms spread wide with pure joy. Below, the garden is a magical landscape of glowing flowers and luminous paths. Dreamy ethereal quality, soft-focus edges, sparkles. Crescent moon in sky. Magical dreamlike ending.",
}

for p, scene in s30_scenes.items():
    PAGES.append(("story30", p, scene))

# Story 31 - 咘咘的小脚丫 (spring)
s31_scenes = {
    2: f"Indoor cozy living room. {TINA_MOM} kneeling down trying to put small pink shoes on {BUBU}. Bubu has a mischievous grin and is kicking one shoe off with her bare foot, showing cute pink paw pads. The kicked shoe flies through the air. Warm morning light from window. Playful comedic moment.",
    3: f"{TINA_MOM} standing at the front door holding small pink shoes, looking lovingly at {BUBU} who shakes her head defiantly with arms crossed, bare feet with cute pink paw pads on wooden floor. {NOMI} watches from behind with amused expression. Bright doorway with spring sunshine.",
    4: f"{BUBU} in a park on a gravel path, hopping on one foot with a pained expression, tears forming. She holds up one bare foot showing pink paw pads with a small pebble stuck to it. Park with green trees, flowers, playground in background. Spring daytime, bright.",
    5: f"{NOMI} kneeling on a park path, gently holding {BUBU}'s small bare foot, carefully picking a tiny pebble from her cute pink paw pad. Bubu sits on the ground looking teary but trusting. {NONO} hovers nearby looking worried. Soft spring sunlight, green park.",
    6: f"Inside a bright supermarket with colorful shelves. {BUBU} standing barefoot on shiny cold tile floor, sneezing dramatically with eyes squeezed shut, ears blown back. Bare feet with pink paw pads on icy-looking white tile. Cold blue tint on floor contrasting with warm store lighting. Comedic sneeze pose.",
    7: f"Sunny beach scene. {BUBU} hopping from foot to foot on hot golden sand, feet lifted alternately, face scrunched in discomfort, mouth open yelling. Heat waves from sand. Pink paw pads reddened. {NOMI} rushes toward her with arms outstretched. Blue ocean, bright sun. Comedic dynamic pose.",
    8: f"{NOMI} carrying {BUBU} in her arms, walking on a cheerful street toward a colorful shoe store with a big shoe-shaped sign. Bubu tilts her head curiously with one ear flopped. {NONO} flies ahead. Warm spring afternoon, pastel buildings.",
    9: f"Inside a magical colorful children's shoe store with rainbow shelves. {BUBU} standing in the middle, eyes sparkling with excitement, pointing at a special pair of white bunny-shaped shoes on a glowing display. The bunny shoes are white with long rabbit ears and tiny pink bows. Sparkles around the shoes. Wonder-filled atmosphere.",
    10: f"{BUBU} jumping high in the air with pure joy, wearing adorable white bunny-shaped shoes with long ears and pink bows. Mid-leap, arms spread wide, huge delighted smile. {NOMI} claps below. {NONO} flies excitedly around. Inside colorful shoe store, sparkle effects. Dynamic triumphant moment.",
    11: f"Triple-scene montage: {BUBU} wearing white bunny shoes with pink bows, confidently and happily in three settings: running on park path over pebbles, walking on supermarket floor comfortably, playing on beach sand without pain. Bright cheerful montage. {NOMI} and {NONO} as small companion figures.",
    12: f"Cozy living room scene. {BUBU} walking barefoot on a fluffy cream carpet with blissful smile, eyes half-closed, wiggling her toes showing pink paw pads. Her white bunny shoes neatly placed by the front door. {NOMI} on the couch smiling. {NONO} nestled on a cushion. Golden evening light. Warm, safe, home feeling. The end.",
}

for p, scene in s31_scenes.items():
    PAGES.append(("story31", p, scene))

print(f"Total pages to generate: {len(PAGES)}")

def generate_image(prompt, output_path, retries=3):
    """Generate image via Azure OpenAI API."""
    full_prompt = f"{STYLE_PREFIX} {prompt} {STYLE_SUFFIX}"
    
    for attempt in range(retries):
        try:
            url = f"{ENDPOINT}?api-version={API_VERSION}"
            headers = {
                "api-key": API_KEY,
                "Content-Type": "application/json"
            }
            body = {
                "prompt": full_prompt,
                "n": 1,
                "size": "1024x1536",
                "quality": "medium",
                "output_format": "png"
            }
            
            resp = requests.post(url, headers=headers, json=body, timeout=120)
            
            if resp.status_code == 429:
                wait = 45
                print(f"  429 rate limited, waiting {wait}s (attempt {attempt+1}/{retries})")
                time.sleep(wait)
                continue
            
            if resp.status_code != 200:
                print(f"  Error {resp.status_code}: {resp.text[:200]}")
                if attempt < retries - 1:
                    time.sleep(15)
                    continue
                return False
            
            data = resp.json()
            
            # Extract base64 image
            b64 = data.get("data", [{}])[0].get("b64_json")
            if not b64:
                # Try URL-based response
                img_url = data.get("data", [{}])[0].get("url")
                if img_url:
                    img_resp = requests.get(img_url, timeout=60)
                    png_data = img_resp.content
                else:
                    print(f"  No image data in response: {str(data)[:200]}")
                    if attempt < retries - 1:
                        time.sleep(10)
                        continue
                    return False
            else:
                png_data = base64.b64decode(b64)
            
            # Save PNG temporarily, convert to JPG
            tmp_png = output_path.replace(".jpg", ".tmp.png")
            with open(tmp_png, "wb") as f:
                f.write(png_data)
            
            # Convert to JPG with ffmpeg
            subprocess.run(
                ["ffmpeg", "-y", "-i", tmp_png, "-q:v", "2", output_path],
                capture_output=True, check=True
            )
            os.remove(tmp_png)
            
            size_kb = os.path.getsize(output_path) / 1024
            print(f"  ✅ {output_path} ({size_kb:.0f} KB)")
            return True
            
        except Exception as e:
            print(f"  Exception: {e}")
            if attempt < retries - 1:
                time.sleep(15)
                continue
            return False
    
    return False

# Main generation loop
failed = []
for i, (story, page, scene) in enumerate(PAGES):
    outdir = os.path.join(OUTDIR, story)
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, f"page-{page:02d}.jpg")
    
    if os.path.exists(outpath) and os.path.getsize(outpath) > 10000:
        size_kb = os.path.getsize(outpath) / 1024
        print(f"[{i+1}/{len(PAGES)}] SKIP {story}/page-{page:02d}.jpg (exists, {size_kb:.0f} KB)")
        continue
    
    print(f"[{i+1}/{len(PAGES)}] Generating {story}/page-{page:02d}.jpg ...")
    ok = generate_image(scene, outpath)
    if not ok:
        failed.append(f"{story}/page-{page:02d}")
        print(f"  ❌ FAILED {story}/page-{page:02d}")
    
    if i < len(PAGES) - 1:
        time.sleep(8)

print(f"\n{'='*50}")
print(f"Done! Generated {len(PAGES) - len(failed)}/{len(PAGES)} images")
if failed:
    print(f"Failed: {failed}")

# Report file sizes
print(f"\n{'='*50}")
print("File sizes:")
for story, page, _ in PAGES:
    path = os.path.join(OUTDIR, story, f"page-{page:02d}.jpg")
    if os.path.exists(path):
        size_kb = os.path.getsize(path) / 1024
        print(f"  {story}/page-{page:02d}.jpg: {size_kb:.0f} KB")
    else:
        print(f"  {story}/page-{page:02d}.jpg: MISSING")
