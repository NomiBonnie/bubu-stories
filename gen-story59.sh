#!/bin/bash
set -e

ENDPOINT="https://kaixi-mmimphd8-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-image-2/images/generations"
API_KEY="G0XzcVpk6KUGX53HbGfW6nBFiU4yh4Wjfowo8BSseYoSL8HAL9E4JQQJ99CCACHYHv6XJ3w3AAAAACOGJIkM"
API_VERSION="2025-04-01-preview"
OUTDIR="/Users/samyuan/.openclaw/workspace/bubu-stories/public/images/story59"
mkdir -p "$OUTDIR"

STYLE_PREFIX="Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition 1024x1536."

# Character descriptions
BUBU="a small white rabbit toddler (snow-white fur, exactly two long ears with pink insides, big round brown eyes, small pink nose, wearing a pink dress with a pink bow on top of her head centered between her two ears)"
NOMI="a raccoon (grey-brown fur with black eye mask markings and ringed tail, big round clever eyes, wearing a blue-and-white striped sweater)"
NONO="a small red bird (bright red feathers, round body, round bright little eyes, orange-yellow beak)"
DAD="a golden retriever dog dad (golden fur, big warm build, wearing a casual summer polo shirt, kind gentle smile)"
MOM="a cow mom (black-and-white patches, medium-large build, elegant, wearing a stylish summer dress, gentle patient expression)"
WAIGONG="an elderly horse grandpa (dark brown coat, grey-white mane showing age, deep calm eyes, wearing a polo shirt and casual pants, tall dignified)"
WAIPO="an elderly goat grandma (light grey-white fur, small curved horns, short goatee, warm brown eyes, wearing a floral blouse and light pants, plump warm grandma)"
YEYE="a cute chubby light-green dinosaur grandpa (smooth round body, big round gentle eyes, not scary at all, very cute and round, wearing a polo shirt and casual pants, shorter than dad but stout and sturdy)"
NAINAI="a gentle light-brown monkey grandma (soft short fur, warm peach-colored face, loving big eyes, wearing a Chinese-style floral top, small and nimble)"
GANMA="a tall elegant pink flamingo godmother (classic pink feathers, long pink legs, wearing an elegant summer dress, warm and graceful)"
XIAOQIAO="a young light-pink flamingo girl (lighter pink than her mother, a bit bigger than Bubu, wearing a cute pink dress with a small bow, lively and caring)"
ZHUZHU="a white sheep girl (cloud-like curly white wool, wearing a light blue vest, brown little hooves, pink nose, same size as Bubu)"

generate_image() {
  local page_num=$1
  local prompt=$2
  local outfile="$OUTDIR/page-$(printf '%02d' $page_num).jpg"
  
  if [ -f "$outfile" ]; then
    echo "⏭️ Page $page_num already exists, skipping"
    return
  fi

  echo "🎨 Generating page $page_num..."
  
  # Escape prompt for JSON
  local escaped_prompt=$(python3 -c "import json; print(json.dumps($( python3 -c "import sys; print(repr('$prompt'))" 2>/dev/null || echo "\"$prompt\"" )))" 2>/dev/null)
  
  # Use python to properly handle the prompt
  local response=$(python3 -c "
import json, urllib.request, sys

prompt = sys.stdin.read().strip()
data = json.dumps({
    'prompt': prompt,
    'n': 1,
    'size': '1024x1536',
    'quality': 'medium',
    'output_format': 'png'
}).encode()

req = urllib.request.Request(
    '${ENDPOINT}?api-version=${API_VERSION}',
    data=data,
    headers={
        'Content-Type': 'application/json',
        'api-key': '${API_KEY}'
    }
)

try:
    resp = urllib.request.urlopen(req, timeout=120)
    result = json.loads(resp.read())
    b64 = result['data'][0]['b64_json']
    import base64
    with open('${outfile%.jpg}.png', 'wb') as f:
        f.write(base64.b64decode(b64))
    print('OK')
except Exception as e:
    print(f'ERROR: {e}', file=sys.stderr)
    sys.exit(1)
" <<< "$prompt")

  if [ -f "${outfile%.jpg}.png" ]; then
    # Convert PNG to JPG
    ffmpeg -y -i "${outfile%.jpg}.png" -q:v 4 "$outfile" 2>/dev/null
    rm "${outfile%.jpg}.png"
    local size=$(stat -f%z "$outfile" 2>/dev/null || stat -c%s "$outfile" 2>/dev/null)
    echo "✅ Page $page_num done ($(( size / 1024 ))KB)"
  else
    echo "❌ Page $page_num FAILED"
    return 1
  fi
}

