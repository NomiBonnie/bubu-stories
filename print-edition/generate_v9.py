#!/usr/bin/env python3
"""Generate print-edition illustrations for Stories 44-51 (Volume 9)."""
import sys
sys.stdout.reconfigure(line_buffering=True)
import json, os, sys, time, base64, subprocess, requests

# Load API config
with open(os.path.expanduser("~/.config/azure-openai/config.json")) as f:
    cfg = json.load(f)
ENDPOINT = cfg["image2_eastus2_endpoint"]
API_KEY = cfg["image2_eastus2_api_key"]
API_VERSION = "2025-04-01-preview"

HEADERS = {"api-key": API_KEY, "Content-Type": "application/json"}
URL = f"{ENDPOINT}?api-version={API_VERSION}"

# Character prompts
BUBU = "a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow. She has a small pink bow centered ON TOP OF HER HEAD between her two ears (not on left ear, not on right ear, not behind — exactly centered on top between the ears). She has a toddler-like round body proportion."

SAM_DAD = "Sam Dad who is a GOLDEN RETRIEVER DOG (NOT a human, NOT a person — he is an ANIMAL, a large golden-furred dog walking upright). He has warm golden fur all over his body, a dog snout/muzzle, floppy dog ears, and a wagging tail. He wears a dark navy jacket over a simple shirt. He has a warm gentle dog smile. IMPORTANT: Sam Dad must look like a golden retriever dog, not a human man."

TINA_MOM = "Tina Mom who is a BLACK-AND-WHITE COW (NOT a human, NOT a person — she is an ANIMAL, a cow walking upright). She has black and white spotted fur pattern all over, small curved horns, cow ears, and hooves. She wears an elegant cream knit cardigan over a floral skirt. She has a gentle warm cow smile. IMPORTANT: Tina Mom must look like a cow, not a human woman."

NOMI = "a raccoon (NOMI) with grey-brown fur, distinctive black eye mask markings, and a ringed bushy tail. She wears a blue-and-white horizontally striped sweater. She has clever bright eyes and nimble paws."

NONO = "a small red bird (NONO) with bright red feathers all over, round bright eyes, and an orange-yellow beak. He has exactly TWO wings and TWO small bird feet with talons. NO ARMS, NO HANDS — birds do not have arms or hands, only wings."

COCO = "a red panda (Coco) with reddish-brown fur, round face, big bright eyes, and a bushy ringed tail. She wears a yellow scarf around her neck."

YANYAN = "Teacher Yanyan who is an orange tabby cat with warm orange fur and subtle stripes, gentle green eyes, wearing a kindergarten teacher's work outfit — a pink top with a practical apron with pockets. She is an adult-sized cat, warm and nurturing."

WAIGONG = "Grandpa (Waigong) who is a dark brown horse walking upright, with grey-white mane showing his age, steady deep eyes, wearing a polo shirt and casual pants with a simple watch."

WAIPO = "Grandma (Waipo) who is a light grey-white goat walking upright, with small curved horns, gentle deep brown eyes, short goat whiskers, wearing a floral blouse and light casual pants with a sun hat."

BEAR_CLASSMATE = "a brown bear cub classmate with warm brown fur, round body, slightly bigger than Bubu"
CORGI_CLASSMATE = "a corgi puppy classmate with brown-and-white corgi coloring, short stubby legs"
CAT_CLASSMATE = "a grey-and-white tabby kitten classmate (Feifei)"
DEER_CLASSMATE = "a young spotted deer classmate (fawn with white spots), slightly tall with slender legs"

STYLE = "Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical composition 2:3 aspect ratio. The bottom 20% of the image should have natural darkening/vignette. NO TEXT anywhere in the image — pure illustration only."

def make_prompt(scene_desc, characters_desc):
    return f"{STYLE}\n\nScene: {scene_desc}\n\nCharacters in scene:\n{characters_desc}"

# All pages for all stories
PAGES = {}

