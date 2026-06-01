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
const WAIGONG = `Grandpa (Waigong): a horse with dark brown fur, grey-white mane, deep calm eyes. Wears a polo shirt and casual pants.`;
const WAIPO = `Grandma (Waipo): a goat with light grey-white fur, small curved horns, warm brown eyes, short goat beard. Wears a floral blouse and light pants with a sun hat.`;

const STYLE = `Pixar 3D animation style, warm soft lighting, children's picture book illustration. Portrait orientation. The bottom 20% of the image should have a subtle dark gradient overlay. NO TEXT, NO WORDS, NO LETTERS anywhere in the image. Pure illustration only.`;

// Story 44 scenes
const story44 = [
  { page: 2, prompt: `${STYLE} Scene: A safari zoo entrance with rows of colorful electric carts (blue, green, yellow) with two rows of seats each. ${BUBU} is bouncing excitedly, tugging the hands of ${SAM_DAD} on her left and ${TINA_MOM} on her right. ${COCO} follows behind excitedly. Bright sunny outdoor scene with zoo entrance arch.` },
  { page: 3, prompt: `${STYLE} Scene: Everyone in a blue electric safari cart. ${BUBU} sits front row center. ${SAM_DAD} on the left, ${TINA_MOM} on the right. ${NOMI} and ${COCO} sit in the back row. ${NONO} perches on top of the cart's railing as lookout. A friendly elephant zookeeper hands them a basket of carrots and vegetables.` },
  { page: 4, prompt: `${STYLE} Scene: Ostrich zone in a safari park. Two tall ostriches stretch their long necks toward the electric cart. ${BUBU} holds up a carrot, half excited half scared, shrinking toward ${TINA_MOM}. One ostrich snatches the carrot. ${COCO} claps in the back seat. Green grassy savanna setting.` },
  { page: 5, prompt: `${STYLE} Scene: Alpaca zone. Three fluffy white alpacas gently lower heads to eat vegetables from ${BUBU}'s hand. ${BUBU} touches an alpaca's wool with wonder. ${SAM_DAD} watches with a warm smile. Soft grassy area with fence.` },
  { page: 6, prompt: `${STYLE} Scene: A small lake in a safari park. White swans glide gracefully on the water. ${BUBU} places a leaf by the water's edge, a swan delicately picks it up. ${COCO} watches mesmerized from the cart. ${NONO} flies near the lakeside, chirping at the swans. Peaceful water reflections.` },
  { page: 7, prompt: `${STYLE} Scene: Pony zone. A brown pony stands by the safari cart, chomping loudly on a carrot. ${BUBU} covers her mouth laughing so hard she bends over. ${TINA_MOM} also laughs. Fun energetic scene.` },
  { page: 8, prompt: `${STYLE} Scene: Camel zone. A large camel lowers its head with a huge mouth and long tongue reaching for a carrot. ${BUBU} stares wide-eyed in amazement. In the back row, ${NOMI} grabs ${COCO}'s arm nervously. ${COCO} pats NOMI reassuringly. Desert-like area in the safari.` },
  { page: 9, prompt: `${STYLE} Scene: A large pond in a safari park. ${SAM_DAD} points toward the water. ${BUBU} looks where he's pointing — a hippo mostly submerged with only two eyes and a round nose visible above water. ${BUBU} tilts her head curiously. Calm water scene.` },
  { page: 10, prompt: `${STYLE} Scene: Raccoon exhibit in a zoo. Behind a fence, many chubby little raccoons with black mask markings and striped tails. ${NOMI} stands up excitedly in the cart, tail wagging. ${BUBU} takes out a small cookie to toss over the fence. ${NOMI} looks thrilled to see raccoons that look like her family.` },
  { page: 11, prompt: `${STYLE} Scene: Close-up of the raccoon exhibit. Multiple chubby raccoons scrambling and pushing each other with fat little paws, fighting over a cookie. Round bottoms bumping. ${NOMI} watches from the cart with proud joyful expression, eyes crinkled with laughter. Funny chaotic scene.` },
  { page: 12, prompt: `${STYLE} Scene: The smallest raccoon in the exhibit hugs a cookie in its arms, nibbling in a corner. Other raccoons gather around watching longingly. ${BUBU} tosses more cookies over the fence. ${COCO} laughs. ${NOMI} rubs her nose shyly. Cute heartwarming scene.` },
  { page: 13, prompt: `${STYLE} Scene: Sunset at the safari park. The electric cart drives toward the exit. ${BUBU} turns around waving goodbye. In the distance, little raccoons stand by the fence waving their tiny paws. Golden sunset light bathes the zoo meadow. ${NOMI} has a soft expression. Warm farewell scene.` },
];

