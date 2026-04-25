# 咘咘绘本制作完整流程 (Story Production Workflow)

> **铁规：每次创建新故事前，sub-agent 和主 session 都必须读此文件。**
> **不允许跳过任何步骤。**

---

## 📋 整体参数

| 项目 | 值 |
|------|-----|
| 页数 | 12-13 页（含封面，不少于 12 页） |
| 图片尺寸 | 1024×1536（竖版） |
| 图片模型 | gpt-image-2（Poland Central: `gpt-image-2-1`） |
| 图片质量 | medium |
| 输出格式 | PNG → ffmpeg -q:v 4 转 JPG |
| API 限速 | 9 RPM，每张间隔 7 秒 |
| API 配置 | `~/.config/azure-openai/config.json` 中的 `image2_poland_api_key` + `image2_poland_endpoint` |
| API 版本 | `2025-04-01-preview` |

---

## 🔄 制作流程（6 步）

### Step 1: 写故事文本

1. 根据 Sam 的主题要求写故事
2. 12-13 页（Page 01 = 封面，Page 02-13 = 正文）
3. 每页包含：中文文本 (`text`) + 英文文本 (`text_en`)
4. 角色选择：查 `CHARACTER-BIBLE.md`，确认哪些角色出场
5. **英语启蒙元素**：如果有 Coco 出场，融入自然的英文对话
6. **情感节奏**：开头引入 → 中间递进 → 高潮 → 温馨收尾（睡前场景）

### Step 2: 写 JSON 文件

格式必须严格遵守（对照已有故事文件）：

```json
{
  "title": "中文标题",
  "title_en": "English Title",
  "pages": [
    {
      "text": "第一页中文",
      "text_en": "Page 1 English",
      "image": "images/storyXX/page-01.jpg"
    }
  ]
}
```

**注意：**
- **不要加** `id`, `color`, `titleEn` 等额外字段
- 字段名用 `title_en` 和 `text_en`（下划线，不是驼峰）
- `image` 路径格式：`images/storyXX/page-XX.jpg`
- 保存到 `stories/storyXX.json` **和** `public/stories/storyXX.json`

### Step 3: 生成封面（Page 01）⚠️ 关键步骤

**封面 = 电影海报风格，必须包含以下元素：**

1. **大字标题**：彩色 3D 立体泡泡字（rainbow colors），醒目位于画面上方
   - 英文标题为主（如 "Happy Birthday Mom!"）
   - 风格参考 Story 32 "Hello World!" 的封面
2. **主角前置**：咘咘在画面中心/前方，最突出
3. **配角环绕**：其他出场角色在周围，有层次感
4. **场景氛围**：与故事主题相关的背景元素
5. **海报层次**：前景 → 中景 → 背景，有景深和 bokeh 效果

**封面 Prompt 模板：**
```
Pixar 3D animation style, cinematic children's picture book cover poster, warm golden lighting, vertical portrait 1024x1536.

TOP: Large colorful 3D puffy bubble letters spelling "[英文标题]" in rainbow colors (red, orange, yellow, green, blue, pink), with small hearts and stars decorating around the letters. The text is prominent and eye-catching like a Disney movie title.

CENTER: [咘咘完整描述] — she stands in front [做什么动作]. [其他主要角色描述和位置].

BEHIND THEM: [家长/其他角色描述].

BOTTOM CORNER: [NOMI + NONO 描述，如果出场].

BACKGROUND: [场景相关背景元素]. Rich layered movie poster depth composition.
```

**封面检查清单：**
- [ ] 有大字彩色标题？
- [ ] 咘咘在最显眼位置？
- [ ] 所有出场角色都在？
- [ ] 海报层次感（前中后）？
- [ ] 与故事主题匹配？

### Step 4: 生成正文插画（Page 02-13）

1. **每张 prompt 必须内联完整角色描述**（从 CHARACTER-BIBLE.md 复制）
2. **Prompt 前缀**：`Pixar 3D animation style, warm soft lighting, children's picture book illustration, vertical portrait composition 1024x1536.`
3. **同故事内一致性**：
   - 角色服装全程不变（除非剧情需要换装）
   - 场景内道具前后一致（比如蛋糕样式、房间布置）
   - 光线氛围和时间段一致（白天/夜晚/室内）
4. **Safety filter 处理**：
   - 被拦截时简化 prompt，去掉可能敏感的词
   - 不要加 "knife", "cutting" 等可能触发的词，改用中性描述
   - 最多重试 3 次，3 次失败则调整场景描述

### Step 5: 更新项目文件

完成所有图片后，必须更新以下文件：