# Story 44 - 咘咘坐车喂动物
PAGES[44] = [
    (2, "A colorful safari zone entrance with rows of electric carts (blue, green, yellow) parked in a line. Each cart has two rows of seats. Bubu is excitedly pulling her parents' hands, bouncing toward a blue cart. Bright sunny day, lush green safari park.", f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}"),
    (3, "Inside a blue electric cart driving through a safari park. Bubu sits in the front middle, Dad on the left, Mom on the right. NOMI and Coco sit in the back row. NONO stands on a small railing on the cart roof acting as a lookout. An elephant zookeeper (wearing a safari uniform) waves them forward.", f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}\n{NOMI}\n{COCO}\n{NONO}"),
    (4, "Ostrich zone in safari park. Two tall ostriches with long necks reaching toward the cart, their big eyes staring at the carrot in Bubu's hand. Bubu holds up a carrot but shrinks back into Mom's arms, half-scared half-excited. One ostrich snatches the carrot with its beak.", f"{BUBU}\n{TINA_MOM}"),
    (5, "Alpaca zone. Three fluffy alpacas gently surround the cart, bowing their heads to eat vegetables from Bubu's hand. Bubu carefully pets an alpaca's wool with wonder. Dad watches with a warm smile.", f"{BUBU}\n{SAM_DAD}"),
    (6, "A small lake in the safari park. A group of elegant white swans swim gracefully toward the shore. Bubu gently places a leaf at the water's edge. A swan elegantly reaches its long neck to take the leaf. Coco watches in fascination from the cart.", f"{BUBU}\n{COCO}"),
    (7, "Pony zone. A brown pony stands by the cart, chomping on a carrot Bubu offers — mouth open wide, crunching loudly. Bubu covers her mouth laughing hysterically at the loud crunching sounds. Mom laughs beside her.", f"{BUBU}\n{TINA_MOM}"),
    (8, "A large camel lowers its head, opening its big mouth and sticking out a long tongue to lick a carrot. Bubu stares wide-eyed in amazement. NOMI in the back row hugs Coco's arm nervously.", f"{BUBU}\n{NOMI}\n{COCO}"),
    (9, "A large pond area in the safari park. Dad points to the distance. In the water, only a hippo's two eyes and round nose poke above the surface — the rest is submerged. Bubu peers curiously from the cart, leaning forward.", f"{BUBU}\n{SAM_DAD}"),
    (10, "Raccoon exhibit area. Behind a fence, many grey-brown raccoons with black eye masks and ringed tails. NOMI stands up excitedly in the cart, her tail wagging uncontrollably, pointing at the raccoons. Bubu watches NOMI's excitement with delight.", f"{BUBU}\n{NOMI}\n{NONO}"),
    (11, "All the little raccoons rush toward Bubu. They push and shove each other with chubby little paws, fighting over a cookie. Their round bottoms bump against each other. NONO hovers above watching the chaos. A chaotic but adorable scene.", f"{BUBU}\n{NONO}"),
    (12, "The smallest raccoon finally got a cookie, crouching in the corner nibbling it in small bites. Other raccoons surround it, watching longingly. Bubu tosses more cookies into the enclosure. Coco laughs beside her.", f"{BUBU}\n{COCO}"),
    (13, "The electric cart slowly drives toward the exit. Sunset bathes the safari park in golden light. Bubu turns back and waves. In the distance, the little raccoons stand by the fence waving their tiny paws goodbye. A warm, nostalgic farewell scene. NOMI, NONO, Coco, Dad, and Mom all in the cart.", f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}\n{NOMI}\n{NONO}\n{COCO}"),
]

