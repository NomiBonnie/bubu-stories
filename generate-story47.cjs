#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const config = JSON.parse(fs.readFileSync(path.expanduser ? path.join(process.env.HOME, '.config/azure-openai/config.json') : `${process.env.HOME}/.config/azure-openai/config.json`));
const endpoint = config.image2_eastus2_endpoint;
const apiKey = config.image2_eastus2_api_key;
const url = `${endpoint}?api-version=2025-04-01-preview`;
const outDir = `${process.env.HOME}/.openclaw/workspace/bubu-stories/public/images/story47`;

// Character descriptions
const BUBU = "a small toddler white rabbit (100% snow-white fur, long ears with pink insides, big round brown eyes, small pink nose) wearing a pink summer dress with a pink bow on her ear, carrying a small pink backpack";
const SAM = "a golden retriever dad (golden fur, warm brown eyes) wearing a casual light blue linen shirt and khaki shorts (early summer attire)";
const TINA = "a cow mom (black and white spotted pattern, gentle dark eyes) wearing an elegant light floral blouse and white linen skirt (early summer attire)";
const NOMI = "a raccoon (grey-brown fur, black eye mask markings, ringed tail, big round clever eyes) wearing a blue-and-white striped sweater";
const NONO = "a small red bird (bright red feathers, round shiny eyes, orange-yellow beak, tiny and cute)";
const COCO = "a red panda (reddish-brown fur, round face, big bright eyes) wearing a yellow scarf";
const TEACHER = "an orange tabby cat teacher (warm orange fur with darker stripes, gentle eyes) wearing a cream-colored apron over a light green dress";

const PREFIX = "Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition 1024x1536.";
const SEASON = "Early summer setting (May) — bright warm sunshine, green trees, light breezy atmosphere.";

