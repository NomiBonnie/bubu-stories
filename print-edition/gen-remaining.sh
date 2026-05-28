#!/bin/bash
set -e

API_ENDPOINT="https://kaixi-mmimphd8-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-image-2/images/generations"
API_KEY="G0XzcVpk6KUGX53HbGfW6nBFiU4yh4Wjfowo8BSseYoSL8HAL9E4JQQJ99CCACHYHv6XJ3w3AAAAACOGJIkM"
API_VERSION="2025-04-01-preview"

BUBU='a cute snow-white rabbit girl (Bubu) with exactly TWO long floppy ears with pink insides, big round brown eyes, tiny pink nose. She wears a pink dress with a pink bow. She has a small pink bow centered ON TOP OF HER HEAD between her two ears (not on left ear, not on right ear, not behind — exactly centered on top between the ears). She has a toddler-like round body proportion.'

SAM_DAD='Sam Dad who is a GOLDEN RETRIEVER DOG (NOT a human, NOT a person — he is an ANIMAL, a large golden-furred dog walking upright). He has warm golden fur all over his body, a dog snout/muzzle, floppy dog ears, and a wagging tail. He wears a dark navy jacket over a simple shirt. He has a warm gentle dog smile. IMPORTANT: Sam Dad must look like a golden retriever dog, not a human man.'

TINA_MOM='Tina Mom who is a BLACK-AND-WHITE COW (NOT a human, NOT a person — she is an ANIMAL, a cow walking upright). She has black and white spotted fur pattern all over, small curved horns, cow ears, and hooves. She wears an elegant cream knit cardigan over a floral skirt. She has a gentle warm cow smile. IMPORTANT: Tina Mom must look like a cow, not a human woman.'

NOMI='a raccoon (NOMI) with grey-brown fur, distinctive black eye mask markings, and a ringed bushy tail. She wears a blue-and-white horizontally striped sweater. She has clever bright eyes and nimble paws.'

NONO='a small red bird (NONO) with bright red feathers all over, round bright eyes, and an orange-yellow beak. He has exactly TWO wings and TWO small bird feet with talons. NO ARMS, NO HANDS — birds do not have arms or hands, only wings.'

DOUDOU='a small hedgehog (Doudou) with a brown body covered in dark brown spines/quills, small round shiny eyes, a tiny nose. He is small, round, and shy-looking.'

MANMAN='a small turtle (Manman) with a green shell with dark green hexagonal patterns, light green skin, small round eyes, and a gentle slow expression.'

generate_image() {
    local prompt="$1"
    local output_dir="$2"
    local page_name="$3"
    local png_path="/tmp/bubu_${page_name}.png"
    local jpg_path="${output_dir}/${page_name}.jpg"

    mkdir -p "$output_dir"

    local retries=0
    while [ $retries -lt 3 ]; do
        echo ">>> Generating ${output_dir}/${page_name} (attempt $((retries+1)))..."
        
        local response
        response=$(curl -s -w "\n%{http_code}" -X POST \
            "${API_ENDPOINT}?api-version=${API_VERSION}" \
            -H "Content-Type: application/json" \
            -H "api-key: ${API_KEY}" \
            -d "$(python3 -c "
import json
print(json.dumps({
    'prompt': '''$prompt''',
    'size': '1024x1536',
    'quality': 'medium',
    'n': 1,
    'output_format': 'png'
}))
")" 2>/dev/null)

        local http_code=$(echo "$response" | tail -1)
        local body=$(echo "$response" | sed '$d')

        if [ "$http_code" = "429" ]; then
            echo "Rate limited (429), waiting 45s..."
            retries=$((retries+1))
            sleep 45
            continue
        fi

        if [ "$http_code" != "200" ]; then
            echo "Error $http_code: $body"
            retries=$((retries+1))
            sleep 10
            continue
        fi

        # Extract base64 data
        local b64=$(echo "$body" | python3 -c "import sys,json; print(json.load(sys.stdin)['data'][0]['b64_json'])")
        if [ -z "$b64" ]; then
            echo "No b64 data found"
            retries=$((retries+1))
            sleep 10
            continue
        fi

        echo "$b64" | base64 -d > "$png_path"
        ffmpeg -y -i "$png_path" -q:v 2 "$jpg_path" 2>/dev/null
        rm -f "$png_path"
        
        local size=$(stat -f%z "$jpg_path" 2>/dev/null || stat -c%s "$jpg_path" 2>/dev/null)
        echo "✅ ${page_name}.jpg — ${size} bytes"
        return 0
    done
    
    echo "❌ FAILED ${page_name} after 3 retries"
    return 1
}