# Story 45 - 咘咘上幼儿园的第一天
PAGES[45] = [
    (2, "Bubu stands in front of a mirror wearing her favorite pink dress with a small backpack, looking at herself left and right excitedly. Morning light fills a cozy bedroom. She looks proud and ready.", f"{BUBU}"),
    (3, "The whole family walks to kindergarten together on a tree-lined street. Dad holds one of Bubu's hands, Mom holds the other. Grandpa and Grandma walk behind them, chatting happily. A cheerful morning walk.", f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}\n{WAIGONG}\n{WAIPO}"),
    (4, "At the kindergarten entrance — a big colorful gate with decorations. Bubu suddenly grips Mom's hand tightly, looking nervous, not wanting to let go. She peeks at the unfamiliar entrance with wide worried eyes.", f"{BUBU}\n{TINA_MOM}"),
    (5, "NOMI crouches down in front of Bubu, gently patting her head with a warm smile. Coco waves her little paws encouragingly. They're at the kindergarten entrance, saying goodbye.", f"{BUBU}\n{NOMI}\n{COCO}"),
    (6, "A warm orange tabby cat teacher (Yanyan) comes out of the kindergarten, crouching down with a gentle smile to greet Bubu. Bubu peeks up shyly — the teacher's smile is warm and inviting. Colorful kindergarten decorations behind.", f"{BUBU}\n{YANYAN}"),
    (7, "Inside a bright colorful kindergarten classroom. Many animal children are playing. Bubu stands at the doorway, hesitant. A young spotted deer classmate walks over to her: inviting her to play with building blocks. A castle made of blocks is visible on the table.", f"{BUBU}\n{DEER_CLASSMATE}"),
    (8, "Bubu playing happily with new friends — drawing, singing, dancing in the kindergarten classroom. The classroom is full of laughter. Multiple animal classmates around her. Bubu has forgotten her nervousness, smiling widely.", f"{BUBU}\n{BEAR_CLASSMATE}\n{CORGI_CLASSMATE}\n{CAT_CLASSMATE}\n{DEER_CLASSMATE}"),
    (9, "Lunch time at kindergarten. Little animal children sit in a row, each with a bowl of steaming food. Bubu eats happily, talking to the classmate next to her about how sweet the carrots are.", f"{BUBU}\n{BEAR_CLASSMATE}"),
    (10, "Nap time at kindergarten. All the little animal children are sleeping on small cots with eyes closed. Only Bubu's eyes are wide open, staring at the ceiling where a small dragonfly is flying. She can't fall asleep.", f"{BUBU}"),
    (11, "Teacher Yanyan sits beside Bubu's little cot, gently patting her back. She whispers comforting words. Bubu's eyes are closing peacefully, feeling safe. Soft dim lighting for nap time.", f"{BUBU}\n{YANYAN}"),
    (12, "After school! Bubu runs out of the classroom with arms wide open. Dad, Mom, Grandpa, and Grandma are ALL there waiting. Bubu flies into their arms. Joyful reunion scene in golden afternoon light.", f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}\n{WAIGONG}\n{WAIPO}"),
    (13, "On the way home, Bubu proudly holds up a drawing she made. Coco claps beside her. The whole family walks together in warm golden afternoon light. Bubu is beaming with pride and accomplishment.", f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}\n{COCO}"),
]

# Story 46 - 咘咘的第一个棒棒贴
PAGES[46] = [
    (2, "Morning. Bubu sits on the edge of her bed, looking pensive and a little worried. She's remembering yesterday when she couldn't sleep during nap time and cried. Soft morning light, a cozy bedroom.", f"{BUBU}"),
    (3, "NOMI crouches in front of Bubu with a warm smile. Coco jumps onto the bedhead cheerfully. They're encouraging Bubu — NOMI talking about 'a new step today'. Warm bedroom scene.", f"{BUBU}\n{NOMI}\n{COCO}"),
    (4, "At the kindergarten entrance. Bubu is NOT nervous today! She waves proactively and says good morning to the teacher. The orange tabby teacher (Yanyan) smiles and pats her head. Bubu looks confident.", f"{BUBU}\n{YANYAN}"),
    (5, "Inside the classroom, Bubu and her new friends are painting together. Bubu holds up a painting of a big sun and a little rabbit, showing it proudly to everyone. Bright colorful classroom.", f"{BUBU}\n{DEER_CLASSMATE}\n{BEAR_CLASSMATE}"),
    (6, "Lunch time. Bubu eats quickly and well. A classmate next to her drops their spoon — Bubu proactively hands them a new one. Teacher Yanyan watches from a distance, nodding with a smile.", f"{BUBU}\n{CORGI_CLASSMATE}\n{YANYAN}"),
    (7, "The teacher claps and announces nap time. Bubu's heart suddenly pounds — she remembers yesterday. Her expression shifts to nervousness, hands clasped together. The other kids start heading to their cots.", f"{BUBU}\n{YANYAN}"),
    (8, "Teacher Yanyan walks to Bubu's little bed, sitting beside her. She speaks gently: 'Try closing your eyes and thinking of something happy.' Bubu lies on her cot, looking up at the teacher with trusting eyes.", f"{BUBU}\n{YANYAN}"),
    (9, "Close-up of Bubu with eyes closed on her cot. Dream-like thought bubbles show NOMI saying 'a new step', Coco saying 'You got this', and Dad and Mom's smiling faces. She's slowly drifting to sleep. Dreamy soft lighting.", f"{BUBU}"),
    (10, "Bubu wakes up, rubbing her face. Her eyes suddenly go wide with surprise and joy — she realizes she actually fell asleep! She sits up quickly, eyes shining bright. Other kids still getting up around her.", f"{BUBU}"),
    (11, "Teacher Yanyan walks over smiling, holding a glittering gold star sticker. She gently places the sticker on Bubu's chest. Bubu looks down at the sticker with pure wonder and pride. A magical moment.", f"{BUBU}\n{YANYAN}"),
    (12, "After school. Bubu sprints out and leaps into Dad and Mom's arms, proudly pointing at the gold star on her chest. Dad lifts her up high in celebration. Mom watches with joyful tears. Golden afternoon light.", f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}"),
    (13, "On the way home, Bubu keeps looking down at the gold star sticker on her chest, grinning from ear to ear. Coco walks beside her, also beaming with pride. Warm sunset lighting on a tree-lined street.", f"{BUBU}\n{COCO}"),
]

