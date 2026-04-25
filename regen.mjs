import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
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
  sam: 'golden retriever named Sam (Daddy), golden fur, large and warm, wearing a dark fitted jacket',
  tina: 'cow named Tina (Mommy), black and white patches, gentle and elegant, wearing a stylish knit top and skirt',
  doudou: 'hedgehog named Doudou (豆豆), brown body with dark brown spines, small round eyes, small and round',
  manman: 'turtle named Manman (慢慢), green shell with dark green pattern, light green skin, small round shell',
};

const STYLE = 'Pixar 3D animation style, warm soft lighting, children\'s picture book quality, vertical composition 1024x1536';
const COVER_EXTRA = ', with a clear banner/header area at the top for title text overlay';

// Build prompts for each story
function buildStory3Prompts() {
  // pages 7-13 (1-indexed), story has 13 pages
  const s = JSON.parse(readFileSync(join(BASE, '../stories/story3.json'), 'utf8'));
  const prompts = [];
  const pages = s.pages;
  
  // page-07: Bubu apologizes to Doudou
  prompts.push({ page: 7, prompt: `${STYLE}. Scene: In a sunny park sandpit, ${CHARS.bubu} is standing shyly, looking down and speaking softly to ${CHARS.doudou} who is sitting on the sand with tear-stained face. Bubu looks apologetic. The sandcastle is collapsed between them. A small shovel lies on the ground. ${CHARS.sam} watches warmly from behind.` });
  
  // page-08: Doudou forgives, let's play together
  prompts.push({ page: 8, prompt: `${STYLE}. Scene: In a sunny park sandpit, ${CHARS.doudou} is wiping tears and smiling, nodding at ${CHARS.bubu} who looks hopeful and happy. They are facing each other. Warm friendly atmosphere. Sandpit background with scattered sand toys.` });
  
  // page-09: Building sandcastle together
  prompts.push({ page: 9, prompt: `${STYLE}. Scene: ${CHARS.bubu} and ${CHARS.doudou} are happily building a big beautiful sandcastle together in the sandpit. Bubu holds a small shovel, Doudou pats sand with tiny paws. The sandcastle is bigger and prettier than before. Sunny park, joyful cooperation.` });
  
  // page-10: NOMI and NONO join with bucket and flag
  prompts.push({ page: 10, prompt: `${STYLE}. Scene: ${CHARS.bubu} and ${CHARS.doudou} are at their sandcastle. ${CHARS.nomi} arrives carrying a small water bucket, and ${CHARS.nono} flies in carrying a tiny flag in his beak to plant on top of the sandcastle. Everyone is happy and excited. Sunny park.` });
  
  // page-11: Tina watching everyone with smile
  prompts.push({ page: 11, prompt: `${STYLE}. Scene: ${CHARS.tina} stands nearby watching with a warm smile. In the foreground, ${CHARS.bubu}, ${CHARS.doudou}, ${CHARS.nomi}, and ${CHARS.nono} are gathered around a magnificent sandcastle with a flag on top. Sunny park, warm family atmosphere.` });
  
  // page-12: Walking home, Bubu holds Doudou's hand
  prompts.push({ page: 12, prompt: `${STYLE}. Scene: On a path at sunset, ${CHARS.bubu} is walking and gently holding ${CHARS.doudou}'s little paw (the soft palm side without spines). They look at each other happily. ${CHARS.sam} and ${CHARS.tina} walk behind them. Golden hour warm light, trees along the path.` });
  
  // page-13: Lesson learned page
  prompts.push({ page: 13, prompt: `${STYLE}. Scene: A warm summary illustration showing ${CHARS.bubu} and ${CHARS.doudou} playing happily together in the sandpit, sharing toys. ${CHARS.nomi} and ${CHARS.nono} are nearby. A speech bubble or gentle glow around them. Bright, cheerful, educational feel. Sunny park.` });
  
  return { story: 3, prompts };
}