// Story 45 scenes
const story45 = [
  { page: 2, prompt: `${STYLE} Scene: Morning at home. ${BUBU} stands in front of a full-length mirror wearing her pink dress and a small colorful backpack, checking herself left and right excitedly. Bedroom setting, morning light.` },
  { page: 3, prompt: `${STYLE} Scene: Walking to kindergarten. ${SAM_DAD} holds Bubu's left hand, ${TINA_MOM} holds her right hand. ${WAIGONG} and ${WAIPO} walk behind them. Everyone is chatting happily. Tree-lined street with a kindergarten visible ahead. ${BUBU} walks between her parents.` },
  { page: 4, prompt: `${STYLE} Scene: Kindergarten entrance with a big colorful gate/arch. ${BUBU} suddenly grips ${TINA_MOM}'s hand tightly, looking nervous and hesitant. The kindergarten building is cheerful and colorful behind them.` },
  { page: 5, prompt: `${STYLE} Scene: Outside kindergarten. ${NOMI} kneels down to ${BUBU}'s level, gently patting her head with a warm smile. ${COCO} waves her little paws encouragingly. ${BUBU} looks a bit uncertain but comforted. ${NONO} perches nearby.` },
  { page: 6, prompt: `${STYLE} Scene: At the kindergarten entrance. ${YANYAN} kneels down to greet ${BUBU} with a warm welcoming smile. ${BUBU} peeks up shyly at the teacher. The teacher extends a friendly paw. Colorful kindergarten interior visible behind.` },
  { page: 7, prompt: `${STYLE} Scene: Kindergarten classroom with toys and colorful decorations. ${BUBU} stands at the doorway looking shy. A little deer (fawn with white spots, wearing a small vest) walks over to her, showing building blocks and a castle made of blocks. Other animal children play in the background.` },
  { page: 8, prompt: `${STYLE} Scene: Kindergarten classroom full of activity. ${BUBU} happily paints with new friends (a little bear cub, a corgi puppy, a grey-white kitten). They sing and dance. Colorful artwork on walls. Joyful atmosphere with laughter.` },
  { page: 9, prompt: `${STYLE} Scene: Kindergarten lunch room. Little animal children sit in a row at a low table, each with a bowl of food. ${BUBU} eats happily, turning to talk to the friend next to her. Cozy dining atmosphere.` },
  { page: 10, prompt: `${STYLE} Scene: Nap room in kindergarten. Rows of small beds. All the little animal children are sleeping with eyes closed, except ${BUBU} who lies in her bed with eyes wide open, staring up at the ceiling. A small dragonfly flutters near the ceiling. Quiet dim naptime lighting.` },
  { page: 11, prompt: `${STYLE} Scene: Nap room. ${YANYAN} sits beside ${BUBU}'s small bed, gently patting her back. ${BUBU} relaxes, eyes closing. Soft warm dim lighting, peaceful and safe feeling.` },
  { page: 12, prompt: `${STYLE} Scene: Kindergarten entrance at pickup time. ${BUBU} runs out of the classroom with arms wide open. ${SAM_DAD}, ${TINA_MOM}, ${WAIGONG}, and ${WAIPO} all wait outside. ${BUBU} dashes toward them joyfully. Afternoon light.` },
  { page: 13, prompt: `${STYLE} Scene: Walking home from kindergarten. ${BUBU} proudly holds up a colorful painting. ${SAM_DAD} and ${TINA_MOM} walk beside her, beaming with pride. ${COCO} claps nearby. ${NOMI} gives thumbs up. ${NONO} flies overhead. ${BUBU} holds her chin up confidently. Warm golden hour light.` },
];

