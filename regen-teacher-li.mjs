#!/usr/bin/env node
// Regenerate Teacher Li images: panda → white-tailed deer
// Pages: story56/page-14, story58/page-03, page-04, page-10, page-11
import fs from 'fs';
import path from 'path';

const WORKSPACE = '/Users/samyuan/.openclaw/workspace/bubu-stories';
const CONFIG = JSON.parse(fs.readFileSync(path.join(process.env.HOME, '.config/azure-openai/config.json'), 'utf8'));
const ENDPOINT = CONFIG.image_endpoint;
const API_KEY = CONFIG.image_api_key;
const API_VERSION = '2025-04-01-preview';
const DELAY_MS = 7500; // 9 RPM limit

// Character descriptions
const CHARS = {
  bubu: 'a pure snow-white rabbit toddler (Bubu) with long ears (pink inside), big round brown eyes, small pink nose, wearing a pink dress and a small pink bow centered on top of her head between her two ears, round chubby toddler proportions',
  teacher_li: 'a white-tailed deer teacher (Teacher Li) with deep brown smooth fur (no spots), white underside of tail, long eyelashes, gentle big deep-brown eyes, slender elegant build much taller than Bubu, wearing a light pink kindergarten apron, warm motherly smile, graceful long deer legs',
  teacher_kate: 'a red fox teacher (Teacher Kate) with reddish-brown fur, fluffy tail, wearing a light yellow kindergarten apron, friendly smile',
  teacher_gan: 'a gray koala teacher (Teacher Gan) with gray fluffy fur, big round eyes, black nose, wearing a light green kindergarten apron, gentle and slow-moving',
  teacher_yan: 'a black-and-white swallow teacher (Teacher Yan) with black upper body, white belly, forked tail, small and agile, flying gracefully',
  sam_dad: 'a golden retriever dad with golden fur, large warm build, wearing casual stylish clothes, gentle loving smile',
  tina_mom: 'a black-and-white cow mom with classic cow markings, medium-large build, elegant, wearing fashionable outfit, patient warm expression',
};

const STYLE = "Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition (9:16 aspect ratio).";

// Pages to regenerate
const PAGES = [
  {
    story: 56,
    page: 14,
    output: 'public/images/story56/page-14.jpg',
    prompt: `${STYLE} A warm kindergarten entrance scene. ${CHARS.teacher_li} is squatting down gracefully to be at eye level with ${CHARS.bubu}. Teacher Li extends her slender hand to gently hold Bubu's little hand, smiling warmly. The kindergarten door is behind them with colorful decorations. Bubu looks a little cautious but trusting, following Teacher Li. Warm morning sunlight, inviting atmosphere.`
  },
  {
    story: 58,
    page: 3,
    output: 'public/images/story58/page-03.jpg',
    prompt: `${STYLE} At the kindergarten gate on a sunny summer morning. ${CHARS.teacher_li} squatting down gracefully to meet ${CHARS.bubu} at eye level, smiling warmly with her big gentle brown eyes. Teacher Li's deep brown fur is smooth and elegant. Behind them, the kindergarten entrance is decorated with colorful artwork. ${CHARS.sam_dad} and ${CHARS.tina_mom} standing behind Bubu, smiling. Warm golden morning light.`
  },
  {
    story: 58,
    page: 4,
    output: 'public/images/story58/page-04.jpg',
    prompt: `${STYLE} Inside a bright cheerful kindergarten classroom. ${CHARS.teacher_li} holding ${CHARS.bubu}'s small hand, walking into the classroom together. Teacher Li is tall and elegant with her slender deer legs, looking down at Bubu with a warm smile. Several animal toddler classmates are playing in the background (building blocks, drawing). Colorful classroom decorations, warm lighting, welcoming atmosphere.`
  },
  {
    story: 58,
    page: 10,
    output: 'public/images/story58/page-10.jpg',
    prompt: `${STYLE} Lunchtime scene in a kindergarten dining area. ${CHARS.teacher_li} helping ${CHARS.bubu} with a steaming bowl of tomato egg soup. Teacher Li is bending down gracefully with her elegant deer posture, carefully serving the soup. Bubu is sitting at a small table, blowing on the soup. Other animal toddlers eating at nearby tables. Warm cozy lunchtime atmosphere, steam rising from food.`
  },
  {
    story: 58,
    page: 11,
    output: 'public/images/story58/page-11.jpg',
    prompt: `${STYLE} Naptime scene in a kindergarten. ${CHARS.bubu} lying on a small cot, hugging a bunny-shaped pillow, eyes half-closed and drowsy. ${CHARS.teacher_li} sitting beside the cot, gently patting Bubu's back with her slender hand, humming a lullaby. Soft dim lighting, other toddlers sleeping on nearby cots. Peaceful, cozy, dreamlike atmosphere with soft warm tones.`
  },
];

async function generateImage(prompt, outputPath) {
  const url = `${ENDPOINT}openai/deployments/gpt-image-1.5/images/generations?api-version=${API_VERSION}`;
  const body = JSON.stringify({
    prompt,
    n: 1,
    size: '1024x1792',
    quality: 'medium',
    output_format: 'b64_json',
  });

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'api-key': API_KEY,
    },
    body,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text.slice(0, 200)}`);
  }

  const data = await res.json();
  const b64 = data.data[0].b64_json;
  const buffer = Buffer.from(b64, 'base64');
  
  const fullPath = path.join(WORKSPACE, outputPath);
  fs.mkdirSync(path.dirname(fullPath), { recursive: true });
  fs.writeFileSync(fullPath, buffer);
  console.log(`✅ Saved: ${outputPath} (${(buffer.length / 1024).toFixed(0)}KB)`);
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function main() {
  console.log(`🎨 Regenerating ${PAGES.length} images (Teacher Li: panda → white-tailed deer)`);
  console.log(`Rate limit: ${DELAY_MS}ms between requests\n`);

  for (let i = 0; i < PAGES.length; i++) {
    const p = PAGES[i];
    console.log(`[${i+1}/${PAGES.length}] Story ${p.story} page ${p.page}...`);
    try {
      await generateImage(p.prompt, p.output);
    } catch (e) {
      console.error(`❌ Failed: ${e.message}`);
    }
    if (i < PAGES.length - 1) {
      console.log(`  Waiting ${DELAY_MS/1000}s...`);
      await sleep(DELAY_MS);
    }
  }
  console.log('\n🎉 Done! All Teacher Li images regenerated.');
}

main().catch(e => { console.error(e); process.exit(1); });
