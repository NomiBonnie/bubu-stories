#!/usr/bin/env node
// Regenerate Story 1-8 illustrations with gpt-image-2 Poland
import fs from 'fs';
import path from 'path';
import https from 'https';
import http from 'http';

const WORKSPACE = '/Users/samyuan/.openclaw/workspace/bubu-stories';
const CONFIG = JSON.parse(fs.readFileSync(path.join(process.env.HOME, '.config/azure-openai/config.json'), 'utf8'));
const ENDPOINT = CONFIG.image2_poland_endpoint;
const API_KEY = CONFIG.image2_poland_api_key;
const DEPLOYMENT = CONFIG.image2_poland_deployment;
const API_VERSION = '2025-04-01-preview';
const DELAY_MS = 7500; // 7.5s between requests (9 RPM limit)

// Character descriptions for prompts
const CHARS = {
  bubu: 'a pure snow-white rabbit toddler (Bubu) with long ears (pink inside), big round brown eyes, small pink nose, wearing a pink dress and a small pink bow on her head, round chubby toddler proportions',
  nomi: 'a raccoon (NOMI) with gray-brown fur, black eye mask markings, ringed tail, big round clever eyes, wearing a blue-and-white striped sweater, nimble paws',
  nono: 'a small bright red-feathered bird (NONO) with orange-yellow beak, round bright eyes, small and perky',
  sam_dad: 'a golden retriever dad (Sam) with golden fur, large and warm build, wearing casual stylish clothes (dark fitted jacket), gentle loving smile',
  tina_mom: 'a black-and-white cow mom (Tina) with classic cow markings, medium-large build, elegant and gentle, wearing fashionable outfit (knit top and skirt), patient warm expression',
  doudou: 'a small hedgehog (Doudou) with brown body and dark brown spines, small round eyes, tiny and round, shy and cute',
  manman: 'a small turtle (Manman) with green shell with dark green patterns, light green skin, small and round, slow-moving with a silly sweet expression',
  zhuzhu: 'a white sheep (Zhuzhu, NOT a pig despite the name) with cloud-like curly white wool, light blue vest, brown little hooves, pink nose, about the same size as Bubu',
  dr_giraffe: 'a tall giraffe doctor (Dr. Giraffe) with standard giraffe spots, wearing a white doctor coat and stethoscope, warm professional expression, bending down to talk to small children',
  nurse_squirrel: 'a squirrel nurse with reddish-brown fur, wearing a pink nurse uniform with white nurse cap (red cross), fluffy big tail, small and agile',
  yuanyuan: 'a giant panda (Yuanyuan) with classic black-and-white coloring, round black ears, signature dark eye circles, big round dark brown sparkling eyes, wearing a yellow dress, chubby and round, same size as Bubu',
};

const STYLE_PREFIX = 'Pixar 3D animation style, warm soft lighting, children\'s picture book illustration, vertical portrait composition (9:16 aspect ratio).';

