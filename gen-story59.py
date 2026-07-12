#!/usr/bin/env python3
"""Generate all images for Story 59: Bubu's Third Birthday"""
import json, urllib.request, base64, subprocess, time, os, sys

ENDPOINT = "https://kaixi-mmimphd8-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-image-2/images/generations"
API_KEY = "G0XzcVpk6KUGX53HbGfW6nBFiU4yh4Wjfowo8BSseYoSL8HAL9E4JQQJ99CCACHYHv6XJ3w3AAAAACOGJIkM"
API_VERSION = "2025-04-01-preview"
OUTDIR = os.path.expanduser("~/.openclaw/workspace/bubu-stories/public/images/story59")
os.makedirs(OUTDIR, exist_ok=True)

S = "Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition 1024x1536."

# Character inline descriptions
BUBU = "a small white rabbit toddler (snow-white fur, exactly two long ears with pink insides, big round brown eyes, small pink nose, wearing a pink dress with a pink bow centered on top of her head between her two ears)"
NOMI = "a raccoon (grey-brown fur with black eye mask markings and ringed tail, big round clever eyes, wearing a blue-and-white striped sweater)"
NONO = "a small red bird (bright red feathers, round body, round bright eyes, orange-yellow beak)"
DAD = "a golden retriever dog dad (golden fur, big warm build, wearing a casual summer polo shirt, kind gentle smile)"
MOM = "a cow mom (black-and-white patches, medium-large build, elegant, wearing a stylish summer dress, gentle expression)"
WAIGONG = "an elderly horse grandpa (dark brown coat, grey-white mane, deep calm eyes, wearing polo shirt and casual pants, tall dignified)"
WAIPO = "an elderly goat grandma (light grey-white fur, small curved horns, short goatee, warm brown eyes, wearing floral blouse, plump warm)"
YEYE = "a cute chubby light-green dinosaur grandpa (smooth round body, big round gentle eyes, not scary, very cute and round, wearing polo shirt and casual pants, shorter than dad but stout)"
NAINAI = "a gentle light-brown monkey grandma (soft short fur, warm peach-colored face, loving big eyes, wearing a Chinese-style floral top, small and nimble)"
GANMA = "a tall elegant pink flamingo godmother (classic pink feathers, long pink legs, wearing an elegant summer dress)"
XIAOQIAO = "a young light-pink flamingo girl (lighter pink feathers, a bit bigger than Bubu, wearing a cute pink dress with a small bow, lively)"
ZHUZHU = "a white sheep girl (cloud-like curly white wool, wearing a light blue vest, brown little hooves, pink nose, same size as Bubu)"

