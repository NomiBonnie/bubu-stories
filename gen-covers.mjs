import fs from 'fs';
import path from 'path';

const config = JSON.parse(fs.readFileSync(path.join(process.env.HOME, '.config/azure-openai/config.json'), 'utf8'));
const endpoint = config.image2_poland_endpoint;
const apiKey = config.image2_poland_api_key;
const deployment = config.image2_poland_deployment;
const url = `${endpoint}openai/deployments/${deployment}/images/generations?api-version=2025-04-01-preview`;

const BUBU = "a snow-white rabbit with long ears with pink inner, big round brown eyes, small pink nose, wearing a pink dress and a pink bow on her head, toddler proportions";
const NOMI = "a raccoon with grey-brown fur, black eye mask, ringed tail, wearing a blue-and-white striped sweater";
const NONO = "a small bird with bright red feathers and an orange-yellow beak";
const SAM = "a golden retriever with golden fur wearing a dark fitted jacket";
const DOUDOU = "a small hedgehog with brown body, dark brown spines, and small round eyes";

const stories = [
  { num: 1, title: "小兔子找月亮", scene: `A magical nighttime meadow under a big glowing full moon and starry sky. ${BUBU} stands in the center looking up at the moon with wonder. ${NOMI} stands beside her pointing at the moon. ${NONO} perches on the raccoon's shoulder. Fireflies glow around them.` },
  { num: 2, title: "彩虹桥在哪里", scene: `A bright sunny meadow with a magnificent rainbow arching across the sky. ${BUBU} stands on a small hill gazing up at the rainbow with curiosity, one paw raised. ${NOMI} and ${NONO} are beside her. Colorful wildflowers, butterflies.` },
  { num: 3, title: "小刺猬的新朋友", scene: `A sunny forest clearing with dappled light. ${BUBU} and ${DOUDOU} face each other with friendly smiles, meeting for the first time. Mushrooms, flowers, soft moss on the ground.` },
  { num: 4, title: "咘咘学会说对不起", scene: `A cozy park scene. ${BUBU} looks apologetic with a gentle expression, offering a small flower. ${NOMI} and ${NONO} watch warmly nearby. Soft golden afternoon light, trees and flowers.` },
  { num: 5, title: "咘咘学会说你好", scene: `A cheerful village path on a sunny morning. ${BUBU} waves happily with a big smile. ${NOMI} and ${NONO} wave alongside her. Other small woodland animals peek from behind bushes.` },
  { num: 6, title: "咘咘学会等一等", scene: `A peaceful riverside scene. ${BUBU} and ${SAM} sit side by side on a grassy riverbank, each holding a small fishing rod. Calm water with lily pads. ${NOMI} naps nearby. Warm golden sunset light.` },
];

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function generate(story) {
  const outPath = `public/images/story${story.num}/page-01.jpg`;
  if (fs.existsSync(outPath)) {
    const stat = fs.statSync(outPath);
    if (stat.size > 1000000) {
      console.log(`[Story ${story.num}] ⏭️  Already exists (${(stat.size/1024).toFixed(0)}KB), skipping`);
      return true;
    }
  }

  const prompt = `Pixar 3D animation style, children's picture book cover illustration, vertical 1024x1536. A decorative wooden sign/banner at the top of the image with the Chinese title text「${story.title}」carved/painted on it in warm brown/gold colors. The title text must be clearly legible. ${story.scene} Warm, bright, joyful children's book cover mood. High detail, soft lighting, vibrant colors.`;
  console.log(`[Story ${story.num}] Generating: ${story.title}`);

  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'api-key': apiKey },
        body: JSON.stringify({ prompt, n: 1, size: '1024x1536', quality: 'medium' })
      });
      if (!response.ok) {
        console.error(`  Attempt ${attempt} HTTP ${response.status}: ${(await response.text()).slice(0,200)}`);
        if (attempt < 3) { await sleep(10000); continue; }
        return false;
      }
      const data = await response.json();
      const item = data.data[0];
      let buf;
      if (item.b64_json) {
        buf = Buffer.from(item.b64_json, 'base64');
      } else if (item.url) {
        const imgResp = await fetch(item.url);
        buf = Buffer.from(await imgResp.arrayBuffer());
      }
      fs.mkdirSync(path.dirname(outPath), { recursive: true });
      fs.writeFileSync(outPath, buf);
      console.log(`  ✅ Saved ${outPath} (${(buf.length/1024).toFixed(0)}KB)`);
      return true;
    } catch (e) {
      console.error(`  Attempt ${attempt} error: ${e.message}`);
      if (attempt < 3) await sleep(10000);
    }
  }
  return false;
}

async function main() {
  let ok = 0, fail = 0;
  for (let i = 0; i < stories.length; i++) {
    const result = await generate(stories[i]);
    if (result) ok++; else fail++;
    if (i < stories.length - 1) { console.log('  Sleeping 7s...'); await sleep(7000); }
  }
  console.log(`\nDone: ${ok} succeeded, ${fail} failed`);
}
main();
