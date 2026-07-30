const fs = require('fs'), path = require('path');
const C = JSON.parse(fs.readFileSync(
  path.join(process.env.HOME, '.config/azure-openai/config.json'), 'utf8'
));
const url = C.image2_eastus2_endpoint + '?api-version=2025-04-01-preview';
const apiKey = C.image2_eastus2_api_key;
const sleep = ms => new Promise(r => setTimeout(r, ms));
const outDir = '/Users/samyuan/.openclaw/workspace/bubu-stories/public/images/story64';

const PREFIX = "Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition 1024x1536. No text anywhere in the image.";

const BUBU = "a cute snow-white rabbit toddler with exactly TWO long ears with pink insides, big round brown eyes, small pink nose, wearing a pink dress and a pink bow on top of her head centered between her two ears. Toddler proportions, round and adorable.";
const ZHUZHU = "a cute white sheep (lamb) with cloud-like curly wool, small pink nose, brown little hooves, wearing a blue dress. Same size as Bubu.";
const ZHUZHU_DAD = "an adult white sheep (ram) with curly wool and small curved horns, wearing a blue polo shirt and pants. Bipedal anthropomorphic.";
const ZHUZHU_MOM = "an adult white sheep (ewe) with soft curly wool, wearing a floral blouse and skirt. Bipedal anthropomorphic.";
const DAD = "an anthropomorphic golden retriever dog standing upright on two legs (bipedal humanoid, NOT on all fours), golden fur, tall and warm, wearing a stylish dark casual jacket and pants, kind smile.";
const MOM = "an anthropomorphic dairy cow standing upright on two legs (bipedal humanoid, NOT on all fours), black and white spotted, elegant, wearing a fashionable knit top and skirt, gentle expression.";
// Key fix: Grandpa description matching Story 60 style
const GRANDPA = "an elderly cute SHORT-NECKED round chubby green dinosaur grandpa (NOT a long-necked brontosaurus, more like a short stubby cartoon dinosaur with a VERY SHORT neck, round head directly on round body). Olive-green skin, small round head, wearing small round glasses (spectacles), white collared shirt, looks OLD and grandfatherly with gentle wrinkles. Short and stout, pudgy belly. Bipedal, standing upright.";
const GRANDMA = "a small elderly monkey grandma with light brown fur, warm peach-colored face, kind big eyes, hair in a small bun, wearing a Chinese-style floral blouse. Small and nimble, grandmotherly feel.";
const NOMI = "a raccoon with grey-brown fur, black eye mask markings, ringed tail, big round intelligent eyes, wearing a blue-and-white striped sweater.";
const NONO = "a small bright red bird with round body, orange-yellow beak, round shiny eyes. Tiny, perches on shoulders or heads.";
const COCO = "a red panda (NOT a giant panda) with reddish-brown fur, round face, big round eyes, wearing a yellow scarf. Slightly bigger than Bubu.";