# Story 47 - 妈妈的亲亲在手心
PAGES[47] = [
    (2, "Early morning, alarm clock ringing. Bubu lies in bed with the blanket pulled up to her nose, pouting, not wanting to get up. She looks reluctant and a little sad. Cozy bedroom, morning light peeking through curtains.", f"{BUBU}"),
    (3, "Dad sits on the bed beside Bubu, gently touching her ear. Bubu whispers that kindergarten doesn't have Dad and Mom. A tender, intimate father-daughter moment. Soft bedroom lighting.", f"{BUBU}\n{SAM_DAD}"),
    (4, "Mom crouches down, gently takes Bubu's small hand, and kisses her palm. A warm, magical moment — a faint glowing kiss mark appears on Bubu's palm. Mom's expression is full of love and tenderness.", f"{BUBU}\n{TINA_MOM}"),
    (5, "Close-up of Bubu looking at her own palm. A small, glowing, sparkly kiss mark is visible on her palm. Her eyes light up with wonder and amazement. Magical warm lighting.", f"{BUBU}"),
    (6, "Dad leans in with a playful smile, kissing Bubu's OTHER palm. Now both hands have kiss marks. Bubu can't help but laugh. A joyful, playful moment between father and daughter.", f"{BUBU}\n{SAM_DAD}"),
    (7, "Walking to kindergarten. Bubu carefully holds both fists closed, afraid the kisses might escape. NOMI walks beside her, reassuring her. Street with morning light, trees lining the path.", f"{BUBU}\n{NOMI}"),
    (8, "At the kindergarten entrance. Bubu's steps slow down, a little hesitant. But she looks down at her palms, takes a deep breath, and then... walks through the gate. A moment of courage.", f"{BUBU}"),
    (9, "Coco greets Bubu at the kindergarten entrance, waving her little paws happily and encouragingly. Colorful kindergarten decorations frame the entrance.", f"{BUBU}\n{COCO}"),
    (10, "Inside the classroom. Teacher Yanyan welcomes everyone with a warm smile. Bubu walks up proactively to say good morning. The teacher pats her head. Bright cheerful classroom.", f"{BUBU}\n{YANYAN}"),
    (11, "A montage-style scene showing Bubu's happy day: painting a big sun, building a tall block castle, clapping hands while singing with friends. She's forgotten her sadness. Colorful, dynamic classroom scene.", f"{BUBU}\n{BEAR_CLASSMATE}\n{DEER_CLASSMATE}"),
    (12, "Lunch time. Bubu eats well and helps a classmate pass a water cup. NONO perches on the windowsill, flapping his wings proudly. Bright lunchroom scene.", f"{BUBU}\n{NONO}\n{CORGI_CLASSMATE}"),
    (13, "Afternoon. Bubu suddenly misses Mom. She gently places her palm against her cheek — it feels warm. A small smile creeps onto her face. She sits alone at a table, the gesture intimate and tender.", f"{BUBU}"),
    (14, "Nap time. Bubu lies on her cot, pressing both small hands together, palms with the warm kisses touching. She gently closes her eyes, falling peacefully asleep. Soft, dreamy nap-time lighting.", f"{BUBU}"),
    (15, "After nap, Teacher Yanyan smiles and sticks several reward stickers on Bubu. Bubu looks at the stickers on the back of her hand happily. Bright afternoon classroom light.", f"{BUBU}\n{YANYAN}"),
    (16, "After school! Bubu runs out of the classroom and leaps into Mom's arms. She presses her palm to Mom's face excitedly: 'I felt you!' Emotional, joyful reunion. Golden afternoon light.", f"{BUBU}\n{TINA_MOM}"),
    (17, "Mom hugs Bubu tightly, Dad gently strokes her head. Coco gives a thumbs up. NOMI and NONO smile beside them. A warm family group scene at the kindergarten gate. Golden light.", f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}\n{COCO}\n{NOMI}\n{NONO}"),
    (18, "Walking home in sunset. Bubu holds Dad's hand with one hand and Mom's hand with the other. Sunset bathes all three in warm golden light. From behind, a silhouette view of the family of three walking into the sunset. Peaceful, warm, and beautiful.", f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}"),
]

