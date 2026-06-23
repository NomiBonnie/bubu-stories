#!/usr/bin/env python3
"""Generate all illustrations for Volume 6 (Stories 53-57) print edition."""

import json
import os
import sys
import time
import base64
import subprocess
import urllib.request
import urllib.error

# ── Config ──
with open(os.path.expanduser("~/.config/azure-openai/config.json")) as f:
    cfg = json.load(f)

ENDPOINT = cfg["image2_eastus2_endpoint"]
API_KEY = cfg["image2_eastus2_api_key"]
API_VERSION = "2025-04-01-preview"
BASE_DIR = os.path.expanduser("~/.openclaw/workspace/bubu-stories/print-edition")

INTERVAL = 8  # seconds between requests
RETRY_WAIT = 45  # seconds on 429
MAX_RETRIES = 3

# ── Character Prompts ──
BUBU = """a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow. She has a small pink bow centered ON TOP OF HER HEAD between her two ears (not on left ear, not on right ear, not behind — exactly centered on top between the ears). She has a toddler-like round body proportion."""

SAM_DAD = """Sam Dad who is a GOLDEN RETRIEVER DOG (NOT a human, NOT a person — he is an ANIMAL, a large golden-furred dog walking upright). He has warm golden fur all over his body, a dog snout/muzzle, floppy dog ears, and a wagging tail. He wears a dark navy jacket over a simple shirt. He has a warm gentle dog smile. IMPORTANT: Sam Dad must look like a golden retriever dog, not a human man."""

TINA_MOM = """Tina Mom who is a BLACK-AND-WHITE COW (NOT a human, NOT a person — she is an ANIMAL, a cow walking upright). She has black and white spotted fur pattern all over, small curved horns, cow ears, and hooves. She wears an elegant cream knit cardigan over a floral skirt. She has a gentle warm cow smile. IMPORTANT: Tina Mom must look like a cow, not a human woman."""

NOMI = """a raccoon (NOMI) with grey-brown fur, distinctive black eye mask markings, and a ringed bushy tail. She wears a blue-and-white horizontally striped sweater. She has clever bright eyes and nimble paws."""

NONO = """a small red bird (NONO) with bright red feathers all over, round bright eyes, and an orange-yellow beak. He has exactly TWO wings and TWO small bird feet with talons. NO ARMS, NO HANDS — birds do not have arms or hands, only wings."""

YANYAN = """Teacher Yanyan, an orange tabby cat with warm orange fur and subtle stripes, gentle green eyes, wearing a pink top with a pocketed apron. She is an adult cat, warm and kind."""

ZHANG = """Teacher Zhang, a young deer (fawn) with light brown fur and white spots, gentle big dark brown eyes, slender deer legs, wearing a light blue top and white apron. She is a female teacher, lively and cheerful."""

MOYU = """Moyu, a corgi girl with brown-and-white fur (standard corgi coloring), short stubby legs, chubby body. She is Bubu's kindergarten best friend."""

FEIFEI = """Feifei, a grey-and-white tabby cat with grey and white fur, about the same size as Bubu. She is Bubu's kindergarten best friend."""

OLIVER = """Oliver, a real Border Collie dog (NOT anthropomorphic — he walks on four legs, does NOT wear clothes, does NOT stand upright). He has classic black and white fur, intelligent deep brown eyes, medium-sized. He is a real family pet dog."""

YUANYUAN_TEACHER = """Teacher Yuanyuan, a giant panda with classic black and white coloring, round black ears, signature black eye patches, wearing a gentle smile. She is a kindergarten teacher, warm and patient."""

LELE = """Lele, a small otter with sleek brown fur, bright curious eyes, playful expression. She is a young girl otter, about the same age as Bubu."""

# ── Summer clothing note ──
SUMMER_NOTE = "All characters wear summer clothing appropriate for hot weather (short sleeves, light fabrics, sandals). "

# ── Prompt template ──
PROMPT_TEMPLATE = """Pixar 3D animation style, {lighting}, children's picture book illustration, vertical portrait composition 1024x1536. No text anywhere in the image. No letters, no words, no writing, no signs with text.

SCENE: {scene}

CHARACTERS: {characters}

{extra}The composition naturally centers characters in the middle of the frame. The bottom 20% of the image should gradually darken as a natural vignette/gradient (for later text overlay). Professional children's picture book quality, warm and heartfelt."""

# ── All pages ──
PAGES = []

