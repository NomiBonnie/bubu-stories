const fs = require('fs');
const path = require('path');

const config = JSON.parse(fs.readFileSync(`${process.env.HOME}/.config/azure-openai/config.json`));
const endpoint = config.image2_eastus2_endpoint;
const apiKey = config.image2_eastus2_api_key;
const url = `${endpoint}?api-version=2025-04-01-preview`;
const outDir = `${process.env.HOME}/.openclaw/workspace/bubu-stories/public/images/story47`;

const BUBU = "a small toddler white rabbit (100% snow-white fur, long ears with pink insides, big round brown eyes, small pink nose) wearing a pink summer dress with a pink bow on her ear, carrying a small pink backpack";
const SAM = "a golden retriever dad (golden fur, warm brown eyes) wearing a casual light blue linen shirt and khaki shorts (early summer attire)";
const TINA = "a cow mom (black and white spotted pattern, gentle dark eyes) wearing an elegant light floral blouse and white linen skirt (early summer attire)";
const NOMI = "a raccoon (grey-brown fur, black eye mask markings, ringed tail, big round clever eyes) wearing a blue-and-white striped sweater";
const NONO = "a small red bird (bright red feathers, round shiny eyes, orange-yellow beak, tiny and cute)";
const COCO = "a red panda (reddish-brown fur, round face, big bright eyes) wearing a yellow scarf";
const TEACHER = "an orange tabby cat teacher (warm orange fur with darker stripes, gentle eyes) wearing a cream-colored apron over a light green dress";

const PREFIX = "Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition 1024x1536.";
const SEASON = "Early summer setting (May) — bright warm sunshine, green trees, light breezy atmosphere.";

// Pages 7-18 (remaining)
const pages = [
  { num: 7, prompt: `${PREFIX} ${SEASON} Outdoor sidewalk scene with green trees and flowers. ${BUBU} walks carefully holding both hands close to her chest with a sweet protective expression, as if carrying something precious. ${NOMI} walks beside her, speaking reassuringly with one paw gently raised. ${NONO} flies nearby overhead. Morning sun is bright and warm. Bubu wears her pink backpack. Green leafy trees and blooming flowers along the path. Gentle warm atmosphere.` },
  { num: 8, prompt: `${PREFIX} ${SEASON} At a colorful kindergarten entrance gate decorated with flowers and a welcome sign. ${BUBU} stands at the threshold, one foot slightly forward, looking down at her open palm for courage. She takes a deep breath with slightly puffed cheeks. The kindergarten yard is visible behind with play equipment and colorful walls. Morning sunlight. Her pink backpack on her back. A brave determined expression forming on her face.` },
  { num: 9, prompt: `${PREFIX} ${SEASON} Just inside the kindergarten entrance, ${COCO} waves both paws excitedly at ${BUBU} who is stepping through the door. Coco has a big encouraging smile. Bubu looks slightly shy but is smiling back. The classroom is colorful and inviting behind them. Other small animal children visible in the background. Warm cheerful lighting.` },
  { num: 10, prompt: `${PREFIX} ${SEASON} In the bright colorful classroom, ${TEACHER} bends down to greet ${BUBU} who walks up to her proactively with a small wave. The teacher has a warm gentle smile and is patting Bubu's head. The classroom has children's drawings on walls, small tables and chairs, toys. Other small animal students settling in. Warm natural light from large windows.` },
  { num: 11, prompt: `${PREFIX} ${SEASON} A montage-style composition showing ${BUBU} happily engaged in classroom activities. She's painting a big yellow sun on an easel, with colorful blocks stacked into a tall castle nearby. Other small animal children around her. ${COCO} builds blocks beside her. ${NONO} perches on a shelf watching happily. Bright cheerful classroom with art supplies and toys everywhere. Bubu looks completely absorbed and happy.` },
  { num: 12, prompt: `${PREFIX} ${SEASON} Lunchtime in the kindergarten dining area. ${BUBU} sits at a small table eating happily from a colorful tray. She's reaching over to hand a water cup to a small animal friend beside her. ${NONO} sits on the windowsill nearby, flapping wings proudly. ${TEACHER} watches from behind with approval. The table has healthy food, small cups, and cheerful tablecloths. Warm midday light.` },
  { num: 13, prompt: `${PREFIX} ${SEASON} A quiet emotional moment: ${BUBU} sits by a window in the classroom, gently pressing her right palm against her cheek with closed eyes. A subtle warm golden glow comes from her palm. Her expression is peaceful and comforted, with a small tender smile. Soft afternoon light streams through the window. Other children play in the blurred background. ${NOMI} watches from nearby with a knowing gentle smile. Intimate and touching.` },
  { num: 14, prompt: `${PREFIX} ${SEASON} Nap room with small beds in rows. ${BUBU} lies on her little bed under a light blanket, both small hands held together over her heart, palms touching. Her eyes are closed peacefully, with a serene smile. Soft dim lighting with curtains partially drawn. Other small animal children sleeping in nearby beds. A calm, tranquil atmosphere.` },
  { num: 15, prompt: `${PREFIX} ${SEASON} ${TEACHER} is smiling warmly and placing colorful star stickers on ${BUBU}'s hand. Bubu looks down at the stickers with pure delight, eyes sparkling. She already has two stickers on the back of one hand. The teacher holds a sheet of stickers. Afternoon classroom light. ${COCO} and other children nearby look happy for her. Cheerful celebratory mood.` },
  { num: 16, prompt: `${PREFIX} ${SEASON} The kindergarten pickup area in warm late afternoon golden light. ${BUBU} is running with arms wide open toward ${TINA} who kneels with open arms. Bubu's expression is pure joy and excitement. Her pink backpack bounces as she runs. Tina has happy tears in her eyes. Other parents and children in the soft background. Green trees and warm sunset glow. Dynamic running pose, emotional reunion.` },
  { num: 17, prompt: `${PREFIX} ${SEASON} A warm group scene: ${TINA} holds ${BUBU} in a tight hug, while ${SAM} stands beside them gently patting Bubu's head. ${COCO} gives a thumbs-up with a proud smile. ${NOMI} and ${NONO} stand nearby, nodding with warm smiles. Late afternoon golden light. The kindergarten building in the background. Everyone looks happy and proud.` },
  { num: 18, prompt: `${PREFIX} ${SEASON} Beautiful sunset scene on a tree-lined path. ${BUBU} walks in the center, holding ${SAM}'s hand on one side and ${TINA}'s hand on the other. They walk toward the warm orange-pink sunset. Bubu looks up at her parents with a content peaceful smile. ${NOMI} walks alongside and ${NONO} flies above. Long warm shadows stretch behind them. Green trees frame the path. Golden hour lighting. A perfect ending shot.` }
];