// Story 46 scenes
const story46 = [
  { page: 2, prompt: `${STYLE} Scene: ${BUBU}'s bedroom, morning. ${BUBU} sits on the edge of her bed looking worried and lost in thought. Morning light through window. She remembers yesterday's naptime. Worried expression, clutching her blanket.` },
  { page: 3, prompt: `${STYLE} Scene: ${BUBU}'s bedroom. ${NOMI} kneels in front of ${BUBU} with an encouraging smile. ${COCO} hops onto the headboard of the bed. ${BUBU} starts to look a bit brighter. Morning light.` },
  { page: 4, prompt: `${STYLE} Scene: Kindergarten entrance. ${BUBU} waves cheerfully and confidently at ${YANYAN} who stands at the entrance. ${BUBU} is not nervous today, she looks happy. The teacher smiles warmly and pats her head.` },
  { page: 5, prompt: `${STYLE} Scene: Kindergarten classroom. ${BUBU} sits at a table drawing with her animal friends (a little deer, a bear cub, a corgi). She proudly holds up her drawing of a big sun and a bunny. Happy collaborative atmosphere.` },
  { page: 6, prompt: `${STYLE} Scene: Kindergarten lunchtime. ${BUBU} eats happily. The little animal friend next to her dropped a spoon. ${BUBU} kindly hands over a new spoon. ${YANYAN} watches from across the room, nodding with a smile. Warm cafeteria setting.` },
  { page: 7, prompt: `${STYLE} Scene: Kindergarten classroom. ${YANYAN} claps her hands gently announcing naptime. ${BUBU} sits at her desk, heart pounding, looking slightly nervous, remembering yesterday. Other children start getting up. Transitional moment.` },
  { page: 8, prompt: `${STYLE} Scene: Nap room. ${YANYAN} sits beside ${BUBU}'s small bed, leaning close and whispering softly with a gentle encouraging expression. ${BUBU} lies in bed looking up at the teacher. Soft dim naptime lighting.` },
  { page: 9, prompt: `${STYLE} Scene: Dreamy, soft-focus illustration. ${BUBU} lies in bed with eyes closed, a peaceful smile forming. Around her head, floating soft-glow dream bubbles show NOMI's encouraging face, Coco waving, and Mom and Dad's smiling faces. Warm ethereal atmosphere.` },
  { page: 10, prompt: `${STYLE} Scene: Nap room. ${BUBU} sits up in her small bed, eyes sparkling with surprise and delight, rubbing her face. She just realized she actually fell asleep! Other kids still waking up around her. Morning light through curtains.` },
  { page: 11, prompt: `${STYLE} Scene: Kindergarten classroom. ${YANYAN} walks toward ${BUBU} holding a sparkling gold star sticker. She gently places it on ${BUBU}'s chest. ${BUBU} looks down at it with wonder and pride. Warm glowing highlight on the star sticker. Celebratory moment.` },
  { page: 12, prompt: `${STYLE} Scene: Kindergarten entrance at pickup. ${BUBU} runs and leaps into the arms of ${SAM_DAD} and ${TINA_MOM}. She proudly points at the gold star on her chest. ${SAM_DAD} lifts her high in the air. Joyful reunion, afternoon light.` },
  { page: 13, prompt: `${STYLE} Scene: Walking home. ${BUBU} keeps looking down at the gold star sticker on her chest, grinning ear to ear. ${COCO} walks beside her happily. ${NOMI} gives a thumbs up. ${NONO} flies overhead singing. Golden hour warm light, tree-lined path.` },
];

