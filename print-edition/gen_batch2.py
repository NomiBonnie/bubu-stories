#!/usr/bin/env python3
"""Generate missing print-edition illustrations for Stories 49-51."""
import json, os, sys, time, base64, subprocess, urllib.request, urllib.error
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Load API config
with open(os.path.expanduser("~/.config/azure-openai/config.json")) as f:
    cfg = json.load(f)

ENDPOINT = cfg["image2_eastus2_endpoint"]
API_KEY = cfg["image2_eastus2_api_key"]
API_VERSION = "2025-04-01-preview"
URL = f"{ENDPOINT}?api-version={API_VERSION}"

OUTDIR = os.path.dirname(os.path.abspath(__file__))

BUBU = 'a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow. She has a small pink bow centered ON TOP OF HER HEAD between her two ears (not on left ear, not on right ear, not behind — exactly centered on top between the ears). She has a toddler-like round body proportion.'
SAM_DAD = 'Sam Dad who is a GOLDEN RETRIEVER DOG (NOT a human — he is an ANIMAL, a large golden-furred dog walking upright). He has warm golden fur, a dog snout/muzzle, floppy dog ears, and a wagging tail. He wears a dark navy jacket over a simple shirt. He has a warm gentle dog smile.'
TINA_MOM = 'Tina Mom who is a BLACK-AND-WHITE COW (NOT a human — she is an ANIMAL, a cow walking upright). She has black and white spotted fur pattern all over, small curved horns, cow ears, and hooves. She wears an elegant cream knit cardigan over a floral skirt. She has a gentle warm cow smile.'
NOMI = 'a raccoon (NOMI) with grey-brown fur, distinctive black eye mask markings, and a ringed bushy tail. She wears a blue-and-white horizontally striped sweater. She has clever bright eyes and nimble paws.'
NONO = 'a small red bird (NONO) with bright red feathers, round bright eyes, and an orange-yellow beak. He has exactly TWO wings and TWO small bird feet. NO ARMS, NO HANDS — only wings.'
YANYAN = 'Teacher Yanyan, an orange tabby cat with warm orange fur and subtle stripes, kind green eyes, wearing a pink teacher apron over a light-colored blouse. She is adult-sized, warm and nurturing.'
WAIGONG = 'Grandpa (Waigong), a tall dark-brown horse walking upright, with grey-streaked mane showing his age, deep steady eyes, wearing a polo shirt and casual pants.'
WAIPO = 'Grandma (Waipo), a light grey-white goat walking upright, with small curved horns, kind brown eyes, short goat beard, wearing a floral blouse and light pants with a sun hat.'
BEAR_CLS = 'a brown bear classmate (round and chubby, warm brown fur, slightly bigger than Bubu)'
CORGI_CLS = 'a corgi classmate (tan and white fur, short stubby legs, cute and small)'
GREY_CAT_CLS = 'Feifei, a grey-and-white tabby kitten classmate (grey and white striped fur, same size as Bubu)'

STYLE = 'Pixar 3D animation style, warm soft lighting, children\'s picture book quality. The bottom 20% of the image should have a subtle dark gradient overlay. No text, no words, no letters, no captions anywhere in the image. Pure illustration only.'

# Pages to generate: (story, page_num, scene_prompt)
PAGES = []

# Story 49 page08
PAGES.append((49, 8, f"Indoor scene at a modern tech office. {BUBU} walks in with eyes wide open in wonder, mouth agape. The office has colorful toys on desks and game consoles. {SAM_DAD} kneels down with open arms welcoming her. {WAIGONG} stands behind Bubu. The office is bright, modern, and playful. {STYLE}"))