# Story 3 P10-P14
S3_DIR="bubu-stories/print-edition/story3"

echo "=== Story 3: P10-P14 ==="

generate_image "Pixar 3D animation style, warm golden afternoon sunlight, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: A park sandpit. Bubu and Doudou the hedgehog are building a sandcastle together. Bubu uses a small shovel to scoop sand while Doudou pats the sand with his little paws. Their new sandcastle is big and beautiful, even bigger than before. They are happy and cooperating. CHARACTERS: ${BUBU}. ${DOUDOU}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S3_DIR" "page-10"
sleep 8

generate_image "Pixar 3D animation style, warm afternoon sunlight, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: A park sandpit with a big beautiful sandcastle. NOMI the raccoon arrives carrying a small water bucket, and NONO the red bird flies in carrying a tiny flag in his beak to place on top of the sandcastle. Bubu and Doudou watch happily. CHARACTERS: ${BUBU}. ${DOUDOU}. ${NOMI}. ${NONO}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S3_DIR" "page-11"
sleep 8

generate_image "Pixar 3D animation style, warm golden sunlight, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: A park with a beautiful sandcastle in the sandpit. Tina Mom stands nearby watching the children with a warm smile. Bubu, Doudou, NOMI and NONO are around the sandcastle looking happy. CHARACTERS: ${TINA_MOM}. ${BUBU}. ${DOUDOU}. ${NOMI}. ${NONO}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S3_DIR" "page-12"
sleep 8

generate_image "Pixar 3D animation style, warm sunset light, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: A park path at sunset. Bubu the rabbit is walking and gently holding Doudou the hedgehog's paw — carefully holding the soft palm side without spines. They walk side by side, looking at each other happily. Trees line the path with golden sunset light. CHARACTERS: ${BUBU}. ${DOUDOU}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S3_DIR" "page-13"
sleep 8

generate_image "Pixar 3D animation style, soft warm glowing light, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: A cheerful summary scene. Bubu stands happily in the center with a big smile. Around her are visual elements suggesting friendship — a sandcastle, a small shovel, and sparkles. The mood is warm, uplifting and encouraging. CHARACTERS: ${BUBU}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S3_DIR" "page-14"
sleep 8

# Story 4 P2-P16
S4_DIR="bubu-stories/print-edition/story4"

echo ""
echo "=== Story 4: P2-P16 ==="

generate_image "Pixar 3D animation style, bright sunny morning light, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: A beautiful riverbank with sandy shore. Bubu and Manman the turtle are playing in the sand. Manman is slowly and carefully building a beautiful sandcastle. The river sparkles in the background. CHARACTERS: ${BUBU}. ${MANMAN}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S4_DIR" "page-02"
sleep 8

generate_image "Pixar 3D animation style, bright sunny light, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: Riverbank sandy area. Bubu watches Manman's beautiful sandcastle admiringly, then tries to build her own bigger one next to it. Bubu's castle keeps falling apart as she piles sand. She looks determined but a bit frustrated. Manman's castle stands pretty nearby. CHARACTERS: ${BUBU}. ${MANMAN}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S4_DIR" "page-03"
sleep 8

generate_image "Pixar 3D animation style, bright daylight, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: Riverbank. A dramatic moment — Bubu has accidentally bumped into Manman's sandcastle and it collapses into a pile of sand. Sand particles fly. Bubu looks shocked with wide eyes and her paws up. Manman's castle is now a pile of rubble. CHARACTERS: ${BUBU}. ${MANMAN}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S4_DIR" "page-04"
sleep 8

generate_image "Pixar 3D animation style, soft diffused light, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: Riverbank with a destroyed sandcastle now just a pile of sand. Manman the turtle sits next to the pile, crying with tears streaming down, looking devastated. Bubu stands nearby looking guilty and sad. CHARACTERS: ${BUBU}. ${MANMAN}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S4_DIR" "page-05"
sleep 8

generate_image "Pixar 3D animation style, dim indoor light, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: Inside Bubu's cozy bedroom. Bubu sits on her bed hugging her knees, looking sad and troubled. The room has soft warm colors, some toys around, and a window showing daylight outside. She feels guilty but doesn't know what to do. CHARACTERS: ${BUBU}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S4_DIR" "page-06"
sleep 8