// Story 47 scenes
const story47 = [
  { page: 2, prompt: `${STYLE} Scene: ${BUBU}'s bedroom, early morning. ${BUBU} lies in bed pulling the blanket up to her nose, pouting, not wanting to get up. Alarm clock on bedside table. Soft morning light. Reluctant moody atmosphere.` },
  { page: 3, prompt: `${STYLE} Scene: ${BUBU}'s bedroom. ${SAM_DAD} sits on the bed edge, gently touching ${BUBU}'s ear. ${BUBU} looks up at him sadly, still under the blanket. Soft intimate morning scene.` },
  { page: 4, prompt: `${STYLE} Scene: Emotional close-up. ${TINA_MOM} kneels down and gently holds ${BUBU}'s small hand, kissing her palm tenderly. ${BUBU} watches with big curious eyes. Warm intimate moment, soft golden light. Key emotional scene.` },
  { page: 5, prompt: `${STYLE} Scene: Close-up of ${BUBU} looking down at her own open palm with wonder. A tiny magical glowing kiss mark appears in her palm (soft pink/golden sparkle). Her eyes light up with amazement. Magical warm lighting.` },
  { page: 6, prompt: `${STYLE} Scene: ${SAM_DAD} leans in with a smile, kissing ${BUBU}'s other palm. ${BUBU} giggles. Both her palms now have a subtle magical glow. Playful warm family moment.` },
  { page: 7, prompt: `${STYLE} Scene: Walking to kindergarten. ${BUBU} carefully holds both small fists closed, protecting the kisses. ${NOMI} walks beside her with a reassuring gentle expression. Tree-lined morning path. ${BUBU} looks determined but careful.` },
  { page: 8, prompt: `${STYLE} Scene: Kindergarten gate. ${BUBU}'s steps slow down, she looks slightly hesitant. She looks down at her closed palm, takes a deep breath. The colorful kindergarten entrance is ahead. Moment of courage.` },
  { page: 9, prompt: `${STYLE} Scene: Just inside the kindergarten entrance. ${COCO} greets ${BUBU} happily, waving paws. ${BUBU} steps inside looking braver now. Colorful kindergarten hallway. Encouraging welcoming atmosphere.` },
  { page: 10, prompt: `${STYLE} Scene: Kindergarten classroom. ${YANYAN} stands at the front with a warm welcoming smile. ${BUBU} walks up confidently and greets the teacher. The teacher pats her head. Other animal children in the background. Cheerful classroom.` },
  { page: 11, prompt: `${STYLE} Scene: Montage-style kindergarten activities. ${BUBU} painting a big sun at an easel, building a tall block castle, and clapping along during singing time with other animal friends. Active joyful classroom. Multiple activities shown.` },
  { page: 12, prompt: `${STYLE} Scene: Kindergarten lunch. ${BUBU} eats happily and helps pass a water cup to a friend beside her. ${NONO} perches on the windowsill flapping wings. Cozy lunch atmosphere.` },
  { page: 13, prompt: `${STYLE} Scene: Afternoon in kindergarten. ${BUBU} sits quietly, gently pressing her hand against her cheek with a soft tender smile. She misses Mommy. The hand on her cheek has a subtle warm glow. Emotional intimate moment, soft afternoon light.` },
  { page: 14, prompt: `${STYLE} Scene: Nap room. ${BUBU} lies peacefully in her small bed, holding both hands together at her chest. A subtle warm glow comes from her clasped hands. Her eyes are gently closed, sleeping peacefully. Serene quiet atmosphere.` },
  { page: 15, prompt: `${STYLE} Scene: After nap. ${YANYAN} smiles and places several star stickers on ${BUBU}'s hand. ${BUBU} looks at the stickers happily. Other kids in background waking up. Cheerful rewarding moment.` },
  { page: 16, prompt: `${STYLE} Scene: Kindergarten exit. ${BUBU} runs at full speed out of the classroom, leaping into ${TINA_MOM}'s open arms. Pure joy on both their faces. Emotional reunion. Afternoon golden light.` },
  { page: 17, prompt: `${STYLE} Scene: Outside kindergarten. ${TINA_MOM} hugs ${BUBU} tightly. ${SAM_DAD} gently pats ${BUBU}'s head. ${COCO} gives thumbs up nearby. ${NOMI} and ${NONO} stand beside them smiling and nodding. Warm family group scene.` },
  { page: 18, prompt: `${STYLE} Scene: Walking home at sunset. ${BUBU} holds ${SAM_DAD}'s hand in one hand and ${TINA_MOM}'s hand in the other. All three walk together bathed in warm golden sunset light. View from behind showing them walking toward the sunset. Peaceful, loving, warm conclusion. Silhouette-like with warm golden tones.` },
];

