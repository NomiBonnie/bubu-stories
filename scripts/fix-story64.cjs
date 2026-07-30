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
const ZHUZHU = "a cute white sheep (lamb) with cloud-like curly wool, small pink nose, brown little hooves, wearing a blue dress. Same size as Bubu. Friendly and cheerful.";
const DAD = "an anthropomorphic golden retriever dog standing upright on two legs like a human (NOT on all fours, NOT a real dog), golden fur, tall and warm, wearing a stylish dark casual jacket and pants, walking upright bipedally, kind smile. He is a bipedal humanoid animal character.";
const MOM = "an anthropomorphic dairy cow standing upright on two legs like a human (NOT on all fours), black and white spotted, medium-large, elegant, wearing a fashionable knit top and skirt, gentle patient expression. She is a bipedal humanoid animal character.";
const GRANDPA = "a cute round green dinosaur (brontosaurus type, NOT scary, NOT a T-rex) standing upright, big round kind eyes, WEARING GLASSES (small round spectacles), wearing a white collared shirt and casual pants. Stout round body, lovable grandfatherly feel. Bipedal humanoid character.";
const ZHUZHU_MOM = "an adult white sheep (ewe) standing upright like a human, soft curly wool, wearing a floral blouse and skirt. Gentle warm expression. Bipedal humanoid animal character.";

const pages = [
  {
    idx: 7,
    prompt: `${PREFIX} Living room scene. In the foreground, ${BUBU} holds ${ZHUZHU}'s hoof, leading her excitedly toward a coffee table where a long purple gift box with a ribbon bow sits. Zhuzhu's eyes are wide with surprise. In the background on the sofa, ${DAD} and ${MOM} sit together watching and smiling warmly. ${GRANDPA} stands nearby also smiling. All adult characters are bipedal anthropomorphic animals sitting/standing upright like humans. Warm home atmosphere.`
  },
  {
    idx: 16,
    prompt: `${PREFIX} Evening street scene outside a restaurant, golden sunset sky, warm streetlights. On the left, ${ZHUZHU} leans sleepily against ${ZHUZHU_MOM} who holds her, Zhuzhu still clutching a purple fishing rod. On the right, ${DAD} stands upright on two legs (bipedal anthropomorphic golden retriever, NOT on all fours) carrying ${BUBU} on his back piggyback style. Bubu is sleepy but waves one paw goodbye. Dad walks upright like a human father carrying his child. Tender farewell moment.`
  }
];

async function gen(prompt, outPath, label) {
  console.log(`Generating ${label}...`);
  const r = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'api-key': apiKey },
    body: JSON.stringify({ prompt, n: 1, size: '1024x1536', quality: 'medium' })
  });
  if (!r.ok) { console.error('ERR', r.status, (await r.text()).slice(0, 300)); return; }
  const d = await r.json();
  let buf;
  if (d.data[0].b64_json) buf = Buffer.from(d.data[0].b64_json, 'base64');
  else if (d.data[0].url) { const ir = await fetch(d.data[0].url); buf = Buffer.from(await ir.arrayBuffer()); }
  if (buf) { fs.writeFileSync(outPath, buf); console.log(`✅ ${label} (${(buf.length/1024)|0}KB)`); }
}

(async () => {
  for (let i = 0; i < pages.length; i++) {
    const p = pages[i];
    const outPath = path.join(outDir, `page-${String(p.idx).padStart(2,'0')}.jpg`);
    await gen(p.prompt, outPath, `page-${String(p.idx).padStart(2,'0')}`);
    if (i < pages.length - 1) await sleep(8000);
  }
  console.log('Done!');
})();