# ═══ Story 53: 咘咘的幼儿园朋友们 ═══
s53 = [
    # P2
    {"story": 53, "page": 2, "lighting": "warm golden morning sunlight streaming through a bedroom window",
     "scene": "A cozy bedroom in the morning. Bubu jumps out of bed excitedly, arms raised. NOMI stands nearby helping pack a small pink backpack. NONO perches on Bubu's shoulder chirping. Warm morning light fills the room.",
     "characters": f"{BUBU}\n{NOMI}\n{NONO}",
     "extra": SUMMER_NOTE},
    # P3
    {"story": 53, "page": 3, "lighting": "bright outdoor morning light at a kindergarten entrance",
     "scene": "At the kindergarten gate, Teacher Yanyan bends down to greet Bubu warmly, gently patting her head. The kindergarten entrance is colorful with a cheerful sign (no readable text). Green trees and flowers around.",
     "characters": f"{BUBU}\n{YANYAN}",
     "extra": SUMMER_NOTE},
    # P4
    {"story": 53, "page": 4, "lighting": "bright cheerful morning light",
     "scene": "At the kindergarten entrance, Teacher Zhang stands next to Teacher Yanyan, introducing herself to the children. She waves warmly. Several small animal children look up at her with curiosity. The scene is welcoming.",
     "characters": f"{BUBU}\n{YANYAN}\n{ZHANG}",
     "extra": SUMMER_NOTE},
    # P5
    {"story": 53, "page": 5, "lighting": "warm bright outdoor light",
     "scene": "Three best friends hugging each other tightly in the kindergarten yard. Bubu in the middle, Moyu (short corgi legs) on one side, and Feifei (grey-white cat) on the other. They look overjoyed to see each other. Background shows playground equipment.",
     "characters": f"{BUBU}\n{MOYU}\n{FEIFEI}",
     "extra": SUMMER_NOTE},
    # P6
    {"story": 53, "page": 6, "lighting": "soft indoor classroom light",
     "scene": "In a colorful kindergarten classroom, Teacher Zhang holds up a large picture book. Small animal children sit in a semicircle on the floor. Bubu, Moyu, and Feifei sit together in the front row with wide eyes full of wonder. Decorations on walls.",
     "characters": f"{BUBU}\n{MOYU}\n{FEIFEI}\n{ZHANG}",
     "extra": SUMMER_NOTE},
    # P7
    {"story": 53, "page": 7, "lighting": "warm indoor light with colorful classroom",
     "scene": "Music time in kindergarten. Teacher Yanyan leads singing. Bubu claps her little paws. Moyu wags her short tail. Feifei twitches her ears to the rhythm. NONO flaps his wings along nearby. Musical notes float in the air (but no text). Joyful atmosphere.",
     "characters": f"{BUBU}\n{MOYU}\n{FEIFEI}\n{YANYAN}\n{NONO}",
     "extra": SUMMER_NOTE},
    # P8
    {"story": 53, "page": 8, "lighting": "bright art classroom light",
     "scene": "Art class. Three friends work together on a large painting on the floor/table. Bubu paints a sun, Moyu paints flowers, Feifei paints butterflies. Crayons and paint scattered around. Teacher Zhang watches and claps with delight. Colorful and messy creative scene.",
     "characters": f"{BUBU}\n{MOYU}\n{FEIFEI}\n{ZHANG}",
     "extra": SUMMER_NOTE},
    # P9
    {"story": 53, "page": 9, "lighting": "warm indoor cafeteria light",
     "scene": "Kindergarten lunchtime. Small animal children sit at low tables eating. Teacher Yanyan serves food. Bubu eats happily, Moyu finishes her bowl eagerly, Feifei drinks soup. Cute little bowls and plates. Cozy canteen atmosphere.",
     "characters": f"{BUBU}\n{MOYU}\n{FEIFEI}\n{YANYAN}",
     "extra": SUMMER_NOTE},
    # P10
    {"story": 53, "page": 10, "lighting": "soft dim nap-time light with drawn curtains",
     "scene": "Quiet nap time in kindergarten. Curtains drawn, soft ambient light. Small children sleep on little beds. Bubu and Feifei nap side by side. Moyu is already snoring softly on a nearby bed. NOMI sits quietly in the corner watching over them with a gentle smile. Peaceful dreamy atmosphere.",
     "characters": f"{BUBU}\n{MOYU}\n{FEIFEI}\n{NOMI}",
     "extra": ""},
    # P11
    {"story": 53, "page": 11, "lighting": "bright afternoon outdoor sunlight",
     "scene": "Kindergarten playground. Bubu and Moyu go down a colorful slide together, laughing. Feifei swings on a swing set nearby. Both teachers stand at the side watching and smiling. Trees and blue sky in the background. Active and joyful scene.",
     "characters": f"{BUBU}\n{MOYU}\n{FEIFEI}\n{YANYAN}\n{ZHANG}",
     "extra": SUMMER_NOTE},
    # P12
    {"story": 53, "page": 12, "lighting": "warm golden afternoon light",
     "scene": "Three friends hold hands and spin in a circle in the playground, laughing with joy. NONO flies above them in a circle, singing happily. Grass and flowers around. Beautiful late afternoon light. Pure happiness.",
     "characters": f"{BUBU}\n{MOYU}\n{FEIFEI}\n{NONO}",
     "extra": SUMMER_NOTE},
    # P13
    {"story": 53, "page": 13, "lighting": "warm golden late afternoon / sunset light",
     "scene": "At the kindergarten gate, pickup time. Bubu leaps into Sam Dad's arms excitedly, telling him about her day. The kindergarten building is in the background. Other parents picking up children in the distance. Warm father-daughter moment.",
     "characters": f"{BUBU}\n{SAM_DAD}",
     "extra": SUMMER_NOTE},
    # P14
    {"story": 53, "page": 14, "lighting": "warm indoor evening light",
     "scene": "At home, Bubu sits at a small table drawing a picture. The drawing shows stick-figure versions of her teachers and friends (no readable text on the drawing). Crayons scattered around. She looks proud of her artwork. Cozy home atmosphere.",
     "characters": f"{BUBU}",
     "extra": SUMMER_NOTE},
    # P15
    {"story": 53, "page": 15, "lighting": "soft warm bedtime light, dim room with gentle glow",
     "scene": "Bedtime. Bubu lies in bed hugging NOMI like a stuffed animal. NONO perches on the headboard, sleepy. Star-shaped nightlight casts soft glow. Bubu has a peaceful smile, whispering sleepily. Dreamy and peaceful bedtime scene.",
     "characters": f"{BUBU}\n{NOMI}\n{NONO}",
     "extra": ""},
]
PAGES.extend(s53)