# Story 50 pages 04-15
s50 = [
    (4, f"Kindergarten classroom. {BUBU} sitting in a small chair but fidgeting — her feet swinging, pulling at {BEAR_CLS}'s sleeve, touching her own ears. {YANYAN} stands at the front near a blackboard, gently telling Bubu to sit down. Other animal classmates sit quietly. {STYLE}"),
    (5, f"Kindergarten classroom. {BUBU} sitting but wiggling in her chair again. {CORGI_CLS} next to her gives a quiet 'shh' gesture. Bubu looks slightly embarrassed with pink cheeks. {YANYAN} is at the front teaching. {STYLE}"),
    (6, f"Kindergarten playground/hallway after class. {NOMI} holds {BUBU}'s hand, talking to her. Bubu tilts her head thinking. A large tree is visible nearby as a visual metaphor. Warm afternoon light. {STYLE}"),
    (7, f"Close-up scene. {NONO} flies above {BUBU}'s head with red wings spread. Bubu sits in a chair practicing the 'little tree' pose — feet flat on ground, hands on knees. {NOMI} watches approvingly nearby. {STYLE}"),
    (8, f"Kindergarten classroom, afternoon. {YANYAN} holds up colorful shape cards at the front. {BUBU} sits perfectly still in her chair like a little tree, feet firmly on ground, hands on knees. She concentrates hard. Other animal classmates around her. {STYLE}"),
    (9, f"Kindergarten classroom. {BUBU} sneaks a glance sideways at {NOMI} who gives her a thumbs up. Bubu takes a deep breath, focusing on {YANYAN}'s shape cards at the front. Bubu is sitting still but with visible effort. {STYLE}"),
    (10, f"Kindergarten classroom, joyful moment. {YANYAN} smiles at the class asking who sat best. All animal classmates point at {BUBU} who has her long ears shooting straight up, rosy cheeks, looking surprised and happy. {BEAR_CLS}, {CORGI_CLS}, and a deer classmate (fawn with white spots) visible. {STYLE}"),
    (11, f"Close-up heartwarming scene. {YANYAN} places a golden star sticker on {BUBU}'s hand. Bubu looks at the sparkling star with pure joy, beaming smile. Warm golden light. {STYLE}"),
    (12, f"Kindergarten gate at pickup time, spring afternoon. {BUBU} runs toward {SAM_DAD} and {TINA_MOM} holding up her hand showing the gold star sticker. Mom kneels to hug her. Dad pats her ears. Flowers and trees around the gate. {STYLE}"),
    (13, f"Walking home on a spring sidewalk with trees and flowers. {NOMI} holds {BUBU}'s hand walking together. {NONO} flies above. Bubu looks up at the sky happily, talking about being a little tree tomorrow. Warm sunset light. {STYLE}"),
    (14, f"Bubu's bedroom at night, moonlight streaming in. {BUBU} lies in bed in soft pajamas, eyes closed, sweet smile, hugging a plushie. The golden star on her hand glimmers in moonlight. A dream bubble shows a little tree covered in pink blossoms with {NOMI} as a raccoon in the tree and {NONO} as a bird perched on a branch. {STYLE}"),
    (15, f"Kindergarten classroom, bright morning. {BUBU} bounces into the classroom and sits perfectly in her chair — feet planted, hands placed properly. {YANYAN} smiles at her approvingly. Bubu nods proudly with a big smile. Spring flowers visible through the window. {STYLE}"),
]
for pnum, prompt in s50:
    PAGES.append((50, pnum, prompt))

# Story 51 pages 02-13
s51 = [
    (2, f"Bright cheerful living room. {BUBU} stands proudly with hands on hips, looking confident. {NOMI} and {NONO} nearby, looking impressed. Warm home interior. The scene conveys Bubu is growing up and learning new skills. {STYLE}"),
    (3, f"Bathroom scene. {BUBU} calls out excitedly. {TINA_MOM} smiles and holds Bubu's hand, leading her toward the bathroom. Bubu looks proud. Clean, bright, child-friendly bathroom visible. {STYLE}"),
    (4, f"Living room. {BUBU} sits on the floor playing with toys, looking slightly confused, touching her tummy. Her expression shows she feels something in her tummy but isn't sure what to do. {NOMI} watches nearby. {STYLE}"),
    (5, f"Bathroom/changing area. {TINA_MOM} gently helps {BUBU} change into clean clothes. Mom has a warm patient smile. Bubu looks a little sheepish but not sad. Clean and bright setting. {STYLE}"),
    (6, f"Cozy scene. {NOMI} pats {BUBU}'s head gently with her raccoon paw, encouraging her. {NONO} flaps his wings beside them cheerfully. Bubu looks up with determined eyes. {STYLE}"),
    (7, f"Living room afternoon. {BUBU} and {NOMI} sit on the floor building a colorful block tower together. Warm sunlight from window. Peaceful, happy scene. {STYLE}"),
    (8, f"Close-up of {BUBU} pausing from playing, touching her tummy with one hand. Her expression shows realization — she remembers mama's words. A small thought bubble or light bulb moment. {STYLE}"),
    (9, f"Living room. {BUBU} shouts with determination, mouth open calling out. {TINA_MOM} rushes in from the kitchen doorway looking surprised and thrilled, with a big joyful smile. {NOMI} and {NONO} look excited. {STYLE}"),
    (10, f"Bright child-friendly bathroom. {TINA_MOM} helps {BUBU} sit on a colorful small child-sized chair. Bubu sits steadily, her little feet dangling. Mom holds her hand supportively. Clean, cheerful bathroom setting. {STYLE}"),
    (11, f"Bathroom scene. {BUBU} sits on a colorful small chair, clapping her little hands with pure joy and excitement. Her face shows triumph and happiness. Bright cheerful atmosphere. {STYLE}"),
    (12, f"Bathroom/living room. {NOMI} and {NONO} rush in to applaud {BUBU}. NONO loops excitedly in the air. {TINA_MOM} smiles warmly. Bubu beams with pride. Celebratory joyful atmosphere. {STYLE}"),
    (13, f"Bubu's bedroom, evening. {BUBU} walks around proudly in clean pajamas, chin up, confident stride. {NOMI} and {NONO} watch her adoringly. Warm bedtime lighting, cozy room. Goodnight atmosphere. {STYLE}"),
]
for pnum, prompt in s51:
    PAGES.append((51, pnum, prompt))