PROMPTS = [
    # Page 01 - Cover
    f'Pixar 3D animation style, cinematic children\'s picture book cover poster, warm golden lighting, vertical portrait 1024x1536. TOP: Large elegant 3D golden embossed letters spelling "Bubu\'s Third Birthday" with small stars and hearts, Disney movie poster title style. CENTER: {BUBU} — wearing a birthday crown, arms raised joyfully, surrounded by colorful balloons and confetti. Behind her: {DAD} and {MOM} on either side. Left: {YEYE} and {NAINAI}. Right: {WAIGONG} and {WAIPO}. LOWER: {GANMA} and {XIAOQIAO} on one side, {ZHUZHU} on the other. BOTTOM CORNER: {NOMI} and {NONO}. BACKGROUND: festive living room with birthday decorations, a big blue trampoline visible, pink birthday cake with 3 candles. Rich layered movie poster depth with bokeh.',

    # Page 02 - Morning surprise
    f'{S} {BUBU} sitting up in bed, eyes wide with wonder, mouth open in joyful gasp. Bedroom filled with colorful floating balloons (red, yellow, blue, pink, green) and a rainbow streamer hanging from the doorway. Morning sunlight streams through the window. Summer bedroom.',

    # Page 03 - Parents greeting
    f'{S} Bright festive living room with balloons and streamers. {MOM} lifting {BUBU} up and spinning her around, both laughing joyfully. {DAD} stands beside them, one paw reaching to rub Bubu\'s ear, smiling warmly. Summer morning light.',

    # Page 04 - Yeye and Nainai arrive
    f'{S} At the front door. {YEYE} crouching down at the doorway, reaching his short dinosaur arms toward {BUBU} who looks up curiously. {NAINAI} stands beside Yeye, eyes full of love, smiling. {DAD} stands behind Bubu. Doorway decorated with birthday balloons.',

    # Page 05 - Yeye holds Bubu
    f'{S} {YEYE} holding {BUBU} in his short sturdy dinosaur arms, hugging tightly, both smiling with eyes closed. {NAINAI} beside them, reaching her nimble monkey hand to pat Bubu\'s head, eyes crinkled with loving smile. Warm indoor lighting, festive living room.',

    # Page 06 - Ganma and Xiaoqiao arrive
    f'{S} At the front door. {GANMA} standing tall and elegant. {XIAOQIAO} bouncing excitedly, holding {BUBU}\'s hand. {MOM} greeting them warmly. Birthday decorations visible. Bright summer daylight from outside.',

    # Page 07 - Zhuzhu arrives with cake
    f'{S} {ZHUZHU} running ahead giving {BUBU} a big hug. Behind them, two adult sheep (Zhuzhu\'s parents) carry a large cake box. Pink frosted cake visible with 3 candles and a sugar bunny on top. Festive living room. {NOMI} and {NONO} watching.',

    # Page 08 - Unwrapping trampoline
    f'{S} Sunny backyard. {BUBU} standing before a newly unwrapped big blue trampoline, eyes perfectly round with shock and joy, mouth in a big O. Torn wrapping paper and a big bow on the ground. {XIAOQIAO} beside her excitedly pointing at the trampoline. {GANMA} watching proudly in background. Bright summer sunshine.',

    # Page 09 - Bouncing on trampoline (KEY scene)
    f'{S} {BUBU} and {XIAOQIAO} holding hands bouncing high on a big blue trampoline, both laughing with pure joy. Bubu\'s long white ears flapping in the air. {NOMI} standing beside the trampoline clapping hands. {NONO} flying in circles around them. Other characters cheering in background. Bright sunny day, dynamic action pose.',

    # Page 10 - Fishing rod gift
    f'{S} {DAD} crouching down presenting a small fishing rod to {BUBU}. Bubu holds the fishing rod up excitedly, waving it with a huge grin. {MOM} standing beside smiling. Long gift box open on the floor. Festive living room, summer afternoon light.',

    # Page 11 - Birthday song
    f'{S} Large round dining table with pink birthday cake with 3 lit candles in center. {BUBU} sitting in center. Around: {DAD} and {MOM} beside Bubu, {YEYE} and {NAINAI}, {WAIGONG} and {WAIPO}, {GANMA} and {XIAOQIAO}, {ZHUZHU} and two adult sheep parents. Everyone singing happily. {NOMI} and {NONO} present. Warm golden indoor lighting.',

    # Page 12 - Making a wish
    f'{S} Close-up. {BUBU} with eyes closed, hands together in front of chest, making a wish. Three lit candles on pink cake in front of her, warm candlelight on her face. Peaceful concentration. Soft bokeh of family watching tenderly in background.',

    # Page 13 - Eating cake, grandpa funny
    f'{S} {BUBU} with pink frosting all over her little mouth, laughing hard. {YEYE} has a blob of pink cream on his round green dinosaur nose, making a silly face. {NAINAI} wiping Yeye\'s nose with a napkin, laughing. Everyone at the table laughing. Pink cake partially eaten. Warm joyful atmosphere.',

    # Page 14 - Family dinner
    f'{S} Big round dinner table full of colorful dishes. {BUBU} between {DAD} and {MOM}. One side: {YEYE} and {NAINAI}. Other side: {WAIGONG} and {WAIPO}. Across: {GANMA}, {XIAOQIAO}, {ZHUZHU} and two adult sheep parents. {NOMI} near Bubu, {NONO} perched on table edge. Warm evening indoor lighting, everyone eating happily.',

    # Page 15 - Guests leaving
    f'{S} Front door, evening. {ZHUZHU} and {BUBU} doing a pinky promise. {XIAOQIAO} kissing Bubu\'s forehead. Background: {NAINAI} waiting with arms open, {YEYE} beside her. {GANMA} and adult sheep parents at door. Warm golden light from inside, blue evening sky outside. Bittersweet farewell.',

    # Page 16 - Bedtime ending
    f'{S} Cozy bedroom at night, warm dim nightlight. {BUBU} lying in bed under soft blanket, eyes half-closed with peaceful smile. {NOMI} sitting on bed edge, holding Bubu\'s hand gently. {NONO} perched on pillow beside Bubu\'s head. Nightstand has a small birthday crown and tiny cake piece. Moonlight through window. Blue trampoline and fishing rod visible in room corner. Peaceful perfect ending.',
]

def generate_image(page_num, prompt):
    outfile = os.path.join(OUTDIR, f"page-{page_num:02d}.jpg")
    if os.path.exists(outfile):
        size = os.path.getsize(outfile) // 1024
        print(f"⏭️  Page {page_num} exists ({size}KB), skip")
        return True

    print(f"🎨 Page {page_num}...", flush=True)
    data = json.dumps({
        "prompt": prompt,
        "n": 1,
        "size": "1024x1536",
        "quality": "medium",
        "output_format": "png"
    }).encode()

    req = urllib.request.Request(
        f"{ENDPOINT}?api-version={API_VERSION}",
        data=data,
        headers={"Content-Type": "application/json", "api-key": API_KEY}
    )

    for attempt in range(3):
        try:
            resp = urllib.request.urlopen(req, timeout=180)
            result = json.loads(resp.read())
            b64 = result["data"][0]["b64_json"]
            png_path = outfile.replace(".jpg", ".png")
            with open(png_path, "wb") as f:
                f.write(base64.b64decode(b64))
            subprocess.run(["ffmpeg", "-y", "-i", png_path, "-q:v", "4", outfile],
                         capture_output=True)
            os.remove(png_path)
            size = os.path.getsize(outfile) // 1024
            print(f"✅ Page {page_num} done ({size}KB)")
            return True
        except Exception as e:
            print(f"⚠️  Page {page_num} attempt {attempt+1} failed: {e}")
            if attempt < 2:
                time.sleep(10)
    print(f"❌ Page {page_num} FAILED after 3 attempts")
    return False

failed = []
for i, prompt in enumerate(PROMPTS):
    page = i + 1
    ok = generate_image(page, prompt)
    if not ok:
        failed.append(page)
    if page < len(PROMPTS):
        time.sleep(8)

print(f"\n🎉 Generation complete!")
if failed:
    print(f"❌ Failed pages: {failed}")
else:
    print("✅ All 16 pages generated successfully!")

# List files
for f in sorted(os.listdir(OUTDIR)):
    fp = os.path.join(OUTDIR, f)
    print(f"  {f}: {os.path.getsize(fp)//1024}KB")
