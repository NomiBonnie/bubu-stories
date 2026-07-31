const fs = require('fs'), path = require('path');
const C = JSON.parse(fs.readFileSync(
  path.join(process.env.HOME, '.config/azure-openai/config.json'), 'utf8'
));
const url = C.image2_eastus2_endpoint + '?api-version=2025-04-01-preview';
const apiKey = C.image2_eastus2_api_key;
const sleep = ms => new Promise(r => setTimeout(r, ms));
const outDir = '/Users/samyuan/.openclaw/workspace/bubu-stories/public/images/story65';

const PREFIX = "Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition 1024x1536. No text anywhere in the image.";

const BUBU = "a cute snow-white rabbit toddler with exactly TWO long ears with pink insides, big round brown eyes, small pink nose, wearing a pink kindergarten uniform and a pink bow on top of her head centered between her two ears. Toddler proportions, round and adorable.";
const DAD = "an anthropomorphic golden retriever dog standing upright on two legs (bipedal humanoid, NOT on all fours), golden fur, tall and warm, wearing a stylish dark casual jacket and pants, kind smile.";
const GRANDPA = "a cute SHORT-NECKED round chubby GREEN dinosaur grandpa (bright green smooth skin, NOT grey, NOT with any hair on head, small pointy spikes on top of his round head like a cartoon dinosaur). Very short neck, round head almost directly on round body. Wearing small gold round spectacles, white collared shirt, brown pants. Short stout pudgy belly. Bipedal. Ref: Story 60 page-04.";
const GRANDMA = "a small monkey grandma with BROWN fur and BROWN hair in a neat bun (NOT grey, NOT white), warm peach face, kind big dark eyes, Chinese-style floral blouse, small green earrings. Small and nimble.";
const NOMI = "a raccoon with grey-brown fur, black eye mask markings, ringed tail, big round intelligent eyes, wearing a blue-and-white striped sweater.";
const TEACHER_LI = "a giant panda (NOT human, black and white coloring, round black eye patches like glasses), round and cuddly, wearing a light pink kindergarten apron. Warm kind smile, kneeling to talk to children.";
const TEACHER_GAN = "an anthropomorphic koala with grey fuzzy fur, big round eyes, black nose, wearing a light green kindergarten apron. Gentle and warm expression.";

