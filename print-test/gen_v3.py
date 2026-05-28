import requests, json, base64, os, time

with open(os.path.expanduser('~/.config/azure-openai/config.json')) as f:
    config = json.load(f)
url = config['image2_eastus2_endpoint'] + '?api-version=2025-04-01-preview'
headers = {'api-key': config['image2_eastus2_api_key'], 'Content-Type': 'application/json'}
outdir = os.path.expanduser('~/.openclaw/workspace/bubu-stories/print-test')

STYLE = "Pixar 3D animation style, children picture book FULL PAGE illustration with integrated text, vertical 1024x1536."
BINDING = "LAYOUT RULE: keep the left 10% of the image as safe margin (no text, no key characters). All text starts from 12% from left edge."
FONT = "FONT RULES: ALL text across ALL pages must use the EXACT SAME font style and size. Chinese text: clean sans-serif font similar to PingFang SC, white color, size equivalent to 16pt. English text: clean sans-serif similar to SF Pro, soft cream color, size equivalent to 12pt, directly below Chinese. Both languages use the same translucent dark panel background."
COMPACT = "Text layout: pack text compactly, multiple sentences per line when possible. The text panel should be minimal height — just enough to fit the text with small padding."

pages = [
    ("p2_v3", f"""{STYLE} Warm sunny daylight. {BINDING} {FONT} SCENE: Beautiful green meadow with wildflowers, butterflies, blue sky, fluffy white clouds, warm golden sunlight. CENTER-RIGHT: snow-white rabbit girl Bubu with pink insides ears, big brown eyes, pink dress pink bow on ear, hopping joyfully through meadow with big smile. BOTTOM: compact translucent dark navy panel blending into grass edge. Chinese: 从前，在一片绿绿的大草地上，住着一只小兔子，名字叫咘咘。咘咘有长长的耳朵，粉粉的鼻子，最喜欢蹦蹦跳跳。English: Once upon a time, on a big green meadow, there lived a little bunny named Bubu. Bubu had long floppy ears, a tiny pink nose, and loved to hop, hop, hop! {COMPACT}"""),

    ("p5_v3", f"""{STYLE} Warm twilight purple-orange sky. {BINDING} {FONT} SCENE: Small grassy hilltop at dusk, purple orange pink sunset sky, huge full moon rising on horizon glowing warm yellow, fireflies floating. CENTER-RIGHT: snow-white rabbit girl Bubu pink ears big brown eyes pink dress, standing on hilltop arms raised toward moon calling out joyfully. BOTTOM: compact translucent dark navy panel blending with twilight sky. Chinese: 每天晚上睡觉前，咘咘都会跑到小山坡上，看天上的月亮。"月亮月亮，晚安！"咘咘会大声说。English: Every night before bed, Bubu would run up to the little hill and look at the moon. "Goodnight, Moon!" Bubu would call out loud. {COMPACT}"""),

    ("p8_v3", f"""{STYLE} Warm cozy indoor lamplight. {BINDING} {FONT} SCENE: Cozy tree hollow interior with warm orange lamp, bookshelves with colorful books, scattered open books, night sky visible through round window. CENTER-RIGHT: raccoon NOMI in blue-and-white striped sweater wearing tiny round glasses sitting on cushion reading big book. Snow-white rabbit girl Bubu pink ears pink dress stands at entrance looking worried pulling NOMI paw. BOTTOM: compact translucent dark navy panel blending with wooden floor. Chinese: 小浣熊NOMI正在树洞里看书。"NOMI NOMI，月亮不见了！你能帮我找找吗？"咘咘说。NOMI推了推眼镜说："别急，我们一起去找！" English: Little raccoon NOMI was reading in her cozy tree hollow. "NOMI, the moon is gone! Can you help me find it?" said Bubu. NOMI pushed up her glasses: "Dont worry, lets go look together!" {COMPACT}""")
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
