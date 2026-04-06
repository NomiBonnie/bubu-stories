# 咘咘绘本 · 新故事创建规范 (STORY-CHECKLIST.md)

> **⛔ 创建新故事的 sub-agent 必须首先读这个文件，按规范执行。**
> **主 session spawn sub-agent 时，task 第一行必须写：`先读 bubu-stories/STORY-CHECKLIST.md`**

---

## 1. 必读文件（按顺序）

1. **本文件** `STORY-CHECKLIST.md` — 创建规范
2. **`CHARACTER-BIBLE.md`** — 角色外观（每张图 prompt 必须内联完整描述）
3. **`stories/index.json`** — 看最新的 story 编号和完整字段格式

## 2. 图片命名规范

代码来自 `src/StoryReader.jsx` 的 `imgUrl` 函数：
```js
return `${BASE}images/${id}/page-${String(pageNum).padStart(2, '0')}.jpg`
```

**所以图片必须命名为：**
- `page-01.jpg`, `page-02.jpg`, ... `page-12.jpg`
- ✅ 连字符 + 两位数补零
- ❌ `page1.jpg`（错！）
- ❌ `page_01.jpg`（错！）

## 3. index.json 必填字段

每个新故事在 `stories/index.json` 和 `public/stories/index.json` 中的 entry 必须包含**所有**以下字段：

```json
{
  "id": "storyN",
  "title": "故事标题",
  "chapter": N,
  "pages": 页数,
  "cover": "page-XX",
  "tags": ["标签1", "标签2", "标签3"]
}
```

- `chapter`: 整数，递增（看现有最大值 +1）
- `pages`: 整数，总页数（含封面）
- `cover`: 选一张好看的图做封面，格式 `page-XX`（不含 .jpg 后缀）
- `tags`: 3-4 个标签

**新 entry 插入数组开头。**

## 4. story JSON 格式

`stories/storyN.json` 和 `public/stories/storyN.json`（两份完全一样）：

```json
{
  "title": "故事标题",
  "pages": [
    {
      "text": "封面标题（第1页只有标题）",
      "image": "images/storyN/page-01.jpg"
    },
    {
      "text": "第二页文字内容",
      "image": "images/storyN/page-02.jpg"
    }
  ]
}
```

- image 路径**不加前导斜杠**：`images/storyN/page-01.jpg`（不是 `/images/...`）
- 第 1 页是封面（只有标题文字）

## 5. App.jsx 注册

在 `src/App.jsx` 中：
1. 添加 `import storyN from '../stories/storyN.json'`
2. 在 `storyMap` 对象中添加 `'storyN': storyN`

## 6. 图片生成规范

- **尺寸**: 1024x1536（竖版）
- **quality**: medium
- **画风**: `Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition`
- **prompt 语言**: 英文（中文会导致 GPT-image 文字渲染乱码）
- **季节服装**: 根据当月确定季节（详见 CHARACTER-BIBLE.md 季节规则）
- **每张图 prompt 必须内联角色完整外观描述**

## 7. 图片压缩

```bash
mkdir -p public/images/storyN
for i in $(seq 1 N); do
  num=$(printf "%02d" $i)
  ffmpeg -i /tmp/storyN-raw-$i.png -q:v 4 public/images/storyN/page-$num.jpg -y
done
```

## 8. 部署（双端！）

```bash
# 1. Cloudflare 先
CF_PAGES=1 npm run build
CLOUDFLARE_API_TOKEN=$(cat ~/.config/cloudflare/config.json | python3 -c "import sys,json;print(json.load(sys.stdin)['api_token'])") npx wrangler pages deploy dist --project-name bubu-stories --commit-dirty=true

# 2. GitHub Pages 后
npm run build
npx gh-pages -d dist

# 3. Git
git add -A && git commit -m "Add Story N: 标题" && git push origin main
```

## 9. 验证（sub-agent 也要做）

部署后用浏览器验证：
1. 打开首页 → 确认新故事卡片有 **Chapter 编号**、**封面图片**、**tags**
2. 点进故事 → 确认第 1 页图片加载正常
3. 翻到最后一页 → 确认总页数正确

**只有验证通过才能报告"完成"。**

---

*创建于 2026-04-05 | Story 15 踩坑教训*