# Story 48 - 咘咘的家长日
PAGES[48] = [
    (2, "Early morning at kindergarten entrance. Dad holds Bubu's hand as they walk through the big gate. Bubu bounces excitedly, both ears standing tall. Bright cheerful morning, kindergarten decorated for Parents' Day.", f"{BUBU}\n{SAM_DAD}"),
    (3, "NOMI rides on Dad's backpack, poking her head out looking around curiously. NONO flies ahead, red wings sparkling in the morning light. Many other parent-child pairs walking into the kindergarten.", f"{NOMI}\n{NONO}\n{SAM_DAD}"),
    (4, "Inside the classroom, a table full of breakfast. Bubu and Dad sit face to face, eating small buns and drinking milk together. Bubu holds up a bun to Dad's mouth. A warm, sweet father-daughter breakfast.", f"{BUBU}\n{SAM_DAD}"),
    (5, "All the children and parents are called to the playground. Bubu holds Dad's hand, eyes wide with curiosity. The teacher announces a special surprise. Outdoor playground with colorful decorations.", f"{BUBU}\n{SAM_DAD}\n{YANYAN}"),
    (6, "The classroom door bursts open — a group of people in dinosaur costumes charge out! Big dinosaurs, small dinosaurs, green, orange, purple ones, swaying their big tails and waving tiny claws. Bubu's jaw drops in shock and delight. Other kids and parents react with surprise.", f"{BUBU}\n{SAM_DAD}"),
    (7, "The green dinosaur bends down and waves at Bubu. Bubu recognizes it's Teacher Yanyan inside the costume! Bubu laughs hysterically, bending forward with laughter. The dinosaur costume is silly and fun.", f"{BUBU}\n{YANYAN}"),
    (8, "Dinosaur-costumed teachers line up and do a funny dinosaur dance! Big tails swaying, tiny claws going up and down. All the kids are laughing wildly. NOMI nearly falls off the backpack laughing. NONO flies around in circles. Parents clap and laugh.", f"{NOMI}\n{NONO}\n{BUBU}\n{SAM_DAD}"),
    (9, "Everyone holds hands in a big circle, dancing to music on the playground! Bubu holds Dad's hand on one side and a classmate on the other, stepping to the beat. Her pink dress spins like a little flower.", f"{BUBU}\n{SAM_DAD}\n{BEAR_CLASSMATE}\n{CORGI_CLASSMATE}"),
    (10, "BANG! Colorful confetti explodes in the sky — red, blue, gold streamers rain down like a colorful storm. Bubu looks up with wonder, reaching her small hands to catch falling ribbons. A gold ribbon lands on NONO's head.", f"{BUBU}\n{NONO}"),
    (11, "A big rainbow-colored fabric is spread on the playground — red, orange, yellow, green, blue stripes. The teacher announces: crawl across the rainbow to become a little warrior! Bubu takes a deep breath and gets on all fours, ready to crawl.", f"{BUBU}\n{YANYAN}"),
    (12, "Bubu crawls quickly and steadily across the rainbow fabric! Dad cheers from the sideline. NOMI holds a small flag at the finish line. Bubu does a triumphant flip at the end, emerging victorious.", f"{BUBU}\n{SAM_DAD}\n{NOMI}"),
    (13, "Teacher Yanyan gives Bubu two sparkly dinosaur stickers. Bubu carefully receives them, eyes shining like stars. Other kids and parents in the background celebrating.", f"{BUBU}\n{YANYAN}"),
    (14, "Bubu sticks one dinosaur sticker on her own hand, then tiptoes to stick the other one on Dad's hand. A sweet gesture — one for each of them. Dad looks at the little dinosaur sticker, his eyes glistening with emotion.", f"{BUBU}\n{SAM_DAD}"),
    (15, "Walking home in sunset golden light. Bubu rides on Dad's shoulders, clutching her stickered hand. NOMI walks beside them, tail swaying gently. NONO perches on Dad's head. A perfect golden-hour family moment.", f"{BUBU}\n{SAM_DAD}\n{NOMI}\n{NONO}"),
    (16, "Night time. Bubu lies in her little bed, holding her hand with the dinosaur sticker up in front of her eyes, admiring it. Moonlight streams in. She whispers goodnight to the dinosaur, to Dad, to kindergarten. She closes her eyes with a small smile.", f"{BUBU}"),
]