function buildStory2Prompts() {
  const prompts = [];
  
  // page-01: COVER - rainbow morning
  prompts.push({ page: 1, prompt: `${STYLE}${COVER_EXTRA}. Cover illustration: ${CHARS.bubu} looking out a window in wonder at a magnificent rainbow spanning across a sky after rain. Bright colors, magical atmosphere, raindrops on the window.` });
  
  // page-02: Bubu at window amazed by rainbow
  prompts.push({ page: 2, prompt: `${STYLE}. Scene: ${CHARS.bubu} pressing her face against a window, eyes wide with wonder, looking at a huge beautiful rainbow in the sky after rain. Morning light, raindrops on glass, cozy room interior.` });
  
  // page-03: Bubu jumps down and runs outside
  prompts.push({ page: 3, prompt: `${STYLE}. Scene: ${CHARS.bubu} excitedly jumping off a windowsill and running out through the front door toward the rainbow. Dynamic motion, determined cute expression. House exterior, wet ground after rain, rainbow visible in sky.` });
  
  // page-04: Running to hilltop, rainbow still far
  prompts.push({ page: 4, prompt: `${STYLE}. Scene: ${CHARS.bubu} standing on top of a small grassy hill, looking up at a rainbow that still appears very far away. Slightly tired but determined expression. Wide landscape, post-rain freshness, puddles on grass.` });
  
  // page-05: Meeting NOMI picking mushrooms
  prompts.push({ page: 5, prompt: `${STYLE}. Scene: On a hillside, ${CHARS.nomi} is holding a basket of colorful mushrooms. ${CHARS.bubu} is running toward her excitedly. NOMI looks curious. Green hillside with wildflowers, rainbow visible in background sky.` });
  
  // page-06: Meeting NONO shaking off rain
  prompts.push({ page: 6, prompt: `${STYLE}. Scene: ${CHARS.nono} is perched on a tree branch, shaking rainwater off his bright red wings, water droplets flying. ${CHARS.bubu} and ${CHARS.nomi} look up at him from below. Forest path, wet leaves, rainbow in distant sky.` });
  
  // page-07: NONO flies high near clouds
  prompts.push({ page: 7, prompt: `${STYLE}. Scene: ${CHARS.nono} flying very high in the sky near fluffy white clouds, looking down and pointing with a wing. Far below on the ground, tiny figures of ${CHARS.bubu} and ${CHARS.nomi} look up. Rainbow arcs across the sky. Dramatic aerial perspective.` });
  
  // page-08: At the river, rainbow moved further
  prompts.push({ page: 8, prompt: `${STYLE}. Scene: ${CHARS.bubu}, ${CHARS.nomi}, and ${CHARS.nono} standing at a riverbank, looking disappointed. The rainbow appears to have moved even further away in the distance. Sparkling river, green banks, slightly cloudy sky.` });
  
  // page-09: Bubu tired, sitting on a stone
  prompts.push({ page: 9, prompt: `${STYLE}. Scene: ${CHARS.bubu} sitting tiredly on a round stone by the river, looking a bit sad and exhausted. ${CHARS.nomi} and ${CHARS.nono} nearby looking concerned. River flows gently, the rainbow is fading in the far distance.` });
  
  // page-10: NOMI discovers mini rainbows in water
  prompts.push({ page: 10, prompt: `${STYLE}. Scene: ${CHARS.nomi} excitedly pointing at the river surface where sunlight creates many small sparkling rainbows in the splashing water. ${CHARS.bubu} looks over with surprise. Magical glowing light effects on water, prismatic colors.` });
  
  // page-11: Bubu touches rainbow in her paw
  prompts.push({ page: 11, prompt: `${STYLE}. Scene: ${CHARS.bubu} reaching her small white paw into river water. Water splashes up and a tiny beautiful rainbow appears right in her palm. Her face shows pure joy and amazement. Close-up, magical prismatic light, sparkling water drops.` });
  
  // page-12: NONO makes rainbow at waterfall
  prompts.push({ page: 12, prompt: `${STYLE}. Scene: ${CHARS.nono} flying beside a small waterfall, flapping his bright red wings, creating a spray of mist. A vivid rainbow appears in the mist. NONO looks thrilled. Lush green surroundings, magical water mist.` });
  
  // page-13: NOMI's wisdom - rainbow is everywhere
  prompts.push({ page: 13, prompt: `${STYLE}. Scene: ${CHARS.nomi} smiling wisely, gesturing with her paws. ${CHARS.bubu} and ${CHARS.nono} listen attentively. Around them, multiple small rainbows appear in water droplets, puddles, and mist. Warm sunlight streaming through, magical atmosphere.` });
  
  // page-14: Walking home, jumping in puddles
  prompts.push({ page: 14, prompt: `${STYLE}. Scene: ${CHARS.bubu} happily hopping and splashing in puddles on a path, each puddle reflecting a tiny rainbow. ${CHARS.nomi} and ${CHARS.nono} follow joyfully. Sunset golden light, wet path lined with trees, magical rainbow reflections everywhere.` });
  
  // page-15: Lesson learned
  prompts.push({ page: 15, prompt: `${STYLE}. Scene: A warm summary illustration. ${CHARS.bubu}, ${CHARS.nomi}, and ${CHARS.nono} sitting together on a hillside, looking at both the rainbow in the sky and its reflections in a pond below. Dreamy, educational atmosphere, soft pastel colors, peaceful sunset.` });
  
  return { story: 2, prompts };
}

