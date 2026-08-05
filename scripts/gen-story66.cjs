const fs = require('fs'), path = require('path');
const C = JSON.parse(fs.readFileSync(path.join(process.env.HOME, '.config/azure-openai/config.json'), 'utf8'));
const url = C.image2_eastus2_endpoint + '?api-version=2025-04-01-preview';
const apiKey = C.image2_eastus2_api_key;
const sleep = ms => new Promise(r => setTimeout(r, ms));
const outDir = '/Users/samyuan/.openclaw/workspace/bubu-stories/public/images/story66';

const PREFIX = 'Pixar 3D animation style, warm soft lighting, children\'s picture book illustration, vertical portrait composition 1024x1536. No text anywhere in the image.';
const BUBU_PJ = 'a cute snow-white rabbit toddler with exactly TWO long ears with pink insides, big round brown eyes, a small pink nose, wearing pink pajamas and a pink bow centered on top of her head between her two ears; toddler proportions, round and adorable.';
const BUBU_UNIFORM = 'a cute snow-white rabbit toddler with exactly TWO long ears with pink insides, big round brown eyes, a small pink nose, wearing a neat pink kindergarten uniform and a pink bow centered on top of her head between her two ears; toddler proportions, round and adorable.';
const NOMI = 'an anthropomorphic raccoon with grey-brown fur, black eye mask markings, ringed tail, big round intelligent eyes, wearing a blue-and-white striped sweater; gentle and clever.';
const NONO = 'a tiny bright red bird with a round body, round shiny eyes, and a small orange-yellow beak.';
const DAD = 'an anthropomorphic golden retriever father standing upright on two legs like a human, NOT on all fours, golden fur, warm kind smile, wearing a stylish dark casual jacket and pants.';
const MOM = 'an anthropomorphic dairy cow mother standing upright on two legs like a human, NOT on all fours, classic black-and-white spots, gentle and elegant, wearing a soft knit top and skirt.';
const GRANDPA = 'a cute elderly short-necked chubby bright-green dinosaur grandpa, NOT a long-neck dinosaur, NO hair, smooth green skin, tiny pointy spikes on top of a round head, small gold round glasses, white collared shirt, brown pants, very short and stout with a round belly, standing upright.';
const GRANDMA = 'a small elderly monkey grandma with warm brown fur and brown hair in a neat bun, NOT grey or white hair, warm peach face, kind dark eyes, tiny green earrings, wearing a Chinese-style floral blouse, standing upright.';
const TEACHER_LI = 'a giant panda kindergarten teacher, NOT human, black-and-white fur, round dark eye patches, big warm brown eyes, wearing a light pink kindergarten apron, round and friendly.';