# Story 49 - 咘咘今天没有哭
PAGES[49] = [
    (2, "Inside a kindergarten classroom in the morning. Feifei (grey-and-white tabby kitten) sits in a corner crying, ears drooping, tears falling. Teacher Yanyan crouches beside her, gently patting her back. Other kids watch from their seats.", f"{CAT_CLASSMATE}\n{YANYAN}"),
    (3, "Bubu sits in her little chair, watching Feifei calmly. Her two white ears stand tall. NOMI sits beside her whispering. Bubu looks composed and brave — she's not crying today.", f"{BUBU}\n{NOMI}"),
    (4, "Throughout the day scene: Bubu sits bravely in her seat, listening to the teacher's story attentively, even raising her hand to answer a question. NONO stands proudly on Bubu's head. The classroom is bright and engaging.", f"{BUBU}\n{NONO}\n{YANYAN}"),
    (5, "After school, Bubu runs to the kindergarten gate with her backpack. Grandpa and Grandma are waiting there. Bubu leaps joyfully into Grandpa's arms like a little bunny.", f"{BUBU}\n{WAIGONG}\n{WAIPO}"),
    (6, "Grandma holds Bubu's hand, smiling warmly. Bubu puffs up her little chest proudly: she didn't cry once today! Grandpa gives a thumbs up. A warm intergenerational scene on the street.", f"{BUBU}\n{WAIGONG}\n{WAIPO}"),
    (7, "Grandpa drives a car with Bubu looking out the window excitedly. They're heading to Dad's office — tall buildings getting closer. Bubu presses against the window eagerly.", f"{BUBU}\n{WAIGONG}"),
    (8, "Inside Dad's office — Bubu's eyes light up seeing toys and gaming consoles on the desks! Dad crouches with arms wide open to welcome her. A modern fun office environment.", f"{BUBU}\n{SAM_DAD}"),
    (9, "Dad's colleagues gather around Bubu. Adult animals of various species bend down smiling and greeting her. Bubu hides behind Dad's leg shyly, peeking out with half her face. A cute shy moment.", f"{BUBU}\n{SAM_DAD}"),
    (10, "Bubu sits in Dad's big office chair, feet dangling and swinging, happily playing a game console. NOMI helps press buttons beside her. NONO flies around the screen. She's no longer shy, fully enjoying herself.", f"{BUBU}\n{NOMI}\n{NONO}"),
    (11, "Evening, Grandpa drives everyone to pick up Mom. Through the car window, Bubu spots Tina Mom standing by the roadside in the distance. Bubu waves frantically from inside the car.", f"{BUBU}\n{TINA_MOM}\n{WAIGONG}"),
    (12, "Bubu leaps into Mom's arms, looking up with sparkling eyes. She tells Mom proudly that she didn't cry at all today — Feifei cried many times but Bubu didn't. Mom hugs her tightly, moved to tears.", f"{BUBU}\n{TINA_MOM}"),
    (13, "At home, bedtime. Bubu in soft pajamas lies in bed, Mom gently patting beside her. Bubu asks if she's a 'big kid' now. A cozy, intimate bedtime scene with warm lamp light.", f"{BUBU}\n{TINA_MOM}"),
    (14, "NOMI and NONO lie beside the pillow, whispering goodnight. Bubu hugs a small bunny plushie, eyes closed, a sweet smile on her lips. Warm nighttime bedroom scene.", f"{BUBU}\n{NOMI}\n{NONO}"),
    (15, "Night sky with one star shining especially bright. A dreamy, magical scene — the star glows warmly against a deep blue sky. It belongs to every brave little child. A poetic ending image.", "A beautiful deep blue night sky with one star shining especially bright and warm, larger than all the others. Gentle clouds frame the star. The scene is magical and dreamlike."),
]