# ═══ Story 54: 咘咘想念Oliver ═══
s54 = [
    # P2
    {"story": 54, "page": 2, "lighting": "bright hot summer light through living room windows",
     "scene": "A living room in Suzhou on a hot summer day. Bubu sits on the floor holding a fluffy toy Border Collie (black and white stuffed dog). She looks at it wistfully. Summer light streams through the window. A fan or AC visible.",
     "characters": f"{BUBU}",
     "extra": SUMMER_NOTE},
    # P3
    {"story": 54, "page": 3, "lighting": "warm indoor light",
     "scene": "In the living room, Bubu looks up at Mama Tina who kneels down and pats her head. Bubu still holds the toy Border Collie. The conversation is about Oliver. Warm and comforting mother-daughter moment.",
     "characters": f"{BUBU}\n{TINA_MOM}",
     "extra": SUMMER_NOTE},
    # P4
    {"story": 54, "page": 4, "lighting": "warm golden morning light (memory/flashback feel with soft dreamy edges)",
     "scene": "FLASHBACK/MEMORY scene with dreamy soft edges. In a bedroom in Shenzhen, Oliver (a real Border Collie dog on four legs) nudges a bedroom door with his nose, tail wagging excitedly. Young Bubu peeks from under the blanket with a sleepy smile. Warm nostalgic morning light.",
     "characters": f"{BUBU}\n{OLIVER}",
     "extra": "This is a memory/flashback scene — add a dreamy soft glow or vignette around the edges. "},
    # P5
    {"story": 54, "page": 5, "lighting": "warm kitchen light (memory/flashback feel)",
     "scene": "FLASHBACK/MEMORY scene. Bubu squats next to Oliver (real dog, four legs), carefully dropping kibble piece by piece from a small bowl into his big food bowl. Oliver tilts his head watching her patiently. Kitchen setting. Sweet and gentle moment.",
     "characters": f"{BUBU}\n{OLIVER}",
     "extra": "This is a memory/flashback scene — add a dreamy soft glow. "},
    # P6
    {"story": 54, "page": 6, "lighting": "warm golden evening light (memory/flashback)",
     "scene": "FLASHBACK/MEMORY scene. Sam Dad walks Oliver (real dog on leash, four legs) while little Bubu holds the leash too, being pulled along and laughing. They walk along a tree-lined path in Shenzhen at sunset. Oliver runs ahead energetically. Happy family walk.",
     "characters": f"{BUBU}\n{SAM_DAD}\n{OLIVER}",
     "extra": "This is a memory/flashback scene — dreamy warm glow. " + SUMMER_NOTE},
    # P7
    {"story": 54, "page": 7, "lighting": "warm outdoor light (memory scene)",
     "scene": "FLASHBACK/MEMORY scene. Close-up: Oliver (real Border Collie, four legs) licks Bubu's face. Bubu laughs and tries to dodge away, her eyes scrunched up with giggly joy. Wet doggy kiss moment. Intimate and heartwarming.",
     "characters": f"{BUBU}\n{OLIVER}",
     "extra": "Memory/flashback scene with dreamy glow. "},
    # P8
    {"story": 54, "page": 8, "lighting": "somber indoor light, slightly melancholy",
     "scene": "Present day. The family sits in their Suzhou apartment living room. Sam Dad, Tina Mom, and Bubu look a bit wistful. A window shows the Suzhou cityscape. The mood is bittersweet — they miss Oliver but this is their current home. A suitcase or moving box visible.",
     "characters": f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}",
     "extra": SUMMER_NOTE},
    # P9
    {"story": 54, "page": 9, "lighting": "soft melancholy afternoon window light",
     "scene": "Bubu stands at a window, looking out at the Suzhou sky with clouds. She presses one paw against the glass. Her expression is thoughtful and a little sad, as if talking to someone far away. NOMI watches her from behind with a caring expression. Emotional and reflective.",
     "characters": f"{BUBU}\n{NOMI}",
     "extra": SUMMER_NOTE},
    # P10
    {"story": 54, "page": 10, "lighting": "warm but lonely indoor light at a pet hotel",
     "scene": "In a clean, comfortable pet hotel room in Shenzhen, Oliver (real Border Collie, four legs, no clothes) lies on a small dog bed, his nose resting on his front paws. He looks at the door with ears perked up, waiting. A food bowl and water nearby. The scene feels lonely but hopeful.",
     "characters": f"{OLIVER}",
     "extra": "Oliver is a REAL dog — four legs, no clothes, no anthropomorphism. "},
    # P11
    {"story": 54, "page": 11, "lighting": "soft warm bedtime light",
     "scene": "Nighttime in Bubu's bedroom. NOMI holds Bubu in her arms gently, telling her something comforting. Bubu listens with wide eyes. The room has soft warm nightlight glow. Stuffed Oliver toy visible nearby. Intimate bedtime conversation.",
     "characters": f"{BUBU}\n{NOMI}",
     "extra": ""},
    # P12
    {"story": 54, "page": 12, "lighting": "warm hopeful indoor light",
     "scene": "Bubu's eyes light up with hope. She picks up her stuffed Border Collie toy and kisses it on the forehead. She looks determined and happy. NOMI smiles watching her. A sense of hope and anticipation. Maybe a thought bubble showing Oliver wagging his tail.",
     "characters": f"{BUBU}\n{NOMI}",
     "extra": ""},
    # P13
    {"story": 54, "page": 13, "lighting": "soft dreamy nighttime glow with moonlight",
     "scene": "Bubu sleeps peacefully in bed with a smile on her face. Above her, a dream cloud shows her pushing open a door and Oliver (real dog) rushing to greet her, tail wagging, jumping up to lick her face. The dream is rendered in a lighter, dreamier style. Moonlight through the window. Hopeful ending.",
     "characters": f"{BUBU}\n{OLIVER}",
     "extra": "Split composition: sleeping Bubu below, dream sequence above with dreamy translucent border. Oliver in dream is a REAL dog, four legs. "},
]
PAGES.extend(s54)

