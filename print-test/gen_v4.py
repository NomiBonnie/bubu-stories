import requests, json, base64, os, time

with open(os.path.expanduser('~/.config/azure-openai/config.json')) as f:
    config = json.load(f)
url = config['image2_eastus2_endpoint'] + '?api-version=2025-04-01-preview'
headers = {'api-key': config['image2_eastus2_api_key'], 'Content-Type': 'application/json'}
outdir = os.path.expanduser('~/.openclaw/workspace/bubu-stories/print-test')

STYLE = "Pixar 3D animation style, children picture book FULL PAGE illustration with integrated text, vertical 1024x1536."
BINDING = "LAYOUT: left 10% is binding safe margin. No text or key content in left 10%."
FONT = "FONT: Chinese = clean sans-serif like PingFang, white, 16pt equivalent. English = clean sans-serif like SF Pro, soft cream, 12pt equivalent, directly below Chinese."
PANEL = "TEXT PANEL: A translucent dark navy semi-transparent rectangle at the bottom of the image. The panel has FIXED edges: left edge at exactly 10% from image left, right edge at exactly 5% from image right, bottom edge touches the image bottom with 2% padding. The TOP edge of the panel adjusts based on how much text is needed — shorter text = shorter panel, longer text = taller panel. The panel shape is a clean rectangle with slightly rounded corners. All pages must have the panel at the SAME left, right, and bottom position — only the top edge varies."
COMPACT = "Pack text compactly. Multiple sentences per line when possible."

pages = [
    ("p2_v4", f"""{STYLE} Warm sunny daylight. {BINDING} {FONT} {PANEL} SCENE: Beautiful green meadow with wildflowers, butterflies, blue sky, fluffy white clouds. CENTER-RIGHT: snow-white rabbit girl Bubu with pink insides ears, big brown eyes, pink dress pink bow, hopping joyfully. TEXT IN PANEL - Chinese: 从前，在一片绿绿的大草地上，住着一只小兔子，名字叫咘咘。咘咘有长长的耳朵，粉粉的鼻子，最喜欢蹦蹦跳跳。English: Once upon a time, on a big green meadow, there lived a little bunny named Bubu. Bubu had long floppy ears, a tiny pink nose, and loved to hop, hop, hop! {COMPACT}"""),

    ("p5_v4", f"""{STYLE} Warm twilight purple-orange sky. {BINDING} {FONT} {PANEL} SCENE: Grassy hilltop at dusk, purple orange pink sunset, huge full moon rising, fireflies. CENTER-RIGHT: snow-white rabbit girl Bubu pink ears pink dress, standing on hilltop arms raised toward moon. TEXT IN PANEL - Chinese: 每天晚上睡觉前，咘咘都会跑到小山坡上，看天上的月亮。"月亮月亮，晚安！"咘咘会大声说。English: Every night before bed, Bubu would run up to the little hill and look at the moon. "Goodnight, Moon!" Bubu would call out loud. {COMPACT}"""),

    ("p8_v4", f"""{STYLE} Warm cozy indoor lamplight. {BINDING} {FONT} {PANEL} SCENE: Cozy tree hollow with warm orange lamp, bookshelves, night through round window. CENTER-RIGHT: raccoon NOMI in blue-white striped sweater tiny glasses reading book. Bubu pink dress at entrance looking worried. TEXT IN PANEL - Chinese: 小浣熊NOMI正在树洞里看书。"NOMI NOMI，月亮不见了！你能帮我找找吗？"咘咘说。NOMI推了推眼镜说："别急，我们一起去找！" English: Little raccoon NOMI was reading in her cozy tree hollow. "NOMI, the moon is gone! Can you help me find it?" said Bubu. NOMI pushed up her glasses: "Dont worry, lets go look together!" {COMPACT}""")
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