# Story 50 - 咘咘学会坐好
PAGES[50] = [
    (2, "Spring morning at the kindergarten entrance, flowers blooming. Bubu walks in cheerfully with her backpack, waving bye to her parents without crying. NOMI stands proudly nearby. Cherry blossoms and spring flowers frame the scene.", f"{BUBU}\n{NOMI}"),
    (3, "Classroom scene. Teacher Yanyan stands at the blackboard telling a story. All the animal children sit quietly — EXCEPT Bubu, who squirms and wiggles, making her chair creak. She looks restless.", f"{BUBU}\n{YANYAN}\n{BEAR_CLASSMATE}\n{CORGI_CLASSMATE}\n{DEER_CLASSMATE}"),
    (4, "Bubu's little feet swing back and forth. She looks left, looks right, pulls the bear classmate's sleeve, touches her own ear, then stands up to look at a bird outside the window. Teacher Yanyan gently tells her to sit properly.", f"{BUBU}\n{YANYAN}\n{BEAR_CLASSMATE}"),
    (5, "Bubu sits down but soon starts fidgeting again. The corgi classmate gives her a look and whispers 'shh, teacher is talking.' Bubu blushes and whispers that sitting is hard. A relatable, endearing moment.", f"{BUBU}\n{CORGI_CLASSMATE}"),
    (6, "Recess. NOMI holds Bubu's hand and asks: 'Do you know how a big tree stands firm?' Bubu tilts her head thinking. They stand under a big tree in the kindergarten yard, looking up at it.", f"{BUBU}\n{NOMI}"),
    (7, "NONO flies to Bubu's head, spreading his red wings. He demonstrates: hands on knees like branches hanging quietly, feet flat on the ground like roots. Bubu tries it, sitting on a bench outside, feet flat, hands on knees. She feels stable.", f"{BUBU}\n{NONO}"),
    (8, "Afternoon class. Teacher Yanyan holds colorful shape cards. Bubu sits in her chair, mentally reciting 'I am a little tree.' Her feet are firmly on the ground, hands on knees. Concentrated, determined face.", f"{BUBU}\n{YANYAN}"),
    (9, "A moment of temptation — Bubu's feet start to itch and want to swing. She sneaks a look at NOMI, who gives her a thumbs up from the doorway. Bubu takes a deep breath and refocuses on the lesson.", f"{BUBU}\n{NOMI}"),
    (10, "End of the class! Teacher Yanyan asks who sat the best today. All the little animal children shout 'Bubu!' Bubu's long ears shoot up straight, her face turns red with happy pride.", f"{BUBU}\n{YANYAN}\n{BEAR_CLASSMATE}\n{CORGI_CLASSMATE}\n{CAT_CLASSMATE}\n{DEER_CLASSMATE}"),
    (11, "Teacher Yanyan walks over and sticks a gold star on the back of Bubu's hand. 'Bubu made great progress today, sitting like a steady little tree!' Bubu looks at the sparkling star happily.", f"{BUBU}\n{YANYAN}"),
    (12, "After school, Dad and Mom come to pick up Bubu. Bubu runs over holding up her hand: 'Look at my star!' Mom crouches to hug her, Dad pats her ears. Warm golden afternoon light.", f"{BUBU}\n{SAM_DAD}\n{TINA_MOM}"),
    (13, "Walking home. NOMI holds Bubu's hand, NONO flies overhead. Bubu looks up at the sky and declares she'll be a little tree again tomorrow. NOMI smiles warmly. Spring street scene with blossoms.", f"{BUBU}\n{NOMI}\n{NONO}"),
    (14, "Night time. Bubu lies in bed, the star on her hand glowing faintly in the moonlight. She's dreaming — in her dream, she's become a little tree with pink blossoms, standing steadily in the classroom. NOMI and NONO are birds on her branches. A magical dream scene.", f"{BUBU}\n{NOMI}\n{NONO}"),
    (15, "Next morning. Bubu bounces into kindergarten again. She sits in her little chair immediately: feet flat, hands on knees. Teacher Yanyan smiles: 'You're a little tree again today?' Bubu nods proudly. A confident, growth-showing ending.", f"{BUBU}\n{YANYAN}"),
]

