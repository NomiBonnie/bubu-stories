const fs = require('fs'), path = require('path');
const C = JSON.parse(fs.readFileSync(
  path.join(process.env.HOME, '.config/azure-openai/config.json'), 'utf8'
));
const url = C.image2_eastus2_endpoint + '?api-version=2025-04-01-preview';
const apiKey = C.image2_eastus2_api_key;
const sleep = ms => new Promise(r => setTimeout(r, ms));
const outDir = '/Users/samyuan/.openclaw/workspace/bubu-stories/public/images/story64';

// Character descriptions (inline for consistency)
const BUBU = "a cute snow-white rabbit toddler with exactly TWO long ears with pink insides, big round brown eyes, small pink nose, wearing a pink dress and a pink bow on top of her head centered between her two ears. Toddler proportions, round and adorable.";
const ZHUZHU = "a cute white sheep (lamb) with cloud-like curly wool, small pink nose, brown little hooves, wearing a blue dress. Same size as Bubu. Friendly and cheerful.";
const ZHUZHU_DAD = "an adult white sheep (ram) with curly wool, wearing a casual polo shirt and pants. Larger than Zhuzhu, warm and friendly.";
const ZHUZHU_MOM = "an adult white sheep (ewe) with soft curly wool, wearing a floral blouse. Gentle and warm expression.";
const DAD = "a golden retriever dog (NOT human), golden fur, large and warm, wearing a stylish dark casual jacket, kind smile.";
const MOM = "a dairy cow (NOT human, black and white spotted cow), medium-large, elegant, wearing a fashionable knit top and skirt, gentle patient expression.";
const GRANDPA = "a cute round green dinosaur (brontosaurus type, NOT scary), big round kind eyes, wearing a polo shirt and casual pants. Stout and lovable.";
const GRANDMA = "a small monkey with light brown fur, warm peach-colored face, kind big eyes, wearing a Chinese-style floral blouse. Small and nimble.";
const NOMI = "a raccoon with grey-brown fur, black eye mask markings, ringed tail, big round intelligent eyes, wearing a blue-and-white striped sweater.";
const NONO = "a small bright red bird with round body, orange-yellow beak, round shiny eyes. Tiny, perches on shoulders or heads.";
const COCO = "a red panda (NOT a giant panda) with reddish-brown fur, round face, big round eyes, wearing a yellow scarf. Slightly bigger than Bubu.";

const PREFIX = "Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition 1024x1536. No text anywhere in the image.";

