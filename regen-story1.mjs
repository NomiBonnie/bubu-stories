import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const config = JSON.parse(readFileSync(join(process.env.HOME, '.config/azure-openai/config.json'), 'utf8'));
const endpoint = config.image2_poland_endpoint.replace(/\/$/, '');
const apiKey = config.image2_poland_api_key;
const deployment = config.image2_poland_deployment;
const BASE = '/Users/samyuan/.openclaw/workspace/bubu-stories/public/images';

const CHARS = {
  bubu: 'snow-white rabbit named Bubu (咘咘), long floppy ears with pink inner, big round brown eyes, small pink nose, wearing a pink dress with a pink bow on her head, toddler proportions, round and cute',
  nomi: 'raccoon named NOMI (grey-brown fur, black eye mask, ringed fluffy tail), big round eyes, wearing a blue-and-white striped sweater, dexterous paws',
  nono: 'small bird named NONO (bright red feathers), tiny and round, round bright eyes, orange-yellow beak',
};

const STYLE = 'Pixar 3D animation style, warm soft lighting, children\'s picture book quality, vertical composition 1024x1536';
const COVER_EXTRA = ', with a clear banner/header area at the top for title text overlay';

const prompts = [
  // page-01: COVER
  { page: 1, prompt: `${STYLE}${COVER_EXTRA}. Cover illustration: ${CHARS.bubu} standing on a grassy hill at night, looking up at a big bright full moon. ${CHARS.nomi} and ${CHARS.nono} beside her. Magical moonlit scene, stars twinkling, dreamy night sky.` },
  
  // page-02: Bubu on green meadow
  { page: 2, prompt: `${STYLE}. Scene: ${CHARS.bubu} hopping joyfully on a lush green meadow at golden sunset. Long ears bouncing, happy expression. Wildflowers, butterflies, warm pastoral scene.` },
  
  // page-03: NOMI
  { page: 3, prompt: `${STYLE}. Scene: ${CHARS.nomi} waving happily on a green meadow. She looks clever and friendly. Background of gentle hills and flowers. Warm afternoon light.` },
  
  // page-04: NONO
  { page: 4, prompt: `${STYLE}. Scene: ${CHARS.nono} flying cheerfully through a bright blue sky with fluffy white clouds. Bright red feathers catching sunlight. Vibrant and energetic.` },
  
  // page-05: Bubu says goodnight to moon
  { page: 5, prompt: `${STYLE}. Scene: ${CHARS.bubu} sitting on a small grassy hilltop at night, looking up at a big beautiful full moon. Stars twinkling in dark blue sky. Peaceful, dreamy, serene atmosphere. Bubu has a happy gentle smile.` },
  
  // page-06: Moon is gone!
  { page: 6, prompt: `${STYLE}. Scene: ${CHARS.bubu} on the hilltop at night looking up at the sky with a worried expression. The sky is dark with only a few dim stars - NO moon visible. Slightly dramatic, mysterious atmosphere.` },
  
  // page-07: Bubu runs to find NOMI
  { page: 7, prompt: `${STYLE}. Scene: ${CHARS.bubu} running urgently through the meadow at night toward a cozy treehouse in the distance. Worried expression, ears flying back from running. Dark moonless night, few stars.` },
  
  // page-08: NOMI reading in tree hollow
  { page: 8, prompt: `${STYLE}. Scene: ${CHARS.nomi} wearing tiny round glasses, reading a book inside a cozy tree hollow lit by a warm lamp. ${CHARS.bubu} appears at the entrance looking worried. Bookshelf inside, warm cozy interior contrasting with dark night outside.` },
  
  // page-09: NONO flies high searching
  { page: 9, prompt: `${STYLE}. Scene: ${CHARS.nono} flying high in the dark night sky, searching around with determined eyes. Below on the ground, small figures of ${CHARS.bubu} and ${CHARS.nomi} look up. Stars visible but no moon. Dramatic night scene.` },
  
  // page-10: NONO finds moon in pond
  { page: 10, prompt: `${STYLE}. Scene: ${CHARS.nono} hovering excitedly above a pond, pointing down with his wing. A perfect full moon is reflected in the still pond water below. Magical glow, night scene, fireflies around the pond.` },
  
  // page-11: Bubu and NOMI look at moon reflection
  { page: 11, prompt: `${STYLE}. Scene: ${CHARS.bubu} and ${CHARS.nomi} at the edge of a pond, looking down in amazement at a perfect bright moon reflection in crystal clear water. Fireflies hover around. Magical, serene night atmosphere.` },
  
  // page-12: Bubu splashes, moon breaks
  { page: 12, prompt: `${STYLE}. Scene: ${CHARS.bubu} with her paw in pond water creating a big splash. The moon reflection shatters into shimmering fragments. ${CHARS.nomi} and ${CHARS.nono} getting splashed, with funny surprised expressions. Water droplets flying, comical and cute moment.` },
  
  // page-13: Real moon revealed in sky
  { page: 13, prompt: `${STYLE}. Scene: ${CHARS.bubu} looking up in amazement at a big beautiful full moon now visible in the night sky. ${CHARS.nomi} pointing up with a knowing smile. ${CHARS.nono} perched on NOMI's head. Beautiful moonlight bathing them all. Wonder and joy.` },
  
  // page-14: Bubu in bed
  { page: 14, prompt: `${STYLE}. Scene: ${CHARS.bubu} tucked in a cozy bed with soft blankets and pillows, looking out the window at the full moon with a sleepy happy smile. A warm bedside lamp glows. Stuffed raccoon and bird plush toys beside her pillow. Peaceful, dreamy bedtime scene.` },
  
  // page-15: Lesson learned
  { page: 15, prompt: `${STYLE}. Scene: A warm educational summary illustration. ${CHARS.bubu}, ${CHARS.nomi}, and ${CHARS.nono} sitting together on a hilltop, looking at the full moon in the sky and its reflection in a pond below. Soft pastel colors, dreamy atmosphere, gentle moonlight.` },
];

