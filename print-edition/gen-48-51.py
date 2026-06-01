#!/usr/bin/env python3
"""Generate print-edition illustrations for stories 48-51."""
import json, os, sys, time, base64, subprocess, urllib.request, urllib.error

# Load API config
with open(os.path.expanduser("~/.config/azure-openai/config.json")) as f:
    cfg = json.load(f)
ENDPOINT = cfg["image2_eastus2_endpoint"]
API_KEY = cfg["image2_eastus2_api_key"]
API_VERSION = "2025-04-01-preview"
URL = f"{ENDPOINT}?api-version={API_VERSION}"

BUBU = "a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow. She has a small pink bow centered ON TOP OF HER HEAD between her two ears. She has a toddler-like round body proportion."
SAM_DAD = "Sam Dad who is a GOLDEN RETRIEVER DOG (NOT a human — he is an ANIMAL, a large golden-furred dog walking upright). He has warm golden fur, a dog snout/muzzle, floppy dog ears, and a wagging tail. He wears a dark navy jacket over a simple shirt. He has a warm gentle dog smile."
TINA_MOM = "Tina Mom who is a BLACK-AND-WHITE COW (NOT a human — she is an ANIMAL, a cow walking upright). She has black and white spotted fur pattern, small curved horns, cow ears, and hooves. She wears an elegant cream knit cardigan over a floral skirt. She has a gentle warm cow smile."
NOMI = "a raccoon (NOMI) with grey-brown fur, distinctive black eye mask markings, and a ringed bushy tail. She wears a blue-and-white horizontally striped sweater. She has clever bright eyes and nimble paws."
NONO = "a small red bird (NONO) with bright red feathers, round bright eyes, and an orange-yellow beak. He has exactly TWO wings and TWO small bird feet with talons. NO ARMS, NO HANDS — only wings."
YANYAN = "Teacher Yanyan who is an ORANGE TABBY CAT (warm orange fur with subtle stripes, gentle green eyes). She wears a kindergarten teacher apron over a pink top. She is medium-sized, warm and kind."
FEIFEI = "Feifei who is a grey-and-white kitten with droopy ears, small and shy."
WAIGONG = "Grandpa (Waigong) who is a dark brown HORSE walking upright, with grey-white mane showing age, steady deep eyes. He wears a polo shirt and casual pants."
WAIPO = "Grandma (Waipo) who is a light grey-white GOAT walking upright, with small curved horns, warm brown eyes. She wears a floral blouse and light pants."
BEAR_KID = "a brown bear cub classmate, round and chubby"
CORGI_KID = "a corgi puppy classmate, short-legged and chubby"
CAT_KID = "a grey-white tabby kitten classmate"
DEER_KID = "a young fawn classmate with white spots"

STYLE = "Pixar 3D animated style, warm soft lighting, children's picture book quality. Vertical composition 2:3 ratio. Pure illustration with NO text, NO words, NO letters, NO numbers anywhere. The bottom 20% of the image should be subtly darkened with a gentle gradient for text overlay."
SUMMER_NOTE = "Summer clothing: light short-sleeve outfits, cool and comfortable."