const prompts = [
  // Page 1 - Cover
  `${PREFIX} Movie poster style children's book cover. In the center, ${BUBU} and ${ZHUZHU} stand together holding fishing rods - Bubu holds a yellow fishing rod and Zhuzhu holds a purple fishing rod. Behind them, a birthday cake with candles and colorful balloons. Around them: ${DAD}, ${MOM}, ${GRANDPA}, ${GRANDMA}, ${NOMI}, ${NONO}, ${COCO}, ${ZHUZHU_DAD}, ${ZHUZHU_MOM}. Warm golden light, celebration atmosphere. The English title "Zhuzhu's Birthday" in playful hand-lettered style at the top, with decorative fishing line curls around the letters.`,

  // Page 2 - Bubu sees the gift
  `${PREFIX} A cozy modern living room in the morning. ${BUBU} stands excitedly looking at a long rectangular gift box on the sofa, wrapped with a purple ribbon bow. ${MOM} kneels beside Bubu, patting her head lovingly. Morning sunlight streams through the window. Warm home atmosphere.`,

  // Page 3 - Doorbell, Zhuzhu arrives
  `${PREFIX} Front door of a modern apartment opened wide. ${BUBU} at the door greeting ${ZHUZHU} who stands outside wearing a blue dress, smiling with eyes curved. Behind Zhuzhu stand ${ZHUZHU_DAD} and ${ZHUZHU_MOM}, smiling warmly. Bright daylight from outside.`,

  // Page 4 - Everyone inside, NOMI/NONO/Coco welcome
  `${PREFIX} A warm living room. ${BUBU} and ${ZHUZHU} hold hands running inside happily. At the table, ${NOMI} arranges snacks on a plate. ${NONO} flies above Zhuzhu's head chirping. ${COCO} walks from the kitchen carrying a fruit plate, yellow scarf swaying. Welcoming cozy atmosphere.`,

  // Page 5 - Adults chatting on sofa
  `${PREFIX} A cozy living room sofa scene. ${ZHUZHU_DAD} and ${ZHUZHU_MOM} sit on one side of the sofa chatting with ${DAD} and ${MOM} on the other side. ${GRANDPA} stands nearby holding a tea tray, ${GRANDMA} places fruit on the coffee table. Warm friendly conversation atmosphere.`,

  // Page 6 - Kids playing in room
  `${PREFIX} A children's playroom. ${BUBU} and ${ZHUZHU} sit on the floor playing together. Zhuzhu has built a tall block castle. Bubu holds up a drawing of a big colorful fish. Building blocks, crayons, and stuffed animals scattered around. Warm playful atmosphere.`,

  // Page 7 - Bringing Zhuzhu to see the gift
  `${PREFIX} Living room. ${BUBU} holds ${ZHUZHU}'s hoof, leading her to the coffee table where a long purple gift box with a ribbon bow sits. Zhuzhu's eyes are wide with surprise and excitement. Adults watch from the sofa in the background, smiling.`,

  // Page 8 - Opening the gift - purple fishing rod!
  `${PREFIX} Close-up scene. ${ZHUZHU} has opened the box revealing a beautiful shiny purple fishing rod (real fishing rod, about 1.5 meters long, slender). Zhuzhu jumps with joy, curly white wool bouncing. The purple ribbon and box wrapping scattered around. ${BUBU} watches happily beside her. Sparkle effects around the rod.`,

  // Page 9 - Two fishing rods side by side
  `${PREFIX} ${BUBU} and ${ZHUZHU} stand proudly holding their fishing rods side by side - Bubu holds a yellow fishing rod in her left paw, Zhuzhu holds a purple fishing rod in her right hoof. Both rods are real slender fishing rods about 1.5m long. The two friends beam at each other with excitement. Bright warm lighting.`,

  // Page 10 - NOMI helps put away rods
  `${PREFIX} ${NOMI} kneels on the floor carefully helping ${BUBU} and ${ZHUZHU} put away their fishing rods (one yellow, one purple) into a long bag. ${NONO} flaps wings excitedly nearby. The two little ones look up at NOMI listening. Warm gentle atmosphere.`,

  // Page 11 - Going to restaurant by car
  `${PREFIX} A car interior from back seat perspective. ${DAD} drives (golden retriever paws on steering wheel), ${MOM} sits in passenger seat looking at phone for navigation. In the back seat, ${BUBU} and ${ZHUZHU} sit close together chatting excitedly. ${COCO} leans against the car window, ${NONO} perches on Coco's head. Through the window, a sunny city street. Summer daylight.`,

  // Page 12 - Restaurant, cake on table
  `${PREFIX} A cheerful restaurant with a big round table full of colorful dishes. In the center, a beautiful round birthday cake with strawberries and cream flowers on top, four small candles. ${ZHUZHU} claps her hooves in delight. ${MOM} stands nearby having arranged everything. ${DAD} helps place candles on the cake. All characters seated around: ${BUBU}, ${GRANDPA}, ${GRANDMA}, ${ZHUZHU_DAD}, ${ZHUZHU_MOM}, ${NOMI}, ${COCO}. Festive warm restaurant lighting.`,

  // Page 13 - Blowing candles, singing
  `${PREFIX} Birthday celebration moment. ${ZHUZHU} sits in front of the lit birthday cake, hooves pressed together, eyes closed making a wish. All other characters circle around singing - ${BUBU}, ${DAD}, ${MOM}, ${GRANDPA}, ${GRANDMA}, ${ZHUZHU_DAD}, ${ZHUZHU_MOM}, ${NOMI}, ${NONO}, ${COCO}. Warm candlelight illuminates everyone's happy faces. Golden warm atmosphere.`,

  // Page 14 - Candied strawberries
  `${PREFIX} Close-up of ${BUBU} and ${ZHUZHU} sitting side by side, each holding a stick of candied strawberries (bright red strawberries coated in glossy crystal sugar shell, like jewels on a stick). Both are mid-bite with happy expressions. The restaurant table in background with other characters. Sweet joyful moment.`,

  // Page 15 - Ice cream
  `${PREFIX} Dessert time at the restaurant table. ${BUBU} holds a pink strawberry ice cream scoop. ${ZHUZHU} has a white vanilla scoop. ${COCO} licks a chocolate ice cream. In the background, ${NONO} perches on the rim of an ice cream cup sneaking a taste. Everyone is happy and relaxed. Soft warm lighting.`,

  // Page 16 - Going home, sleepy goodbyes
  `${PREFIX} Evening street scene outside the restaurant. ${ZHUZHU} leans sleepily against ${ZHUZHU_MOM}, still clutching the purple fishing rod. ${BUBU} rides on ${DAD}'s back, sleepy but waving goodbye with one paw. Warm streetlights, golden sunset sky. Tender farewell moment.`,

  // Page 17 - Bedtime
  `${PREFIX} A cozy children's bedroom at night. ${BUBU} lies in bed in pajamas, hugging a pink stuffed bunny toy. A yellow fishing rod leans against the wall nearby. ${NOMI} sits beside the bed tucking her in with a gentle smile. Soft warm nightlight glow. Peaceful sleepy atmosphere.`,

  // Page 18 - Dream scene
  `${PREFIX} A dreamy magical scene. A beautiful blue lake surrounded by gentle green hills under bright sunshine. ${BUBU} and ${ZHUZHU} stand at the lake shore, each holding their fishing rod (Bubu yellow, Zhuzhu purple). The rods sparkle in the sunlight. They look at each other with big smiles, about to cast their lines. Dreamy soft-focus edges, magical sparkles in the air. Fantasy dream atmosphere.`
];

