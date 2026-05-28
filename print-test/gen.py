import requests, json, base64, os, time

with open(os.path.expanduser('~/.config/azure-openai/config.json')) as f:
    config = json.load(f)
url = config['image2_eastus2_endpoint'] + '?api-version=2025-04-01-preview'
headers = {'api-key': config['image2_eastus2_api_key'], 'Content-Type': 'application/json'}
outdir = os.path.expanduser('~/.openclaw/workspace/bubu-stories/print-test')

BINDING = "IMPORTANT: keep the left 15% of the image free of important content or text (binding margin). Text starts from 20% from left edge."
COMPACT = "Compact text, pack tight, NOT one sentence per line. Professional picture book quality."

pages = [
    ("p2_v2", f"Pixar 3D animation style, warm sunny day, children picture book FULL PAGE with integrated text, vertical 1024x1536. {BINDING} SCENE: Beautiful green meadow with wildflowers, butterflies, blue sky, fluffy clouds. CENTER-RIGHT: snow-white rabbit girl Bubu with pink insides ears, big brown eyes, pink dress pink bow, hopping joyfully, positioned right of center. BOTTOM: compact translucent dark blue-purple panel (15% height) blending into grass. Chinese (white, clear): 从前，在一片绿绿的大草地上，住着一只小兔子，名字叫咘咘。咘咘有长长的耳朵，粉粉的鼻子，最喜欢蹦蹦跳跳。English (cream, smaller, below): Once upon a time, on a big green meadow, there lived a little bunny named Bubu. Bubu had long floppy ears, a tiny pink nose, and loved to hop, hop, hop! {COMPACT}"),

    ("p5_v2", f"Pixar 3D animation style, warm twilight purple-orange sky, children picture book FULL PAGE with integrated text, vertical 1024x1536. {BINDING} SCENE: Grassy hilltop at dusk, purple orange pink sunset, huge full moon rising, fireflies. CENTER-RIGHT: snow-white rabbit girl Bubu pink ears pink dress, standing on hilltop arms raised toward moon, positioned right of center. BOTTOM: compact translucent dark blue panel (12% height) blending with sky. Chinese (white): 每天晚上睡觉前，咘咘都会跑到小山坡上，看天上的月亮。\"月亮月亮，晚安！\"咘咘会大声说。English (cream, smaller): Every night before bed, Bubu would run up to the little hill and look at the moon. \"Goodnight, Moon!\" Bubu would call out loud. {COMPACT}"),

    ("p8_v2", f"Pixar 3D animation style, warm cozy indoor lamplight, children picture book FULL PAGE with integrated text, vertical 1024x1536. {BINDING} SCENE: Cozy tree hollow with warm lamp, bookshelves, night through round window. CENTER-RIGHT: raccoon NOMI in blue-white striped sweater with tiny glasses sitting reading a book. Snow-white rabbit Bubu pink dress stands at entrance looking anxious pulling NOMI paw. BOTTOM: compact translucent warm brown panel (18% height) blending with wooden floor. Chinese (cream white): 小浣熊NOMI正在树洞里看书。\"NOMI NOMI，月亮不见了！你能帮我找找吗？\"咘咘说。NOMI推了推眼镜说：\"别急，我们一起去找！\" English (cream, smaller): Little raccoon NOMI was reading in her cozy tree hollow. \"NOMI, the moon is gone! Can you help me find it?\" said Bubu. NOMI pushed up her glasses: \"Dont worry, lets go look together!\" {COMPACT}")
]

for name, prompt in pages:
    print(f'Generating {name}...')
    body = {'prompt': prompt, 'n': 1, 'size': '1024x1536', 'quality': 'medium', 'output_format': 'png'}
    for attempt in range(3):
        resp = requests.post(url, headers=headers, json=body, timeout=180)
        print(f'  Attempt {attempt+1}: {resp.status_code}')
        if resp.status_code == 200:
            b64 = resp.json()['data'][0]['b64_json']
            out = os.path.join(outdir, f'{name}.png')
            with open(out, 'wb') as f:
                f.write(base64.b64decode(b64))
            os.system(f'ffmpeg -y -i {out} -q:v 2 {out.replace(".png",".jpg")} 2>/dev/null')
            print(f'  Done')
            break
        else:
            print(f'  Retrying in 30s...')
            time.sleep(30)
    time.sleep(10)
print('All done')
