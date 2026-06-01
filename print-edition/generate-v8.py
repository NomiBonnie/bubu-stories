#!/usr/bin/env python3
"""Generate all illustrations for print edition volume 8 (Stories 38-43)."""

import json, os, time, sys, subprocess, base64, urllib.request, urllib.error

# Force unbuffered output
os.environ['PYTHONUNBUFFERED'] = '1'
sys.stdout.reconfigure(line_buffering=True)

# Load API config
with open(os.path.expanduser("~/.config/azure-openai/config.json")) as f:
    cfg = json.load(f)

API_KEY = cfg["image2_eastus2_api_key"]
ENDPOINT = cfg["image2_eastus2_endpoint"]
API_VERSION = "2025-04-01-preview"
WORKSPACE = os.path.expanduser("~/.openclaw/workspace/bubu-stories/print-edition")

# Character prompts
BUBU = "a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow. She has a small pink bow centered ON TOP OF HER HEAD between her two ears (not on left ear, not on right ear, not behind — exactly centered on top between the ears). She has a toddler-like round body proportion."
SAM_DAD = "Sam Dad who is a GOLDEN RETRIEVER DOG (NOT a human, NOT a person — he is an ANIMAL, a large golden-furred dog walking upright). He has warm golden fur all over his body, a dog snout/muzzle, floppy dog ears, and a wagging tail. He wears a dark navy jacket over a simple shirt. He has a warm gentle dog smile. IMPORTANT: Sam Dad must look like a golden retriever dog, not a human man."
TINA_MOM = "Tina Mom who is a BLACK-AND-WHITE COW (NOT a human, NOT a person — she is an ANIMAL, a cow walking upright). She has black and white spotted fur pattern all over, small curved horns, cow ears, and hooves. She wears an elegant cream knit cardigan over a floral skirt. She has a gentle warm cow smile. IMPORTANT: Tina Mom must look like a cow, not a human woman."
NOMI = "a raccoon (NOMI) with grey-brown fur, distinctive black eye mask markings, and a ringed bushy tail. She wears a blue-and-white horizontally striped sweater. She has clever bright eyes and nimble paws."
NONO = "a small red bird (NONO) with bright red feathers all over, round bright eyes, and an orange-yellow beak. He has exactly TWO wings and TWO small bird feet with talons. NO ARMS, NO HANDS — birds do not have arms or hands, only wings."
COCO = "a red panda (Coco) with reddish-brown fur, a round cute face with typical red panda markings, big round shiny eyes, and a fluffy ringed tail. She wears a yellow scarf around her neck."

STYLE = "Pixar 3D animation style, warm soft lighting, children's picture book quality, vibrant colors, detailed textures. The bottom 20% of the image should have natural gradual darkening/vignette. NO TEXT, NO WORDS, NO LETTERS anywhere in the image. Pure illustration only."
SIZE = "1024x1536"