generate_image "Pixar 3D animation style, warm soft indoor light, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: Inside Bubu's bedroom. Sam Dad sits on the bed next to Bubu, who looks sad. Sam Dad has a gentle comforting expression, looking at Bubu warmly. He leans in slightly to listen to her. CHARACTERS: ${BUBU}. ${SAM_DAD}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S4_DIR" "page-07"
sleep 8

generate_image "Pixar 3D animation style, warm indoor light, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: Inside the bedroom. Close-up conversation between Sam Dad and Bubu. Sam Dad speaks gently with a wise expression. Bubu looks thoughtful with a hand on her chin, starting to understand. The mood is intimate and reflective. CHARACTERS: ${BUBU}. ${SAM_DAD}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S4_DIR" "page-08"
sleep 8

generate_image "Pixar 3D animation style, warm kitchen light, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: A cozy kitchen. Tina Mom stands by a counter with a tray of freshly baked cookies, offering them to Bubu with a warm encouraging smile. The kitchen smells delicious with steam rising from the cookies. Bubu looks up at her mom with a hopeful expression. CHARACTERS: ${BUBU}. ${TINA_MOM}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S4_DIR" "page-09"
sleep 8

generate_image "Pixar 3D animation style, warm afternoon light, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: Back at the riverbank. Bubu walks up to Manman carrying a plate of cookies. Manman is quietly rebuilding her sandcastle alone. Bubu approaches with a sincere, apologetic expression, offering the cookies. CHARACTERS: ${BUBU}. ${MANMAN}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S4_DIR" "page-10"
sleep 8

generate_image "Pixar 3D animation style, soft afternoon light, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: Riverbank close-up. Bubu kneels down and places cookies in front of Manman. Manman looks up from rebuilding, expression still a bit hurt but curious about the cookies. The cookies look delicious on a small plate between them. CHARACTERS: ${BUBU}. ${MANMAN}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S4_DIR" "page-11"
sleep 8

generate_image "Pixar 3D animation style, warm golden light, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: Riverbank. Manman looks at the cookies, then at Bubu, and slowly smiles. Manman starts to forgive. Both characters face each other with warm expressions. A half-rebuilt sandcastle is between them. CHARACTERS: ${BUBU}. ${MANMAN}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S4_DIR" "page-12"
sleep 8

generate_image "Pixar 3D animation style, bright happy afternoon light, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: Riverbank with a magnificent completed sandcastle, bigger and more beautiful than before. Bubu and Manman stand proudly next to it. NOMI the raccoon passes by and looks amazed at the castle. Everyone is happy and proud. CHARACTERS: ${BUBU}. ${MANMAN}. ${NOMI}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S4_DIR" "page-13"
sleep 8

generate_image "Pixar 3D animation style, bright joyful light, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: Riverbank with the grand sandcastle. Bubu and Manman laugh together happily. NONO the red bird flies down and plants a tiny flag on top of the castle with his beak. Everyone celebrates. CHARACTERS: ${BUBU}. ${MANMAN}. ${NONO}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S4_DIR" "page-14"
sleep 8

generate_image "Pixar 3D animation style, warm sunset golden hour light, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: A path along the river at sunset. Sam Dad walks with Bubu, holding her paw gently. They walk together in warm golden light. Bubu looks up at Sam Dad with a happy, proud expression. Trees and warm sunset colors in the background. CHARACTERS: ${BUBU}. ${SAM_DAD}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S4_DIR" "page-15"
sleep 8

generate_image "Pixar 3D animation style, soft warm glowing light, children's picture book illustration, vertical portrait 1024x1536. No text anywhere in the image. SCENE: A cheerful summary scene. Bubu stands in the center with a warm confident smile. Around her are visual elements suggesting apology and friendship — a rebuilt sandcastle, cookies, and sparkles. The mood is warm, encouraging, and uplifting. CHARACTERS: ${BUBU}. The composition naturally centers characters in the middle of the frame. The bottom 20% should be slightly darker as a natural gradient. Professional children's picture book quality." "$S4_DIR" "page-16"

echo ""
echo "=== ALL DONE ==="
echo ""
echo "File sizes:"
ls -la bubu-stories/print-edition/story3/page-1*.jpg 2>/dev/null
ls -la bubu-stories/print-edition/story4/page-*.jpg 2>/dev/null