const prompts = [
  // P1 - Cover
  `Pixar 3D animation style, cinematic children's picture book cover poster, warm golden morning lighting, vertical portrait 1024x1536. A heartwarming movie-poster composition. CENTER: A cow mom (black and white spotted, wearing elegant light floral blouse) kneeling down and gently kissing the open palm of ${BUBU} who looks up with wonder and a tiny smile. Warm golden morning light streams from behind them, creating a halo effect. The kindergarten entrance is visible in the soft-focus background with colorful decorations. TOP: The English title "A Kiss in My Hand" appears naturally integrated into the warm morning light rays, written in soft golden 3D letters with a gentle glow, small heart shapes floating around the letters. BOTTOM CORNER: ${NOMI} and ${NONO} watch the tender moment from behind a flowering bush. The overall mood is tender, warm, and reassuring. Bokeh background with green trees and flowers. Early summer morning atmosphere.`,

  // P2 - Morning, Bubu doesn't want to get up
  `${PREFIX} ${SEASON} A cozy bedroom scene. ${BUBU} is lying in her small bed, pulling a light pink blanket up to her nose, pouting with slightly worried big eyes. Morning sunlight peeks through curtains. Her pink backpack sits ready by the door. The room has cheerful decorations but Bubu looks reluctant. Soft warm tones.`,

  // P3 - Dad asks what's wrong
  `${PREFIX} ${SEASON} In the living room, ${SAM} is kneeling beside ${BUBU} who sits on the couch looking down at her feet sadly. She's in her pink dress but hasn't put on her shoes yet. Sam is gently touching her ear with a concerned loving expression. Bubu has a small tear in her eye. Warm indoor morning light.`,

  // P4 - Mom kisses her palm ⭐
  `${PREFIX} ${SEASON} The most tender moment: ${TINA} is kneeling down to Bubu's level, gently holding ${BUBU}'s small open right hand and pressing her lips to the little palm in a soft kiss. Bubu watches with wide curious eyes. A subtle warm golden glow emanates from where mom's lips touch the palm. ${SAM} watches from behind with a gentle smile. Living room with morning light streaming through windows. Intimate close-up composition focusing on the kiss.`,

  // P5 - Bubu looks at her palm
  `${PREFIX} ${SEASON} Close-up of ${BUBU} looking down at her own open palm with wonder and amazement. Her big brown eyes are sparkling with delight. On her palm, there's a subtle warm golden glow suggesting the kiss mark. Her expression shifts from worry to hope. A warm ray of sunlight illuminates her hand. ${TINA} and ${SAM} are visible in the soft background, smiling.`,

  // P6 - Dad kisses the other hand
  `${PREFIX} ${SEASON} ${SAM} is playfully kissing ${BUBU}'s other palm with a big warm smile. Bubu is giggling happily, her other hand already closed protectively. ${TINA} watches with a loving smile beside them. The scene is joyful and lighthearted. Both of Bubu's hands now have a subtle warm glow. Living room, morning sunshine.`,

  // P7 - Walking to school, carefully holding hands closed
  `${PREFIX} ${SEASON} Outdoor sidewalk scene with green trees and flowers. ${BUBU} walks with both fists carefully closed, holding them close to her chest protectively, looking down at them with a determined cute expression. ${NOMI} walks beside her, speaking reassuringly with one paw raised. ${NONO} flies nearby. The morning sun is bright and warm. Bubu wears her pink backpack. Green leafy trees and flowers along the path.`,

  // P8 - At kindergarten gate, hesitating then entering
  `${PREFIX} ${SEASON} At a colorful kindergarten entrance gate decorated with flowers and a welcome sign. ${BUBU} stands at the threshold, one foot slightly forward, looking down at her open palm for courage. She takes a deep breath (cheeks slightly puffed). The kindergarten yard is visible behind with play equipment and colorful walls. Morning sunlight. Her pink backpack on her back. A brave determined expression forming on her face.`,

  // P9 - Coco greets her
  `${PREFIX} ${SEASON} Just inside the kindergarten entrance, ${COCO} waves both paws excitedly at ${BUBU} who is stepping through the door. Coco has a big encouraging smile. Bubu looks slightly shy but is smiling back. The classroom is colorful and inviting behind them. Other small animal children visible in the background. Warm cheerful lighting.`,

  // P10 - Teacher greets her
  `${PREFIX} ${SEASON} In the bright colorful classroom, ${TEACHER} bends down to greet ${BUBU} who walks up to her proactively with a small wave. The teacher has a warm gentle smile and is patting Bubu's head. The classroom has children's drawings on walls, small tables and chairs, toys. Other small animal students settling in. Warm natural light from large windows.`,

  // P11 - Playing with friends
  `${PREFIX} ${SEASON} A montage-style composition showing ${BUBU} happily engaged in classroom activities. She's painting a big yellow sun on an easel, with colorful blocks stacked into a tall castle nearby. Other small animal children around her. ${COCO} builds blocks beside her. ${NONO} perches on a shelf watching happily. Bright cheerful classroom with art supplies and toys everywhere. Bubu looks completely absorbed and happy, having forgotten her earlier sadness.`,

  // P12 - Lunchtime
  `${PREFIX} ${SEASON} Lunchtime in the kindergarten dining area. ${BUBU} sits at a small table eating happily from a colorful tray. She's reaching over to hand a water cup to a small animal friend beside her. ${NONO} sits on the windowsill nearby, flapping wings proudly. ${TEACHER} watches from behind with approval. The table has healthy food, small cups, and cheerful tablecloths. Warm midday light through windows.`,

  // P13 - Missing mommy, hand on cheek ⭐
  `${PREFIX} ${SEASON} A quiet emotional moment: ${BUBU} sits in a corner of the classroom, gently pressing her right palm against her cheek with closed eyes. A subtle warm golden glow comes from her palm. Her expression is peaceful and comforted, with a small tender smile forming. Soft afternoon light. Other children play in the blurred background. The moment is intimate and touching. ${NOMI} watches from nearby with a knowing gentle smile.`,

  // P14 - Nap time
  `${PREFIX} ${SEASON} Nap room with small beds in rows. ${BUBU} lies on her little bed under a light blanket, both small hands held together over her heart, palms touching (keeping the kisses safe). Her eyes are closed peacefully, with a serene smile. Soft dim lighting with curtains partially drawn. Other small animal children sleeping in nearby beds. A calm, tranquil atmosphere.`,

  // P15 - Getting stickers
  `${PREFIX} ${SEASON} ${TEACHER} is smiling warmly and placing colorful star stickers on ${BUBU}'s hand. Bubu looks down at the stickers with pure delight, eyes sparkling. She already has two stickers on the back of one hand. The teacher holds a sheet of stickers. Afternoon classroom light. ${COCO} and other children nearby look happy for her. Cheerful celebratory mood.`,

  // P16 - Running to mommy after school
  `${PREFIX} ${SEASON} The kindergarten pickup area in warm late afternoon golden light. ${BUBU} is running with arms wide open toward ${TINA} who kneels with open arms. Bubu's expression is pure joy and excitement. Her pink backpack bounces as she runs. Tina has happy tears in her eyes. Other parents and children in the soft background. Green trees and warm sunset glow. Dynamic running pose, emotional reunion.`,

  // P17 - Family hug with friends
  `${PREFIX} ${SEASON} A warm group scene: ${TINA} holds ${BUBU} in a tight hug, while ${SAM} stands beside them gently patting Bubu's head. ${COCO} gives a thumbs-up with a proud smile. ${NOMI} and ${NONO} stand nearby, nodding with warm smiles. Late afternoon golden light. The kindergarten building in the background. Everyone looks happy and proud. A feeling of accomplishment and love.`,

  // P18 - Walking home, sunset
  `${PREFIX} ${SEASON} Beautiful sunset scene on a tree-lined path. ${BUBU} walks in the center, holding ${SAM}'s hand on one side and ${TINA}'s hand on the other. They walk toward the warm orange-pink sunset. Bubu looks up at her parents with a content, peaceful smile. ${NOMI} walks alongside and ${NONO} flies above. Long warm shadows stretch behind them. Green trees frame the path. The overall mood is warm, complete, and reassuring. A perfect ending shot with golden hour lighting.`
];

