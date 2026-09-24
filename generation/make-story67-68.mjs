import fs from 'node:fs'
import path from 'node:path'
import { spawnSync } from 'node:child_process'

const root = process.cwd()
const tool = '/Users/samyuan/.openclaw/workspace/tools/azure-image25-generate.mjs'
const node = '/opt/homebrew/opt/node@24/bin/node'
const only = process.argv.slice(2).filter(arg => /^\d+:[1-9]\d*$/.test(arg)).map(arg => {
  const [story, page] = arg.split(':').map(Number)
  return { story, page }
})

const cast = `CHARACTER BIBLE — all illustrated family members are upright bipedal anthropomorphic characters, never on all fours; no NOMI, no NONO. Bubu: a toddler-sized, 100% snow-white fur rabbit with exactly TWO long ears with pink inner ears, large sparkling brown eyes, a small pink nose, a pink dress, and one pink bow fixed precisely at the top center of her head between both ears. Dad: a golden retriever with standard golden fur, wearing a dark autumn warm coat. Mom: a black-and-white dairy cow, explicitly NOT human, wearing an autumn trench coat. Grandpa: a short-necked, round and stocky bright-green dinosaur with smooth green skin, tiny head spikes, golden round spectacles, a white collared shirt and brown trousers; no hair, not a long-neck dinosaur. Grandma: a brown-furred monkey with brown hair in a neat bun, green earrings and a Chinese-style floral top; never grey or white hair. Maternal grandpa: an upright anthropomorphic horse. Maternal grandma: an upright anthropomorphic goat. For this September Harbin trip, all characters wear warm outerwear appropriate for cool weather, with NO scarves and NO gloves. Do not add any extra people or rabbit parents.`
const art = `Pixar 3D children's picture-book illustration, refined cinematic character animation, vertical portrait 1024x1536, no text, no logos, no watermarks. Keep character scale and features consistent. `

