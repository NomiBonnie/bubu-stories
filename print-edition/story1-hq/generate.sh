#!/bin/bash
set -e

ENDPOINT="https://kaixi-mmimphd8-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-image-2/images/generations"
API_KEY="G0XzcVpk6KUGX53HbGfW6nBFiU4yh4Wjfowo8BSseYoSL8HAL9E4JQQJ99CCACHYHv6XJ3w3AAAAACOGJIkM"
API_VERSION="2025-04-01-preview"
OUTDIR="/Users/samyuan/.openclaw/workspace/bubu-stories/print-edition/story1-hq"

BUBU="a snow-white rabbit with long ears with pink insides, big brown eyes, a small pink nose, wearing a pink dress with a pink bow on one ear, toddler proportions, round and cute"
NOMI="a raccoon with grey-brown fur, black eye mask markings, a ring-striped tail, wearing a blue-and-white striped sweater, big clever eyes, sometimes wearing tiny glasses"
NONO="a small red bird with bright red feathers, round bright eyes, and an orange-yellow beak"

STYLE="Pixar 3D animation style, children's picture book illustration, warm soft lighting, vertical portrait composition 1024x1536. IMPORTANT: No text, no letters, no words, no writing anywhere in the image. The bottom 20 percent of the image should be slightly darker and softer (for text overlay later). Keep left 10 percent clear of important content (binding margin). Place characters and key elements in the upper-center and center-right areas."

generate_image() {
  local page_num=$1
  local prompt=$2
  local outfile="$OUTDIR/page-$(printf '%02d' $page_num).png"
  local jpgfile="$OUTDIR/page-$(printf '%02d' $page_num).jpg"
  
  if [ -f "$jpgfile" ]; then
    echo "SKIP page-$(printf '%02d' $page_num).jpg already exists"
    return 0
  fi

  echo "=== Generating page $page_num ==="
  
  local retries=0
  while [ $retries -lt 3 ]; do
    local response
    response=$(curl -s -w "\n%{http_code}" -X POST \
      "${ENDPOINT}?api-version=${API_VERSION}" \
      -H "Content-Type: application/json" \
      -H "api-key: ${API_KEY}" \
      -d "$(jq -n --arg p "$prompt" '{prompt: $p, n: 1, size: "1024x1536", quality: "high", output_format: "png"}')")
    
    local http_code=$(echo "$response" | tail -1)
    local body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "429" ]; then
      retries=$((retries + 1))
      echo "Rate limited (429), waiting 45s... (retry $retries/3)"
      sleep 45
      continue
    elif [ "$http_code" != "200" ]; then
      echo "ERROR page $page_num: HTTP $http_code"
      echo "$body" | head -5
      retries=$((retries + 1))
      sleep 15
      continue
    fi
    
    # Extract base64 image data
    local b64=$(echo "$body" | jq -r '.data[0].b64_json // empty')
    if [ -z "$b64" ]; then
      echo "ERROR: No b64_json in response for page $page_num"
      echo "$body" | head -5
      return 1
    fi
    
    echo "$b64" | base64 -d > "$outfile"
    ffmpeg -y -i "$outfile" -q:v 2 "$jpgfile" 2>/dev/null
    rm -f "$outfile"
    local size=$(ls -la "$jpgfile" | awk '{print $5}')
    echo "OK page-$(printf '%02d' $page_num).jpg — ${size} bytes"
    return 0
  done
  
  echo "FAILED page $page_num after 3 retries"
  return 1
}

# P2
generate_image 2 "A sunny lush green meadow on a beautiful day. ${BUBU} is happily hopping and bouncing across the grass with a joyful expression, long ears flopping. Wildflowers dot the meadow, golden sunlight streams down. ${STYLE}"
sleep 8

# P3
generate_image 3 "${NOMI} sitting under a large leafy tree, looking clever and curious, holding a small magnifying glass, surrounded by books and small inventions. Green meadow background. ${STYLE}"
sleep 8