# ═══ Story 55: 咘咘在安吉度假 ═══
s55 = [
    # P2
    {"story": 55, "page": 2, "lighting": "bright early morning light, driveway/parking area",
     "scene": "Early morning by a car. Sam Dad loads a suitcase into the trunk. Tina Mom holds Bubu's hand. Bubu jumps excitedly. A packed car ready for a road trip. Suburban morning atmosphere.",
     "characters": f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}",
     "extra": SUMMER_NOTE},
    # P3
    {"story": 55, "page": 3, "lighting": "beautiful green natural light, lush landscape",
     "scene": "A gorgeous mountain resort (Anji) with green bamboo-covered hills, a grand hotel building in the background with fountains, beautiful gardens, and winding pathways. The family car arrives. Lush green bamboo forests frame the scene. Breathtaking natural beauty.",
     "characters": "",
     "extra": "Wide landscape establishing shot. No main characters needed — show the resort entrance with the car arriving in the distance. "},
    # P4
    {"story": 55, "page": 4, "lighting": "bright outdoor resort entrance light",
     "scene": "At the hotel entrance, NOMI waves excitedly to welcome the arriving family. NONO stands on NOMI's head flapping his wings. Beautiful resort lobby/entrance in background with plants and welcome decorations.",
     "characters": f"{BUBU}\n{NOMI}\n{NONO}\n{SAM_DAD}\n{TINA_MOM}",
     "extra": SUMMER_NOTE},
    # P5
    {"story": 55, "page": 5, "lighting": "bright cheerful outdoor light in a resort garden",
     "scene": "A colorful small tourist train parked in a beautiful garden. Bubu points at it excitedly. The family rushes toward the train. Flowers and hedges surround the area. The train is charming with bright colors.",
     "characters": f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}",
     "extra": SUMMER_NOTE},
    # P6
    {"story": 55, "page": 6, "lighting": "dappled sunlight through bamboo and garden",
     "scene": "The little tourist train moves along a track through the resort. It passes through a garden, over a small stone bridge, and through a bamboo grove. Bubu sits on Sam Dad's lap in the front row, wind blowing her ears, clapping with delight. Tina Mom sits next to them smiling. Beautiful scenery passing by.",
     "characters": f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}",
     "extra": SUMMER_NOTE},
    # P7
    {"story": 55, "page": 7, "lighting": "bright outdoor afternoon light",
     "scene": "A large outdoor trampoline at the resort. Bubu kicks off her sandals at the edge and scrambles up onto the trampoline with excitement. Her sandals lie on the ground. Green mountains visible in the background.",
     "characters": f"{BUBU}",
     "extra": SUMMER_NOTE},
    # P8
    {"story": 55, "page": 8, "lighting": "bright joyful outdoor light",
     "scene": "Bubu bounces HIGH on the giant trampoline, her white fur and pink dress flying, ears flapping in the wind. She laughs with pure joy. NOMI stands at the edge counting. Mountains and blue sky in background. Dynamic action pose capturing the height of a bounce.",
     "characters": f"{BUBU}\n{NOMI}",
     "extra": SUMMER_NOTE + "Dynamic pose — Bubu mid-bounce high in the air. "},
    # P9
    {"story": 55, "page": 9, "lighting": "warm afternoon golden light",
     "scene": "Bubu sits on the trampoline catching her breath, looking exhausted but triumphant. Sam Dad stands at the edge giving a big thumbs up with a proud smile. Bubu's fur is a bit ruffled from all the bouncing. Achievement moment.",
     "characters": f"{BUBU}\n{SAM_DAD}",
     "extra": SUMMER_NOTE},
    # P10
    {"story": 55, "page": 10, "lighting": "sparkling natural light reflecting off water",
     "scene": "A clear shallow stream next to the resort, surrounded by rocks and greenery. Bubu steps into the ankle-deep water, creating splashes. The water is crystal clear with pebbles visible at the bottom. Lush green nature surrounds the scene. Refreshing summer vibe.",
     "characters": f"{BUBU}",
     "extra": SUMMER_NOTE},
    # P11
    {"story": 55, "page": 11, "lighting": "bright sparkling water reflections",
     "scene": "Bubu splashes playfully in the shallow stream, chasing little fish. NONO flies low over the water surface, dipping a wing tip in. Bubu laughs and splashes water toward NONO. Water droplets catch the light. Fun and lively water play scene.",
     "characters": f"{BUBU}\n{NONO}",
     "extra": SUMMER_NOTE},
    # P12
    {"story": 55, "page": 12, "lighting": "warm golden afternoon light",
     "scene": "Tina Mom holds up her phone taking photos of Bubu. Bubu leans in to look at the phone screen, pointing at it and laughing. Behind them is the resort scenery. A sweet mother-daughter moment captured through photography.",
     "characters": f"{BUBU}\n{TINA_MOM}",
     "extra": SUMMER_NOTE},
    # P13
    {"story": 55, "page": 13, "lighting": "soft warm bedtime light in a hotel room, moonlight through window",
     "scene": "A nice hotel room at night. Bubu lies on a big bed, eyes half-closed with a peaceful smile. Sam Dad on one side, Tina Mom on the other, both looking at her lovingly. NOMI gently tucks her in with a blanket. Through the window, a moonlit bamboo forest is visible. Quiet, peaceful ending scene.",
     "characters": f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}\n{NOMI}",
     "extra": ""},
]
PAGES.extend(s55)