const allTasks = [
  ...story44.map(s => ({ ...s, story: 44 })),
  ...story45.map(s => ({ ...s, story: 45 })),
  ...story46.map(s => ({ ...s, story: 46 })),
  ...story47.map(s => ({ ...s, story: 47 })),
];

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function generateImage(prompt) {
  return new Promise((resolve, reject) => {
    const url = new URL(`${ENDPOINT}?api-version=${API_VERSION}`);
    const body = JSON.stringify({
      prompt,
      n: 1,
      size: '1024x1536',
      quality: 'medium',
      output_format: 'png',
    });
    const opts = {
      hostname: url.hostname,
      path: url.pathname + url.search,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'api-key': API_KEY,
        'Content-Length': Buffer.byteLength(body),
      },
    };
    const req = https.request(opts, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        if (res.statusCode === 429) return resolve({ retry: true, raw: data });
        if (res.statusCode !== 200) return reject(new Error(`HTTP ${res.statusCode}: ${data.slice(0, 300)}`));
        try {
          const j = JSON.parse(data);
          resolve({ b64: j.data[0].b64_json });
        } catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function main() {
  const startIdx = parseInt(process.env.START_IDX || '0');
  console.log(`Total tasks: ${allTasks.length}, starting from index ${startIdx}`);
  
  for (let i = startIdx; i < allTasks.length; i++) {
    const t = allTasks[i];
    const dir = path.join(__dirname, `story${t.story}`);
    const jpgPath = path.join(dir, `page-${String(t.page).padStart(2, '0')}.jpg`);
    
    if (fs.existsSync(jpgPath)) {
      console.log(`[${i+1}/${allTasks.length}] story${t.story}/page-${String(t.page).padStart(2, '0')}.jpg EXISTS, skipping`);
      continue;
    }
    
    console.log(`[${i+1}/${allTasks.length}] Generating story${t.story} page ${t.page}...`);
    
    let result;
    for (let attempt = 0; attempt < 3; attempt++) {
      try {
        result = await generateImage(t.prompt);
        if (result.retry) {
          console.log(`  429 rate limited, waiting 45s (attempt ${attempt+1}/3)...`);
          await sleep(45000);
          continue;
        }
        break;
      } catch (e) {
        console.error(`  Error attempt ${attempt+1}: ${e.message}`);
        if (attempt < 2) await sleep(15000);
        else throw e;
      }
    }
    
    if (!result || result.retry) {
      console.error(`  FAILED after 3 retries, skipping`);
      continue;
    }
    
    // Save PNG then convert to JPG
    const pngPath = path.join(dir, `page-${String(t.page).padStart(2, '0')}.png`);
    fs.writeFileSync(pngPath, Buffer.from(result.b64, 'base64'));
    execSync(`ffmpeg -y -i "${pngPath}" -q:v 2 "${jpgPath}" 2>/dev/null`);
    fs.unlinkSync(pngPath);
    
    const size = fs.statSync(jpgPath).size;
    console.log(`  ✅ ${jpgPath} (${(size/1024).toFixed(0)}KB)`);
    
    if (i < allTasks.length - 1) await sleep(8000);
  }
  
  // Report
  console.log('\n=== COMPLETION REPORT ===');
  for (const storyNum of [44, 45, 46, 47]) {
    const dir = path.join(__dirname, `story${storyNum}`);
    const files = fs.readdirSync(dir).filter(f => f.endsWith('.jpg')).sort();
    let totalSize = 0;
    files.forEach(f => totalSize += fs.statSync(path.join(dir, f)).size);
    console.log(`Story ${storyNum}: ${files.length} files, total ${(totalSize/1024/1024).toFixed(1)}MB`);
    files.forEach(f => {
      const s = fs.statSync(path.join(dir, f)).size;
      console.log(`  ${f}: ${(s/1024).toFixed(0)}KB`);
    });
  }
}

main().catch(e => { console.error(e); process.exit(1); });