// Story-specific prompt generators
const storyPrompts = {
  8: {
    title: '咘咘坐飞机',
    title_en: "Bubu's Plane Adventure",
    characters: ['bubu', 'tina_mom', 'sam_dad'],
    coverPrompt: `${STYLE_PREFIX} Book cover scene. A bright sunny airport exterior with a large airplane in the background. ${CHARS.bubu} standing excitedly with a small backpack, looking up at the airplane with wonder. ${CHARS.tina_mom} standing beside her holding her hand lovingly. A clear blue sky with fluffy clouds. The top third of the image has a clear open sky area suitable for title text overlay. Warm, adventurous, exciting mood.`,
    pagePrompts: [
      `${STYLE_PREFIX} A cozy home interior in the morning. ${CHARS.bubu} jumping with excitement, wearing a small backpack. ${CHARS.tina_mom} smiling beside her, holding suitcases. Through the window, a bright sunny day. Warm morning light.`,
      `${STYLE_PREFIX} A huge bustling airport terminal with high ceilings and many animal passengers. ${CHARS.bubu} holding tightly onto ${CHARS.tina_mom}'s hand, eyes wide with wonder, looking around at the enormous space. Long queues, departure boards, bright lights.`,
      `${STYLE_PREFIX} Close-up scene. ${CHARS.tina_mom} handing a boarding pass to ${CHARS.bubu}. Bubu hugging the boarding pass to her chest proudly, looking very grown-up. Airport check-in counter in the background.`,
      `${STYLE_PREFIX} Inside a large airplane cabin. ${CHARS.bubu} touching the soft airplane seat curiously, looking at the round airplane window with wonder. ${CHARS.tina_mom} sitting in the next seat smiling. Warm cabin lighting, rows of seats.`,
      `${STYLE_PREFIX} Dramatic scene inside airplane. ${CHARS.bubu} gripping ${CHARS.tina_mom}'s hand tightly as the plane takes off, her tummy feeling ticklish, giggling with a mix of excitement and nervousness. Motion blur outside the window showing acceleration. Dynamic angle.`,
      `${STYLE_PREFIX} ${CHARS.bubu} pressing her face against the airplane window, looking down at tiny houses like building blocks and a river like a shiny ribbon far below. Fluffy white clouds right beside the window. ${CHARS.tina_mom} leaning over to look too. Magical aerial view, golden sunlight through clouds.`,
      `${STYLE_PREFIX} Inside the airplane. A kind deer flight attendant in uniform bringing a tray with juice and cookies to ${CHARS.bubu}. Bubu saying thank you politely with a happy smile. ${CHARS.tina_mom} sitting beside her looking proud. Warm cabin lighting.`,
      `${STYLE_PREFIX} The airplane landing scene. ${CHARS.bubu} clapping her little hands with joy, looking out the window at the runway. Expression of triumph and pride. "I did it!" energy. ${CHARS.tina_mom} smiling proudly beside her.`,
      `${STYLE_PREFIX} Emotional reunion scene outside airport exit. ${CHARS.sam_dad} with open arms as ${CHARS.bubu} runs and leaps toward him. Dad catching and hugging Bubu, kissing her forehead. ${CHARS.tina_mom} walking behind with luggage, smiling warmly. Sunset golden light, airport exit in background. Heartwarming family moment.`,
      `${STYLE_PREFIX} Cozy nighttime scene. ${CHARS.bubu} in bed in pajamas, looking out the window at a starry sky with an airplane silhouette. A toy airplane on her nightstand. Dreamy, peaceful atmosphere. Moonlight and warm bedside lamp glow. ${CHARS.sam_dad} and ${CHARS.tina_mom} tucking her in together.`,
    ]
  },
  7: {
    title: '猪猪不怕打针',
    title_en: "Zhuzhu Is Not Afraid of Shots",
    characters: ['bubu', 'zhuzhu', 'dr_giraffe', 'nurse_squirrel'],
    coverPrompt: `${STYLE_PREFIX} Book cover scene. A bright, cheerful hospital entrance decorated with colorful lanterns on a big tree. ${CHARS.bubu} and ${CHARS.zhuzhu} standing together holding hands bravely. ${CHARS.dr_giraffe} visible in the doorway waving. Bright sunshine, flowers around the entrance. The top third has clear sky area for title text overlay. Encouraging, warm, brave mood.`,
    pagePrompts: [
      `${STYLE_PREFIX} A meadow scene. ${CHARS.bubu} playing with ${CHARS.zhuzhu}. Zhuzhu has soft cloud-like curly wool. They're laughing together on green grass with flowers. Warm sunny day.`,
      `${STYLE_PREFIX} ${CHARS.zhuzhu} looking unwell, red nose, sneezing. A sheep mother (white wool, gentle) feeling Zhuzhu's forehead with concern. Cozy home interior. Soft warm lighting.`,
      `${STYLE_PREFIX} ${CHARS.zhuzhu} hiding behind his sheep mother, looking scared and worried. A thought bubble showing a scary hospital (from his imagination). Nervous expression.`,
      `${STYLE_PREFIX} ${CHARS.bubu} holding ${CHARS.zhuzhu}'s hand firmly, looking determined and encouraging. "Don't be scared, I'll go with you!" expression. Bright outdoor setting, path ahead.`,
      `${STYLE_PREFIX} A bright, warm, friendly animal hospital exterior. A big tree with colorful lanterns at the entrance. Everything is bright and welcoming, not scary at all. ${CHARS.bubu} and ${CHARS.zhuzhu} arriving, looking around. Sunshine, flowers.`,
      `${STYLE_PREFIX} Inside the hospital. ${CHARS.dr_giraffe} bending down with a warm smile, holding a stethoscope. ${CHARS.zhuzhu} looking up at the tall gentle giraffe doctor. Bright clean hospital interior with cheerful decorations.`,
      `${STYLE_PREFIX} Close-up. ${CHARS.dr_giraffe} placing a stethoscope on ${CHARS.zhuzhu}'s tummy. Zhuzhu flinching slightly at the cool touch but relaxing. ${CHARS.bubu} watching nearby encouragingly. Warm medical room.`,
      `${STYLE_PREFIX} ${CHARS.dr_giraffe} explaining kindly that Zhuzhu needs a shot. Zhuzhu looking worried. Doctor holding up a tiny syringe showing it's small. Gentle, reassuring atmosphere.`,
      `${STYLE_PREFIX} Close-up of ${CHARS.zhuzhu} with teary red eyes, looking scared. Small voice asking "will it hurt?" Emotional, sympathetic scene. Soft lighting.`,
      `${STYLE_PREFIX} ${CHARS.bubu} gripping ${CHARS.zhuzhu}'s hand tightly, looking into his eyes with a brave encouraging smile. "Look at me! Let's count 1, 2, 3 together!" Friendship and courage. Warm lighting.`,
      `${STYLE_PREFIX} The shot moment. A rabbit nurse gently wiping Zhuzhu's arm. ${CHARS.bubu} and ${CHARS.zhuzhu} counting together "1, 2, 3!" with determined expressions. Quick moment, not scary. Bright hospital room.`,
      `${STYLE_PREFIX} ${CHARS.zhuzhu} looking at a star-shaped bandaid on his arm with wonder and delight. The rabbit nurse smiling. It's already done! Relief and happiness. Sparkle effect around the star bandaid.`,
      `${STYLE_PREFIX} ${CHARS.zhuzhu} laughing happily, proudly showing his star bandaid arm to ${CHARS.bubu}. "It wasn't scary at all!" Both smiling brightly. Cheerful hospital corridor.`,
      `${STYLE_PREFIX} ${CHARS.dr_giraffe} patting ${CHARS.zhuzhu}'s head gently. "You were so brave!" Zhuzhu beaming with pride. ${CHARS.bubu} clapping. Warm, proud moment.`,
      `${STYLE_PREFIX} Walking home scene. ${CHARS.zhuzhu} bouncing happily alongside ${CHARS.bubu}. "Next time I'll go with you too! We're the brave team!" Sunset path, golden light, happy mood. Trees and flowers along the road.`,
      `${STYLE_PREFIX} Dreamy lesson scene. ${CHARS.zhuzhu} and ${CHARS.bubu} in a warm glow, showing their star bandaids like medals. A friendly hospital in the background with a rainbow. "Being brave is the best!" message. Warm, uplifting, storybook ending.`,
    ]
  },
  6: {
    title: '咘咘学会等一等',
    title_en: "Bubu Learns to Wait",
    characters: ['bubu', 'sam_dad', 'tina_mom', 'nomi', 'nono'],
    coverPrompt: `${STYLE_PREFIX} Book cover scene. A peaceful riverside with ${CHARS.bubu} and ${CHARS.sam_dad} sitting together fishing. Bubu holding a fishing rod patiently, looking at fluffy clouds reflected in the calm water. Beautiful nature scene with trees and flowers. The top portion has clear sky area for title text overlay. Patient, peaceful, warm mood.`,
    pagePrompts: [
      `${STYLE_PREFIX} Home kitchen scene. ${CHARS.bubu} impatiently asking "Is it ready yet?" at the dining table. ${CHARS.tina_mom} cooking in the background. Bubu looks antsy, fidgeting. Clock on the wall. Warm kitchen lighting.`,
      `${STYLE_PREFIX} ${CHARS.bubu} running to the front door and peeking out repeatedly, waiting for someone. Impatient expression, tapping her foot. Cozy home entrance. "Why aren't they here yet?" mood.`,
      `${STYLE_PREFIX} A beautiful riverside scene. ${CHARS.sam_dad} and ${CHARS.bubu} walking together carrying fishing rods. Dad asking about fishing patience. Sunny day, willow trees, sparkling river.`,
      `${STYLE_PREFIX} ${CHARS.bubu} standing up impatiently at the riverbank, peeking at the fishing line in the water. ${CHARS.sam_dad} gently shushing her, whispering. Fishing rods in the calm water. Peaceful nature setting.`,
      `${STYLE_PREFIX} ${CHARS.bubu} sitting back down by the river, looking a bit bored. Counting clouds in the sky. A few fluffy clouds visible. Fishing rod in the water. Peaceful but slightly restless mood.`,
      `${STYLE_PREFIX} ${CHARS.bubu} and ${CHARS.sam_dad} looking up at clouds together, pointing at cloud shapes. One cloud shaped like a rabbit, another like a fish. Both smiling and laughing. Blue sky with creative cloud shapes. Fun bonding moment.`,
      `${STYLE_PREFIX} Exciting moment! The fishing rod bending with a bite! ${CHARS.bubu} eyes wide, mouth open in excitement, grabbing the fishing rod. Water splashing. ${CHARS.sam_dad} reaching to help. Dynamic action scene.`,
      `${STYLE_PREFIX} ${CHARS.bubu} and ${CHARS.sam_dad} pulling up a shiny silver fish together! Bubu jumping with joy, water droplets sparkling in sunlight. Fish gleaming. Triumphant, exciting moment.`,
      `${STYLE_PREFIX} ${CHARS.sam_dad} kneeling beside ${CHARS.bubu} at the riverbank, explaining that patience brought the fish. Bubu listening thoughtfully, holding the fish proudly. Warm golden afternoon light.`,
      `${STYLE_PREFIX} Home kitchen. ${CHARS.tina_mom} putting a cake in the oven. ${CHARS.bubu} about to say something impatient but stopping herself, remembering the fishing lesson. Thought bubble showing the fishing scene. Kitchen counter with baking supplies.`,
      `${STYLE_PREFIX} ${CHARS.bubu} sitting on a small stool in the kitchen, drawing pictures while waiting for the cake. Content and patient expression. Timer on the counter. Warm kitchen atmosphere.`,
      `${STYLE_PREFIX} The cake is done! ${CHARS.tina_mom} taking a beautiful golden cake out of the oven. ${CHARS.bubu} sniffing the delicious aroma with eyes closed and a huge smile. Steam and sparkles around the cake. Warm, delightful scene.`,
      `${STYLE_PREFIX} Evening scene. ${CHARS.bubu} sitting by the front door looking at stars in the night sky while waiting. Peaceful, not anxious. Beautiful starry sky through the doorway. Warm porch light.`,
      `${STYLE_PREFIX} ${CHARS.nomi} running up to the house. ${CHARS.bubu} greeting NOMI happily. "It's okay you're late, I saw lots of stars!" Both smiling. Starry night background. Warm friendship moment. ${CHARS.nono} flying nearby.`,
      `${STYLE_PREFIX} Dreamy lesson scene. ${CHARS.bubu} peacefully fishing by the river under a starry sky, surrounded by images of things worth waiting for: a cake, stars, a friend arriving. Magical glow. "Good things come to those who wait" mood. Warm, peaceful storybook ending.`,
    ]
  },
  5: {
    title: '咘咘学会说你好',
    title_en: "Bubu Learns to Say Hello",
    characters: ['bubu', 'sam_dad', 'nomi', 'nono', 'doudou', 'manman'],
    coverPrompt: `${STYLE_PREFIX} Book cover scene. A lively forest marketplace with colorful stalls and bunting. ${CHARS.bubu} in the center waving hello with a bright smile. ${CHARS.sam_dad} standing behind her proudly. Various animal characters around. Sunshine streaming through trees. The top third has clear sky/canopy area for title text overlay. Friendly, social, warm mood.`,
    pagePrompts: [
      `${STYLE_PREFIX} A sunny morning at home. ${CHARS.sam_dad} kneeling beside ${CHARS.bubu} at the door, asking her a question about meeting people. Bubu blinking curiously, not knowing the answer. Bright doorway leading outside.`,
      `${STYLE_PREFIX} ${CHARS.sam_dad} smiling warmly at ${CHARS.bubu}, teaching her to say hello. Bubu listening intently. A speech bubble with "你好!" (Hello!). Warm, gentle teaching moment. Forest path visible outside.`,
      `${STYLE_PREFIX} A forest path. ${CHARS.bubu} and ${CHARS.sam_dad} walking when they spot ${CHARS.doudou} picking berries by the path. Bubu hiding shyly behind dad. Doudou focused on berries. Sunny forest setting.`,
      `${STYLE_PREFIX} ${CHARS.sam_dad} gently encouraging ${CHARS.bubu} with a little push. Bubu stepping forward shyly, saying "hello" softly to ${CHARS.doudou}. Small speech bubble. Encouraging moment.`,
      `${STYLE_PREFIX} ${CHARS.doudou} turning around with a big happy smile, offering a red berry to ${CHARS.bubu}. Bubu's face lighting up with surprise and joy. Warm interaction between new friends. Forest clearing.`,
      `${STYLE_PREFIX} ${CHARS.bubu} bouncing happily along the forest path, holding the berry. ${CHARS.sam_dad} walking beside her smiling proudly. "Saying hello makes friends!" realization. Bright sunny path with butterflies.`,
      `${STYLE_PREFIX} By a small river. ${CHARS.bubu} boldly calling out hello to ${CHARS.manman} who is sunbathing on a rock. Bubu looking confident this time, not shy. Sunny riverbank with sparkling water.`,
      `${STYLE_PREFIX} ${CHARS.manman} slowly lifting head with a big warm smile. Inviting Bubu to sunbathe together. ${CHARS.bubu} and Manman sitting on the warm rock by the river. Peaceful, lazy afternoon sun.`,
      `${STYLE_PREFIX} A bustling forest marketplace with colorful stalls. ${CHARS.bubu} saying hello to a big friendly bear selling honey from a wooden stall. Bubu looking up bravely. ${CHARS.sam_dad} in the background. Lively market scene.`,
      `${STYLE_PREFIX} The big bear laughing heartily, handing a small jar of honey to ${CHARS.bubu}. "What a polite little bunny!" Bubu beaming with pride. Market stall with honey jars.`,
      `${STYLE_PREFIX} ${CHARS.bubu} greeting a rabbit lady selling flowers at a market stall. The rabbit lady smiling and giving Bubu a small daisy. Colorful flower stall. Cheerful market atmosphere.`,
      `${STYLE_PREFIX} ${CHARS.nomi} at a market stall fixing things for other animals. ${CHARS.bubu} running over to say hello. NOMI looking up with a warm smile. "You're so polite today!" Tools and gadgets on the stall.`,
      `${STYLE_PREFIX} ${CHARS.nono} diving down from the sky playfully. "I heard you saying hello everywhere from up in the sky!" ${CHARS.bubu} laughing, looking up at the red bird. Blue sky, treetops.`,
      `${STYLE_PREFIX} Walking home in golden sunset light. ${CHARS.bubu} carrying berries, honey, and a daisy happily. ${CHARS.sam_dad} walking beside her. "Are you happy today?" Bubu nodding vigorously. Warm sunset path.`,
      `${STYLE_PREFIX} Dreamy lesson scene. ${CHARS.bubu} surrounded by all the friends she met today, all waving hello to each other. A big warm "你好!" in the center. Everyone smiling. Magical glow, storybook ending. ${CHARS.sam_dad}, ${CHARS.doudou}, ${CHARS.manman}, ${CHARS.nomi}, ${CHARS.nono} all present.`,
    ]
  },
  4: {
    title: '咘咘学会说对不起',
    title_en: "Bubu Learns to Say Sorry",
    characters: ['bubu', 'sam_dad', 'tina_mom', 'manman', 'nomi', 'nono'],
    coverPrompt: `${STYLE_PREFIX} Book cover scene. A riverside sand area with a beautiful sandcastle in the foreground. ${CHARS.bubu} and ${CHARS.manman} working together to build it, smiling at each other. A small flag on top of the castle. Warm afternoon sunlight. The top portion has clear sky area for title text overlay. Friendship, forgiveness, warm mood.`,
    pagePrompts: [
      `${STYLE_PREFIX} A sunny riverside. ${CHARS.bubu} and ${CHARS.manman} playing in the sand. Manman slowly and carefully building a beautiful sandcastle. Bubu watching admiringly. Sparkling river, warm sunshine.`,
      `${STYLE_PREFIX} ${CHARS.bubu} admiring ${CHARS.manman}'s beautiful sandcastle, then trying to build her own. Her castle keeps collapsing. Frustrated expression. Sand tools scattered around. Manman's perfect castle nearby.`,
      `${STYLE_PREFIX} Accident moment! ${CHARS.bubu} accidentally bumping into ${CHARS.manman}'s sandcastle, knocking it over! Sand crumbling. Bubu looking shocked with mouth open. Dramatic moment with sand particles flying.`,
      `${STYLE_PREFIX} ${CHARS.manman} looking at the ruined sandcastle, tears flowing down. "I worked on it for so long..." Heartbreaking scene. Pile of sand where the beautiful castle was. Sad, emotional lighting.`,
      `${STYLE_PREFIX} ${CHARS.bubu} alone in her bedroom, hiding. Looking sad and guilty, hugging her knees. Room with stuffed animals and a window showing the riverside in the distance. Moody, introspective lighting.`,
      `${STYLE_PREFIX} ${CHARS.sam_dad} entering Bubu's room, sitting beside ${CHARS.bubu} on the bed. Gentle, understanding expression. Bubu looking up with teary eyes about to explain. Warm bedside lamp light. Father-daughter heart-to-heart.`,
      `${STYLE_PREFIX} ${CHARS.sam_dad} talking to ${CHARS.bubu} about empathy. "What do you think Manman feels right now?" Bubu thinking deeply, a thought bubble showing sad Manman. Warm, gentle teaching moment.`,
      `${STYLE_PREFIX} Kitchen scene. ${CHARS.tina_mom} taking fresh cookies out of the oven, putting them on a plate. Offering them to ${CHARS.bubu}. "Bring these to Manman." Warm, delicious-looking cookies. Cozy kitchen.`,
      `${STYLE_PREFIX} Riverside scene. ${CHARS.bubu} walking toward ${CHARS.manman} carrying a plate of cookies nervously. Manman quietly rebuilding her sandcastle alone. Bubu taking a deep breath. Afternoon light, emotional moment.`,
      `${STYLE_PREFIX} ${CHARS.bubu} offering cookies to ${CHARS.manman}, saying "I'm sorry" with sincere eyes. Manman looking up silently. The plate of cookies between them. Tender, vulnerable moment. Warm river light.`,
      `${STYLE_PREFIX} ${CHARS.manman} slowly smiling, accepting the apology. "Okay... help me but don't knock it over again!" ${CHARS.bubu} relieved and happy. Cookies being shared. Reconciliation moment, warm golden light.`,
      `${STYLE_PREFIX} ${CHARS.bubu} and ${CHARS.manman} building an even bigger and more beautiful sandcastle together! Teamwork scene, both focused and happy. ${CHARS.nomi} walking by, amazed at the castle. Afternoon sunshine.`,
      `${STYLE_PREFIX} The completed magnificent sandcastle with ${CHARS.nono} flying down to place a small flag on top. ${CHARS.bubu} and ${CHARS.manman} high-fiving proudly. ${CHARS.nomi} applauding. Golden sunset light on the sand.`,
      `${STYLE_PREFIX} Walking home in sunset. ${CHARS.sam_dad} asking ${CHARS.bubu} what she learned. Bubu holding up two fingers explaining. Happy, reflective mood. Beautiful orange sunset sky along the path.`,
      `${STYLE_PREFIX} Dreamy lesson scene. ${CHARS.bubu} and ${CHARS.manman} hugging in front of their beautiful sandcastle, with a glowing "对不起" (Sorry) and heart shapes floating around. ${CHARS.nomi} and ${CHARS.nono} nearby. Magical warm glow, forgiveness and friendship. Storybook ending.`,
    ]
  },
  3: {
    title: '小刺猬的新朋友',
    title_en: "The Hedgehog's New Friend",
    characters: ['bubu', 'sam_dad', 'tina_mom', 'doudou', 'nomi', 'nono'],
    coverPrompt: `${STYLE_PREFIX} Book cover scene. A sunny park with a big sandbox. ${CHARS.bubu} and ${CHARS.doudou} building a sandcastle together happily in the sand. Park playground with slides and swings in the background. The top portion has clear bright sky for title text overlay. Friendship, sharing, joyful mood.`,
    pagePrompts: [
      `${STYLE_PREFIX} A beautiful sunny park. ${CHARS.sam_dad} walking with ${CHARS.bubu} into the park. Slides, swings, and a big sandbox visible. Bubu looking excited. Green trees, blue sky, colorful playground.`,
      `${STYLE_PREFIX} Next to the sandbox. ${CHARS.doudou} sitting alone, carefully building a beautiful sandcastle with a small shovel. Bubu watching from nearby, fascinated. Detailed sandcastle. Warm sunshine.`,
      `${STYLE_PREFIX} ${CHARS.bubu} running over and grabbing ${CHARS.doudou}'s shovel! Bubu's impulsive expression. Doudou looking surprised and upset, reaching for the shovel. Quick, dynamic scene.`,
      `${STYLE_PREFIX} ${CHARS.bubu} and ${CHARS.doudou} pushing and pulling over the shovel. The sandcastle crumbling between them! Doudou starting to cry with tears flowing. Shovel fallen on the ground. Emotional, dramatic scene.`,
      `${STYLE_PREFIX} ${CHARS.sam_dad} kneeling down to ${CHARS.bubu}'s level in the sandbox area. Gentle but serious expression. "You wanted the shovel, but grabbing makes Doudou sad." Bubu looking down ashamed. ${CHARS.doudou} crying in background.`,
      `${STYLE_PREFIX} ${CHARS.sam_dad} teaching ${CHARS.bubu} what to say. Speech bubble: "可以借我玩一下吗？" (Can I play with it?). Bubu practicing the words, looking toward ${CHARS.doudou}. Patient, teaching moment.`,
      `${STYLE_PREFIX} ${CHARS.bubu} walking over to ${CHARS.doudou} apologetically, speaking softly. "Doudou... sorry. Can I play with your shovel?" Doudou wiping tears, listening. Tender, vulnerable moment. Sandbox setting.`,
      `${STYLE_PREFIX} ${CHARS.doudou} wiping tears and nodding with a small smile. "Okay! Let's play together!" Reconciliation moment. Both characters looking hopeful. Warm sunshine on the sandbox.`,
      `${STYLE_PREFIX} ${CHARS.bubu} using the shovel to help ${CHARS.doudou} rebuild the sandcastle. Both working together, focused and happy. The new sandcastle growing bigger and more beautiful. Teamwork scene.`,
      `${STYLE_PREFIX} ${CHARS.nomi} arriving with a small bucket, and ${CHARS.nono} flying in with a small flag in his beak. Everyone gathering around the sandbox. ${CHARS.bubu} and ${CHARS.doudou} looking up happily at their friends arriving.`,
      `${STYLE_PREFIX} ${CHARS.tina_mom} watching from a park bench nearby, smiling warmly. In the foreground, all the friends playing together in the sandbox. "Using words works so much better!" Warm, happy park scene.`,
      `${STYLE_PREFIX} Walking home. ${CHARS.bubu} carefully holding ${CHARS.doudou}'s hand (avoiding the spines, holding the soft palm). Both smiling. "Will you come to the park tomorrow?" Sunset park path. ${CHARS.sam_dad} walking behind them smiling.`,
      `${STYLE_PREFIX} Dreamy lesson scene. ${CHARS.bubu} and ${CHARS.doudou} together with the beautiful sandcastle, surrounded by warm glow. Speech bubble "可以借我玩一下吗？" as the magic words. ${CHARS.nomi} and ${CHARS.nono} nearby. Sharing and friendship theme. Storybook ending.`,
    ]
  },
  2: {
    title: '彩虹桥在哪里',
    title_en: "Where Is the Rainbow Bridge",
    characters: ['bubu', 'nomi', 'nono'],
    coverPrompt: `${STYLE_PREFIX} Book cover scene. A stunning rainbow arching across the sky after rain. ${CHARS.bubu} standing on a hilltop reaching toward the rainbow with wonder. ${CHARS.nomi} beside her pointing at the rainbow. ${CHARS.nono} flying toward the rainbow. Wet grass glistening, puddles reflecting rainbow colors. The top portion has clear sky with rainbow for title text overlay. Wonder, adventure, discovery mood.`,
    pagePrompts: [
      `${STYLE_PREFIX} Morning after rain. ${CHARS.bubu} pressing her face against a window, staring in awe at a huge beautiful rainbow in the sky. Rain droplets on the window. Indoor cozy scene looking out. Magical colorful rainbow.`,
      `${STYLE_PREFIX} ${CHARS.bubu} leaping off the windowsill and dashing out the front door excitedly. "I want to touch the rainbow!" Determined, adventurous expression. Wet ground, puddles, rainbow visible in the sky.`,
      `${STYLE_PREFIX} ${CHARS.bubu} running up a grassy hillside, panting. The rainbow still looks far far away in the distance. Wet grass, scattered wildflowers, misty atmosphere. Determined but slightly tired.`,
      `${STYLE_PREFIX} On the hilltop. ${CHARS.nomi} collecting mushrooms in a basket. ${CHARS.bubu} running up breathlessly. "Where is the rainbow?" They look toward the rainbow together. Misty hills, colorful mushrooms.`,
      `${STYLE_PREFIX} ${CHARS.bubu} and ${CHARS.nomi} walking through a forest path toward the rainbow. NOMI pointing ahead. "I heard the rainbow's end is past the forest!" Adventure journey through a magical wet forest with dewdrops everywhere.`,
      `${STYLE_PREFIX} In the forest, meeting ${CHARS.nono} on a tree branch, shaking rain off his wings. "Where are you going?" "To find the rainbow!" Red bird looking excited. Wet forest canopy, dappled light.`,
      `${STYLE_PREFIX} ${CHARS.nono} flying high up near the clouds, looking down and calling out. "I see it! The rainbow is by the river!" Bird's-eye view with the rainbow ending near a river. Dynamic flying pose. Dramatic sky.`,
      `${STYLE_PREFIX} ${CHARS.bubu}, ${CHARS.nomi} arriving at the riverbank excitedly. But the rainbow has moved further away! Rainbow visible in the far distance. Disappointed expressions. Beautiful river scene.`,
      `${STYLE_PREFIX} ${CHARS.bubu} sitting tiredly on a river rock, looking deflated. "The rainbow keeps running away!" Exhausted and sad. River flowing beside her. ${CHARS.nomi} and ${CHARS.nono} beside her looking concerned. Mist over the water.`,
      `${STYLE_PREFIX} ${CHARS.nomi} noticing something sparkling in the river water! Pointing excitedly. Sunlight hitting water spray creating many tiny rainbows on the river surface! Magical discovery moment. Sparkles and light effects.`,
      `${STYLE_PREFIX} ${CHARS.bubu} reaching her paw into the river splash. A tiny rainbow forming right in her palm from the water spray and sunlight! Her face full of wonder and joy. "I touched a rainbow!" Magical sparkles. Close-up emotional scene.`,
      `${STYLE_PREFIX} ${CHARS.nono} flying near a small waterfall, fanning his wings to create mist. A rainbow appearing in the mist! "I have a rainbow too!" Playful, magical scene with water droplets and light.`,
      `${STYLE_PREFIX} ${CHARS.nomi} smiling wisely. "You don't need to chase rainbows. Where there's sunshine and water, there are rainbows." The three friends surrounded by tiny rainbows in the water spray. Wise, warm moment.`,
      `${STYLE_PREFIX} ${CHARS.bubu} hopping happily along the path home, stomping in puddles. Each puddle reflecting tiny rainbows! ${CHARS.nomi} and ${CHARS.nono} following. Sunset golden light, wet path. Joyful, carefree scene. "Best day ever!"`,
      `${STYLE_PREFIX} Dreamy lesson scene. ${CHARS.bubu} with arms open wide, surrounded by rainbow colors in water droplets, puddles, and mist all around her. ${CHARS.nomi} and ${CHARS.nono} nearby. "Beauty is everywhere if you look." Magical warm glow, storybook ending.`,
    ]
  },
  1: {
    title: '小兔子找月亮',
    title_en: "Little Bunny Finds the Moon",
    characters: ['bubu', 'nomi', 'nono'],
    coverPrompt: `${STYLE_PREFIX} Book cover scene. A magical moonlit night. A large bright full moon reflected in a still pond. ${CHARS.bubu} standing on the pond bank looking up at the moon with wonder, paws reaching toward the sky. ${CHARS.nomi} beside her also gazing up. ${CHARS.nono} perched on NOMI's head silhouetted against the moon. Fireflies and stars twinkling. The top portion has clear starry sky for title text overlay. Magical, whimsical, nighttime wonder mood.`,
    pagePrompts: [
      `${STYLE_PREFIX} A green meadow with a cozy burrow home. ${CHARS.bubu} hopping happily on the grass. Long ears bouncing, pink nose twitching. Butterflies and flowers around. Bright cheerful daytime. Introduction scene.`,
      `${STYLE_PREFIX} ${CHARS.bubu} with her best friend ${CHARS.nomi}. NOMI in her blue-and-white striped sweater, looking clever with bright eyes. They're sitting together on a log. Warm friendly scene. Daytime meadow.`,
      `${STYLE_PREFIX} ${CHARS.nono} flying above, red feathers catching the light. Brave and energetic small bird. ${CHARS.bubu} and ${CHARS.nomi} looking up at NONO admiringly. Blue sky with fluffy clouds. Introduction of the trio.`,
      `${STYLE_PREFIX} Twilight scene. ${CHARS.bubu} on top of a small hill, looking up at a beautiful large full moon. "Goodnight, moon!" Arms reaching up. Purple-pink sunset sky transitioning to night. Silhouette of meadow. Magical, peaceful.`,
      `${STYLE_PREFIX} Night scene. ${CHARS.bubu} looking up at a completely dark sky - NO MOON! Eyes wide with shock and worry. Stars visible but moon is gone. Dark blue sky, worried expression. "Where did the moon go?!"`,
      `${STYLE_PREFIX} ${CHARS.bubu} running anxiously through the nighttime meadow to find ${CHARS.nomi}. Worried expression, ears flapping. Dark night with stars. Fireflies lighting the path. Urgent mood.`,
      `${STYLE_PREFIX} ${CHARS.nomi} in a cozy tree hollow, reading a book by candlelight, wearing glasses. ${CHARS.bubu} bursting in worried. "NOMI! The moon is missing!" NOMI pushing up glasses thoughtfully. Warm candlelit interior.`,
      `${STYLE_PREFIX} ${CHARS.nono} flying high in the night sky, searching for the moon. Wings spread wide against the starry sky. Looking around in all directions. Below, ${CHARS.bubu} and ${CHARS.nomi} watching from the ground. Dramatic night sky.`,
      `${STYLE_PREFIX} ${CHARS.nono} calling down excitedly from the sky. "I found it! The moon is in the pond!" Pointing with a wing toward a sparkling pond below. ${CHARS.bubu} and ${CHARS.nomi} looking up excitedly. Night scene with starlight.`,
      `${STYLE_PREFIX} ${CHARS.bubu} and ${CHARS.nomi} at the pond's edge, looking down. A beautiful round bright moon perfectly reflected in the still pond water. Both amazed, mouths open. Magical reflection, fireflies, starry night.`,
      `${STYLE_PREFIX} ${CHARS.bubu} reaching her paw into the pond to grab the moon - SPLASH! Water spraying everywhere, hitting everyone's faces! The moon reflection shattering into sparkling fragments. Dynamic, funny scene. ${CHARS.nomi} getting splashed.`,
      `${STYLE_PREFIX} ${CHARS.nomi} wiping water off face and laughing, pointing up at the sky. "Bubu, look up!" ${CHARS.bubu} looking up with water dripping from her ears. Above them, the real full moon shining bright and whole in the sky! Revelation moment.`,
      `${STYLE_PREFIX} ${CHARS.nomi} explaining to ${CHARS.bubu}: "That was the moon's reflection! The real moon was always in the sky." Bubu's face changing from confusion to understanding to joy. "The moon was always there!" Night scene, real moon above, reflection below.`,
      `${STYLE_PREFIX} The three friends (${CHARS.bubu}, ${CHARS.nomi}, ${CHARS.nono}) walking home hand in hand (NONO on Bubu's head) under the bright moonlight. Path through the meadow. ${CHARS.bubu} waving goodnight to the moon. Warm, peaceful, magical nighttime scene.`,
      `${STYLE_PREFIX} Dreamy lesson scene. ${CHARS.bubu} tucked in bed in a cozy burrow, looking out the window at the bright moon. Moonlight streaming in. "Goodnight, moon! Goodnight, Bubu!" Peaceful, sleepy, magical ending. Stars and fireflies outside the window.`,
    ]
  }
};