const stories = {
  67: {
    title: '咘咘和夜晚的圣索菲亚', title_en: 'Bubu and Saint Sophia at Night',
    texts: [
      ['封面：夜晚的圣索菲亚教堂灯光亮起；咘咘站在最前面，爸爸妈妈、爷爷奶奶、外公外婆温暖地围在身边。','Cover: The lights of Saint Sophia Cathedral glow at night. Bubu stands in front while Dad, Mom, Grandpa, Grandma, Maternal Grandpa, and Maternal Grandma gather warmly around her.'],
      ['今天，咘咘要飞到很远很远的哈尔滨。','Today, Bubu is flying far, far away to Harbin.'],
      ['飞机飞进云朵里，咘咘从小窗户看见软软的白云。','The airplane flies into the clouds, and Bubu sees soft white clouds through the little window.'],
      ['“我们到哈尔滨啦！”爸爸开心地说。','“We are in Harbin!” Dad says happily.'],
      ['北方的空气凉凉的。咘咘穿着厚厚的衣服，还是觉得有一点冷。','The northern air feels cool. Bubu wears warm clothes, but she still feels a little chilly.'],
      ['妈妈牵住咘咘的小手，爷爷奶奶和外公外婆也走在身边。','Mom holds Bubu’s little hand, while Grandpa, Grandma, Maternal Grandpa, and Maternal Grandma walk beside them.'],
      ['晚上，大家来到一座特别特别漂亮的大教堂前。','That evening, everyone comes to a very, very beautiful cathedral.'],
      ['圆圆的大屋顶像一颗大洋葱，绿色的小尖顶高高地指向天空。','The round roof looks like a great onion, and little green spires point high into the sky.'],
      ['“这是圣索菲亚教堂。”爸爸轻轻告诉咘咘。','“This is Saint Sophia Cathedral,” Dad tells Bubu softly.'],
      ['夜幕慢慢落下，大教堂的灯一盏一盏亮起来。','Night slowly falls, and the cathedral lights turn on one by one.'],
      ['金色的灯光照着圆圆的屋顶，也照亮了咘咘亮晶晶的眼睛。','Golden light shines on the round roof and lights up Bubu’s sparkling eyes.'],
      ['咘咘抬起头，好想把这座漂亮的大教堂看个够。','Bubu looks up. She wants to admire the beautiful cathedral forever.'],
      ['爸爸妈妈、爷爷奶奶、外公外婆陪她在广场上慢慢走、慢慢看。','Dad, Mom, Grandpa, Grandma, Maternal Grandpa, and Maternal Grandma walk slowly with her through the square and look around.'],
      ['咘咘说：“圣索菲亚教堂晚上像一座发光的城堡！”','Bubu says, “Saint Sophia Cathedral looks like a glowing castle at night!”'],
      ['大家一起拍下第一张哈尔滨全家福。','Everyone takes their first Harbin family photo together.'],
      ['看完教堂，一家人来到新的酒店。','After seeing the cathedral, the family arrives at their new hotel.'],
      ['新房间有软软的大床。咘咘钻进暖暖的被窝，觉得一点也不冷了。','The new room has a soft big bed. Bubu snuggles into the warm covers and does not feel cold at all.'],
      ['晚安，亮闪闪的圣索菲亚。晚安，哈尔滨的第一夜。','Good night, shining Saint Sophia. Good night, Harbin’s first evening.']
    ],
    scenes: [
      'COVER COMPOSITION: Bubu in the foremost center, warmly surrounded by her six family members. Behind them is the real Harbin Saint Sophia Cathedral at night: deep-red brick facade, central green onion dome and surrounding green spires and domes, all glowing under warm golden architectural illumination; cinematic family travel poster composition.',
      'Inside a bright airplane boarding area, Bubu looks excited before a flight to Harbin, with her six family members nearby and an airplane visible through the large windows.',
      'Inside an airplane cabin, Bubu sits at the window and gazes at soft white clouds outside; calm travel moment.',
      'At the Harbin airport arrival hall, Dad joyfully welcomes Bubu while the whole family stands together with small travel bags.',
      'A calm cool-city arrival scene. Bubu, Dad, and Mom walk together on a clean city sidewalk beneath a pale sky. Bubu wears a warm outer coat over her pink dress; the weather simply looks cool and calm. No airport, no signs, no crowds.',
      'On a Harbin street, Mom holds Bubu’s hand while both pairs of grandparents walk close beside them; cool-air family stroll.',
      'At evening, the whole family arrives before the real Saint Sophia Cathedral, carefully accurate deep red brick facade, green onion dome, green spires; the family looks up in wonder.',
      'A grand upward view of the real Saint Sophia Cathedral’s round central green onion dome and surrounding tall green spires against the evening sky, Bubu and family small in the foreground looking up.',
      'Dad gently points out the real Saint Sophia Cathedral to Bubu, all family gathered at the cathedral square; accurate red-brick, green-dome landmark.',
      'Twilight at Saint Sophia Cathedral: warm golden lights begin to illuminate its accurate red-brick walls, central green onion dome, and green spires; family watches peacefully.',
      'Close portrait of Bubu’s sparkling brown eyes catching warm golden reflection, with the accurate glowing green onion dome of Saint Sophia Cathedral behind her.',
      'Bubu looks high up at Saint Sophia Cathedral in delighted wonder, accurate red-brick architecture and green onion dome prominent in the nighttime composition.',
      'The entire family walks slowly together in the cathedral square at night, warmly lit, the accurate Saint Sophia Cathedral behind them.',
      'Bubu joyfully gestures toward the glowing Saint Sophia Cathedral as if calling it a shining castle; keep the building accurate as a real cathedral, not a fantasy castle.',
      'A warm posed first Harbin family portrait: Bubu front center, six family members around her, Saint Sophia Cathedral’s accurate illuminated red brick and green dome behind them.',
      'The family arrives at the entrance lobby of a cozy new Harbin hotel after their cathedral visit; small travel bags, warm amber indoor light.',
      'In a hotel room, Bubu in her pink dress and warm nighttime bedding snuggles beneath a soft big blanket; parents at bedside, peaceful cozy atmosphere.',
      'A quiet hotel-room bedtime scene: Bubu sleeps warmly in the big bed, while through the window a distant small, accurate warm-lit silhouette of Saint Sophia Cathedral glimmers in Harbin night.'
    ],
    tags: ['哈尔滨','旅行','圣索菲亚教堂','家人','夜景','秋天']
  },
  68: {
    title: '咘咘的马迭尔冰棍和金色老江桥', title_en: 'Bubu’s Favorite Ice Cream and the Golden Old River Bridge',
    texts: [
      ['封面：咘咘拿着马迭尔冰棍，在金色夕阳中的老江桥上开心跑；爸爸妈妈、爷爷奶奶、外公外婆在旁边笑着陪她，鸥鸟飞过松花江。','Cover: Bubu happily runs on the old river bridge in golden sunset light, holding a Madieer ice cream bar. Dad, Mom, Grandpa, Grandma, Maternal Grandpa, and Maternal Grandma smile alongside her while gulls fly over the Songhua River.'],
      ['今天，咘咘和全家来到热热闹闹的中央大街。','Today, Bubu and her whole family come to lively Central Street.'],
      ['街上有漂亮的老房子，还有好多好多好吃的香味。','The street has beautiful old buildings and so many delicious smells.'],
      ['爸爸停在一个小店前：“咘咘，今天有你最喜欢的马迭尔冰棍。”','Dad stops in front of a little shop. “Bubu, today they have your favorite Madieer ice cream bar.”'],
      ['咘咘接过冰棍，开心得眼睛弯成了小月亮。','Bubu takes the ice cream bar, and her happy eyes curve like little moons.'],
      ['她舔一小口——凉凉的、甜甜的，真好吃！','She licks a little bite—cool, sweet, and so delicious!'],
      ['咘咘又舔一小口，爸爸妈妈、爷爷奶奶、外公外婆都笑了。','Bubu takes another little lick, and Dad, Mom, Grandpa, Grandma, Maternal Grandpa, and Maternal Grandma all smile.'],
      ['吃完最喜欢的冰棍，大家慢慢走向宽宽的松花江。','After finishing her favorite ice cream bar, everyone slowly walks toward the broad Songhua River.'],
      ['天空飞来好多白白的鸥鸟，在江面上张开翅膀转呀转。','Many white gulls fly into the sky, spreading their wings and circling over the river.'],
      ['咘咘安静地看着鸥鸟，不追它们，也不喂它们零食。','Bubu watches the gulls quietly. She does not chase them or feed them snacks.'],
      ['前面是一座长长的老桥——哈尔滨铁路桥，也叫老江桥。','Ahead is a long old bridge—the Harbin Railway Bridge, also called the Old River Bridge.'],
      ['爸爸说：“它以前通火车，现在是一座能散步看风景的观光桥。”','Dad says, “It used to carry trains. Now it is a sightseeing bridge where people can walk and enjoy the view.”'],
      ['桥上有旧旧的铁轨和高高的钢梁，脚下是宽宽的松花江。','On the bridge are old rails and high steel beams, with the wide Songhua River below.'],
      ['咘咘一下子跑起来！她在老江桥上跑呀跑，开心得像一只小白兔。','Bubu suddenly starts running! She runs and runs across the Old River Bridge, happy like a little white rabbit.'],
      ['爸爸妈妈、爷爷奶奶、外公外婆在旁边跟着她，笑着提醒：“慢一点，注意脚下。”','Dad, Mom, Grandpa, Grandma, Maternal Grandpa, and Maternal Grandma follow beside her, smiling as they remind her, “Slow down and watch your step.”'],
      ['太阳一点一点落下去，天空和松花江都变成金色。','The sun slowly goes down, turning both the sky and the Songhua River golden.'],
      ['咘咘停下来，靠在爸爸妈妈身边看夕阳：“今天有我最喜欢的冰棍，还有最漂亮的夕阳！”','Bubu stops and leans against Dad and Mom to watch the sunset. “Today had my favorite ice cream bar and the most beautiful sunset!”'],
      ['金色的老江桥、飞翔的鸥鸟和一家人的笑声，陪咘咘一起回到酒店。','The golden Old River Bridge, flying gulls, and the family’s laughter go with Bubu back to the hotel.']
    ],
    scenes: [
      'COVER COMPOSITION: Bubu runs joyfully on the real Binzhou Railway Bridge, holding a plain white milk-flavored Madieer ice cream bar with no words or logo. Golden sunset, six family members smiling beside her, white-and-grey gulls flying over the Songhua River. Show accurate steel trusses and old railway tracks; no train.',
      'The entire family arrives at lively Harbin Central Street, a broad pedestrian street lined with accurate European-style historical buildings.',
      'Bubu and family stroll among beautiful European-style historic facades on Harbin Central Street, savoring a lively food-street atmosphere with no readable signs.',
      'Dad stops at a small Central Street shop and happily presents Bubu with a plain white milk ice-cream bar, no logo and no text; family gathers nearby.',
      'Close warm portrait: Bubu holds the plain white milk ice-cream bar and smiles with crescent-shaped eyes; Central Street is softly blurred behind.',
      'Bubu carefully takes one tiny lick from the plain white ice cream bar, an adorable cool-and-sweet expression; no logo, no text.',
      'Bubu takes another small lick as Dad, Mom and all four grandparents smile warmly around her on Central Street.',
      'After the ice cream, the family walks from Central Street toward the broad Songhua River, seen ahead in cool September daylight.',
      'Many white-and-grey gulls spread their wings and circle gracefully over the broad Songhua River; Bubu and family look upward from the riverbank.',
      'Bubu stands quietly by the riverbank watching the gulls from a respectful distance, hands to herself, not chasing and not feeding them; family nearby.',
      'A clear establishing view ahead of the long real Binzhou Railway Bridge (Harbin Railway Bridge / Old River Bridge): pedestrian sightseeing bridge, steel trusses and old rails, no running train; family approaches.',
      'Dad explains the bridge’s history while the family stands near the real Binzhou Railway Bridge, showing its steel trusses and old tracks, designed for walking visitors, no train.',
      'The family walks on the real Binzhou Railway Bridge: old railway tracks underfoot, towering steel truss beams, broad Songhua River below; no train.',
      'Bubu runs happily but safely along the wide pedestrian portion of the real Old River Bridge, her pink dress moving, family visible close behind; accurate steel trusses and old tracks, no train.',
      'Dad, Mom, both grandparents pairs follow beside Bubu on the bridge, smiling and gently reminding her to slow down; safe spacing, accurate steel trusses and old rails.',
      'Wide golden-hour scene on the real Binzhou Railway Bridge: sun descending, sky and Songhua River glowing gold, gulls in the distance, no train.',
      'Bubu leans warmly against Dad and Mom on the old bridge, watching the glowing sunset over the Songhua River; family nearby, steel truss bridge accurate, no train.',
      'At golden dusk, the family walks back toward their hotel together, with the golden Old River Bridge behind them and white-and-grey gulls flying over the Songhua River.'
    ],
    tags: ['哈尔滨','中央大街','马迭尔冰棍','老江桥','松花江','家人','秋天']
  }
}