# All pages to generate
PAGES = {
    "story38": [
        (2, f"A warm spring afternoon in a little garden full of blooming flowers and fluttering butterflies. {BUBU}, {NOMI}, {NONO}, and {COCO} are playing together happily in the garden. Bright colorful flowers everywhere, butterflies in the air. {STYLE}"),
        (3, f"In the garden, {BUBU} has just spat on the ground and is lifting her little foot to step on the spit, looking down with a mischievous giggle. Her expression is playful and naughty. The garden background with flowers. {STYLE}"),
        (4, f"In the garden, {NOMI} is kneeling down gently in front of {BUBU}, frowning slightly with a concerned expression, talking to Bubu about not spitting. Bubu looks a bit surprised. Flowers in background. {STYLE}"),
        (5, f"{NONO} is perched on a flower branch nearby, pouting with his beak, looking disgusted, wings slightly spread as if about to fly away. Garden background with flowers. {STYLE}"),
        (6, f"In the garden, {COCO} is stepping backward with a disapproving head shake, looking at Bubu with a gentle but firm expression. Flowers in background. {BUBU} is visible nearby. {STYLE}"),
        (7, f"{BUBU} stands alone in the little garden, looking sad and lonely. Her lip is trembling, eyes red and teary. All her friends have moved away. Empty garden around her with flowers but no other characters nearby. Emotional scene. {STYLE}"),
        (8, f"{TINA_MOM} is gently picking up {BUBU} and holding her in her arms, speaking warmly to her. Bubu looks up at Mom with slightly teary eyes but listening. Garden background. {STYLE}"),
        (9, f"{SAM_DAD} is kneeling down to Bubu's eye level, patting {BUBU}'s head gently with his big golden paw. He has a warm, patient expression. Garden background. {STYLE}"),
        (10, f"{BUBU} is nodding earnestly with a determined expression, eyes still slightly red but looking resolute. She's making a promise. Garden background with warm sunlight. {STYLE}"),
        (11, f"Happy reunion scene in the garden. {NOMI} is holding {BUBU}'s hand, {NONO} is flying back to land on Bubu's head, and {COCO} is running towards them excitedly. Everyone is smiling and happy. Flowers blooming, bright sunshine. {STYLE}"),
        (12, f"Close-up of {BUBU} pressing her lips tightly together with a determined expression, resisting the urge to spit. Her cheeks are puffed slightly, she's telling herself 'no'. Garden background. {STYLE}"),
        (13, f"Big celebration scene! {BUBU} is in the center smiling proudly showing two bunny teeth. {NOMI} is clapping, {NONO} is singing overhead, {COCO} is giving thumbs up. {SAM_DAD} and {TINA_MOM} are hugging Bubu from behind, all smiling happily. Garden with flowers, warm golden sunlight. {STYLE}"),
    ],
    "story39": [
        (2, f"Early morning sunrise. {SAM_DAD} is loading a tent, folding chairs and picnic basket into a car. {BUBU} holds a little water bottle, bouncing excitedly. {NOMI} carries a blanket. {NONO} stands on the car roof directing. {COCO} wears a small backpack. Everyone excited for camping. Spring clothing. {STYLE}"),
        (3, f"Arriving at a beautiful lake. Blue sky, white clouds, crystal-clear lake water reflecting like a mirror. {TINA_MOM} holds {BUBU}'s hand. Bubu has her mouth wide open in awe, eyes sparkling at the beautiful scenery. Mountains in distance. Spring day. {STYLE}"),
        (4, f"Funny camping scene. {SAM_DAD} is under a collapsed tent that fell on his head, with a tent pole sticking up on top of his head. He's laughing. {BUBU} is laughing hysterically beside him. The tent is half-assembled and wobbly. Lakeside background. {STYLE}"),
        (5, f"{BUBU} and {NOMI} squatting by the lake shore, looking at small fish swimming in clear water. Bubu reaches toward the water excitedly. NOMI gently holds her back. Bubu holds a round stone in one hand. Lake and green nature background. {STYLE}"),
        (6, f"By the lake, {COCO} is pointing at the lake teaching Bubu English words. {BUBU} tilts her head cutely. {NONO} flaps his wings nearby joining in. Sunny sky, lake in background. Learning moment. {STYLE}"),
        (7, f"{BUBU} spinning in a circle with arms spread wide, looking joyful. {COCO} clapping happily nearby. Green grass, lake in background, trees around. Bubu's ears flowing in the spin. Bright spring day. {STYLE}"),
        (8, f"Peaceful lakeside noon rest. Family sitting in folding chairs. {SAM_DAD} in a sun hat, eyes squinted comfortably. {TINA_MOM} leaning back smiling at lake. {NOMI} curled up reading a book beside a chair. {NONO} on a chair back yawning. Warm sunlight, gentle breeze, lake sparkling. {STYLE}"),
        (9, f"Picnic scene by the lake. {TINA_MOM} has opened a picnic basket with sandwiches, fruit and juice. {BUBU} biting into a sandwich happily. {COCO} holding juice. {NOMI} adding cucumber to her sandwich. {NONO} flying to a tree branch with a blueberry in his beak. Lakeside background. {STYLE}"),
        (10, f"Soft afternoon light. {BUBU} lying in a small chair next to {SAM_DAD}, holding a small stone, looking peaceful and sleepy. {COCO} sitting nearby. Lake in background, golden warm light. Peaceful, serene atmosphere. {STYLE}"),
        (11, f"Beautiful sunset scene by the lake. The lake surface is golden, reflecting the setting sun behind distant mountains. The whole family ({SAM_DAD}, {TINA_MOM}, {BUBU}, {NOMI}, {NONO}, {COCO}) sitting together by the lake watching the sunset. Bubu leaning against Mom. Orange-gold sky. {STYLE}"),
        (12, f"Night time, inside a car. {SAM_DAD} packing tent in background. {BUBU} hugging {NOMI} climbing into the back seat. {COCO} and {NONO} hopping in. Stars twinkling outside the car windows. Dark blue sky. {STYLE}"),
        (13, f"{BUBU} asleep in the car back seat with a small smile, still clutching a little stone. {NOMI} gently tucking a blanket over her. {NONO} quietly standing guard on the headrest. {COCO} nearby whispering goodnight. Big round moon visible through the car window. Warm, tender nighttime scene. {STYLE}"),
    ],
    "story40": [
        (2, f"Early summer afternoon in a lush green park. {BUBU} in her pink dress running across the grass with arms spread wide, ears flowing in the breeze. She looks ecstatic, like a little cotton candy ball. Bright green grass, warm sunshine. Summer clothing. {STYLE}"),
        (3, f"Park scene. {SAM_DAD} sitting on a bench watching Bubu run. {TINA_MOM} standing nearby smiling, taking photos with phone. {NOMI} crouching on grass observing a ladybug. {NONO} perched on NOMI's head sunbathing. {COCO} chasing after {BUBU} in the background. Summer day. {STYLE}"),
        (4, f"{BUBU} turning her head back while running, making a silly face at {COCO} who's chasing her. Bubu's foot is about to trip on a small stone on the grass. Dynamic motion, playful moment just before the fall. Park background. {STYLE}"),
        (5, f"{BUBU} has fallen flat on the grass, face down. Her pink dress has grass bits on it, knees dusty, her pink bow slipped to one side. A moment of impact. Green grass park background. {STYLE}"),
        (6, f"Close-up emotional scene. {BUBU} lying on the ground, stunned, lip quivering, eyes red with tears welling up. She's sniffling. Grass around her. Vulnerable, tender moment. {STYLE}"),
        (7, f"{NOMI} kneeling beside fallen {BUBU}, gently touching her ear. {NONO} flying in a circle above. {COCO} tilting head looking at Bubu with concern. None of them are picking her up - they're encouraging but waiting for her to get up herself. Park grass. {STYLE}"),
        (8, f"{SAM_DAD} crouching down to {BUBU}'s eye level as she lies on the grass. His expression is gentle but firm and encouraging. He holds out his big golden paw in front of her but doesn't pull her up. Park background, warm light. {STYLE}"),
        (9, f"{BUBU} pushing herself up from the grass with both small paws, bottom up first, knees lifting off ground, wobbling but determined. She's looking at Dad's eyes with determination. Grass stains on her dress. Getting up by herself moment. {STYLE}"),
        (10, f"{BUBU} standing up, brushing grass and dust off her pink dress. Eyes still slightly red but she didn't cry. {TINA_MOM} giving thumbs up from the side with a proud smile. Park background, warm sunlight. {STYLE}"),
        (11, f"{SAM_DAD} holding up his big golden paw for a high five. {BUBU} reaching up with her small paw to slap it — the moment of contact. Bubu grinning widely showing two bunny teeth. Joyful celebration moment. Park background. {STYLE}"),
        (12, f"Celebration! {COCO} jumping up clapping. {NONO} doing a flip in the air. {NOMI} straightening {BUBU}'s crooked bow on her head. Everyone happy and proud of Bubu. Park with green grass, warm light. {STYLE}"),
        (13, f"Beautiful wide shot from behind. {BUBU} running steadily across the grass, pink dress sparkling in sunlight, ears flowing. {SAM_DAD} and {TINA_MOM} watching her from behind with loving smiles. Warm golden afternoon light, lush green park. Sense of growth and pride. {STYLE}"),
    ],
    "story41": [
        (2, f"Nighttime bedroom scene. Moonlight streaming through the window into {BUBU}'s cozy room. Bubu sleeping soundly hugging a pillow, with a dreamy expression, mumbling about BBQ. Soft blue moonlight, warm cozy room. {STYLE}"),
        (3, f"{SAM_DAD} and {TINA_MOM} peeking through the bedroom doorway, looking at sleeping Bubu. Both suppressing laughter, exchanging amused glances. Warm dim hallway light behind them, moonlit room. {STYLE}"),
        (4, f"Morning sunlight filling the bedroom. {BUBU} sitting up in bed rubbing her eyes, yawning big. {NOMI} leaning on the bedside asking her a question. Bright cheerful morning atmosphere. Summer clothing. {STYLE}"),
        (5, f"Breakfast table scene. {SAM_DAD} smiling mysteriously at {BUBU} whose eyes are lit up with curiosity. {NONO} on Dad's shoulder looking secretive with wings slightly raised. Breakfast food on table. Bright morning. {STYLE}"),
        (6, f"Family walking outdoors. {BUBU} sitting in {TINA_MOM}'s arms looking around curiously. {COCO} walking beside them. Bubu guessing excitedly where they're going. Sunny street scene, summer day. {STYLE}"),
        (7, f"Arriving at a beautiful outdoor BBQ garden! Fairy lights hanging from trees, tables full of BBQ ingredients. {BUBU}'s eyes wide with amazement and joy, jumping with ears bouncing up and down. {SAM_DAD}, {TINA_MOM}, {NOMI}, {NONO}, {COCO} all present. Summer evening setting. {STYLE}"),
        (8, f"{SAM_DAD} wearing an apron at the grill, cooking BBQ. {BUBU} standing on a small stool beside him, carefully flipping corn with small tongs. Dad praising her. {NOMI} passing seasonings nearby. Smoke rising from grill, outdoor garden. {STYLE}"),
        (9, f"{COCO} pointing at food on the BBQ grill excitedly, teaching English food words. {BUBU} repeating with enthusiasm. {NONO} standing on Coco's head chirping along. Grilled corn and chicken visible. Outdoor garden, warm light. {STYLE}"),
        (10, f"Everyone sitting together eating BBQ. {BUBU} nibbling a chicken wing with shiny oily mouth. {NOMI} hugging a big corn cob, mouth oily, tail swishing happily. {TINA_MOM} wiping Bubu's mouth. {SAM_DAD}, {NONO}, {COCO} also eating. Outdoor garden, fairy lights. {STYLE}"),
        (11, f"{BUBU} leaning against {TINA_MOM}, patting her round tummy, looking full and satisfied. {SAM_DAD} laughing, telling her about her dream. Bubu's mouth wide open in surprise. Outdoor garden, fairy lights. {STYLE}"),
        (12, f"Joyful scene! {BUBU} dancing with hands and feet, overjoyed. She's hugging {SAM_DAD} and {TINA_MOM}. {NOMI} nearby with glistening emotional eyes. {NONO} and {COCO} celebrating. Outdoor BBQ garden, warm golden light, fairy lights. {STYLE}"),
        (13, f"Sunset scene, orange-red sky. {BUBU} riding on {SAM_DAD}'s back, eyes squinted with a sweet smile, sleepy. {TINA_MOM}, {NOMI}, {NONO}, {COCO} walking alongside. Walking home at golden hour. Warm, dreamy atmosphere. {STYLE}"),
    ],
    "story42": [
        (2, f"Morning at home. {BUBU} bouncing excitedly in summer clothes and a sun hat. {NOMI} helping put the sun hat on Bubu. {COCO} clapping paws excitedly. {SAM_DAD} and {TINA_MOM} preparing to go. Bright cheerful morning, summer day. Excited for the zoo! {STYLE}"),
        (3, f"Grand zoo entrance with a magnificent colorful archway decorated with painted animals. {BUBU} holding {SAM_DAD}'s hand on one side and {TINA_MOM}'s hand on the other, looking up at a tall giraffe statue with wide amazed eyes. {NONO} flying at the top of the archway. {NOMI} and {COCO} nearby. {STYLE}"),
        (4, f"Raccoon exhibit at the zoo! {NOMI} standing at the railing with tail straight up in excitement, looking at raccoons inside the enclosure who are washing things by water. {BUBU} leaning on the railing mesmerized. Raccoons with their typical grey-brown coloring washing food. Zoo setting. {STYLE}"),
        (5, f"A wild raccoon inside the enclosure has walked up to the fence, facing {NOMI} through the railing. Both raccoons tilting their heads at each other curiously. {BUBU} clapping and laughing beside them. Cute encounter moment. Zoo raccoon exhibit. {STYLE}"),
        (6, f"Red panda exhibit at the zoo! {COCO} jumping excitedly. Multiple red pandas in trees - some climbing, some sleeping with fluffy tails curled. {BUBU} looking up at them in wonder. Coco pointing at one on the highest branch. Lush green trees, zoo setting. {STYLE}"),
        (7, f"{BUBU} looking back and forth between a red panda in the tree and {COCO} beside her, comparing them with amazement. Coco proudly touching her yellow scarf. {SAM_DAD} in background laughing, holding up phone for a photo. Zoo red panda exhibit. {STYLE}"),
        (8, f"Zebra feeding area. {BUBU} carefully holding out a carrot to a real zebra. The zebra lowering its head with its long tongue reaching for the carrot. Bubu laughing because it tickled her palm. {TINA_MOM} gently supporting Bubu from behind. Zoo setting. {STYLE}"),
        (9, f"Alpaca feeding area. A fluffy alpaca leaning its face close to {BUBU}, gazing with big gentle eyes. Bubu touching the alpaca's face in wonder. {COCO} also reaching out to touch it. Soft fluffy alpaca fur. Zoo setting, warm light. {STYLE}"),
        (10, f"A magnificent peacock displaying its full tail feathers in a brilliant fan of blue and green with eye-spot patterns. {BUBU} standing in front, mouth agape in awe. {COCO} also stunned beside her. The peacock feathers shimmering with iridescent colors. Zoo setting. {STYLE}"),
        (11, f"Monkey hill at the zoo. Monkeys swinging and jumping between trees. A little monkey at the fence making funny faces (tongue out, eyes crossed) at {BUBU} who is making funny faces back. {NOMI} beside them laughing hard holding her belly. Playful, humorous scene. {STYLE}"),
        (12, f"Lunch break at the zoo. {SAM_DAD} holding popcorn. {BUBU} holding a giant pink cotton candy bigger than her face, taking a bite. {NONO} with his beak stuck in cotton candy, flapping wings in panic. Everyone laughing. Zoo food area, sunny day. {STYLE}"),
        (13, f"Circus/animal show at the zoo. A sea lion balancing a ball on its nose. Dogs in colorful outfits jumping through hoops on stage. {BUBU} clapping enthusiastically. {NOMI} clapping too. {NONO} flying overhead as cheerleader. {COCO} waving a little flag. Audience seating. {STYLE}"),
        (14, f"Giraffe enclosure. A real giraffe lowering its incredibly long neck down, its nose almost touching {BUBU}'s sun hat. Bubu giggling. {TINA_MOM} taking a photo with her phone. Amazing close encounter with the tall giraffe. Zoo setting. {STYLE}"),
        (15, f"Elephant enclosure. A large elephant spraying water from its trunk, creating a spray that catches sunlight forming a small rainbow. {BUBU} looking amazed at the rainbow. {NOMI} hiding behind {SAM_DAD} to avoid getting splashed. Water droplets sparkling. Zoo setting. {STYLE}"),
        (16, f"Zoo gift shop interior with shelves full of plush animal toys. {BUBU} holding a raccoon plushie in one arm and a red panda plushie in the other, offering them to her friends. {NOMI} receiving the raccoon plushie with sparkling emotional eyes. {COCO} hugging the red panda plushie. Warm, touching scene. {STYLE}"),
        (17, f"Sunset, orange-red sky. The family walking out through the zoo gates. {BUBU} carrying raccoon plushie in one arm and red panda plushie in the other. Inside the car, Bubu leaning on {TINA_MOM}'s shoulder, eyelids heavy, falling asleep with a smile. Evening golden light. {STYLE}"),
        (18, f"Dream sequence. All the zoo animals (zebra, alpaca, peacock, monkey, giraffe, elephant) lined up waving at {BUBU}. {NOMI} standing among a group of raccoons, and {COCO} standing among a group of red pandas, both waving at Bubu. Dreamy, magical, soft pastel atmosphere with sparkles and stars. Fantasy dream world. {STYLE}"),
    ],
    "story43": [
        (2, f"Nighttime bedroom scene. {BUBU} lying in bed. {SAM_DAD} leaning over the bed with a mysterious smile, whispering to Bubu about a special trip tomorrow. Warm bedside lamp light, cozy bedroom. {STYLE}"),
        (3, f"{BUBU} sitting up excitedly in bed, guessing where they're going. {SAM_DAD} shaking his head playfully, giving hints about stars and Mars. Cozy bedroom, nighttime. Fun guessing game moment. {STYLE}"),
        (4, f"The family arriving at the Shanghai Astronomy Museum. The magnificent futuristic silver building with curved orbital-shaped architecture, looking like a giant flying saucer. {BUBU} with mouth wide open in awe. {SAM_DAD}, {TINA_MOM}, {NOMI}, {NONO}, {COCO} all present. Bright sunny day, modern architecture. {STYLE}"),
        (5, f"Inside the museum 'Home' exhibition hall. A massive solar system model floating overhead with planets of different sizes. Jupiter is huge. {COCO} pointing up at Jupiter. {BUBU} looking up counting planets. Grand museum interior with dramatic lighting. {STYLE}"),
        (6, f"Museum hall with a giant Foucault pendulum in the center. A golden pendulum bob swinging slowly. {NOMI} kneeling down whispering to {BUBU} who stares wide-eyed at the pendulum. Grand museum interior, dramatic lighting from above. {STYLE}"),
        (7, f"'Universe' exhibition with a huge screen simulating a black hole. Swirling dark vortex with light being pulled in. {NONO} on {BUBU}'s shoulder looking scared. {TINA_MOM} hugging Bubu reassuringly. Dark dramatic lighting with the black hole glow. {NOMI} and {COCO} watching nearby. {STYLE}"),
        (8, f"Simulated spacecraft interior! {BUBU} sitting in the commander's seat raising her paw for countdown. {COCO} beside her calling out commands. {SAM_DAD}, {TINA_MOM}, {NOMI}, {NONO} also seated. Futuristic spacecraft cockpit with control panels and screens showing space. Exciting launch moment. {STYLE}"),
        (9, f"View from inside the spacecraft looking out the window at the red rocky Mars surface. {BUBU} pressing against the window excitedly. {SAM_DAD} giving her a proud smile. Red desert landscape with rocks outside. Futuristic spacecraft interior. {STYLE}"),
        (10, f"'Curious Planet' children's zone with giant fantastical flowers, bizarre alien-like plants, and ice volcanoes. {BUBU} and {COCO} darting through enormous colorful blooms. {NONO} hopping from petal to giant petal. Whimsical alien world atmosphere, vibrant colors. {STYLE}"),
        (11, f"Dome theater interior. Everyone lying back in reclining seats looking up. The domed ceiling shows a stunning starfield with the Milky Way galaxy swirling overhead like a glittering river. {BUBU} reaching up her little paw trying to touch the stars. Magical, immersive atmosphere. {NOMI}, {COCO} nearby in seats. {STYLE}"),
        (12, f"Museum café scene. {BUBU} holding a Saturn-shaped ice cream with colorful rings. {COCO} holding a blue Earth-shaped ice cream. Bubu licking her ice cream happily. Bright cheerful café interior with space decorations. {NOMI} and {NONO} nearby. {STYLE}"),
        (13, f"Nighttime car ride home. {BUBU} pressing against the car window looking at the big moon in the night sky. Then in bed, hugging her pillow, excitedly unable to sleep, eyes wide open with anticipation. Split the scene - cozy bedroom at night, moonlight, excited Bubu in bed. Warm dreamy atmosphere. {STYLE}"),
    ],
}

