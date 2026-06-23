#!/usr/bin/env python3
"""Generate images for Story 58: Bubu's New Kindergarten in Shenzhen"""
import json, time, base64, urllib.request, urllib.error, os, sys

API_KEY = "G0XzcVpk6KUGX53HbGfW6nBFiU4yh4Wjfowo8BSseYoSL8HAL9E4JQQJ99CCACHYHv6XJ3w3AAAAACOGJIkM"
ENDPOINT = "https://kaixi-mmimphd8-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-image-2/images/generations?api-version=2025-04-01-preview"
OUT_DIR = "/Users/samyuan/.openclaw/workspace/bubu-stories/public/images/story58"

# Character descriptions
BUBU = "a small white rabbit toddler (snow-white fur, exactly TWO long ears with pink inner sides, large round brown eyes, small pink nose) wearing a pink summer dress with a pink bow centered ON TOP OF HER HEAD between her two ears, toddler proportions"
DAD = "a golden retriever dog dad (golden fur, warm gentle eyes) wearing a casual summer polo shirt and shorts, tall and warm"
MOM = "a black-and-white cow mom (classic dairy cow coloring) wearing a stylish summer floral blouse and skirt, elegant and gentle"
TEACHER_LI = "a giant panda (classic black-and-white panda coloring, round black ears, iconic black eye patches, large round warm eyes) wearing a light pink kindergarten apron, chubby and round"
TEACHER_KATE = "a red fox (reddish-brown fur, white belly, amber eyes, fluffy tail) wearing a light yellow top with white apron, slender and lively"
TEACHER_GAN = "a koala (grey fluffy fur, big round eyes, black nose, round face) wearing a light green kindergarten apron, medium build"
TEACHER_YANZI = "a swallow bird (black back, white belly, distinctive forked swallow tail, small and agile) wearing a light blue apron — NOT red, distinctly black-and-white colored with forked tail"
GRANDPA = "an elderly horse (dark brown fur, grey-white mane showing age) wearing a summer polo shirt and light pants"
GRANDMA = "an elderly goat (light grey-white fur, small curved horns, short goat beard) wearing a summer floral blouse with sun hat"
NOMI = "a raccoon (grey-brown fur with black eye mask markings, ringed tail) wearing a blue-and-white striped sweater, clever bright eyes"
NONO = "a small red bird (bright red feathers, round body, orange-yellow beak, NO ARMS NO HANDS only wings and bird feet) — distinctly red and round, different from the black-white forked-tail swallow teacher"

PREFIX = "Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition 1024x1536. Summer day in Shenzhen, China."