1. **`stories/index.json`** — 添加新故事条目到最前面
   ```json
   {
     "id": "storyXX",
     "title": "中文标题",
     "chapter": XX,
     "pages": 13,
     "cover": "page-01",
     "tags": ["标签1", "标签2"],
     "title_en": "English Title"
   }
   ```
2. **`public/stories/index.json`** — 同步复制
3. **`src/App.jsx`** — 添加 import 和 storyMap 条目
   ```js
   import storyXX from '../stories/storyXX.json'
   // 在 storyMap 中添加：
   'storyXX': storyXX
   ```

### Step 6: 构建 + 部署 + Git ⚠️ 最容易出错的一步

**双端部署 = Cloudflare + GitHub 必须都成功，缺一不可。**

```bash
# 1. 构建（必须有 CF_PAGES=1，否则资源路径错误导致 404）
cd ~/.openclaw/workspace/bubu-stories
CF_PAGES=1 npm run build

# 2. 部署到 Cloudflare（用户看到的实际网站）
export CLOUDFLARE_API_TOKEN="XaJ24dHOerl_9ddOr1ayc-XR6VEvqPLmdmu2-JM8"
npx wrangler pages deploy dist --project-name bubu-stories --commit-dirty=true

# 3. Git 提交 + 推送（源代码备份 + GitHub Pages 备用）
git add -A
git commit -m "Add Story XX: 中文标题 / English Title

- XX pages with [故事主题]
- Tags: [标签1], [标签2], [标签3]"
git push
```

**部署检查清单（每次都必须执行）：**
- [ ] `CF_PAGES=1` 环境变量设置了？（没设会导致资源路径变成 `/bubu-stories/assets/...` 而不是 `/assets/...`，404）
- [ ] `npm run build` 成功？（检查 dist/ 目录有内容）
- [ ] Cloudflare 部署成功？（输出 `Deployment complete!` + URL）
- [ ] Git commit 成功？（16 files changed 之类的输出）
- [ ] Git push 成功？（`main -> main` 输出）
- [ ] 浏览器验证：打开 https://bubu.sanono.xyz 能看到新故事？能点进去？
- [ ] GitHub 验证：https://github.com/NomiBonnie/bubu-stories 最新 commit 包含新故事？

**常见部署错误：**

| 症状 | 原因 | 解决 |
|------|------|------|
| 首页看不到新故事 | index.json 没更新 | 检查 Step 5 |
| 首页能看到但点不进去 | App.jsx 没加 storyMap | 检查 Step 5 |
| 打开后图片 404 | CF_PAGES=1 没设 | 重新 build + deploy |
| Cloudflare 部署成功但看不到 | 缓存问题 | 硬刷新（Cmd+Shift+R）或等 1 分钟 |
| Git push 失败 | 网络问题或冲突 | `git pull --rebase` 后重试 |

**为什么需要双端？**
- **Cloudflare**：用户访问的实际网站，快速全球 CDN
- **GitHub**：源代码备份 + 协作 + 版本历史 + 备用部署（GitHub Pages）

两者必须保持一致，否则网站和代码会不同步。

---

## ⚠️ 常见错误和教训

| 错误 | 原因 | 预防 |
|------|------|------|
| 封面没有文字 | Prompt 没写标题文字 | 必须用封面模板 |
| 故事点不进去 | 没加到 App.jsx storyMap | Step 5 检查清单 |
| JSON 解析失败 | 字段名不一致（titleEn vs title_en） | 严格用 title_en |
| 图文错位 | 图片编号和 JSON 页码不对应 | 生成时按顺序，完成后核对 |
| 部署后 404 | 没设 CF_PAGES=1 | 部署命令必须带 |
| 角色不一致 | Prompt 没内联完整描述 | 每张必须从 CHARACTER-BIBLE.md 复制 |

---

## 📂 项目结构

```
bubu-stories/
├── CHARACTER-BIBLE.md          # 角色圣经（必读）
├── STORY-WORKFLOW.md           # 本文件（必读）
├── stories/
│   ├── index.json              # 故事索引
│   ├── story1.json ~ storyXX.json
├── public/
│   ├── stories/                # 同步副本
│   └── images/storyXX/         # 插画
├── src/
│   ├── App.jsx                 # 路由 + storyMap
│   ├── Home.jsx                # 首页
│   └── StoryReader.jsx         # 阅读器
└── vite.config.js              # base path 配置
```

---

## 🎯 给 Sub-agent 的特别说明

如果你是被 spawn 来做绘本的 sub-agent：
1. **先读此文件**，然后读 `CHARACTER-BIBLE.md`
2. 按 Step 1-4 执行（JSON + 图片生成）
3. Step 5-6 由主 session 完成
4. 图片生成完成后，报告每张文件的大小确认
5. **封面是最重要的一张**，不要偷懒用简单 prompt