def generate_image(prompt, output_path, retries=3):
    """Call Azure OpenAI image generation API."""
    data = json.dumps({
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
            req = urllib.request.Request(URL, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read())
            
            img_b64 = result["data"][0]["b64_json"]
            png_path = output_path.replace(".jpg", ".png")
            with open(png_path, "wb") as f:
                f.write(base64.b64decode(img_b64))
            
            # Convert to JPG
            subprocess.run(["ffmpeg", "-y", "-i", png_path, "-q:v", "2", output_path],
                         capture_output=True, timeout=30)
            os.remove(png_path)
            
            size_kb = os.path.getsize(output_path) / 1024
            print(f"  ✅ {os.path.basename(output_path)} ({size_kb:.0f}KB)")
            return True
            
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 45
                print(f"  ⚠️ 429 rate limit, waiting {wait}s (attempt {attempt+1}/{retries})")
                time.sleep(wait)
            elif e.code == 400:
                body = e.read().decode()
                if "content_policy" in body.lower() or "safety" in body.lower():
                    print(f"  ❌ Content filter blocked. Retrying with softer prompt...")
                    # Soften the prompt
                    prompt = prompt.replace("potty", "colorful small chair")
                    prompt = prompt.replace("poop", "tummy success")
                    prompt = prompt.replace("Poop", "Tummy success")
                    data = json.dumps({
                        "prompt": prompt, "n": 1, "size": "1024x1536",
                        "quality": "medium", "output_format": "png"
                    }).encode()
                    time.sleep(8)
                else:
                    print(f"  ❌ 400 error: {body[:200]}")
                    return False
            else:
                print(f"  ❌ HTTP {e.code}: {e.read().decode()[:200]}")
                return False
        except Exception as e:
            print(f"  ❌ Error: {e}")
            if attempt < retries - 1:
                time.sleep(10)
            else:
                return False
    return False

def main():
    total = len(PAGES)
    success = 0
    failed = []
    
    for i, (story, page, prompt) in enumerate(PAGES):
        outdir = os.path.join(OUTDIR, f"story{story}")
        os.makedirs(outdir, exist_ok=True)
        outpath = os.path.join(outdir, f"page{page:02d}.jpg")
        
        if os.path.exists(outpath):
            size_kb = os.path.getsize(outpath) / 1024
            print(f"[{i+1}/{total}] Story {story} P{page:02d} — already exists ({size_kb:.0f}KB), skipping")
            success += 1
            continue
        
        print(f"[{i+1}/{total}] Story {story} P{page:02d} — generating...")
        if generate_image(prompt, outpath):
            success += 1
        else:
            failed.append(f"story{story}/page{page:02d}")
        
        if i < total - 1:
            time.sleep(8)
    
    print(f"\n{'='*40}")
    print(f"Done: {success}/{total} succeeded")
    if failed:
        print(f"Failed: {', '.join(failed)}")
    
    # Report sizes
    print(f"\nFile sizes:")
    for story in [49, 50, 51]:
        d = os.path.join(OUTDIR, f"story{story}")
        if os.path.isdir(d):
            files = sorted(os.listdir(d))
            total_kb = sum(os.path.getsize(os.path.join(d, f)) for f in files if f.endswith('.jpg')) / 1024
            print(f"  story{story}/: {len([f for f in files if f.endswith('.jpg')])} files, {total_kb:.0f}KB total")

if __name__ == "__main__":
    main()