prompts = [
    # Page 01 - Cover
    f"Pixar 3D animation style, cinematic children's picture book cover poster, warm golden summer lighting, vertical portrait 1024x1536. TOP: Elegant hand-lettered title 'Bubu's New Kindergarten' in warm gold and soft pink gradient, with small star sparkles around, positioned at the upper portion of the image. CENTER: {BUBU} standing happily in front of a colorful kindergarten entrance with her arms up in excitement. Around her: {TEACHER_LI} waving warmly on the left, {TEACHER_KATE} on the right with a little guitar, {TEACHER_GAN} peeking from behind with paints, {TEACHER_YANZI} flying gracefully above. BEHIND: {DAD} and {MOM} standing together watching proudly. BOTTOM CORNER: {NOMI} and {NONO} sitting together watching the scene. BACKGROUND: A modern colorful kindergarten building with green trees, summer flowers, blue sky with fluffy clouds. Rich layered movie poster depth composition. Bottom 20% naturally darkened vignette.",

    # Page 02 - Walking to kindergarten
    f"{PREFIX} {BUBU} walking happily between {DAD} holding her left hand and {MOM} holding her right hand, on a tree-lined sidewalk in a modern Shenzhen neighborhood. Bubu is bouncing with a new pink backpack. Morning sunlight streaming through green trees. They're approaching a colorful kindergarten building in the background. Bottom 20% naturally darkened.",

    # Page 03 - Teacher Li greets Bubu
    f"{PREFIX} At the kindergarten gate, {TEACHER_LI} squatting down to meet {BUBU} at eye level, smiling warmly with arms slightly open in welcome. The panda teacher's face is gentle and inviting. Behind Bubu, {DAD} and {MOM} stand watching with proud smiles. Colorful kindergarten decorations and children's artwork visible on the walls. Bottom 20% naturally darkened.",

    # Page 04 - Bubu waves goodbye, enters classroom
    f"{PREFIX} Inside a bright cheerful classroom, {TEACHER_LI} holding {BUBU}'s small hand, walking past small tables and chairs. Bubu looks around curiously with a happy expression, waving back toward the door. Other animal toddlers (a small brown bear, a corgi puppy, a grey-white kitten) are playing with toys in the background. Colorful decorations on walls, small cubbies. Bottom 20% naturally darkened.",

    # Page 05 - Teacher Kate says good morning
    f"{PREFIX} {TEACHER_KATE} approaching {BUBU} in the classroom with a warm smile, holding a small colorful ukulele guitar. The fox teacher's fluffy tail sways gently. Bubu looks up at her with curious big eyes. A colorful 'HELLO' poster and English alphabet on the classroom wall behind them. Other toddlers watching with interest. Bottom 20% naturally darkened.",

    # Page 06 - Singing Head Shoulders Knees and Toes
    f"{PREFIX} {TEACHER_KATE} standing in front of a semicircle of animal toddlers, strumming her ukulele. {BUBU} in the front row touching her head with both paws, eyes curved into happy crescents laughing. Other animal toddlers (bear, corgi, kitten, deer) also doing the actions. A poster with body parts drawings on the wall. Bright classroom. Bottom 20% naturally darkened.",

    # Page 07 - Teacher Gan introduces craft time
    f"{PREFIX} {TEACHER_GAN} standing at a craft table, slowly and carefully laying out colorful paint jars (red, yellow, blue, green) and brushes. {BUBU} standing beside the table wearing a small painting apron that Teacher Gan is tying for her. Other toddlers sitting at the table with paper ready. The koala's movements are gentle and unhurried. Art supplies and children's paintings on walls. Bottom 20% naturally darkened.",

    # Page 08 - Bubu painting
    f"{PREFIX} Close-up scene: {BUBU} dipping her small paw into red paint and painting a big cheerful flower on white paper. {TEACHER_GAN} squatting beside her, watching with a warm patient smile, one paw gently resting near Bubu. The table has scattered paint jars and colorful paper. Bubu's face shows concentration and joy. Other toddlers painting nearby. Bottom 20% naturally darkened.",

    # Page 09 - Teacher Yanzi flying around helping kids
    f"{PREFIX} {TEACHER_YANZI} flying gracefully through the classroom, her distinctive forked tail spread behind her. She's helping a small bear toddler drink from a cup while {BUBU} and other toddlers play nearby. The swallow's movements are light and agile. Classroom setting with children's artwork, plants, and sunlight from windows. Bottom 20% naturally darkened.",

    # Page 10 - Lunchtime, Teacher Li serves soup
    f"{PREFIX} Lunchtime scene in a bright cafeteria. {TEACHER_LI} ladling warm tomato egg soup into a small bowl for {BUBU} who sits at a child-sized table. Steam rising from the bowl. Bubu is blowing on the soup with puffed cheeks. Other animal toddlers eating at nearby tables. Warm cozy lighting. Small chairs and tables. Bottom 20% naturally darkened.",

    # Page 11 - Nap time
    f"{PREFIX} A quiet nap room with soft dim lighting. {BUBU} lying on a small bed hugging a tiny bunny-shaped pillow, eyes almost closed, looking peaceful and sleepy. {TEACHER_LI} sitting beside her bed, gently patting Bubu's back with one paw. Other toddlers sleeping in their beds in the background. Soft curtains filtering afternoon light. Bottom 20% naturally darkened.",

    # Page 12 - Playground time
    f"{PREFIX} Outdoor playground in bright summer sunshine. {BUBU} sliding down a colorful slide with arms up, laughing joyfully. Other animal toddlers (bear on swings, corgi running) playing around. {TEACHER_YANZI} flying overhead watching the children, smiling. Green trees, blue sky, modern playground equipment. Everyone slightly sweaty from playing. Bottom 20% naturally darkened.",

    # Page 13 - Grandparents pick up + ending with NOMI/NONO
    f"{PREFIX} Split scene composition. LEFT HALF: At the kindergarten gate in golden evening light, {BUBU} running with open arms toward {GRANDMA} who bends down to catch her, with {GRANDPA} standing behind smiling. RIGHT HALF/FOREGROUND: Later at home, {BUBU} sitting on a couch hugging {NOMI} on her left and {NONO} perched on her right shoulder, excitedly talking with her mouth open telling them about her day. Warm evening home lighting. Both scenes flow naturally. Bottom 20% naturally darkened.",
]

def generate_image(prompt, filename, attempt=1):
    data = json.dumps({"prompt": prompt, "n": 1, "size": "1024x1536", "quality": "medium", "output_format": "png"}).encode()
    req = urllib.request.Request(ENDPOINT, data=data, headers={"Content-Type": "application/json", "api-key": API_KEY})
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        result = json.loads(resp.read())
        img_b64 = result["data"][0]["b64_json"]
        png_path = os.path.join(OUT_DIR, filename.replace('.jpg', '.png'))
        with open(png_path, 'wb') as f:
            f.write(base64.b64decode(img_b64))
        # Convert to jpg
        jpg_path = os.path.join(OUT_DIR, filename)
        os.system(f'ffmpeg -y -i "{png_path}" -q:v 4 "{jpg_path}" 2>/dev/null')
        os.remove(png_path)
        size = os.path.getsize(jpg_path)
        print(f"✅ {filename}: {size/1024:.0f}KB")
        return True
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.readable() else ""
        if e.code == 429 and attempt <= 3:
            print(f"⚠️ 429 on {filename}, waiting 45s (attempt {attempt})...")
            time.sleep(45)
            return generate_image(prompt, filename, attempt+1)
        elif "content_policy" in body.lower() and attempt <= 2:
            print(f"⚠️ Content filter on {filename}, simplifying...")
            return False
        else:
            print(f"❌ {filename}: HTTP {e.code} - {body[:200]}")
            return False
    except Exception as e:
        print(f"❌ {filename}: {e}")
        return False

if __name__ == "__main__":
    start_page = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    for i in range(start_page - 1, len(prompts)):
        filename = f"page-{i+1:02d}.jpg"
        print(f"Generating {filename}...")
        generate_image(prompts[i], filename)
        if i < len(prompts) - 1:
            time.sleep(8)
    print("\n🎉 Done!")