// API call function
async function generateImage(prompt, storyNum, pageNum) {
  const url = new URL(`${ENDPOINT}openai/deployments/${DEPLOYMENT}/images/generations?api-version=${API_VERSION}`);
  
  const body = JSON.stringify({
    prompt,
    n: 1,
    size: '1024x1536',
    quality: 'medium',
  });

  return new Promise((resolve, reject) => {
    const mod = url.protocol === 'https:' ? https : http;
    const req = mod.request(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'api-key': API_KEY,
      },
      timeout: 120000,
    }, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        if (res.statusCode !== 200) {
          reject(new Error(`API ${res.statusCode}: ${data.substring(0, 500)}`));
          return;
        }
        try {
          const json = JSON.parse(data);
          const imageUrl = json.data?.[0]?.url;
          const b64 = json.data?.[0]?.b64_json;
          if (imageUrl) resolve({ type: 'url', value: imageUrl });
          else if (b64) resolve({ type: 'b64', value: b64 });
          else reject(new Error('No image in response: ' + data.substring(0, 300)));
        } catch (e) {
          reject(new Error('Parse error: ' + e.message));
        }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Timeout')); });
    req.write(body);
    req.end();
  });
}

// Save image (from URL or base64)
async function saveImage(result, destPath) {
  fs.mkdirSync(path.dirname(destPath), { recursive: true });
  if (result.type === 'b64') {
    const buf = Buffer.from(result.value, 'base64');
    fs.writeFileSync(destPath, buf);
    return buf.length;
  }
  return new Promise((resolve, reject) => {
    const mod = result.value.startsWith('https') ? https : http;
    mod.get(result.value, { timeout: 60000 }, (res) => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        return saveImage({ type: 'url', value: res.headers.location }, destPath).then(resolve).catch(reject);
      }
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => {
        const buf = Buffer.concat(chunks);
        fs.writeFileSync(destPath, buf);
        resolve(buf.length);
      });
      res.on('error', reject);
    }).on('error', reject);
  });
}

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function processStory(storyNum) {
  const sp = storyPrompts[storyNum];
  if (!sp) { console.error(`No prompts for story ${storyNum}`); return; }
  
  console.log(`\n${'='.repeat(60)}`);
  console.log(`STORY ${storyNum}: ${sp.title} (${sp.title_en})`);
  console.log(`${'='.repeat(60)}`);
  
  // Read existing JSON
  const jsonPath = path.join(WORKSPACE, 'stories', `story${storyNum}.json`);
  const story = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
  const originalPages = story.pages;
  const totalImages = 1 + originalPages.length; // cover + content pages
  
  console.log(`Pages: ${originalPages.length} content + 1 cover = ${totalImages} images`);
  
  const imgDir = path.join(WORKSPACE, 'public', 'images', `story${storyNum}`);
  fs.mkdirSync(imgDir, { recursive: true });
  
  // Build new pages array
  const newPages = [];
  
  // Page 1 = Cover
  const coverPageNum = '01';
  console.log(`\n[page-${coverPageNum}] COVER - generating...`);
  let retries = 3;
  let imageUrl;
  while (retries > 0) {
    try {
      imageUrl = await generateImage(sp.coverPrompt, storyNum, 1);
      break;
    } catch (e) {
      retries--;
      console.error(`  Error: ${e.message}. Retries left: ${retries}`);
      if (retries > 0) await sleep(15000);
      else throw e;
    }
  }
  const coverDest = path.join(imgDir, `page-${coverPageNum}.jpg`);
  const coverSize = await saveImage(imageUrl, coverDest);
  console.log(`  Saved: page-${coverPageNum}.jpg (${(coverSize/1024).toFixed(0)}KB)`);
  
  newPages.push({
    text: sp.title,
    text_en: sp.title_en,
    image: `images/story${storyNum}/page-01.jpg`,
    imagePrompt: sp.coverPrompt,
  });
  
  await sleep(DELAY_MS);
  
  // Content pages
  for (let i = 0; i < originalPages.length; i++) {
    const pageNumStr = String(i + 2).padStart(2, '0');
    const prompt = sp.pagePrompts[i];
    if (!prompt) {
      console.error(`  No prompt for page index ${i}!`);
      // Keep original page without image
      newPages.push({ ...originalPages[i], image: `images/story${storyNum}/page-${pageNumStr}.jpg` });
      continue;
    }
    
    console.log(`\n[page-${pageNumStr}] "${originalPages[i].text?.substring(0, 30)}..." - generating...`);
    
    retries = 3;
    while (retries > 0) {
      try {
        imageUrl = await generateImage(prompt, storyNum, i + 2);
        break;
      } catch (e) {
        retries--;
        console.error(`  Error: ${e.message}. Retries left: ${retries}`);
        if (retries > 0) await sleep(15000);
        else throw e;
      }
    }
    
    const dest = path.join(imgDir, `page-${pageNumStr}.jpg`);
    const size = await saveImage(imageUrl, dest);
    console.log(`  Saved: page-${pageNumStr}.jpg (${(size/1024).toFixed(0)}KB)`);
    
    newPages.push({
      ...originalPages[i],
      image: `images/story${storyNum}/page-${pageNumStr}.jpg`,
      imagePrompt: prompt,
    });
    
    if (i < originalPages.length - 1) await sleep(DELAY_MS);
  }
  
  // Update story JSON
  story.pages = newPages;
  story.cover = 'page-01';
  story.title = sp.title;
  story.title_en = sp.title_en;
  
  // Save to both locations
  const jsonStr = JSON.stringify(story, null, 2);
  fs.writeFileSync(jsonPath, jsonStr);
  const publicJsonPath = path.join(WORKSPACE, 'public', 'stories', `story${storyNum}.json`);
  fs.writeFileSync(publicJsonPath, jsonStr);
  
  console.log(`\n✅ Story ${storyNum} complete: ${newPages.length} pages, JSON updated in both locations.`);
}