# P4
generate_image 4 "${NONO} soaring cheerfully through a bright blue sky with fluffy white clouds, wings spread wide, looking happy and brave. Below is a green landscape with rolling hills. ${STYLE}"
sleep 8

# P5
generate_image 5 "Twilight scene on a small grassy hilltop. ${BUBU} sitting on the hill looking up at a big bright full moon in a dusky sky painted in orange, purple and deep blue. Stars beginning to appear. Peaceful and dreamy. ${STYLE}"
sleep 8

# P6
generate_image 6 "Dark night scene. ${BUBU} standing on the hilltop looking up at the sky with a shocked and worried expression, ears drooping slightly. The sky is completely dark with only a few stars — no moon visible at all. Dramatic and slightly mysterious. ${STYLE}"
sleep 8

# P7
generate_image 7 "${BUBU} running urgently through a moonless dark meadow at night, looking worried and anxious, ears streaming behind. A faint treehouse silhouette in the distance. Motion and urgency in the scene. ${STYLE}"
sleep 8

# P8
generate_image 8 "A cozy warm tree hollow interior with a small glowing lamp. ${NOMI} wearing tiny glasses, sitting in a comfy chair reading a book. ${BUBU} standing at the entrance looking worried and pleading for help. Warm golden lamplight contrasts with the dark night outside. ${STYLE}"
sleep 8

# P9
generate_image 9 "${NONO} flying high up in the dark night sky with wings fully spread, searching and scanning the ground below. Far below on the ground, ${BUBU} and ${NOMI} look up watching. Stars twinkle in the sky. ${STYLE}"
sleep 8

# P10
generate_image 10 "${NONO} hovering excitedly above a still pond, pointing down with one wing, looking thrilled. Below, the full moon is perfectly reflected in the calm water surface. Magical glowing atmosphere, night scene. ${STYLE}"
sleep 8

# P11
generate_image 11 "At the edge of a calm pond at night. ${BUBU} and ${NOMI} kneeling together looking down into the water with amazed expressions. A beautiful perfect full moon reflection glows in the crystal clear water. Fireflies float around. Magical and enchanting. ${STYLE}"
sleep 8

# P12
generate_image 12 "${BUBU} reaching one paw into the pond water, causing a big splash. Water droplets flying everywhere, splashing ${NOMI} and ${NONO}. The moon reflection is shattered into shimmering fragments on the water surface. ${BUBU} looks surprised, ${NOMI} and ${NONO} have funny wet expressions. Night scene. ${STYLE}"
sleep 8

# P13
generate_image 13 "${NOMI} with water droplets on face, smiling and pointing up at the sky. ${BUBU} looking up with an amazed wide-eyed expression. Above them, a big beautiful full moon is now clearly visible in the night sky, bathing everything in magical silver moonlight. ${NONO} perched on ${NOMI}'s head. ${STYLE}"
sleep 8

# P14
generate_image 14 "All three friends together under a beautiful full moon — ${BUBU}, ${NOMI}, and ${NONO} — all smiling and laughing with joy. They stand on a grassy meadow bathed in soft moonlight. Warm, heartfelt, celebratory feeling. ${STYLE}"
sleep 8

# P15
generate_image 15 "Split composition: In the upper portion, the three friends (${BUBU}, ${NOMI}, ${NONO}) walking home together hand-in-hand along a moonlit path. In the lower portion, ${BUBU} tucked in a cozy bed with soft blankets, looking sleepily out a window at the full moon, with a warm bedside lamp. Stuffed raccoon and bird toys beside the pillow. Peaceful, dreamy. ${STYLE}"
sleep 8

# P16
generate_image 16 "A warm educational summary scene. ${BUBU}, ${NOMI}, and ${NONO} sitting together on a grassy hill. Above them, a big full moon in the night sky. Below the hill, a calm pond shows the moon's reflection. The three friends look contemplative and happy. Warm pastel colors, thoughtful and gentle mood. ${STYLE}"

echo ""
echo "=== DONE ==="
ls -la "$OUTDIR"/*.jpg 2>/dev/null | awk '{print $NF, $5}'