# Page 01 - Cover (movie poster style)
P01="Pixar 3D animation style, cinematic children's picture book cover poster, warm golden lighting, vertical portrait 1024x1536. TOP: Large elegant 3D golden embossed letters spelling \"Bubu's Third Birthday\" with small stars and hearts around the letters, like a Disney movie poster title. CENTER: ${BUBU} — she stands in the center wearing a birthday crown, arms raised joyfully, surrounded by colorful balloons and confetti. Behind her: ${DAD} and ${MOM} on either side. To the left: ${YEYE} and ${NAINAI}. To the right: ${WAIGONG} and ${WAIPO}. LOWER: ${GANMA} and ${XIAOQIAO} on one side, ${ZHUZHU} on the other. BOTTOM CORNER: ${NOMI} and ${NONO} sitting together. BACKGROUND: A festive living room with birthday decorations, streamers, a big blue trampoline visible, and a pink birthday cake with 3 candles. Rich layered movie poster depth composition with bokeh."

# Page 02 - Morning surprise
P02="${STYLE_PREFIX} ${BUBU} sitting up in her bed, eyes wide with wonder and excitement, mouth open in a joyful gasp. The bedroom is filled with colorful floating balloons (red, yellow, blue, pink, green) and a rainbow streamer hanging from the doorway. Morning sunlight streams through the window. Summer bedroom setting."

# Page 03 - Parents greeting
P03="${STYLE_PREFIX} In a bright festive living room decorated with balloons and streamers. ${MOM} is lifting ${BUBU} up and spinning her around, both laughing joyfully. ${DAD} stands beside them, one paw reaching out to rub Bubu's ear, smiling warmly. Summer morning light."

# Page 04 - Yeye and Nainai arrive
P04="${STYLE_PREFIX} At the front door of the house. ${YEYE} is crouching down at the doorway, reaching his short dinosaur arms toward ${BUBU} who stands looking up with curious big eyes. ${NAINAI} stands beside Yeye, eyes full of love, smiling warmly. ${DAD} stands behind Bubu. The doorway is decorated with birthday balloons."

# Page 05 - Yeye holds Bubu
P05="${STYLE_PREFIX} ${YEYE} holding ${BUBU} in his short but sturdy dinosaur arms, hugging her tightly, both smiling with eyes closed. ${NAINAI} stands beside them, reaching her nimble monkey hand to pat Bubu's head gently, eyes crinkled with a loving smile. Warm indoor lighting, festive living room background."

# Page 06 - Ganma and Xiaoqiao arrive
P06="${STYLE_PREFIX} At the front door. ${GANMA} standing tall and elegant, ${XIAOQIAO} bouncing excitedly, holding ${BUBU}'s hand. ${MOM} greeting them warmly. Xiaoqiao is leaning toward Bubu with a big smile. Birthday decorations visible in the background. Bright summer daylight from outside."

# Page 07 - Zhuzhu family arrives with cake
P07="${STYLE_PREFIX} ${ZHUZHU} running ahead giving ${BUBU} a big hug, both smiling. Behind them, two adult sheep (Zhuzhu's parents) carry a large cake box. The cake is visible — pink frosted with 3 small candles and a little sugar bunny on top. Festive living room with all the earlier guests visible in the background. ${NOMI} and ${NONO} watching happily."

# Page 08 - Unwrapping trampoline
P08="${STYLE_PREFIX} In the sunny backyard/yard. ${BUBU} standing in front of a newly unwrapped big blue trampoline, eyes perfectly round with shock and joy, mouth in a big O shape. Torn wrapping paper and a big bow on the ground. ${XIAOQIAO} standing beside her excitedly pointing at the trampoline. ${GANMA} watching proudly in the background. Bright summer sunshine."