function buildStory1Prompts() {
  const prompts = [];
  
  // page-01: COVER
  prompts.push({ page: 1, prompt: `${STYLE}${COVER_EXTRA}. Cover illustration: ${CHARS.bubu} standing on a grassy hill at night, looking up at a big bright full moon. ${CHARS.nomi} and ${CHARS.nono} beside her. Magical moonlit scene, stars twinkling, dreamy night sky.` });
  
  // page-02: Bubu on green meadow, introduction
  prompts.push({ page: 2, prompt: `${STYLE}. Scene: ${CHARS.bubu} hopping joyfully on a lush green meadow at golden sunset. Long ears bouncing, happy expression. Wildflowers, butterflies, warm pastoral scene.` });
  
  // page-03: Introducing NOMI
  prompts.push({ page: 3, prompt: `${STYLE}. Scene: ${CHARS.nomi} waving happily on a green meadow. She looks clever and friendly. Background of gentle hills and flowers. Warm afternoon light.` });
  
  // page-04: Introducing NONO
  prompts.push({ page: 4, prompt: `${STYLE}. Scene: ${CHARS.nono} flying cheerfully through a bright blue sky with fluffy white clouds. Bright red feathers catching sunlight. Vibrant and energetic.` });
  
  // page-05: Bubu says goodnight to moon
  prompts.push({ page: 5, prompt: `${STYLE}. Scene: ${CHARS.bubu} sitting on a small grassy hilltop at night, looking up at a big beautiful full moon. Stars twinkling in dark blue sky. Peaceful, dreamy, serene atmosphere. Bubu has a happy gentle smile.` });
  
  // page-06: Moon is gone!
  prompts.push({ page: 6, prompt: `${STYLE}. Scene: ${CHARS.bubu} on the hilltop at night looking up at the sky with a worried expression. The sky is dark with only a few dim stars - NO moon visible. Slightly dramatic, mysterious atmosphere.` });
  
  // page-07: Bubu runs to find NOMI
  prompts.push({ page: 7, prompt: `${STYLE}. Scene: ${CHARS.bubu} running urgently through the meadow at night toward a cozy treehouse in the distance. Worried expression, ears flying back from running. Dark moonless night, few stars.` });
  
  // page-08: NOMI reading in tree hollow
  prompts.push({ page: 8, prompt: `${STYLE}. Scene: ${CHARS.nomi} wearing tiny round glasses, reading a book inside a cozy tree hollow lit by a warm lamp. ${CHARS.bubu} appears at the entrance looking worried. Bookshelf inside, warm cozy interior contrasting with dark night outside.` });
  
  // page-09: NONO flies high searching
  prompts.push({ page: 9, prompt: `${STYLE}. Scene: ${CHARS.nono} flying high in the dark night sky, searching around with determined eyes. Below on the ground, small figures of ${CHARS.bubu} and ${CHARS.nomi} look up. Stars visible but no moon. Dramatic night scene.` });
  
  // page-10: NONO finds moon in pond
  prompts.push({ page: 10, prompt: `${STYLE}. Scene: ${CHARS.nono} hovering excitedly above a pond, pointing down with his wing. A perfect full moon is reflected in the still pond water below. Magical glow, night scene, fireflies around the pond.` });
  
  // page-11: Bubu and NOMI look at moon reflection
  prompts.push({ page: 11, prompt: `${STYLE}. Scene: ${CHARS.bubu} and ${CHARS.nomi} at the edge of a pond, looking down in amazement at a perfect bright moon reflection in crystal clear water. Fireflies hover around. Magical, serene night atmosphere.` });
  
  // page-12: Bubu splashes, moon breaks
  prompts.push({ page: 12, prompt: `${STYLE}. Scene: ${CHARS.bubu} with her paw in pond water creating a big splash. The moon reflection shatters into shimmering fragments. ${CHARS.nomi} and ${CHARS.nono} getting splashed, with funny surprised expressions. Water droplets flying, comical and cute moment.` });
  
  // page-13: Real moon revealed in sky
  prompts.push({ page: 13, prompt: `${STYLE}. Scene: ${CHARS.bubu} looking up in amazement at a big beautiful full moon now visible in the night sky. ${CHARS.nomi} pointing up with a knowing smile. ${CHARS.nono} perched on NOMI's head. Beautiful moonlight bathing them all. Wonder and joy.` });
  
  // page-14: Three friends walk home, Bubu in bed
  prompts.push({ page: 14, prompt: `${STYLE}. Scene: ${CHARS.bubu} tucked in a cozy bed with soft blankets and pillows, looking out the window at the full moon with a sleepy happy smile. A warm bedside lamp glows. Stuffed raccoon and bird plush toys beside her pillow. Peaceful, dreamy bedtime scene.` });
  
  // page-15: Lesson learned
  prompts.push({ page: 15, prompt: `${STYLE}. Scene: A warm educational summary illustration. ${CHARS.bubu}, ${CHARS.nomi}, and ${CHARS.nono} sitting together on a hilltop, looking at the full moon in the sky and its reflection in a pond below. Soft pastel colors, dreamy atmosphere, gentle moonlight.` });
  
  return { story: 1, prompts };
}

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
  // gpt-image-2 may return b64_json instead of url
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
  const tasks = [
    buildStory3Prompts(),
    buildStory2Prompts(),
    buildStory1Prompts(),
  ];
  
  const results = { success: [], failed: [] };
  
  for (const { story, prompts } of tasks) {
    const dir = join(BASE, `story${story}`);
    mkdirSync(dir, { recursive: true });
    
    for (const { page, prompt } of prompts) {
      const pageStr = String(page).padStart(2, '0');
      const outPath = join(dir, `page-${pageStr}.jpg`);
      console.log(`[Story ${story}] Generating page-${pageStr}...`);
      
      try {
        const result = await generateImage(prompt);
        await downloadAndSave(result, outPath);
        const size = readFileSync(outPath).length;
        console.log(`  ✅ Saved (${(size/1024).toFixed(0)}KB)`);
        results.success.push(`story${story}/page-${pageStr}`);
      } catch (e) {
        console.error(`  ❌ Failed: ${e.message}`);
        results.failed.push(`story${story}/page-${pageStr}: ${e.message}`);
      }
      
      await sleep(7000);
    }
  }
  
  console.log(`\n=== DONE ===`);
  console.log(`Success: ${results.success.length}`);
  console.log(`Failed: ${results.failed.length}`);
  if (results.failed.length > 0) {
    console.log('Failed pages:');
    results.failed.forEach(f => console.log(`  - ${f}`));
  }
}

main().catch(e => { console.error(e); process.exit(1); });