async function generateImage(prompt, pageNum) {
  const paddedNum = String(pageNum).padStart(2, '0');
  const outPath = `${outDir}/page-${paddedNum}.png`;
  
  if (fs.existsSync(outPath) || fs.existsSync(outPath.replace('.png', '.jpg'))) {
    console.log(`Page ${paddedNum} already exists, skipping.`);
    return true;
  }
  
  console.log(`Generating page ${paddedNum}...`);
  const body = JSON.stringify({ prompt, n: 1, size: "1024x1536", quality: "medium", output_format: "png" });
  const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json', 'api-key': apiKey }, body });

  if (!res.ok) {
    const errText = await res.text();
    console.error(`Page ${paddedNum} FAILED (${res.status}): ${errText.slice(0,200)}`);
    return false;
  }

  const data = await res.json();
  if (data.data && data.data[0]) {
    const b64 = data.data[0].b64_json;
    if (b64) { fs.writeFileSync(outPath, Buffer.from(b64, 'base64')); console.log(`Page ${paddedNum} saved`); return true; }
    const imgUrl = data.data[0].url;
    if (imgUrl) { const r = await fetch(imgUrl); fs.writeFileSync(outPath, Buffer.from(await r.arrayBuffer())); console.log(`Page ${paddedNum} saved (url)`); return true; }
  }
  console.error(`Page ${paddedNum}: unexpected response`);
  return false;
}

async function main() {
  for (const p of pages) {
    let success = false;
    for (let attempt = 0; attempt < 3; attempt++) {
      success = await generateImage(p.prompt, p.num);
      if (success) break;
      console.log(`Retrying page ${p.num}...`);
      await new Promise(r => setTimeout(r, 10000));
    }
    if (!success) console.error(`FAILED page ${p.num} after 3 attempts`);
    await new Promise(r => setTimeout(r, 7000));
  }
  
  // Convert PNG to JPG
  console.log("Converting to JPG...");
  const { execSync } = require('child_process');
  const files = fs.readdirSync(outDir).filter(f => f.endsWith('.png'));
  for (const f of files) {
    const png = `${outDir}/${f}`;
    const jpg = png.replace('.png', '.jpg');
    try {
      execSync(`ffmpeg -y -i "${png}" -q:v 4 "${jpg}"`, { stdio: 'pipe' });
      fs.unlinkSync(png);
      const size = fs.statSync(jpg).size;
      console.log(`${f} -> jpg (${(size/1024).toFixed(0)}KB)`);
    } catch(e) { console.error(`Failed ${f}: ${e.message}`); }
  }
  console.log("DONE!");
}

main().catch(e => { console.error(e); process.exit(1); });