const prompts = [
  // Page 1 - Cover
  `${PREFIX} Movie poster style children's book cover. ${BUBU} stands proudly at a kindergarten gate, wearing a golden badge on her chest, one arm raised waving hello. Behind her is a colorful kindergarten entrance with morning sunlight. Small silhouettes of other animal children approaching. ${TEACHER_LI} stands behind Bubu smiling proudly. The English title "Bubu the Greeter" in cheerful rounded letters across the top.`,

  // Page 2 - Teacher Li tells Bubu she's greeter tomorrow
  `${PREFIX} Inside a kindergarten classroom at the end of the day. ${TEACHER_LI} kneels down face-to-face with ${BUBU}, smiling warmly. Teacher Li holds Bubu's small paws gently. Bubu's eyes are sparkling with excitement. Warm afternoon light through windows. Other small animal children in background heading to leave.`,

  // Page 3 - Bedtime, excited
  `${PREFIX} A cozy children's bedroom at night. ${BUBU} lies in bed under a pink blanket, eyes wide open with excitement, a big smile on her face, arms gesturing as she talks. ${NOMI} sits beside the bed, tucking her in with a gentle smile. Soft warm nightlight. A pink stuffed bunny beside Bubu.`,

  // Page 4 - Waking up on her own
  `${PREFIX} Early morning, soft golden sunrise light streaming through a window. ${BUBU} sits up in bed by herself, alert and energetic, fists pumped with determination. Her pink blanket is pushed aside. The room is peaceful, morning glow. She looks motivated and excited.`,

  // Page 5 - Brushing teeth
  `${PREFIX} A bright bathroom. ${BUBU} stands on a small wooden step stool at the sink, carefully brushing her teeth with a small toothbrush. She looks focused and determined. A small mirror reflects her face. A small face towel hangs nearby. Clean bright bathroom with warm lighting.`,

  // Page 6 - Getting dressed, grandma watches
  `${PREFIX} A bedroom scene. ${BUBU} is putting on her kindergarten uniform by herself, arms halfway through the sleeves, concentrating hard. ${GRANDMA} stands nearby watching with a warm proud smile and giving a thumbs up. The uniform is a cute small outfit laid on the bed. Morning light.`,

  // Page 7 - Breakfast with family
  `${PREFIX} A warm dining table scene. ${BUBU} sits at the table eating porridge and egg quickly and neatly, bowl almost empty. ${DAD} sits next to her smiling and asking a question. ${GRANDPA} sits across the table with tea, also smiling. Morning kitchen atmosphere, warm and homey.`,

  // Page 8 - Dad and Grandpa take her to school
  `${PREFIX} A sunny morning street. ${DAD} holds ${BUBU}'s left hand, ${GRANDPA} holds her right hand. Bubu wears a small backpack and walks between them proudly with a big smile. All three walking together, golden morning sunlight, tree-lined path. Dad and Grandpa are bipedal anthropomorphic, walking upright like humans.`,

  // Page 9 - Arriving at kindergarten gate
  `${PREFIX} A colorful kindergarten entrance gate. ${TEACHER_LI} stands at the gate welcoming ${BUBU}. ${DAD} and ${GRANDPA} kneel down on either side of Bubu, each kissing one of her cheeks. Bubu has a big confident smile. Morning sunlight, cheerful kindergarten decorations on the gate.`,

  // Page 10 - Getting the badge
  `${PREFIX} Close-up scene. ${TEACHER_LI} pins a small shiny golden badge onto ${BUBU}'s chest. Bubu looks down at it with wide proud eyes, standing very straight with hands in front. The badge glows with a golden sparkle. Warm soft-focus background of kindergarten corridor.`,

  // Page 11 - First greeting - Teacher Gan
  `${PREFIX} Kindergarten gate area. ${BUBU} stands at the entrance, small body straight and proud, mouth open saying hello. ${TEACHER_GAN} walks in pushing a bicycle, smiling warmly at Bubu. Morning light, cheerful atmosphere. Bubu wears the golden badge on her chest.`,

  // Page 12 - Greeting many kids
  `${PREFIX} Kindergarten gate with ${BUBU} standing proudly at the entrance, arms slightly open, greeting arriving children. Multiple small anthropomorphic animal children (a bear cub, a kitten, a puppy, a bunny) walk past her one by one, all smiling. Some older children (bigger) also pass by. Bubu waves enthusiastically. Busy happy morning energy.`,

  // Page 13 - Helping a shy kid
  `${PREFIX} Tender moment at the kindergarten gate. ${BUBU} bends down slightly toward a very small shy hedgehog child who is looking at the ground. Bubu has a gentle kind expression, speaking softly. The shy hedgehog looks up with a small smile beginning to form. Soft warm lighting, intimate close-up feeling.`,

  // Page 14 - Teacher Li gives star sticker
  `${PREFIX} ${TEACHER_LI} reaches over and places a small star sticker on ${BUBU}'s head (between her ears). Bubu touches the star with one paw, beaming with a huge proud smile showing teeth. The golden badge still on her chest. Warm golden light surrounds them. Celebration feeling.`,

  // Page 15 - Dad picks her up
  `${PREFIX} Kindergarten pickup area, afternoon golden light. ${BUBU} runs toward ${DAD} with arms outstretched, huge happy smile. Dad is kneeling with open arms, about to catch her and lift her up. The star sticker still on Bubu's head, badge on chest. Warm reunion moment, trees and kindergarten building in background.`,

  // Page 16 - Bedtime with badge
  `${PREFIX} Cozy bedroom at night. ${BUBU} lies in bed in pajamas, hugging her pink stuffed bunny. On the pillow next to her sits the small golden greeter badge, catching a glint from the nightlight. ${NOMI} sits beside the bed, smiling gently. Soft warm nightlight glow. Peaceful happy ending atmosphere.`
];

async function gen(prompt, outPath, idx) {
  console.log(`[${idx}/16] Generating ${path.basename(outPath)}...`);
  try {
    const r = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'api-key': apiKey },
      body: JSON.stringify({ prompt, n: 1, size: '1024x1536', quality: 'medium' })
    });
    if (!r.ok) { console.error(`  ❌ ERR ${r.status}: ${(await r.text()).slice(0, 300)}`); return false; }
    const d = await r.json();
    let buf;
    if (d.data[0].b64_json) buf = Buffer.from(d.data[0].b64_json, 'base64');
    else if (d.data[0].url) { const ir = await fetch(d.data[0].url); buf = Buffer.from(await ir.arrayBuffer()); }
    if (buf) { fs.writeFileSync(outPath, buf); console.log(`  ✅ ${path.basename(outPath)} (${(buf.length/1024)|0}KB)`); return true; }
  } catch(e) { console.error(`  ❌ ${e.message}`); }
  return false;
}

(async () => {
  console.log(`Story 65: Generating ${prompts.length} pages...`);
  let ok = 0, fail = 0;
  for (let i = 0; i < prompts.length; i++) {
    const outPath = path.join(outDir, `page-${String(i+1).padStart(2,'0')}.jpg`);
    if (await gen(prompts[i], outPath, i+1)) ok++; else fail++;
    if (i < prompts.length - 1) await sleep(8000);
  }
  console.log(`\nDone! ✅ ${ok} succeeded, ❌ ${fail} failed.`);
})();