# Page 09 - Bouncing on trampoline (key scene!)
P09="${STYLE_PREFIX} ${BUBU} and ${XIAOQIAO} holding hands and bouncing high on a big blue trampoline, both laughing with pure joy. Bubu's long white ears are flapping in the air. ${NOMI} standing beside the trampoline clapping. ${NONO} flying in circles around them in the air. Other characters watching and cheering in the background. Bright sunny summer day, dynamic action pose, motion blur on the bounce."

# Page 10 - Fishing rod gift
P10="${STYLE_PREFIX} ${DAD} crouching down presenting a beautiful small fishing rod to ${BUBU}. Bubu is holding the fishing rod up excitedly, waving it around with a huge grin. ${MOM} standing beside them smiling. A long gift box open on the floor. Indoor festive living room. Summer afternoon light."

# Page 11 - Birthday song
P11="${STYLE_PREFIX} A large round dining table with a beautiful pink birthday cake with 3 lit candles in the center, warm candlelight glow. ${BUBU} sitting in the center. Around the table: ${DAD} and ${MOM} on either side of Bubu, ${YEYE} and ${NAINAI}, ${WAIGONG} and ${WAIPO}, ${GANMA} and ${XIAOQIAO}, ${ZHUZHU} and her sheep parents. Everyone is singing with open mouths and happy smiles. ${NOMI} and ${NONO} also present. Warm golden evening indoor lighting."

# Page 12 - Making a wish
P12="${STYLE_PREFIX} Close-up shot. ${BUBU} with eyes closed, hands together in front of her chest, making a birthday wish. Three lit candles on the pink cake in front of her, warm candlelight illuminating her face. A moment of peaceful concentration. Soft bokeh of all the family members watching tenderly in the background."

# Page 13 - Eating cake, grandpa funny
P13="${STYLE_PREFIX} ${BUBU} with pink frosting all over her little mouth, laughing hard. ${YEYE} has a blob of pink cream on his round green dinosaur nose, making a silly face. ${NAINAI} is wiping Yeye's nose with a napkin, laughing. Everyone at the table is laughing. Pink birthday cake partially eaten on the table. Warm joyful atmosphere."

# Page 14 - Family dinner
P14="${STYLE_PREFIX} A big round dinner table full of colorful delicious dishes. ${BUBU} sitting between ${DAD} and ${MOM}. On one side: ${YEYE} and ${NAINAI}. On the other side: ${WAIGONG} and ${WAIPO}. Across: ${GANMA}, ${XIAOQIAO}, ${ZHUZHU} and her sheep parents. ${NOMI} sitting near Bubu, ${NONO} perched on the table edge. Warm indoor evening lighting, everyone eating and chatting happily. A full table of love."

# Page 15 - Guests leaving
P15="${STYLE_PREFIX} At the front door, evening time. ${ZHUZHU} and ${BUBU} doing a pinky promise, both smiling. ${XIAOQIAO} kissing Bubu's forehead. In the background, ${NAINAI} waiting with arms open for one last hug, ${YEYE} standing beside her. ${GANMA} and Zhuzhu's sheep parents also at the door. Warm golden evening light from inside, blue evening sky outside. Bittersweet warm farewell scene."

# Page 16 - Bedtime ending
P16="${STYLE_PREFIX} Cozy bedroom at night, warm dim nightlight. ${BUBU} lying in bed under a soft blanket, eyes half-closed with a small peaceful smile. ${NOMI} sitting on the edge of the bed, holding Bubu's hand gently. ${NONO} perched on the pillow beside Bubu's head. On the nightstand: a small birthday crown and a tiny piece of cake. Moonlight through the window. The blue trampoline and fishing rod visible in the corner of the room. Warm, peaceful, the perfect end to the happiest day."

# Generate all pages
PROMPTS=("$P01" "$P02" "$P03" "$P04" "$P05" "$P06" "$P07" "$P08" "$P09" "$P10" "$P11" "$P12" "$P13" "$P14" "$P15" "$P16")

for i in "${!PROMPTS[@]}"; do
  page=$((i + 1))
  generate_image $page "${PROMPTS[$i]}"
  if [ $page -lt 16 ]; then
    echo "⏳ Waiting 8 seconds..."
    sleep 8
  fi
done

echo ""
echo "🎉 All done! Listing files:"
ls -la "$OUTDIR/"