for (const [id, story] of Object.entries(stories)) {
  const dir = path.join(root, 'public/images', `story${id}`)
  const auditDir = path.join(root, 'generation', `story${id}`)
  const pages = story.texts.map(([text, text_en], i) => ({ text, text_en, image: `images/story${id}/page-${String(i + 1).padStart(2, '0')}.jpg` }))
  const json = { title: story.title, title_en: story.title_en, pages }
  fs.writeFileSync(path.join(root, 'stories', `story${id}.json`), JSON.stringify(json, null, 2) + '\n')
  fs.writeFileSync(path.join(root, 'public/stories', `story${id}.json`), JSON.stringify(json, null, 2) + '\n')
  const prompts = story.scenes.map((scene, i) => ({ page: i + 1, prompt: `${art}${cast}\n\nSCENE: ${scene}` }))
  fs.writeFileSync(path.join(auditDir, 'prompts.json'), JSON.stringify(prompts, null, 2) + '\n')
  for (const { page, prompt } of prompts) {
    const no = String(page).padStart(2, '0')
    const promptFile = path.join(auditDir, `page-${no}.txt`)
    const png = path.join(dir, `page-${no}.png`)
    const jpg = path.join(dir, `page-${no}.jpg`)
    fs.writeFileSync(promptFile, prompt + '\n')
    if (only.length && !only.some(target => target.story === Number(id) && target.page === page)) continue
    if (fs.existsSync(jpg) || fs.existsSync(png)) {
      console.log(`SKIPPED story${id}/page-${no}: an output already exists; nothing overwritten.`)
      continue
    }
    const result = spawnSync(node, ['--use-env-proxy', tool, 'generate', '--variant', 'sunburst', '--prompt-file', promptFile, '--output', png, '--size', '1024x1536', '--quality', 'medium'], { cwd: root, encoding: 'utf8', timeout: 300000 })
    process.stdout.write(`story${id} page-${no} image-tool stdout: ${result.stdout || ''}`)
    process.stderr.write(`story${id} page-${no} image-tool stderr: ${result.stderr || ''}`)
    if (result.status !== 0 || !fs.existsSync(png)) throw new Error(`Image generation failed/unknown for story${id} page-${no}; output retained if present, no retry attempted.`)
    const convert = spawnSync('sips', ['-s', 'format', 'jpeg', '-s', 'formatOptions', '85', png, '--out', jpg], { encoding: 'utf8' })
    if (convert.status !== 0 || !fs.existsSync(jpg)) throw new Error(`JPEG conversion failed for story${id} page-${no}: ${convert.stderr}`)
    const probe = spawnSync('sips', ['-g', 'pixelWidth', '-g', 'pixelHeight', jpg], { encoding: 'utf8' })
    if (probe.status !== 0 || !/pixelWidth: 1024/.test(probe.stdout) || !/pixelHeight: 1536/.test(probe.stdout)) throw new Error(`Dimension check failed for story${id} page-${no}: ${probe.stdout}`)
    fs.unlinkSync(png)
    console.log(`VERIFIED story${id}/page-${no}.jpg ${fs.statSync(jpg).size} bytes; ${probe.stdout.trim().replace(/\n/g, ', ')}`)
  }
}