def generate_image(prompt, output_path):
    """Generate an image via Azure OpenAI API."""
    url = f"{ENDPOINT}?api-version={API_VERSION}"
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }
    body = json.dumps({
        "prompt": prompt,
        "n": 1,
        "size": SIZE,
        "quality": "medium",
        "output_format": "png",
    }).encode()

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")

    for attempt in range(3):
        try:
            resp = urllib.request.urlopen(req, timeout=120)
            data = json.loads(resp.read())
            b64 = data["data"][0]["b64_json"]
            png_path = output_path.replace(".jpg", ".png")
            with open(png_path, "wb") as f:
                f.write(base64.b64decode(b64))
            # Convert PNG to JPG
            subprocess.run([
                "ffmpeg", "-y", "-i", png_path, "-q:v", "2", output_path
            ], capture_output=True)
            os.remove(png_path)
            size = os.path.getsize(output_path)
            print(f"  ✅ {os.path.basename(output_path)} — {size/1024:.0f}KB")
            return size
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"  ⚠️ Rate limited (attempt {attempt+1}/3), waiting 45s...")
                time.sleep(45)
            else:
                body_text = e.read().decode() if e.fp else ""
                print(f"  ❌ HTTP {e.code}: {body_text[:200]}")
                if attempt < 2:
                    time.sleep(10)
                else:
                    return 0
        except Exception as e:
            print(f"  ❌ Error: {e}")
            if attempt < 2:
                time.sleep(10)
            else:
                return 0