def gen_image(prompt, outpath, attempt=0):
    if os.path.exists(outpath):
        sz = os.path.getsize(outpath)
        if sz > 50000:
            print(f"  SKIP {outpath} (exists, {sz} bytes)")
            return True
    
    body = json.dumps({"prompt": prompt, "n": 1, "size": "1024x1536", "quality": "medium"}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json", "api-key": API_KEY})
    
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        data = json.loads(resp.read())
        b64 = data["data"][0]["b64_json"]
        png_path = outpath.replace(".jpg", ".png")
        with open(png_path, "wb") as f:
            f.write(base64.b64decode(b64))
        subprocess.run(["ffmpeg", "-y", "-i", png_path, "-q:v", "2", outpath], capture_output=True)
        os.remove(png_path)
        sz = os.path.getsize(outpath)
        print(f"  OK {outpath} ({sz} bytes)")
        return True
    except urllib.error.HTTPError as e:
        if e.code == 429 and attempt < 3:
            print(f"  429 rate limit, waiting 45s (attempt {attempt+1})...")
            time.sleep(45)
            return gen_image(prompt, outpath, attempt + 1)
        elif e.code == 400:
            body_text = e.read().decode()
            print(f"  CONTENT_FILTER {outpath}: {body_text[:200]}")
            return False
        else:
            print(f"  ERROR {e.code}: {e.read().decode()[:200]}")
            return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

BASE = "bubu-stories/print-edition"

# Story 48 prompts
s48 = [
    (2, f"{STYLE} {SUMMER_NOTE} Scene: A bright kindergarten entrance in the morning. {BUBU} is bouncing happily holding the hand/paw of {SAM_DAD}. Her ears are standing tall with excitement. The kindergarten gate is colorful and welcoming with summer flowers."),
    (3, f"{STYLE} {SUMMER_NOTE} Scene: {SAM_DAD} walking with a backpack. {NOMI} is riding on top of the backpack, peeking out curiously. {NONO} flies ahead with wings spread, red feathers glinting in morning sunlight. Kindergarten courtyard with other animal children in background."),
    (4, f"{STYLE} {SUMMER_NOTE} Scene: Inside a bright kindergarten classroom. {BUBU} and {SAM_DAD} sit facing each other at a small table with breakfast food (little buns, milk). Bubu holds up a small bun toward Dad with a sweet smile. Warm cozy atmosphere."),
    (5, f"{STYLE} {SUMMER_NOTE} Scene: Kindergarten playground. {BUBU} holds {SAM_DAD}'s hand, looking up with wide curious eyes. {YANYAN} stands nearby gesturing toward something exciting. Other animal kids and parents gathered around. Bubu asks about a surprise."),
    (6, f"{STYLE} {SUMMER_NOTE} Scene: A group of colorful inflatable dinosaur costumes bursting through a door onto a playground! Green, orange, purple dinosaurs with big tails and little claws. {BUBU} stands in the foreground with mouth wide open in amazement. {SAM_DAD} behind her, also surprised. Fun and silly atmosphere."),
    (7, f"{STYLE} {SUMMER_NOTE} Scene: A big green dinosaur costume bending down toward {BUBU}. Through the costume opening, we can glimpse {YANYAN} (orange tabby cat) inside. Bubu is laughing hard, recognizing her teacher. Other dinosaur costumes in background."),
    (8, f"{STYLE} {SUMMER_NOTE} Scene: A line of dinosaur-costumed teachers doing a funny dance on the playground, tails swinging. {BUBU} and other animal children ({BEAR_KID}, {CORGI_KID}, {CAT_KID}, {DEER_KID}) laughing hysterically. Parents clapping. {NOMI} laughing on a backpack, {NONO} spinning in the air laughing."),
    (9, f"{STYLE} {SUMMER_NOTE} Scene: A big circle dance on the playground. {BUBU} holds {SAM_DAD}'s hand on one side and {BEAR_KID}'s paw on the other. Everyone in a circle holding hands, dancing to music. Bubu's pink dress twirling like a flower. Joyful festive atmosphere."),
    (10, f"{STYLE} {SUMMER_NOTE} Scene: Colorful streamers and confetti exploding in the sky — red, blue, gold ribbons falling like rainbow rain. {BUBU} looks up with hands outstretched to catch ribbons. {NONO} has a golden streamer landed on his head. Magical celebratory moment."),
    (11, f"{STYLE} {SUMMER_NOTE} Scene: A large colorful rainbow-striped fabric strip laid across the playground ground. {BUBU} is on all fours at the start, ready to crawl across. {YANYAN} (in teacher outfit, no longer in dinosaur costume) encourages from the side. Other animal kids watching."),
    (12, f"{STYLE} {SUMMER_NOTE} Scene: {BUBU} crawling determinedly across a colorful fabric strip on the ground. {SAM_DAD} claps beside her. {NOMI} stands at the finish line waving a small flag. Bubu is almost at the end, looking determined and happy. Triumphant moment."),
    (13, f"{STYLE} {SUMMER_NOTE} Scene: {YANYAN} (orange tabby cat teacher) kneeling down, handing two shiny dinosaur stickers to {BUBU}. Bubu receives them carefully with sparkling starry eyes. Indoor classroom setting."),
    (14, f"{STYLE} {SUMMER_NOTE} Scene: {BUBU} standing on tiptoes, placing a dinosaur sticker on {SAM_DAD}'s hand/paw. She has one sticker on her own hand. Dad looks down at the sticker with emotional teary eyes, about to hug Bubu. Warm tender moment."),
    (15, f"{STYLE} {SUMMER_NOTE} Scene: Golden sunset. {BUBU} rides on {SAM_DAD}'s shoulders, clutching her sticker hand. {NOMI} walks alongside with tail swaying. {NONO} perches on Dad's head. Walking home on a tree-lined path bathed in golden evening light. Warm, peaceful, beautiful."),
    (16, f"{STYLE} {SUMMER_NOTE} Scene: Nighttime bedroom. {BUBU} lies in a small bed, holding up her hand to look at the dinosaur sticker in soft moonlight. She has a tiny peaceful smile. Cozy room with stuffed animals. Dreamy, gentle atmosphere."),
]

# Story 49 prompts
s49 = [
    (2, f"{STYLE} {SUMMER_NOTE} Scene: Kindergarten classroom morning. {FEIFEI} sits in a corner crying, ears drooping, tears falling. {YANYAN} kneels beside her, gently patting her back. Other animal children in the background at their seats."),
    (3, f"{STYLE} {SUMMER_NOTE} Scene: {BUBU} sits calmly in her small chair, ears standing tall, watching quietly. {NOMI} sits beside her whispering. Bubu looks calm and mature, not crying. Classroom setting with other kids."),
    (4, f"{STYLE} {SUMMER_NOTE} Scene: {BUBU} sitting bravely at her desk, raising her hand to answer a question. {NONO} perches proudly on her head. {YANYAN} at the front teaching. Other kids including {FEIFEI} in background. Bubu looks confident."),
    (5, f"{STYLE} {SUMMER_NOTE} Scene: Kindergarten gate at pickup time. {BUBU} runs with her little backpack toward {WAIGONG} (dark brown horse) and {WAIPO} (light grey-white goat) who stand waiting with open arms. Afternoon sunshine. Bubu leaps toward Grandpa joyfully."),
    (6, f"{STYLE} {SUMMER_NOTE} Scene: {WAIPO} holds {BUBU}'s hand, smiling warmly. Bubu puffs up her chest proudly. {WAIGONG} gives a big thumbs up. Outdoor kindergarten gate area. Bubu looks very proud of herself."),
    (7, f"{STYLE} {SUMMER_NOTE} Scene: Inside a car. {BUBU} presses her face against the car window, looking excitedly at approaching city buildings. {WAIGONG} (dark brown horse) drives. Bubu is eager and excited."),
    (8, f"{STYLE} {SUMMER_NOTE} Scene: A modern office space with toys and game consoles on desks. {BUBU} stands at the entrance with wide amazed eyes, mouth open in wonder. {SAM_DAD} kneels with open arms welcoming her. Bright, fun office environment."),
    (9, f"{STYLE} {SUMMER_NOTE} Scene: Several animal colleagues (various species — a fox, a bear, a deer) gathered around {BUBU}, bending down to greet her warmly. Bubu hides shyly behind {SAM_DAD}'s legs, peeking out with half her face. Cute shy moment in an office."),
    (10, f"{STYLE} {SUMMER_NOTE} Scene: {BUBU} sits in a big office swivel chair, feet dangling, happily playing a game console. {NOMI} beside her pressing buttons helpfully. {NONO} flying in front of the screen excitedly. Fun playful office scene."),
    (11, f"{STYLE} {SUMMER_NOTE} Scene: Evening street. {BUBU} leans out of a car window waving wildly. In the distance, {TINA_MOM} (black-and-white cow) stands by the roadside, visible and recognizable. City evening lights."),
    (12, f"{STYLE} {SUMMER_NOTE} Scene: {BUBU} jumps into {TINA_MOM}'s arms, looking up with sparkling eyes. Mom hugs her tightly with tears of joy. Emotional, warm reunion moment on the street at dusk."),
    (13, f"{STYLE} {SUMMER_NOTE} Scene: Cozy bedroom. {BUBU} in soft pajamas lies in bed. {TINA_MOM} sits beside her, gently patting her. Warm nightlight. Peaceful bedtime scene. Bubu looks content and sleepy."),
    (14, f"{STYLE} {SUMMER_NOTE} Scene: Close-up of bed. {BUBU} hugs a small bunny plushie, eyes closed, sweet smile on her face. {NOMI} and {NONO} snuggle beside the pillow. Soft moonlight. Peaceful sleeping scene."),
    (15, f"{STYLE} {SUMMER_NOTE} Scene: A beautiful night sky with one star shining especially bright. Silhouette of a small town below. Magical, dreamy, storybook ending. The bright star symbolizes brave children. Serene and beautiful."),
]

# Story 50 prompts
s50 = [
    (2, f"{STYLE} Spring clothing: light jacket, comfortable. Scene: Spring morning, flowers blooming at kindergarten gate. {BUBU} bounces through the gate with her backpack, waving bye-bye confidently. {NOMI} walks beside her proudly. {NONO} sits on the backpack flapping wings. Parents wave in the background. Cherry blossoms or spring flowers frame the scene."),
    (3, f"{STYLE} Spring clothing. Scene: Classroom. {YANYAN} stands at a blackboard telling a story. All animal children sit quietly — except {BUBU} who is wiggling and squirming in her chair, looking distracted. Her chair seems to creak. Contrast between still kids and restless Bubu."),
    (4, f"{STYLE} Spring clothing. Scene: {BUBU} in her chair, feet swinging, looking left and right. She tugs at {BEAR_KID}'s sleeve, touches her own ears, half-stands to look out the window at birds. {YANYAN} gently gestures for her to sit down. Fidgety toddler energy."),
    (5, f"{STYLE} Spring clothing. Scene: {BUBU} sits down but looks uncomfortable, blushing. {CORGI_KID} beside her whispers 'shh'. Bubu looks embarrassed but honest. Classroom setting."),
    (6, f"{STYLE} Spring clothing. Scene: Outdoor playground after class. {NOMI} holds {BUBU}'s hand, talking to her gently. Bubu tilts her head thinking. A big tree stands nearby as a visual metaphor. Warm teaching moment between friends."),
    (7, f"{STYLE} Spring clothing. Scene: {BUBU} sits in a chair practicing — feet flat on ground, hands on knees, trying to sit still like a tree. {NONO} hovers above with spread wings demonstrating. {NOMI} watches approvingly. Bubu concentrates hard. Practice scene."),
    (8, f"{STYLE} Spring clothing. Scene: Afternoon classroom. {YANYAN} holds up colorful shape cards. {BUBU} sits perfectly still in her chair, feet firmly on the ground, hands on knees, concentrating. Other kids around her. She silently tells herself 'I'm a little tree.' Focused, determined expression."),
    (9, f"{STYLE} Spring clothing. Scene: {BUBU} sneaks a peek sideways at {NOMI}, who gives her a thumbs-up from nearby. Bubu takes a deep breath and refocuses on {YANYAN}'s shape cards. Determination overcoming the urge to fidget. Classroom."),
    (10, f"{STYLE} Spring clothing. Scene: End of class. {YANYAN} asks who sat the best. All the animal children ({BEAR_KID}, {CORGI_KID}, {CAT_KID}, {DEER_KID}) point at {BUBU} and shout her name. Bubu's ears shoot straight up, cheeks rosy with pride and surprise. Joyful classroom moment."),
    (11, f"{STYLE} Spring clothing. Scene: {YANYAN} places a golden star sticker on {BUBU}'s hand. Close-up of the tender moment. Bubu looks at the sparkling star with a beaming smile. Teacher looks proud. Warm classroom light."),
    (12, f"{STYLE} Spring clothing. Scene: Kindergarten gate pickup. {BUBU} runs toward {SAM_DAD} and {TINA_MOM} holding up her hand to show the star sticker. Mom kneels to hug her. Dad pats her ears. Bubu is bursting with pride. Afternoon light."),
    (13, f"{STYLE} Spring clothing. Scene: Walking home on a tree-lined path. {NOMI} holds {BUBU}'s hand. {NONO} flies above. Bubu looks up at the sky saying she'll be a little tree again tomorrow. Spring trees in background. Peaceful, hopeful walk home."),
    (14, f"{STYLE} Scene: Dreamy nighttime. {BUBU} in bed, moonlight catches the star sticker on her hand. Dream visualization: Bubu transformed into a little tree covered in pink blossoms, standing in a classroom. {NOMI} as a raccoon and {NONO} as a bird sit in the tree branches. Magical, whimsical dream sequence."),
    (15, f"{STYLE} Spring clothing. Scene: Next morning. {BUBU} sits perfectly in her kindergarten chair — feet planted, hands placed neatly. {YANYAN} smiles at her. Bubu nods proudly. Other kids around. Morning sunlight streams through windows. Confident, happy ending."),
]

# Story 51 prompts - careful wording for content safety
s51 = [
    (2, f"{STYLE} {SUMMER_NOTE} Scene: {BUBU} stands proudly with hands on hips in a bright living room. She looks confident and growing up. {NOMI} and {NONO} nearby looking proud of her. Warm cheerful atmosphere showing a toddler who's learning new skills."),
    (3, f"{STYLE} {SUMMER_NOTE} Scene: {BUBU} tugs on {TINA_MOM}'s hand/hoof, calling out to her. Mom smiles warmly and holds Bubu's hand, leading her down a hallway toward the bathroom door. Everyday domestic scene, warm and loving."),
    (4, f"{STYLE} {SUMMER_NOTE} Scene: {BUBU} sits on the floor playing with toys, looking a little uncomfortable, touching her tummy with a puzzled expression. {NOMI} watches with slight concern nearby. Living room with scattered toys."),
    (5, f"{STYLE} {SUMMER_NOTE} Scene: {TINA_MOM} gently helps {BUBU} change into fresh clean clothes. Mom smiles patiently and warmly. Bubu looks a little embarrassed but mom is reassuring. Bedroom or bathroom doorway. Gentle parenting moment."),
    (6, f"{STYLE} {SUMMER_NOTE} Scene: {NOMI} gently pats {BUBU}'s head encouragingly. {NONO} flaps wings nearby cheerfully. Bubu looks determined and hopeful. Living room with soft afternoon light. Supportive friends encouraging scene."),
    (7, f"{STYLE} {SUMMER_NOTE} Scene: {BUBU} and {NOMI} sit on the living room floor building a colorful block tower together. Bubu is focused and happy. Afternoon sunlight. Cozy domestic scene with toys scattered around."),
    (8, f"{STYLE} {SUMMER_NOTE} Scene: Close-up of {BUBU} pausing from play, touching her tummy with a thoughtful expression. A thought bubble or memory flash shows Mom's smiling face saying 'remember to call Mama'. Moment of realization."),
    (9, f"{STYLE} {SUMMER_NOTE} Scene: {BUBU} calls out with determination, mouth open calling for mama. {TINA_MOM} rushes from the kitchen doorway with a thrilled surprised expression. Bubu looks proud of herself for remembering. Bright moment of triumph."),
    (10, f"{STYLE} {SUMMER_NOTE} Scene: {TINA_MOM} holds {BUBU}'s hand, walking together toward the bathroom. Bubu walks steadily and confidently beside mom. Hallway with bathroom door visible ahead. Warm domestic scene, milestone moment."),
    (11, f"{STYLE} {SUMMER_NOTE} Scene: {BUBU} sitting on a small colorful child's step stool, looking accomplished and clapping her little hands with joy. Bathroom setting with cheerful tiles. She looks triumphant and proud. Celebratory moment."),
    (12, f"{STYLE} {SUMMER_NOTE} Scene: {NOMI} and {NONO} burst through the doorway clapping and cheering for {BUBU}. {TINA_MOM} smiles warmly behind them. Bubu beams with pride. Joyful celebration of a milestone achievement. Confetti-like sparkles in the air."),
    (13, f"{STYLE} {SUMMER_NOTE} Scene: Evening time. {BUBU} walks proudly around the living room in clean pajamas, chin up, confident stride. {NOMI} and {NONO} watch admiringly. Warm evening light. Bubu looks like she's grown up a little. Peaceful, proud ending scene."),
]

all_tasks = [
    ("story48", s48),
    ("story49", s49),
    ("story50", s50),
    ("story51", s51),
]

# Check which page to start from (for resuming)
start_story = os.environ.get("START_STORY", "story48")
start_page = int(os.environ.get("START_PAGE", "0"))

total = sum(len(pages) for _, pages in all_tasks)
done = 0
failed = []

for story, pages in all_tasks:
    print(f"\n=== {story.upper()} ({len(pages)} pages) ===")
    for page_num, prompt in pages:
        outpath = f"{BASE}/{story}/page-{page_num:02d}.jpg"
        
        # Skip if resuming
        if story < start_story or (story == start_story and page_num < start_page):
            done += 1
            continue
        
        print(f"[{done+1}/{total}] {story} page-{page_num:02d}")
        ok = gen_image(prompt, outpath)
        if not ok:
            failed.append(outpath)
        done += 1
        if ok and done < total:
            time.sleep(8)

print(f"\n=== DONE: {total - len(failed)}/{total} succeeded ===")
if failed:
    print("FAILED:")
    for f in failed:
        print(f"  {f}")