# ═══ Story 56: 咘咘要回深圳了 ═══
s56 = [
    # P2
    {"story": 56, "page": 2, "lighting": "warm indoor evening light after dinner",
     "scene": "In a cozy living room after dinner, Tina Mom holds Bubu on her lap. They have a gentle, serious conversation. Bubu tilts her head looking curious but worried. Warm home atmosphere with soft evening light. An emotional family discussion.",
     "characters": f"{BUBU}\n{TINA_MOM}",
     "extra": SUMMER_NOTE},
    # P3
    {"story": 56, "page": 3, "lighting": "warm emotional indoor light",
     "scene": "Bubu's eyes are red with tears welling up. Tina Mom hugs her tightly. Sam Dad kneels beside them, gently patting Bubu's head. A bittersweet family moment — sad about leaving but comforting each other. Deeply emotional scene.",
     "characters": f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}",
     "extra": SUMMER_NOTE},
    # P4
    {"story": 56, "page": 4, "lighting": "soft golden morning light, slightly melancholy",
     "scene": "Monday morning. Bubu in her favorite pink dress and small backpack stands at the kindergarten gate, looking up at it for a long moment. Sunlight falls on the playground slide visible through the gate. Wind blows gently. A contemplative, bittersweet moment — her last day.",
     "characters": f"{BUBU}",
     "extra": SUMMER_NOTE},
    # P5
    {"story": 56, "page": 5, "lighting": "soft indoor classroom light, nostalgic feel",
     "scene": "Inside the familiar kindergarten classroom. Bubu walks slowly through, gently touching things — children's artwork on the wall, a block castle in the corner, flower buds on the windowsill. She looks nostalgic, trying to memorize everything. The classroom is warm and familiar.",
     "characters": f"{BUBU}",
     "extra": SUMMER_NOTE},
    # P6
    {"story": 56, "page": 6, "lighting": "warm emotional indoor light",
     "scene": "Teacher Yanyan kneels down and hugs Bubu tightly. Bubu wraps her arms around the teacher's neck. Both have emotional, teary expressions but also warm smiles. An intimate farewell embrace between teacher and beloved student.",
     "characters": f"{BUBU}\n{YANYAN}",
     "extra": SUMMER_NOTE},
    # P7
    {"story": 56, "page": 7, "lighting": "soft warm emotional light",
     "scene": "Close-up tender moment. Teacher Yanyan wipes Bubu's tears gently, their noses touching (eskimo kiss). Bubu smiles through tears. Beautiful, intimate farewell moment. Soft light around them.",
     "characters": f"{BUBU}\n{YANYAN}",
     "extra": SUMMER_NOTE},
    # P8
    {"story": 56, "page": 8, "lighting": "warm soft classroom light",
     "scene": "Teacher Zhang (deer) sits next to Bubu, holding her hand. They appear to be singing together. Bubu leans her head on Teacher Zhang's shoulder. Teacher Zhang's eyes are slightly red. An emotional musical farewell moment.",
     "characters": f"{BUBU}\n{ZHANG}",
     "extra": SUMMER_NOTE},
    # P9
    {"story": 56, "page": 9, "lighting": "warm friendship light",
     "scene": "Feifei and Moyu hug Bubu from both sides. Feifei looks sad, Moyu's short tail droops. Bubu holds Feifei's hand and extends her pinky for a pinky promise. All three have teary but brave smiles. A powerful friendship farewell moment.",
     "characters": f"{BUBU}\n{FEIFEI}\n{MOYU}",
     "extra": SUMMER_NOTE},
    # P10
    {"story": 56, "page": 10, "lighting": "warm golden classroom light",
     "scene": "All the kindergarten children form a circle around Bubu, handing her a large handmade card (with colorful drawings, no readable text). Teachers join the group hug circle. Bubu stands in the center, moved and happy. A farewell celebration scene with everyone gathered.",
     "characters": f"{BUBU}\n{MOYU}\n{FEIFEI}\n{YANYAN}\n{ZHANG}",
     "extra": SUMMER_NOTE + "Include several other small animal classmates in the circle (bear cub, small deer). "},
    # P11
    {"story": 56, "page": 11, "lighting": "soft morning light through car windows, slightly misty",
     "scene": "Inside a car, Bubu presses her face against the car window, looking out at the receding Suzhou cityscape — buildings, trees, and a river getting smaller. NOMI sits beside her, quietly holding her hand. A melancholy departure scene. The city fades behind them.",
     "characters": f"{BUBU}\n{NOMI}",
     "extra": SUMMER_NOTE},
    # P12
    {"story": 56, "page": 12, "lighting": "bright cheerful Shenzhen afternoon light",
     "scene": "Arriving in Shenzhen. From the car, Bubu and Tina Mom look through the car window at a beautiful new kindergarten. Through the fence, they see a huge colorful slide, a pretty sandbox, and children playing on grass with bubbles. Bubu's expression changes from sad to curious and excited. A new beginning.",
     "characters": f"{BUBU}\n{TINA_MOM}",
     "extra": SUMMER_NOTE},
    # P13
    {"story": 56, "page": 13, "lighting": "bright morning light but with anxious mood",
     "scene": "First day at new kindergarten. Bubu stands frozen at the new kindergarten gate, gripping Tina Mom's hand very tightly. Her feet won't move. The new kindergarten looks different — different colors, different gate design. Bubu looks scared and overwhelmed. Mom looks down at her with patience and love.",
     "characters": f"{BUBU}\n{TINA_MOM}",
     "extra": SUMMER_NOTE},
    # P14
    {"story": 56, "page": 14, "lighting": "warm welcoming light",
     "scene": "Teacher Yuanyuan (giant panda) kneels down in front of Bubu with a big warm smile, extending her round paw to take Bubu's hand. She is a gentle, welcoming figure. Bubu looks cautious but slightly reassured. The new kindergarten entrance behind them. A hopeful meeting moment.",
     "characters": f"{BUBU}\n{YUANYUAN_TEACHER}",
     "extra": SUMMER_NOTE + "Teacher Yuanyuan is a GIANT PANDA with black and white fur, round black ears, black eye patches. She wears a teacher's apron over a green top. "},
    # P15
    {"story": 56, "page": 15, "lighting": "bright colorful classroom light",
     "scene": "In the new classroom, Lele (a small otter) waves a crayon at Bubu enthusiastically. Lele has already handed Bubu a pink crayon. Bubu takes it tentatively with a shy small smile. A new friendship beginning. Colorful art supplies around.",
     "characters": f"{BUBU}\n{LELE}",
     "extra": SUMMER_NOTE + "Lele is a small OTTER with sleek brown fur, bright curious eyes, playful expression. She is a young girl about Bubu's age. "},
    # P16
    {"story": 56, "page": 16, "lighting": "warm inviting classroom light",
     "scene": "Bubu discovers the new classroom has wonderful things — a huge building block area, a wall of bookshelves with picture books, and a little gardening corner with sunflower seedlings. Bubu's eyes light up looking at the sunflowers. Teacher Yuanyuan smiles beside her. A sense of wonder and discovery.",
     "characters": f"{BUBU}\n{YUANYUAN_TEACHER}",
     "extra": SUMMER_NOTE + "Teacher Yuanyuan is a GIANT PANDA. "},
    # P17
    {"story": 56, "page": 17, "lighting": "bright sunny outdoor playground light",
     "scene": "Outdoor playground at the new kindergarten. Lele pulls Bubu by the hand to the swings. Bubu swings high, wind blowing her ears, with a growing smile. Lele stands nearby grinning. A beautiful playground with slides and green grass. A new friendship blooming.",
     "characters": f"{BUBU}\n{LELE}",
     "extra": SUMMER_NOTE + "Lele is a small OTTER. "},
    # P18
    {"story": 56, "page": 18, "lighting": "soft warm bedtime glow with starry night light",
     "scene": "Bubu's bedroom in Shenzhen at night. Bubu lies in her little bed with star-shaped night light casting soft glow on ceiling. Oliver (real Border Collie, four legs) rests by the bedside, tail wagging softly. NOMI sits by her pillow. NONO dozes on the bedside lamp. Bubu smiles peacefully, whispering goodnight. A sense of new home, new beginning, and old comforts together.",
     "characters": f"{BUBU}\n{NOMI}\n{NONO}\n{OLIVER}",
     "extra": "Oliver is a REAL dog — four legs, no clothes. Peaceful bedtime scene. "},
]
PAGES.extend(s56)

