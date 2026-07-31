const fs = require('fs'), path = require('path');
const C = JSON.parse(fs.readFileSync(
  path.join(process.env.HOME, '.config/azure-openai/config.json'), 'utf8'
));
const url = C.image2_eastus2_endpoint + '?api-version=2025-04-01-preview';
const apiKey = C.image2_eastus2_api_key;
const sleep = ms => new Promise(r => setTimeout(r, ms));
const outDir = '/Users/samyuan/.openclaw/workspace/bubu-stories/public/images/story65';

const PREFIX = "Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition 1024x1536. No text anywhere in the image.";
const BUBU = "a cute snow-white rabbit toddler with exactly TWO long ears with pink insides, big round brown eyes, small pink nose, wearing a pink uniform and a pink bow centered between her ears.";
const TEACHER_LI = "a friendly giant panda in a light pink apron, round and cuddly, black and white fur with round eye patches.";
const NOMI = "a raccoon with grey-brown fur, black eye mask, ringed tail, wearing a blue-and-white striped sweater.";

const pages = [
  {
    idx: 14,
    prompt: `${PREFIX} A happy kindergarten scene. ${TEACHER_LI} gently places a small golden star sticker on the forehead of ${BUBU}. Bubu smiles proudly, one paw touching her head. A small golden badge on her chest. Warm golden light, celebration feeling.`
  },
  {
    idx: 16,
    prompt: `${PREFIX} A cozy children's bedroom at night. ${BUBU} lies in bed in pajamas holding a pink stuffed bunny toy. A small golden badge sits on the pillow beside her. ${NOMI} sits at the bedside smiling gently. Soft nightlight glow, peaceful atmosphere.`
  }
];

async function gen(prompt, outPath, label) {
  console.log(`Generating ${label}...`);
  const r = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'api-key': apiKey },
    body: JSON.stringify({ prompt, n: 1, size: '1024x1536', quality: 'medium' })
  });
  if (!r.ok) { console.error(`  ❌ ERR ${r.status}: ${(await r.text()).slice(0, 200)}`); return; }
  const d = await r.json();
  let buf;
  if (d.data[0].b64_json) buf = Buffer.from(d.data[0].b64_json, 'base64');
  else if (d.data[0].url) { const ir = await fetch(d.data[0].url); buf = Buffer.from(await ir.arrayBuffer()); }
  if (buf) { fs.writeFileSync(outPath, buf); console.log(`  ✅ ${label} (${(buf.length/1024)|0}KB)`); }
}

(async () => {
  for (let i = 0; i < pages.length; i++) {
    const p = pages[i];
    await gen(p.prompt, path.join(outDir, `page-${String(p.idx).padStart(2,'0')}.jpg`), `page-${String(p.idx).padStart(2,'0')}`);
    if (i < pages.length - 1) await sleep(8000);
  }
  console.log('Done!');
})();