async function generateImage(prompt) {
  const url = `${endpoint}/openai/deployments/${deployment}/images/generations?api-version=2025-04-01-preview`;
  const resp = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'api-key': apiKey },
    body: JSON.stringify({ prompt, n: 1, size: '1024x1536', quality: 'medium' })
  });
  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`API ${resp.status}: ${text}`);
  }
  const data = await resp.json();
  if (data.data[0].b64_json) {
    return { b64: data.data[0].b64_json };
  }
  return { url: data.data[0].url };
}

async function downloadAndSave(result, path) {
  if (result.b64) {
    writeFileSync(path, Buffer.from(result.b64, 'base64'));
  } else {
    const resp = await fetch(result.url);
    const buf = Buffer.from(await resp.arrayBuffer());
    writeFileSync(path, buf);
  }
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function main() {
  const dir = join(BASE, 'story1');
  mkdirSync(dir, { recursive: true });
  
  const results = { success: [], failed: [] };
  
  for (const { page, prompt } of prompts) {
    const pageStr = String(page).padStart(2, '0');
    const outPath = join(dir, `page-${pageStr}.jpg`);
    console.log(`[Story 1] Generating page-${pageStr}...`);
    
    try {
      const result = await generateImage(prompt);
      await downloadAndSave(result, outPath);
      const size = readFileSync(outPath).length;
      console.log(`  ✅ Saved (${(size/1024).toFixed(0)}KB)`);
      results.success.push(`page-${pageStr}`);
    } catch (e) {
      console.error(`  ❌ Failed: ${e.message}`);
      results.failed.push(`page-${pageStr}: ${e.message}`);
    }
    
    await sleep(7000);
  }
  
  console.log(`\n=== Story 1 Complete ===`);
  console.log(`Success: ${results.success.length}/15`);
  console.log(`Failed: ${results.failed.length}`);
  if (results.failed.length > 0) {
    console.log('Failed pages:');
    results.failed.forEach(f => console.log(`  - ${f}`));
  }
}

main().catch(e => { console.error(e); process.exit(1); });