# ═══ Story 57: 咘咘学会等一等 ═══
s57 = [
    # P2
    {"story": 57, "page": 2, "lighting": "bright summer afternoon light inside a car",
     "scene": "Inside a car driving to the beach. Bright summer light. Bubu sits in her car seat in the back, happily singing along and bobbing her head. Sam Dad drives, Tina Mom in the passenger seat. Through the windows, a sunny coastal road is visible. Music fills the car. Happy road trip mood.",
     "characters": f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}",
     "extra": SUMMER_NOTE},
    # P3
    {"story": 57, "page": 3, "lighting": "bright car interior light",
     "scene": "Inside the car. Sam Dad turns back slightly (while driving safely) to talk to Bubu gently. Bubu pouts with her little mouth, looking stubborn. She crosses her arms. A playful parent-child negotiation about music.",
     "characters": f"{BUBU}\n{SAM_DAD}",
     "extra": SUMMER_NOTE},
    # P4
    {"story": 57, "page": 4, "lighting": "bright car interior light",
     "scene": "Inside the car. Tina Mom turns around to talk to Bubu. Bubu covers her ears with both paws, looking defiant but cute. A comedic stubborn-toddler moment. Mom looks amused but patient.",
     "characters": f"{BUBU}\n{TINA_MOM}",
     "extra": SUMMER_NOTE},
    # P5
    {"story": 57, "page": 5, "lighting": "bright beach sunlight",
     "scene": "Beautiful beach scene. Sam Dad and Tina Mom sit on a beach blanket having a conversation. Little Bubu runs over and tugs at Mom's hand/arm insistently, trying to show her something. Sandy beach, blue ocean, sunny sky. Classic beach day.",
     "characters": f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}",
     "extra": SUMMER_NOTE + "Beach clothing — Dad in casual beach shirt, Mom in sun dress, Bubu in her pink dress. "},
    # P6
    {"story": 57, "page": 6, "lighting": "bright beach light",
     "scene": "On the beach. Bubu keeps calling and tugging at Mom who hasn't finished her sentence. Dad and Mom exchange a knowing glance and sigh with amused smiles. Bubu is eager and impatient. Comedic family beach moment.",
     "characters": f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}",
     "extra": SUMMER_NOTE},
    # P7
    {"story": 57, "page": 7, "lighting": "bright cheerful beach light",
     "scene": "NOMI walks over carrying a colorful beach ball, smiling knowingly. She approaches Bubu with a fun game idea. Beach in background. NOMI looks playful and clever with a problem-solving expression.",
     "characters": f"{BUBU}\n{NOMI}",
     "extra": SUMMER_NOTE},
    # P8
    {"story": 57, "page": 8, "lighting": "warm beach golden light",
     "scene": "On the beach, NOMI explains the rules of the take-turns game, gesturing with her paws. Bubu, Sam Dad, Tina Mom listen. NONO nearby flaps his wings excitedly wanting to go first. The group is gathered in a circle on the sand. Fun family game setup.",
     "characters": f"{BUBU}\n{NOMI}\n{NONO}\n{SAM_DAD}\n{TINA_MOM}",
     "extra": SUMMER_NOTE},
    # P9
    {"story": 57, "page": 9, "lighting": "warm golden beach light",
     "scene": "Everyone sits in a circle on the beach sand. NONO stands in the center performing — singing with his beak open, wings spread. He's obviously off-key but enthusiastic. Everyone else watches and laughs warmly. Ocean and sunset-beginning sky in background.",
     "characters": f"{BUBU}\n{NOMI}\n{NONO}\n{SAM_DAD}\n{TINA_MOM}",
     "extra": SUMMER_NOTE},
    # P10
    {"story": 57, "page": 10, "lighting": "warm golden hour beach light",
     "scene": "Sam Dad's turn. He sits in the circle playing/humming a song with a gentle expression. Bubu is about to speak but sees NOMI holding a finger to her lips (shh gesture). Bubu catches herself and listens quietly, looking surprised that the song is actually nice. Everyone else listens respectfully.",
     "characters": f"{BUBU}\n{NOMI}\n{SAM_DAD}\n{TINA_MOM}\n{NONO}",
     "extra": SUMMER_NOTE},
    # P11
    {"story": 57, "page": 11, "lighting": "warm golden sunset light",
     "scene": "Tina Mom's turn. She speaks warmly, gesturing as she tells a story about her childhood at the beach. Bubu's eyes are wide with fascination and surprise, leaning forward with interest. Beautiful sunset light on the beach. Engaged family storytelling moment.",
     "characters": f"{BUBU}\n{TINA_MOM}\n{SAM_DAD}\n{NOMI}\n{NONO}",
     "extra": SUMMER_NOTE},
    # P12
    {"story": 57, "page": 12, "lighting": "beautiful golden sunset light",
     "scene": "Finally Bubu's turn! She stands up in the circle proudly, holding up a pink seashell in one paw and singing with her other arm raised. Everyone watches and listens intently with big smiles. They clap for her. Bubu looks absolutely delighted — she feels truly heard. Golden sunset behind them. A breakthrough moment.",
     "characters": f"{BUBU}\n{NOMI}\n{NONO}\n{SAM_DAD}\n{TINA_MOM}",
     "extra": SUMMER_NOTE},
    # P13
    {"story": 57, "page": 13, "lighting": "gorgeous orange-pink sunset light through car windows",
     "scene": "In the car on the way home. Bubu sits quietly in her car seat with a peaceful, mature smile, listening to Dad's music playing. NOMI and NONO in the back seat share a knowing smile. Beautiful sunset light streams through the car windows, illuminating Bubu's face warmly. A moment of growth and contentment. Warm ending.",
     "characters": f"{BUBU}\n{NOMI}\n{NONO}\n{SAM_DAD}",
     "extra": ""},
]
PAGES.extend(s57)