async function generateImage(prompt, pageNum) {
  const paddedNum = String(pageNum).padStart(2, '0');
  const outPath = `${outDir}/page-${paddedNum}.png`;
  
  console.log(`Generating page ${paddedNum}...`);
  
  const body = JSON.stringify({
    prompt: prompt,
    n: 1,
    size: "1024x1536",
    quality: "medium",
    output_format: "png"
  });

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'api-key': apiKey
    },
    body: body
  });

  if (!res.ok) {
    const errText = await res.text();
    console.error(`Page ${paddedNum} FAILED (${res.status}): ${errText}`);
    return false;
  }

  const data = await res.json();
  if (data.data && data.data[0]) {
    const b64 = data.data[0].b64_json;
    if (b64) {
      fs.writeFileSync(outPath, Buffer.from(b64, 'base64'));
      console.log(`Page ${paddedNum} saved (b64)`);
      return true;
    }
    // png output_format returns url
    const imgUrl = data.data[0].url;
    if (imgUrl) {
      const imgRes = await fetch(imgUrl);
      const buf = Buffer.from(await imgRes.arrayBuffer());
      fs.writeFileSync(outPath, buf);
      console.log(`Page ${paddedNum} saved (url, ${(buf.length/1024).toFixed(0)}KB)`);
      return true;
    }
  }
  console.error(`Page ${paddedNum}: unexpected response`, JSON.stringify(data).slice(0, 200));
  return false;
}

async function main() {
  console.log(`Starting generation of ${prompts.length} pages...`);
  for (let i = 0; i < prompts.length; i++) {
    const pageNum = i + 1;
    let success = false;
    for (let attempt = 0; attempt < 3; attempt++) {
      success = await generateImage(prompts[i], pageNum);
      if (success) break;
      console.log(`Retrying page ${pageNum} (attempt ${attempt + 2})...`);
      await new Promise(r => setTimeout(r, 10000));
    }
    if (!success) console.error(`FAILED page ${pageNum} after 3 attempts`);
    if (i < prompts.length - 1) {
      await new Promise(r => setTimeout(r, 7000));
    }
  }
  console.log("All pages done. Converting to JPG...");
  
  // Convert PNG to JPG
  const { execSync } = require('child_process');
  const files = fs.readdirSync(outDir).filter(f => f.endsWith('.png'));
  for (const f of files) {
    const png = `${outDir}/${f}`;
    const jpg = png.replace('.png', '.jpg');
    try {
      execSync(`ffmpeg -y -i "${png}" -q:v 4 "${jpg}"`, { stdio: 'pipe' });
      fs.unlinkSync(png);
      const size = fs.statSync(jpg).size;
      console.log(`${f} -> ${f.replace('.png','.jpg')} (${(size/1024).toFixed(0)}KB)`);
    } catch(e) {
      console.error(`Failed to convert ${f}: ${e.message}`);
    }
  }
  console.log("DONE!");
}

main().catch(e => { console.error(e); process.exit(1); });
