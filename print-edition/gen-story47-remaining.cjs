const https = require('https');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const config = JSON.parse(fs.readFileSync(path.join(process.env.HOME, '.config/azure-openai/config.json'), 'utf8'));
const ENDPOINT = config.image2_eastus2_endpoint;
const API_KEY = config.image2_eastus2_api_key;
const API_VERSION = '2025-04-01-preview';

const BUBU = `a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow. She has a small pink bow centered ON TOP OF HER HEAD between her two ears. Toddler-like round body proportion.`;
const SAM_DAD = `Sam Dad: a GOLDEN RETRIEVER DOG (NOT human — an animal dog walking upright). Golden fur all over, dog snout/muzzle, floppy dog ears, wagging tail. Wears a dark navy jacket over a simple shirt. Warm gentle dog smile.`;
const TINA_MOM = `Tina Mom: a BLACK-AND-WHITE COW (NOT human — an animal cow walking upright). Black and white spotted fur pattern, small curved horns, cow ears, hooves. Wears an elegant cream knit cardigan over a floral skirt. Gentle warm cow smile.`;
const NOMI = `NOMI: a raccoon with grey-brown fur, black eye mask markings, ringed bushy tail. Wears a blue-and-white horizontally striped sweater. Clever bright eyes, nimble paws.`;
const NONO = `NONO: a small red bird with bright red feathers, round bright eyes, orange-yellow beak. Has TWO wings and TWO small bird feet. NO ARMS, NO HANDS — only wings.`;
const COCO = `Coco: a Red Panda with reddish-brown fur, round face, big round shiny eyes, wearing a yellow scarf. Slightly bigger than Bubu.`;
const YANYAN = `Teacher Yanyan: an orange tabby cat (NOT human), warm orange fur with subtle stripes, gentle green eyes, wearing a pink top with an apron with pockets. Adult-sized cat, warm and kind.`;

const STYLE = `Pixar 3D animation style, warm soft lighting, children's picture book illustration. Portrait orientation. The bottom 20% of the image should have a subtle dark gradient overlay. NO TEXT, NO WORDS, NO LETTERS anywhere in the image. Pure illustration only.`;