def main():
    total = sum(len(pages) for pages in PAGES.values())
    done = 0
    results = {}

    for story, pages in PAGES.items():
        story_dir = os.path.join(WORKSPACE, story)
        os.makedirs(story_dir, exist_ok=True)
        print(f"\n{'='*60}")
        print(f"📖 {story} ({len(pages)} pages)")
        print(f"{'='*60}")

        for page_num, prompt in pages:
            done += 1
            output = os.path.join(story_dir, f"page-{page_num:02d}.jpg")
            # Skip if already exists
            if os.path.exists(output) and os.path.getsize(output) > 10000:
                size = os.path.getsize(output)
                print(f"  ⏭️  page-{page_num:02d}.jpg exists ({size/1024:.0f}KB) [{done}/{total}]")
                results[f"{story}/page-{page_num:02d}.jpg"] = size
                continue

            print(f"  🎨 Generating page-{page_num:02d}.jpg [{done}/{total}]...")
            size = generate_image(prompt, output)
            results[f"{story}/page-{page_num:02d}.jpg"] = size
            if done < total:
                time.sleep(8)

    # Summary
    print(f"\n{'='*60}")
    print(f"📊 SUMMARY")
    print(f"{'='*60}")
    success = sum(1 for s in results.values() if s > 0)
    failed = sum(1 for s in results.values() if s == 0)
    print(f"Total: {total} | Success: {success} | Failed: {failed}")
    for name, size in sorted(results.items()):
        status = f"{size/1024:.0f}KB" if size > 0 else "FAILED"
        print(f"  {name}: {status}")

if __name__ == "__main__":
    main()