async function gen(prompt, outPath, idx) {
  console.log(`[${idx}/18] Generating ${path.basename(outPath)}...`);
  try {
    const r = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'api-key': apiKey },
      body: JSON.stringify({ prompt, n: 1, size: '1024x1536', quality: 'medium' })
    });
    if (!r.ok) {
      const errText = (await r.text()).slice(0, 300);
      console.error(`  ❌ ERR ${r.status}: ${errText}`);
      return false;
    }
    const d = await r.json();
    let buf;
    if (d.data[0].b64_json) buf = Buffer.from(d.data[0].b64_json, 'base64');
    else if (d.data[0].url) { const ir = await fetch(d.data[0].url); buf = Buffer.from(await ir.arrayBuffer()); }
    if (buf) {
      fs.writeFileSync(outPath, buf);
      console.log(`  ✅ ${path.basename(outPath)} (${(buf.length/1024)|0}KB)`);
      return true;
    }
  } catch(e) {
    console.error(`  ❌ Exception: ${e.message}`);
    return false;
  }
}

(async () => {
  console.log(`Starting Story 64 image generation (${prompts.length} pages)...`);
  let success = 0, fail = 0;
  for (let i = 0; i < prompts.length; i++) {
    const outPath = path.join(outDir, `page-${String(i+1).padStart(2,'0')}.jpg`);
    const ok = await gen(prompts[i], outPath, i+1);
    if (ok) success++; else fail++;
    if (i < prompts.length - 1) await sleep(8000);
  }
  console.log(`\nDone! ✅ ${success} succeeded, ❌ ${fail} failed.`);
})();