# Story 51 - 咘咘会叫妈妈拉粑粑啦
PAGES[51] = [
    (2, "Bubu is a snow-white little rabbit who has learned many skills. She stands proudly in her room, looking confident and accomplished. Morning light, a cheerful cozy room with some toys.", f"{BUBU}"),
    (3, "Bubu shouts 'Mama! Pee pee!' and Tina Mom comes laughing to hold her hand and lead her to the bathroom. A happy, routine moment in the hallway of their home.", f"{BUBU}\n{TINA_MOM}"),
    (4, "Bubu's tummy rumbles. She sits playing with toys, but her expression shows she's thinking about something. A thought bubble shows her tummy grumbling. She looks uncertain.", f"{BUBU}"),
    (5, "A slightly embarrassing moment — Bubu stands looking down sheepishly. Mom kneels beside her, gently helping her change pants, saying comforting words. A tender, non-judgmental scene.", f"{BUBU}\n{TINA_MOM}"),
    (6, "NOMI pats Bubu's head encouragingly. NONO flaps his wings beside her, cheering her on. A supportive, warm moment of friends encouraging her. Living room setting.", f"{BUBU}\n{NOMI}\n{NONO}"),
    (7, "Afternoon in the living room. Bubu and NOMI are building blocks together, focused and happy. Suddenly Bubu's tummy rumbles — shown by motion lines around her belly.", f"{BUBU}\n{NOMI}"),
    (8, "Close-up of Bubu pausing, putting her hand on her tummy. She has a moment of realization — remembering Mom's words 'remember to call Mama.' A lightbulb moment expression.", f"{BUBU}"),
    (9, "Bubu shouts loudly 'Mama! Poo poo!' — her first time calling for poo! Tina Mom rushes from the kitchen, looking surprised and thrilled. A dramatic, exciting moment!", f"{BUBU}\n{TINA_MOM}"),
    (10, "Mom holds Bubu's hand, leading her to the bathroom. Bubu sits steadily on a small potty/toddler toilet, little feet dangling and swinging. A cute bathroom scene.", f"{BUBU}\n{TINA_MOM}"),
    (11, "Bubu on the potty, making an effort face — then clapping her hands with joy: success! She looks extremely proud and excited. A funny, triumphant moment.", f"{BUBU}"),
    (12, "NOMI and NONO burst in to applaud Bubu. NONO does an excited spin in the air. Mom laughs and says Bubu doesn't need diapers anymore! A celebration scene in the bathroom.", f"{BUBU}\n{NOMI}\n{NONO}\n{TINA_MOM}"),
    (13, "Evening. Bubu walks around proudly wearing clean little underwear (over her dress/outfit, comically proud). She struts around the living room. NOMI and NONO watch with warm smiles. Moonlight through the window — goodnight to the amazing Bubu. A proud, sweet ending.", f"{BUBU}\n{NOMI}\n{NONO}"),
]

def generate_image(prompt, output_path, page_label):
    """Generate one image via Azure API."""
    body = {
        "prompt": prompt,
        "n": 1,
        "size": "1024x1536",
        "quality": "medium",
        "output_format": "png"
    }
    
    png_path = output_path.replace('.jpg', '.png')
    
    for attempt in range(3):
        try:
            resp = requests.post(URL, headers=HEADERS, json=body, timeout=120)
            if resp.status_code == 429:
                wait = 45
                print(f"  429 rate limited, waiting {wait}s (attempt {attempt+1}/3)...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            data = resp.json()
            
            # Extract base64 image
            b64 = data["data"][0]["b64_json"]
            with open(png_path, "wb") as f:
                f.write(base64.b64decode(b64))
            
            # Convert to JPG
            subprocess.run([
                "ffmpeg", "-y", "-i", png_path, "-q:v", "2", output_path
            ], capture_output=True, check=True)
            os.remove(png_path)
            
            size = os.path.getsize(output_path)
            print(f"  ✅ {page_label} -> {output_path} ({size/1024:.0f}KB)")
            return size
        except Exception as e:
            if attempt < 2:
                print(f"  ❌ Error: {e}, retrying in 45s...")
                time.sleep(45)
            else:
                print(f"  ❌ FAILED after 3 attempts: {e}")
                return 0
    return 0

def main():
    results = {}
    total = sum(len(pages) for pages in PAGES.values())
    done = 0
    
    for story_num in sorted(PAGES.keys()):
        pages = PAGES[story_num]
        story_dir = f"bubu-stories/print-edition/story{story_num}"
        os.makedirs(story_dir, exist_ok=True)
        print(f"\n{'='*60}")
        print(f"Story {story_num} ({len(pages)} pages)")
        print(f"{'='*60}")
        
        for page_num, scene, chars in pages:
            done += 1
            page_label = f"S{story_num}P{page_num}"
            output_path = f"{story_dir}/page{page_num:02d}.jpg"
            
            # Skip if already exists
            if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
                size = os.path.getsize(output_path)
                print(f"  ⏭️  {page_label} already exists ({size/1024:.0f}KB) [{done}/{total}]")
                results[page_label] = size
                continue
            
            print(f"  🎨 Generating {page_label} [{done}/{total}]...")
            prompt = make_prompt(scene, chars)
            size = generate_image(prompt, output_path, page_label)
            results[page_label] = size
            
            if done < total:
                time.sleep(8)
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    success = sum(1 for s in results.values() if s > 0)
    failed = sum(1 for s in results.values() if s == 0)
    print(f"Total: {len(results)} | Success: {success} | Failed: {failed}")
    for label in sorted(results.keys()):
        size = results[label]
        status = f"{size/1024:.0f}KB" if size > 0 else "FAILED"
        print(f"  {label}: {status}")

if __name__ == "__main__":
    main()