def generate_image(prompt, output_path, retry=0):
    """Call Azure gpt-image-2 API and save result."""
    url = f"{ENDPOINT}?api-version={API_VERSION}"
    
    body = json.dumps({
        "prompt": prompt,
        "n": 1,
        "size": "1024x1536",
        "quality": "medium",
        "output_format": "png"
    }).encode()
    
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json",
        "api-key": API_KEY
    })
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
        
        b64 = result["data"][0]["b64_json"]
        png_path = output_path.replace(".jpg", ".png")
        with open(png_path, "wb") as f:
            f.write(base64.b64decode(b64))
        
        # Convert PNG to JPG with ffmpeg
        subprocess.run([
            "ffmpeg", "-y", "-i", png_path,
            "-q:v", "2", output_path
        ], capture_output=True, check=True)
        
        # Remove PNG
        os.remove(png_path)
        
        size_kb = os.path.getsize(output_path) / 1024
        return True, size_kb
    
    except urllib.error.HTTPError as e:
        if e.code == 429 and retry < MAX_RETRIES:
            print(f"  ⚠️ 429 rate limited, waiting {RETRY_WAIT}s (retry {retry+1}/{MAX_RETRIES})...")
            sys.stdout.flush()
            time.sleep(RETRY_WAIT)
            return generate_image(prompt, output_path, retry + 1)
        else:
            error_body = e.read().decode() if hasattr(e, 'read') else str(e)
            print(f"  ❌ HTTP {e.code}: {error_body[:300]}")
            sys.stdout.flush()
            return False, 0
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:300]}")
        sys.stdout.flush()
        return False, 0