const pages = [
  {
    idx: 1,
    prompt: `${PREFIX} Movie poster style children's book cover. In the center, ${BUBU} and ${ZHUZHU} stand together holding fishing rods - Bubu holds a yellow fishing rod and Zhuzhu holds a purple fishing rod. Behind them, a birthday cake with candles and colorful balloons. Around them: ${DAD}, ${MOM}, ${GRANDPA}, ${GRANDMA}, ${NOMI}, ${NONO}, ${COCO}, ${ZHUZHU_DAD}, ${ZHUZHU_MOM}. Warm golden light, celebration atmosphere. The English title "Zhuzhu's Birthday" in playful hand-lettered style at the top, with decorative fishing line curls around the letters.`
  },
  {
    idx: 5,
    prompt: `${PREFIX} A cozy living room sofa scene. ${ZHUZHU_DAD} and ${ZHUZHU_MOM} sit on one side of the sofa chatting with ${DAD} and ${MOM} on the other side. ${GRANDPA} stands nearby holding a tea tray with a warm smile. ${GRANDMA} places fruit on the coffee table. All characters are bipedal anthropomorphic animals. Warm friendly conversation atmosphere.`
  },
  {
    idx: 7,
    prompt: `${PREFIX} Living room scene. In the foreground, ${BUBU} holds ${ZHUZHU}'s hoof, leading her excitedly toward a coffee table where a long purple gift box with a ribbon bow sits. Zhuzhu's eyes are wide with surprise. In the background on the sofa, ${DAD} and ${MOM} sit together watching and smiling warmly. ${GRANDPA} stands nearby also smiling. All adult characters are bipedal anthropomorphic animals sitting/standing upright. Warm home atmosphere.`
  },
  {
    idx: 11,
    prompt: `${PREFIX} A car interior from back seat perspective. ${DAD} drives (golden retriever paws on steering wheel, sitting upright), ${MOM} sits in passenger seat looking at phone for navigation. In the back seat, ${BUBU} and ${ZHUZHU} sit close together chatting excitedly. ${COCO} leans against the car window, ${NONO} perches on Coco's head. Through the window, a sunny city street. Summer daylight.`
  },
  {
    idx: 12,
    prompt: `${PREFIX} A cheerful restaurant with a big round table full of colorful dishes. In the center, a beautiful round birthday cake with strawberries and cream flowers on top, four small candles. ${ZHUZHU} claps her hooves in delight. ${MOM} stands nearby having arranged everything. ${DAD} helps place candles on the cake. All characters seated around: ${BUBU}, ${GRANDPA}, ${GRANDMA}, ${ZHUZHU_DAD}, ${ZHUZHU_MOM}, ${NOMI}, ${COCO}. ${NONO} perches on someone's shoulder. Festive warm restaurant lighting.`
  },
  {
    idx: 13,
    prompt: `${PREFIX} Birthday celebration moment. ${ZHUZHU} sits in front of the lit birthday cake, hooves pressed together, eyes closed making a wish. All other characters circle around singing - ${BUBU}, ${DAD}, ${MOM}, ${GRANDPA}, ${GRANDMA}, ${ZHUZHU_DAD}, ${ZHUZHU_MOM}, ${NOMI}, ${NONO}, ${COCO}. Warm candlelight illuminates everyone's happy faces. Golden warm atmosphere.`
  },
  {
    idx: 17,
    prompt: `${PREFIX} A cozy children's bedroom at night. ${BUBU} lies in bed in pajamas, hugging a pink stuffed bunny toy. A yellow fishing rod leans against the wall nearby. ${GRANDMA} sits at the foot of the bed smiling gently. ${NOMI} sits beside the bed tucking Bubu in with a gentle smile. Soft warm nightlight glow. Peaceful sleepy atmosphere.`
  }
];

async function gen(prompt, outPath, label) {
  console.log(`Generating ${label}...`);
  try {
    const r = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'api-key': apiKey },
      body: JSON.stringify({ prompt, n: 1, size: '1024x1536', quality: 'medium' })
    });
    if (!r.ok) { console.error(`  ❌ ERR ${r.status}: ${(await r.text()).slice(0, 300)}`); return; }
    const d = await r.json();
    let buf;
    if (d.data[0].b64_json) buf = Buffer.from(d.data[0].b64_json, 'base64');
    else if (d.data[0].url) { const ir = await fetch(d.data[0].url); buf = Buffer.from(await ir.arrayBuffer()); }
    if (buf) { fs.writeFileSync(outPath, buf); console.log(`  ✅ ${label} (${(buf.length/1024)|0}KB)`); }
  } catch(e) { console.error(`  ❌ ${e.message}`); }
}

(async () => {
  console.log(`Regenerating ${pages.length} pages with fixed grandpa...`);
  for (let i = 0; i < pages.length; i++) {
    const p = pages[i];
    const outPath = path.join(outDir, `page-${String(p.idx).padStart(2,'0')}.jpg`);
    await gen(p.prompt, outPath, `page-${String(p.idx).padStart(2,'0')}`);
    if (i < pages.length - 1) await sleep(8000);
  }
  console.log('\nAll done!');
})();
