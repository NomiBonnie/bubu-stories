#!/usr/bin/env python3
import json, base64, time, subprocess, os, sys, urllib.request, urllib.error

API_ENDPOINT = "https://kaixi-mmimphd8-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-image-2/images/generations"
API_KEY = "G0XzcVpk6KUGX53HbGfW6nBFiU4yh4Wjfowo8BSseYoSL8HAL9E4JQQJ99CCACHYHv6XJ3w3AAAAACOGJIkM"
API_VERSION = "2025-04-01-preview"

BUBU = 'a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow. She has a small pink bow centered ON TOP OF HER HEAD between her two ears (not on left ear, not on right ear, not behind -- exactly centered on top between the ears). She has a toddler-like round body proportion.'
SAM_DAD = 'Sam Dad who is a GOLDEN RETRIEVER DOG (NOT a human, NOT a person -- he is an ANIMAL, a large golden-furred dog walking upright). He has warm golden fur all over his body, a dog snout/muzzle, floppy dog ears, and a wagging tail. He wears a dark navy jacket over a simple shirt. He has a warm gentle dog smile. IMPORTANT: Sam Dad must look like a golden retriever dog, not a human man.'
TINA_MOM = 'Tina Mom who is a BLACK-AND-WHITE COW (NOT a human, NOT a person -- she is an ANIMAL, a cow walking upright). She has black and white spotted fur pattern all over, small curved horns, cow ears, and hooves. She wears an elegant cream knit cardigan over a floral skirt. She has a gentle warm cow smile. IMPORTANT: Tina Mom must look like a cow, not a human woman.'
NOMI = 'a raccoon (NOMI) with grey-brown fur, distinctive black eye mask markings, and a ringed bushy tail. She wears a blue-and-white horizontally striped sweater. She has clever bright eyes and nimble paws.'
NONO = 'a small red bird (NONO) with bright red feathers all over, round bright eyes, and an orange-yellow beak. He has exactly TWO wings and TWO small bird feet with talons. NO ARMS, NO HANDS -- birds do not have arms or hands, only wings.'
DOUDOU = 'a small hedgehog (Doudou) with a brown body covered in dark brown spines/quills, small round shiny eyes, a tiny nose. He is small, round, and shy-looking.'
MANMAN = 'a small turtle (Manman) with a green shell with dark green hexagonal patterns, light green skin, small round eyes, and a gentle slow expression.'

BASE = '/Users/samyuan/.openclaw/workspace/bubu-stories/print-edition'

def gen(prompt, out_dir, page_name):
    os.makedirs(out_dir, exist_ok=True)
    png_path = f'/tmp/bubu_{page_name}.png'
    jpg_path = f'{out_dir}/{page_name}.jpg'
    
    for attempt in range(3):
        print(f'>>> {page_name} (attempt {attempt+1})...', flush=True)
        body = json.dumps({
            'prompt': prompt,
            'size': '1024x1536',
            'quality': 'medium',
            'n': 1,
            'output_format': 'png'
        }).encode()
        
        req = urllib.request.Request(
            f'{API_ENDPOINT}?api-version={API_VERSION}',
            data=body,
            headers={'Content-Type': 'application/json', 'api-key': API_KEY}
        )
        
        try:
            resp = urllib.request.urlopen(req, timeout=120)
            data = json.loads(resp.read())
            b64 = data['data'][0]['b64_json']
            with open(png_path, 'wb') as f:
                f.write(base64.b64decode(b64))
            subprocess.run(['ffmpeg', '-y', '-i', png_path, '-q:v', '2', jpg_path],
                         capture_output=True)
            os.remove(png_path)
            size = os.path.getsize(jpg_path)
            print(f'  OK {page_name}.jpg -- {size} bytes', flush=True)
            return size
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f'  429 rate limit, waiting 45s...', flush=True)
                time.sleep(45)
            else:
                err = e.read().decode()[:200]
                print(f'  HTTP {e.code}: {err}', flush=True)
                time.sleep(10)
        except Exception as e:
            print(f'  Error: {e}', flush=True)
            time.sleep(10)
    
    print(f'  FAILED {page_name}', flush=True)
    return 0

def make_prompt(scene, chars):
    return f'Pixar 3D animation style, {scene}\n\nCHARACTERS: {chars}\n\nThe composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children\'s picture book quality.'

results = []

# Story 3 P10-P14
s3 = f'{BASE}/story3'
pages = [
    ('page-10', 'warm golden afternoon sunlight, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: A park sandpit. Bubu and Doudou the hedgehog are building a sandcastle together happily. Bubu uses a small shovel to scoop sand while Doudou pats the sand with his little paws. Their new sandcastle is big and beautiful.',
     f'{BUBU}. {DOUDOU}'),
    ('page-11', 'warm afternoon sunlight, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: A park sandpit with a big beautiful sandcastle. NOMI the raccoon arrives carrying a small water bucket, and NONO the red bird flies in carrying a tiny flag in his beak to place on top of the sandcastle. Bubu and Doudou watch happily.',
     f'{BUBU}. {DOUDOU}. {NOMI}. {NONO}'),
    ('page-12', 'warm golden sunlight, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: A park with a beautiful sandcastle. Tina Mom stands nearby watching the children with a warm smile. Bubu, Doudou, NOMI and NONO are around the sandcastle looking happy.',
     f'{TINA_MOM}. {BUBU}. {DOUDOU}. {NOMI}. {NONO}'),
    ('page-13', 'warm sunset light, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: A park path at sunset. Bubu the rabbit gently holds Doudou the hedgehog\'s paw, carefully holding the soft palm side. They walk side by side happily. Golden sunset light through trees.',
     f'{BUBU}. {DOUDOU}'),
    ('page-14', 'soft warm glowing light, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: A cheerful summary scene. Bubu stands happily in the center with a big smile. Around her are a sandcastle, a small shovel, and sparkles. Warm uplifting mood.',
     f'{BUBU}'),
]