def build_prompt(page_data):
    """Build the full prompt from page data."""
    return PROMPT_TEMPLATE.format(
        lighting=page_data["lighting"],
        scene=page_data["scene"],
        characters=page_data["characters"],
        extra=page_data.get("extra", "")
    )


def main():
    # Check which pages already exist
    total = len(PAGES)
    results = []
    skipped = 0
    failed = []
    
    print(f"═══ Volume 6 Print Edition: {total} illustrations to generate ═══")
    print(f"Stories 53-57 | 1024x1536 | quality=medium")
    print(f"Interval: {INTERVAL}s | Retry wait: {RETRY_WAIT}s")
    print()
    sys.stdout.flush()
    
    for i, page_data in enumerate(PAGES):
        story = page_data["story"]
        page = page_data["page"]
        output_dir = os.path.join(BASE_DIR, f"story{story}")
        output_path = os.path.join(output_dir, f"page-{page:02d}.jpg")
        
        # Skip if already exists
        if os.path.exists(output_path):
            size_kb = os.path.getsize(output_path) / 1024
            print(f"[{i+1}/{total}] Story {story} P{page:02d} — SKIP (exists, {size_kb:.0f}KB)")
            sys.stdout.flush()
            results.append((story, page, size_kb, "skip"))
            skipped += 1
            continue
        
        prompt = build_prompt(page_data)
        print(f"[{i+1}/{total}] Story {story} P{page:02d} — generating...")
        sys.stdout.flush()
        
        success, size_kb = generate_image(prompt, output_path)
        
        if success:
            print(f"  ✅ {size_kb:.0f}KB")
            results.append((story, page, size_kb, "ok"))
        else:
            print(f"  ❌ FAILED")
            results.append((story, page, 0, "fail"))
            failed.append(f"Story {story} P{page}")
        
        sys.stdout.flush()
        
        # Wait between requests (skip wait for last one)
        if i < total - 1 and success:
            time.sleep(INTERVAL)
    
    # Summary
    print("\n═══ SUMMARY ═══")
    generated = sum(1 for r in results if r[3] == "ok")
    print(f"Generated: {generated} | Skipped: {skipped} | Failed: {len(failed)}")
    
    if failed:
        print(f"Failed pages: {', '.join(failed)}")
    
    # Per-story breakdown
    for story_num in [53, 54, 55, 56, 57]:
        story_results = [r for r in results if r[0] == story_num]
        print(f"\nStory {story_num}:")
        for s, p, sz, status in story_results:
            status_icon = "✅" if status == "ok" else "⏭️" if status == "skip" else "❌"
            print(f"  {status_icon} P{p:02d}: {sz:.0f}KB" if sz > 0 else f"  {status_icon} P{p:02d}: FAILED")
    
    print(f"\nTotal illustrations: {len(results)}")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
