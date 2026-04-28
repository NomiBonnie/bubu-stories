#!/bin/bash
set -e

echo "🚀 Bubu Stories 部署脚本"
echo "========================"

# 1. 检查是否有未提交的更改
if [[ -n $(git status -s) ]]; then
  echo "⚠️  检测到未提交的更改，先提交代码..."
  git add -A
  read -p "提交信息: " commit_msg
  git commit -m "$commit_msg"
  git push
  echo "✅ 代码已提交并推送"
else
  echo "✅ 工作目录干净"
fi

# 2. 构建 Cloudflare 版本（base: /）
echo ""
echo "📦 构建 Cloudflare Pages 版本..."
CF_PAGES=1 npm run build
echo "✅ Cloudflare 版本构建完成"

# 3. 部署到 Cloudflare
echo ""
echo "☁️  部署到 Cloudflare Pages..."
npx wrangler pages deploy dist --project-name=bubu-stories --commit-dirty=true
echo "✅ Cloudflare Pages 部署完成"
echo "   访问: https://bubu.sanono.xyz"

# 4. 构建 GitHub Pages 版本（base: /bubu-stories/）
echo ""
echo "📦 构建 GitHub Pages 版本..."
npm run build
echo "✅ GitHub Pages 版本构建完成"

# 5. 触发 GitHub Actions（自动部署 gh-pages）
echo ""
echo "🔄 触发 GitHub Actions..."
gh workflow run "Deploy to GitHub Pages"
echo "✅ GitHub Actions 已触发"
echo "   访问: https://nomibonnie.github.io/bubu-stories"

echo ""
echo "🎉 部署完成！"
echo "   - Cloudflare: https://bubu.sanono.xyz"
echo "   - GitHub:     https://nomibonnie.github.io/bubu-stories"