print('=== Story 3: P10-P14 ===', flush=True)
for name, scene, chars in pages:
    prompt = f'Pixar 3D animation style, {scene}\n\nCHARACTERS: {chars}\n\nThe composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children\'s picture book quality.'
    sz = gen(prompt, s3, name)
    results.append((f'story3/{name}', sz))
    time.sleep(8)

# Story 4 P2-P16
s4 = f'{BASE}/story4'
s4_pages = [
    ('page-02', 'bright sunny morning light, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: A beautiful riverbank with sandy shore. Bubu and Manman the turtle play in the sand. Manman slowly and carefully builds a beautiful sandcastle. The river sparkles in background.',
     f'{BUBU}. {MANMAN}', False),
    ('page-03', 'bright sunny light, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: Riverbank. Bubu watches Manman\'s pretty sandcastle admiringly, then tries building her own bigger one next to it. Bubu\'s castle keeps falling apart. She looks determined but frustrated. Manman\'s castle stands pretty nearby.',
     f'{BUBU}. {MANMAN}', False),
    ('page-04', 'bright daylight, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: Riverbank. Dramatic moment: Bubu accidentally bumps into Manman\'s sandcastle and it collapses. Sand particles fly. Bubu looks shocked with wide eyes.',
     f'{BUBU}. {MANMAN}', False),
    ('page-05', 'soft diffused light, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: Riverbank with destroyed sandcastle now just a pile of sand. Manman sits next to the pile crying with tears streaming. Bubu stands nearby looking guilty and sad.',
     f'{BUBU}. {MANMAN}', False),
    ('page-06', 'dim indoor light, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: Bubu\'s cozy bedroom. Bubu sits on her bed hugging her knees, looking sad and troubled. Some toys around, window showing daylight outside.',
     f'{BUBU}', False),
    ('page-07', 'warm soft indoor light, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: Bubu\'s bedroom. Sam Dad sits on the bed next to Bubu who looks sad. He has a gentle comforting expression, leaning in to listen.',
     f'{BUBU}. {SAM_DAD}', 'dad'),
    ('page-08', 'warm indoor light, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: Bedroom close-up conversation. Sam Dad speaks gently with a wise expression. Bubu looks thoughtful with a paw on her chin, starting to understand. Intimate reflective mood.',
     f'{BUBU}. {SAM_DAD}', 'dad'),
    ('page-09', 'warm kitchen light, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: A cozy kitchen. Tina Mom stands by a counter with a tray of freshly baked cookies, offering them to Bubu with a warm smile. Steam rises from cookies. Bubu looks up hopefully.',
     f'{BUBU}. {TINA_MOM}', 'mom'),
    ('page-10', 'warm afternoon light, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: Riverbank. Bubu walks up to Manman carrying a plate of cookies. Manman quietly rebuilds her sandcastle alone. Bubu approaches with sincere apologetic expression.',
     f'{BUBU}. {MANMAN}', False),
    ('page-11', 'soft afternoon light, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: Riverbank close-up. Bubu kneels and places cookies in front of Manman. Manman looks up, still a bit hurt but curious about cookies. Delicious cookies on a small plate between them.',
     f'{BUBU}. {MANMAN}', False),
    ('page-12', 'warm golden light, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: Riverbank. Manman looks at cookies then at Bubu and slowly smiles, starting to forgive. Both face each other warmly. A half-rebuilt sandcastle between them.',
     f'{BUBU}. {MANMAN}', False),
    ('page-13', 'bright happy afternoon light, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: Riverbank with a magnificent completed sandcastle, bigger and more beautiful than before. Bubu and Manman stand proudly next to it. NOMI passes by looking amazed.',
     f'{BUBU}. {MANMAN}. {NOMI}', False),
    ('page-14', 'bright joyful light, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: Riverbank with the grand sandcastle. Bubu and Manman laugh together. NONO the red bird flies down and plants a tiny flag on top with his beak.',
     f'{BUBU}. {MANMAN}. {NONO}', False),
    ('page-15', 'warm sunset golden hour light, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: A path along the river at sunset. Sam Dad walks with Bubu, holding her paw gently. Bubu looks up at him happily and proudly. Trees and warm sunset colors.',
     f'{BUBU}. {SAM_DAD}', 'dad'),
    ('page-16', 'soft warm glowing light, children\'s picture book illustration, vertical portrait 1024x1536. No text anywhere in the image.\n\nSCENE: Cheerful summary scene. Bubu stands in center with warm confident smile. Around her are a rebuilt sandcastle, cookies, and sparkles. Warm encouraging uplifting mood.',
     f'{BUBU}', False),
]

print('\n=== Story 4: P2-P16 ===', flush=True)
for name, scene, chars, parent in s4_pages:
    prompt = f'Pixar 3D animation style, {scene}\n\nCHARACTERS: {chars}\n\nThe composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children\'s picture book quality.'
    sz = gen(prompt, s4, name)
    tag = f' [HAS {"DAD" if parent=="dad" else "MOM"}]' if parent else ''
    results.append((f'story4/{name}{tag}', sz))
    time.sleep(8)

print('\n=== SUMMARY ===', flush=True)
for path, sz in results:
    status = 'OK' if sz > 0 else 'FAILED'
    print(f'  {status} {path} -- {sz} bytes', flush=True)
