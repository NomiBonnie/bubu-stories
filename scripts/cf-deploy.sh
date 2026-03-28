#!/bin/bash
set -e
# Cloudflare Pages 部署
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

CF_TOKEN="$(python3 -c 'import json; print(json.load(open("/Users/samyuan/.config/cloudflare/config.json"))["api_token"])')"
export CLOUDFLARE_API_TOKEN="$CF_TOKEN"
export CLOUDFLARE_ACCOUNT_ID="abd70cd0575e6ebe933999645e6fddd2"
export CF_PAGES=1

npm run build
echo "/* /index.html 200" > dist/_redirects
npx wrangler pages deploy dist --project-name=bubu-stories --commit-dirty=true
echo "✅ Cloudflare Pages 部署完成: https://bubu.sanono.xyz"