const prompts = [
`${PREFIX} Cinematic children\'s picture book cover poster. ${BUBU_PJ} sits up in a cozy bed while ${NOMI} sits warmly beside her. A soft sunrise shines through the window, and ${NONO} perches on the bedpost. Gentle magical musical notes float in the warm morning air. TOP: elegant hand-painted English title "Bubu's Morning Song" in golden sunrise lettering. Rich layered poster composition.`,
`${PREFIX} Cozy bedroom at early dawn. ${MOM} gently sits beside ${BUBU_PJ}, who hides her face under a soft pink blanket and looks sleepy. A tiny line of sunrise glows outside the window. Tender quiet mood.`,
`${PREFIX} In the same cozy bedroom, ${NOMI} sits by ${BUBU_PJ}'s bed with a gentle smile, inviting her to sing a simple song. ${NONO} quietly perches by the pillow. Soft morning light, no other objects or characters.`,
`${PREFIX} ${NOMI} softly sings beside the bed. ${BUBU_PJ} peeks her two long pink-inside ears out from under her blanket, curious and slightly sleepy. Golden sunrise light, magical but simple atmosphere.`,
`${PREFIX} ${BUBU_PJ} slowly sits up in bed and rubs her eyes. ${MOM} gives her a warm gentle hug. ${NOMI} and ${NONO} smile nearby. Cozy sunrise bedroom.`,
`${PREFIX} Bright clean bathroom morning scene. ${DAD} gently holds the hand of ${BUBU_PJ}, walking with her toward a small child-friendly toilet. ${NOMI} stands nearby softly singing. Dad is bipedal, warm and patient.`,
`${PREFIX} Bathroom scene after using the toilet. ${BUBU_PJ} presses the flush button, smiling a little. ${NONO} stands at the doorway cheerfully. Small clean sparkles suggest a fresh morning, simple and warm.`,
`${PREFIX} Bathroom sink scene. ${BUBU_PJ} holds a pink electric toothbrush, while ${NOMI} watches encouragingly. Gentle soap bubbles float around the sink like playful dancers.`,
`${PREFIX} Close warm bathroom scene. ${BUBU_PJ} carefully brushes her teeth with a pink electric toothbrush. Tiny happy bubbles dance around her bright teeth, ${NONO} watches from the mirror edge. Not scary, playful and clean.`,
`${PREFIX} ${MOM} gently wipes ${BUBU_PJ}'s face with a warm soft towel in the bathroom. ${NOMI} smiles nearby. A soft sunbeam makes Bubu's clean round face glow like sunshine.`,
`${PREFIX} ${BUBU_PJ} looks at herself in a mirror, delighted by her clean glowing round face like a little sun. ${NONO} flies happily above her. Warm simple bathroom.`,
`${PREFIX} Warm family breakfast table. ${GRANDPA} places milk, egg, and a small bun on the table. ${GRANDMA} carries a small bowl of warm porridge. ${BUBU_PJ} sits at the table with ${NOMI} beside her and ${NONO} perched nearby. Grandpa must be short-necked, green, round, with gold glasses; Grandma has brown hair bun and green earrings.`,
`${PREFIX} Same breakfast table. ${NOMI} sings gently while ${BUBU_PJ} slowly eats a small bun and drinks milk, looking calmer. ${GRANDPA} and ${GRANDMA} watch with warm supportive smiles, no pressure. Morning sunlight.`,
`${PREFIX} At the home entryway, ${BUBU_UNIFORM} wears her neat pink kindergarten uniform. ${GRANDPA} gently helps her put on a small backpack while ${GRANDMA} smiles beside them. ${NOMI} and ${NONO} celebrate quietly. Keep Grandpa short-necked green with gold glasses, Grandma brown-hair bun with green earrings.`,
`${PREFIX} Sunny tree-lined morning street. ${BUBU_UNIFORM} walks between ${GRANDPA} and ${GRANDMA}, holding Grandpa's hand. Grandpa is a short chubby bright-green dinosaur with tiny head spikes and gold glasses; Grandma is a small brown-fur monkey with a brown hair bun, green earrings and floral blouse. All walking upright, warm family mood.`,
`${PREFIX} Same sunny walk. ${BUBU_UNIFORM} sings softly as she walks between ${GRANDPA} and ${GRANDMA}; ${NOMI} walks nearby and ${NONO} flies above. Leaves sway gently in the breeze. Grandpa and Grandma look warm and engaged.`,
`${PREFIX} Colorful Shenzhen kindergarten entrance. ${TEACHER_LI} warmly greets ${BUBU_UNIFORM}, whose clean round face glows like sunshine. ${GRANDPA} and ${GRANDMA} stand nearby waving goodbye. Other generic small animal classmates are in the background, no named Suzhou characters.`,
`${PREFIX} Kindergarten outdoor morning activity. ${BUBU_UNIFORM} happily runs and jumps with generic little animal classmates in a green playground. She touches her tummy with a grateful smile, looking energetic. ${TEACHER_LI} watches kindly in the background.`,
`${PREFIX} Cozy bedtime bedroom. ${BUBU_PJ} lies in bed hugging her pink stuffed bunny. ${NOMI} sits by her side smiling gently, and ${NONO} perches on the bedpost. Outside is a calm moonlit night; a faint musical note glow suggests the morning song will return tomorrow.`
];

async function gen(prompt, outPath, idx) {
  console.log(`[${idx}/${prompts.length}] ${path.basename(outPath)}`);
  try {
    const r = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json','api-key':apiKey}, body:JSON.stringify({prompt,n:1,size:'1024x1536',quality:'medium'})});
    if (!r.ok) { console.error('ERR', r.status, (await r.text()).slice(0,300)); return false; }
    const d=await r.json();
    let buf;
    if (d.data?.[0]?.b64_json) buf=Buffer.from(d.data[0].b64_json,'base64');
    else if (d.data?.[0]?.url) { const ir=await fetch(d.data[0].url); buf=Buffer.from(await ir.arrayBuffer()); }
    if (!buf) throw new Error('no image payload');
    fs.writeFileSync(outPath,buf);
    console.log('OK',Math.round(buf.length/1024)+'KB');
    return true;
  } catch(e) { console.error('ERR',e.message); return false; }
}
(async()=>{let ok=0;for(let i=0;i<prompts.length;i++){const p=path.join(outDir,`page-${String(i+1).padStart(2,'0')}.jpg`);if(fs.existsSync(p)){console.log(`[${i+1}/${prompts.length}] skip existing ${path.basename(p)}`);ok++;continue;}if(await gen(prompts[i],p,i+1))ok++;if(i<prompts.length-1)await sleep(7000)}console.log(`DONE ${ok}/${prompts.length}`)})();
