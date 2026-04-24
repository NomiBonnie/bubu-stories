# 批量重生成 Story 1-8 插图任务

## 目标
用 gpt-image-2 (Poland endpoint) 重新生成 Story 1-8 的所有插图，确保角色一致性和质量。

## 要求

### 1. 角色一致性（强制）
- **必须严格遵循** `memory/projects/bubu-stories/CHARACTER-BIBLE.md`
- 常驻角色：咘咘（主角）+ NOMI（浣熊🦝蓝衣）+ NONO（小鸟🐦红羽）+ Coco（小熊猫🧧黄围巾）
- 每个故事开始前，先读 CHARACTER-BIBLE，提取角色描述
- 每个 prompt 必须包含完整的角色外观描述

### 2. 设备物品一致性
- 同一故事里的道具外观必须保持一致
- 例如：咘咘的床、马桶、玩具等，在同一故事的多张图里要统一风格

### 3. 封面页结构（新规则）
- **第一页 = 封面** — 必须有合适位置/横幅放标题文字
- 封面 prompt 特别要求："Title banner area" 或 "Space for title text"
- 标题不要画在图片上，留白让 React 组件渲染文字

### 4. JSON 结构更新
- 每个 story 的 `pages` 数组第一项是封面
- `pages[0].text` = 故事标题（中文）
- `pages[0].text_en` = 故事标题（英文）
- `pages[0].image` = `images/storyN/page-01.jpg`
- 后续 pages[1], pages[2]... 对应 page-02.jpg, page-03.jpg...

### 5. index.json 更新
- 每个故事的 `cover` 字段设为 `page-01`

## 技术规格

### Azure 配置
- Endpoint: `~/.config/azure-openai/config.json` → `image2_poland_endpoint`
- API Key: `image2_poland_api_key`
- Deployment: `image2_poland_deployment` (gpt-image-2-1)
- API Version: `2025-04-01-preview`

### 图片参数
- Size: `1024x1536` (vertical 9:16)
- Quality: `medium` (Sam 2026-03-11 铁规，除非特别批准才用 high)
- Format: URL (Poland endpoint 不支持 b64_json)

### Rate Limit
- 9 RPM limit
- **每张图片生成后等待 7 秒**（安全间隔）

## 执行步骤

### 对每个 Story (1-8):

1. **读取原始 JSON**
   - `stories/storyN.json` 和 `public/stories/storyN.json`
   
2. **读取 CHARACTER-BIBLE**
   - 提取常驻角色的完整外观描述
   
3. **生成封面 (page-01.jpg)**
   - Prompt 包含：标题区域提示 + 角色描述 + 故事主题场景
   
4. **生成正文页面 (page-02.jpg ~ page-XX.jpg)**
   - 每张图片 prompt 包含：
     - 完整角色描述（从 CHARACTER-BIBLE）
     - 当前页面文字内容对应的场景
     - 道具一致性提示
   
5. **保存图片**
   - 输出到 `public/images/storyN/page-XX.jpg`
   - 覆盖旧图片
   
6. **更新 JSON**
   - 在 `pages` 数组开头插入封面页
   - 更新后续页面的 image 字段（page-02, page-03...）
   - 同步更新 `stories/storyN.json` 和 `public/stories/storyN.json`
   
7. **更新 index.json**
   - 设置 `cover: "page-01"`

## 验证标准

### 每个故事完成后检查：
- [ ] 所有角色外观符合 CHARACTER-BIBLE
- [ ] 同一故事里的道具外观一致
- [ ] 封面图有合适的标题区域
- [ ] JSON 结构正确（pages[0] = 封面）
- [ ] 图片文件命名正确（page-01 ~ page-XX，两位数）
- [ ] stories/ 和 public/stories/ 两个目录的 JSON 同步

## 故事列表

处理顺序（从新到旧）：
1. Story 8 — 咘咘去游乐场
2. Story 7 — 咘咘看彩虹
3. Story 6 — 咘咘去超市
4. Story 5 — 咘咘的生日派对
5. Story 4 — 咘咘和小猫
6. Story 3 — 咘咘学游泳
7. Story 2 — 咘咘找朋友
8. Story 1 — 小兔子找月亮

## 部署

所有故事完成后：
1. 验证本地 JSON 和图片完整性
2. Build + 部署到 Cloudflare Pages
3. 提交到 GitHub（触发 GitHub Pages 部署）

## 注意事项

⚠️ **Sub-agent 对结果负责铁规**：
- 生成完每个故事后，必须抽查至少 3 张图片验证角色外观
- 发现不符合 CHARACTER-BIBLE 的图片必须重新生成
- 不能只看生成日志就说完成

⚠️ **API Key 安全**：
- 生成脚本不能提交到 GitHub
- 完成后删除所有包含 API key 的临时文件

⚠️ **时间预估**：
- 单个故事：12-16 张图 × 15 秒 = 3-4 分钟生成 + 1 分钟验证
- 8 个故事总计：约 30-40 分钟

## 开始

Sub-agent 收到这个任务后，按以下顺序执行：
1. 读取 CHARACTER-BIBLE 全文
2. 读取 Azure config
3. 创建生成脚本（Node.js ESM）
4. 从 Story 8 开始逐个处理
5. 每个故事完成后验证 + 报告
6. 全部完成后部署

---
Sam 批准时间：2026-04-25 00:29
执行者：Sub-agent (to be spawned)