// Update index.json
function updateIndex() {
  for (const dir of ['stories', 'public/stories']) {
    const indexPath = path.join(WORKSPACE, dir, 'index.json');
    if (!fs.existsSync(indexPath)) continue;
    const index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
    if (Array.isArray(index.stories)) {
      for (const s of index.stories) {
        const num = parseInt(s.id?.replace('story', '') || '0');
        if (num >= 1 && num <= 8) {
          s.cover = 'page-01';
        }
      }
    }
    fs.writeFileSync(indexPath, JSON.stringify(index, null, 2));
    console.log(`Updated ${dir}/index.json`);
  }
}

// Main
const ORDER = [8, 7, 6, 5, 4, 3, 2, 1];
const startFrom = parseInt(process.argv[2]) || ORDER[0];
const startIdx = ORDER.indexOf(startFrom);

(async () => {
  console.log(`Starting regeneration from Story ${startFrom}`);
  console.log(`Endpoint: ${ENDPOINT}`);
  console.log(`Deployment: ${DEPLOYMENT}`);
  
  for (let idx = (startIdx >= 0 ? startIdx : 0); idx < ORDER.length; idx++) {
    const storyNum = ORDER[idx];
    try {
      await processStory(storyNum);
      await sleep(DELAY_MS); // gap between stories
    } catch (e) {
      console.error(`\n❌ Story ${storyNum} FAILED: ${e.message}`);
      console.error(`Resume with: node regen-stories.mjs ${storyNum}`);
      process.exit(1);
    }
  }
  
  updateIndex();
  console.log('\n🎉 All stories regenerated successfully!');
})();