const tasks = [
  { page: 6, prompt: `${STYLE} Scene: Cheerful morning family moment. ${SAM_DAD} leans toward ${BUBU} with a warm smile, gently touching her small paw with his large golden paw. ${BUBU} giggles happily, both her small paws glowing with a subtle magical sparkle. Playful warm family interaction in their living room.` },
  { page: 7, prompt: `${STYLE} Scene: Walking to kindergarten. ${BUBU} carefully holds both small fists closed, protecting the kisses. ${NOMI} walks beside her with a reassuring gentle expression. Tree-lined morning path. ${BUBU} looks determined but careful.` },
  { page: 8, prompt: `${STYLE} Scene: Kindergarten gate. ${BUBU}'s steps slow down, she looks slightly hesitant. She looks down at her closed palm, takes a deep breath. The colorful kindergarten entrance is ahead. Moment of courage.` },
  { page: 9, prompt: `${STYLE} Scene: Just inside the kindergarten entrance. ${COCO} greets ${BUBU} happily, waving paws. ${BUBU} steps inside looking braver now. Colorful kindergarten hallway. Encouraging welcoming atmosphere.` },
  { page: 10, prompt: `${STYLE} Scene: Kindergarten classroom. ${YANYAN} stands at the front with a warm welcoming smile. ${BUBU} walks up confidently and greets the teacher. The teacher pats her head. Other animal children in the background. Cheerful classroom.` },
  { page: 11, prompt: `${STYLE} Scene: Montage-style kindergarten activities. ${BUBU} painting a big sun at an easel, building a tall block castle, and clapping along during singing time with other animal friends. Active joyful classroom.` },
  { page: 12, prompt: `${STYLE} Scene: Kindergarten lunch. ${BUBU} eats happily and helps pass a water cup to a friend beside her. ${NONO} perches on the windowsill flapping wings. Cozy lunch atmosphere.` },
  { page: 13, prompt: `${STYLE} Scene: Afternoon in kindergarten. ${BUBU} sits quietly, gently pressing her hand against her cheek with a soft tender smile. She misses Mommy. The hand on her cheek has a subtle warm glow. Emotional intimate moment, soft afternoon light.` },
  { page: 14, prompt: `${STYLE} Scene: Nap room. ${BUBU} lies peacefully in her small bed, holding both hands together at her chest. A subtle warm glow comes from her clasped hands. Her eyes are gently closed, sleeping peacefully. Serene quiet atmosphere.` },
  { page: 15, prompt: `${STYLE} Scene: After nap. ${YANYAN} smiles and places several star stickers on ${BUBU}'s hand. ${BUBU} looks at the stickers happily. Other kids in background waking up. Cheerful rewarding moment.` },
  { page: 16, prompt: `${STYLE} Scene: Kindergarten exit. ${BUBU} runs at full speed out of the classroom, leaping into ${TINA_MOM}'s open arms. Pure joy on both their faces. Emotional reunion. Afternoon golden light.` },
  { page: 17, prompt: `${STYLE} Scene: Outside kindergarten. ${TINA_MOM} hugs ${BUBU} tightly. ${SAM_DAD} gently pats ${BUBU}'s head. ${COCO} gives thumbs up nearby. ${NOMI} and ${NONO} stand beside them smiling and nodding. Warm family group scene.` },
  { page: 18, prompt: `${STYLE} Scene: Walking home at sunset. ${BUBU} holds ${SAM_DAD}'s hand in one hand and ${TINA_MOM}'s hand in the other. All three walk together bathed in warm golden sunset light. View from behind showing them walking toward the sunset. Peaceful, loving, warm conclusion.` },
];

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function generateImage(prompt) {
  return new Promise((resolve, reject) => {
    const url = new URL(`${ENDPOINT}?api-version=${API_VERSION}`);
    const body = JSON.stringify({ prompt, n: 1, size: '1024x1536', quality: 'medium', output_format: 'png' });
    const opts = {
      hostname: url.hostname, path: url.pathname + url.search, method: 'POST',
      headers: { 'Content-Type': 'application/json', 'api-key': API_KEY, 'Content-Length': Buffer.byteLength(body) },
    };
    const req = https.request(opts, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        if (res.statusCode === 429) return resolve({ retry: true });
        if (res.statusCode !== 200) return reject(new Error(`HTTP ${res.statusCode}: ${data.slice(0, 300)}`));
        try { resolve({ b64: JSON.parse(data).data[0].b64_json }); } catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function main() {
  const dir = path.join(__dirname, 'story47');
  for (let i = 0; i < tasks.length; i++) {
    const t = tasks[i];
    const jpgPath = path.join(dir, `page-${String(t.page).padStart(2, '0')}.jpg`);
    if (fs.existsSync(jpgPath)) { console.log(`page-${String(t.page).padStart(2,'0')}.jpg EXISTS, skip`); continue; }
    
    console.log(`[${i+1}/${tasks.length}] story47 page ${t.page}...`);
    let result;
    for (let a = 0; a < 3; a++) {
      try {
        result = await generateImage(t.prompt);
        if (result.retry) { console.log(`  429, wait 45s (${a+1}/3)`); await sleep(45000); continue; }
        break;
      } catch (e) {
        console.error(`  err ${a+1}: ${e.message.slice(0,100)}`);
        if (a < 2) await sleep(15000); else { result = null; }
      }
    }
    if (!result || result.retry) { console.error(`  FAILED page ${t.page}`); continue; }
    
    const pngPath = jpgPath.replace('.jpg', '.png');
    fs.writeFileSync(pngPath, Buffer.from(result.b64, 'base64'));
    execSync(`ffmpeg -y -i "${pngPath}" -q:v 2 "${jpgPath}" 2>/dev/null`);
    fs.unlinkSync(pngPath);
    console.log(`  ✅ ${(fs.statSync(jpgPath).size/1024).toFixed(0)}KB`);
    if (i < tasks.length - 1) await sleep(8000);
  }
  
  // Final report
  console.log('\n=== FINAL REPORT ===');
  for (const s of [44,45,46,47]) {
    const d = path.join(__dirname, `story${s}`);
    const files = fs.readdirSync(d).filter(f => f.match(/^page-\d+\.jpg$/)).sort();
    let total = 0;
    files.forEach(f => total += fs.statSync(path.join(d, f)).size);
    console.log(`Story ${s}: ${files.length} files, ${(total/1024/1024).toFixed(1)}MB`);
  }
}
main().catch(e => { console.error(e); process.exit(1); });
