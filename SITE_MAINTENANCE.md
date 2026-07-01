# 小学知识点站点维护记录

最后更新：2026-06-30

本文档记录本站点的维护细节。若由新的会话或其它 AI Agent 接手，请先读根目录 `AGENTS.md`，再读 `README.md`，最后读本文档。当前站点除英语内容外，也包含 Little Fox 分级阅读内容。

每次新增、修改、删除页面或内容后，都要更新本文档的“当前目录”“当前页面”“变更记录”中受影响的部分。

## 当前方案

当前站点是最基础的 HTML/CSS/JS 静态站，不使用 Astro、Node 构建、打包器或组件框架。

选择原因：
- 当前实际页面较少，但后续会逐步增加。
- 用户后续通常会确认内容后，再由 Codex 或其它 Agent 直接维护。
- 纯静态结构部署简单；公共模板脚本可以避免导航、页脚等内容逐页重复维护。

## 维护入口

开始维护前按顺序阅读：

1. `AGENTS.md`：Agent 操作规则和验证要求。
2. `README.md`：站点用途、预览方式、部署方式。
3. `SITE_MAINTENANCE.md`：当前架构、页面约定、变更记录。
4. `.agents/skills/`：如果涉及英语课文、英语词汇或 PDF 故事页面，优先使用仓库内置的对应 skill。
5. `assets/js/site-shell.js`：如果涉及公共导航、页头、页脚或内容页公共工具栏。
6. 本次要修改的具体页面。

## 页面层级

当前信息架构：
- 一级页面：`/` 首页。
- 二级页面：`/subjects/english/` 英语、`/subjects/little-fox/` Little Fox。
- 三级页面：英语具体内容页、Little Fox 系列页，例如 `/subjects/little-fox/wizard-and-cat/`。
- 故事正文页：Little Fox 系列页下的具体故事，例如 `/subjects/little-fox/wizard-and-cat/once-upon-a-time/`。

顶部主导航只保留一级/二级入口：`首页`、`英语`、`Little Fox`。不要把具体年级、学期、内容类型或单篇故事页面直接放进顶部主导航。

## 核心约定

- 顶部站点导航的固定定位写在外层 `[data-site-header]` 上，`.site-header` 只负责视觉布局；不要把 sticky 只放回内部 header，否则 Chrome 滚动时会被父容器限制。
- `primary-knowledge-site` 是站点根目录。
- 页面资源和站内链接统一使用站点根路径，例如 `/assets/css/site.css`、`/subjects/english/.../`、`/subjects/little-fox/.../`。
- 站点需要通过本地静态服务或 Cloudflare Pages/Worker 访问；不要把双击 `file://` HTML 作为正式预览方式。
- 页头、主导航、页脚、内容页“返回上级”和朗读工具栏集中在 `assets/js/site-shell.js`。
- 后续新增或删除主导航入口时，优先修改 `assets/js/site-shell.js` 中的 `site.nav`，不要逐页改导航 HTML。
- 如需新增复杂交互，优先放到 `assets/js/` 下的独立脚本，不把大量 JavaScript 内联在 HTML 中。

## 当前目录

- `AGENTS.md`：Agent 接手维护入口。
- `.agents/skills/english-pdf-story-html/`：从带插画英文 PDF 创建 Little Fox/故事朗读页面的仓库内置 skill。
- `.agents/skills/english-textbook-html/`：从英语课文文本创建课文朗读页面的仓库内置 skill。
- `.agents/skills/english-vocabulary-html/`：从单词词汇资料创建词汇页面的仓库内置 skill。
- `README.md`：项目概览、预览和部署说明。
- `SITE_MAINTENANCE.md`：维护记录和页面约定。
- `index.html`：首页。
- `assets/favicon.svg`：站点图标。
- `assets/css/site.css`：全站样式、英语内容页样式、Little Fox 故事页样式。
- `assets/js/site-shell.js`：站点公共模板、导航配置、页脚、内容页公共工具栏。
- `assets/js/textbook-reader.js`：课文页、词汇页和 Little Fox 故事页朗读、译文显示、返回顶部交互。
- `assets/images/little-fox/wizard-and-cat/once-upon-a-time/`：Once Upon a Time 由 PDF 渲染出的封面和故事页插画。
- `assets/images/little-fox/wizard-and-cat/toms-gift/`：Tom's Gift 由 PDF 渲染出的封面和故事页插画。
- `assets/images/little-fox/wizard-and-cat/into-the-dark-forest/`：Into the Dark Forest 由 PDF 渲染出的封面和故事页插画。
- `assets/images/little-fox/wizard-and-cat/two-new-friends/`：Two New Friends 由 PDF 渲染出的封面和故事页插画。
- `assets/images/little-fox/wizard-and-cat/the-palace/`：The Palace 由 PDF 渲染出的封面和故事页插画。
- `assets/images/little-fox/wizard-and-cat/the-king-and-queen/`：The King and Queen 由 PDF 渲染出的封面和故事页插画。

- `subjects/english/index.html`：英语二级清单页。
- `subjects/english/grade-3/second/texts/index.html`：英语三年级下学期课文页。
- `subjects/english/grade-3/second/words/index.html`：英语三年级下学期单词词汇页。
- `subjects/english/grade-5/second/texts/index.html`：英语五年级下学期课文页。
- `subjects/english/grade-5/second/words/index.html`：英语五年级下学期单词词汇页。
- `subjects/little-fox/index.html`：Little Fox 二级清单页。
- `subjects/little-fox/wizard-and-cat/index.html`：Wizard and Cat 三级系列页。
- `subjects/little-fox/wizard-and-cat/once-upon-a-time/index.html`：Once Upon a Time 故事朗读页。
- `subjects/little-fox/wizard-and-cat/toms-gift/index.html`：Tom's Gift 故事朗读页。
- `subjects/little-fox/wizard-and-cat/into-the-dark-forest/index.html`：Into the Dark Forest 故事朗读页。
- `subjects/little-fox/wizard-and-cat/two-new-friends/index.html`：Two New Friends 故事朗读页。
- `subjects/little-fox/wizard-and-cat/the-palace/index.html`：The Palace 故事朗读页。
- `subjects/little-fox/wizard-and-cat/the-king-and-queen/index.html`：The King and Queen 故事朗读页。


## 当前页面

- `/`
- `/subjects/english/`
- `/subjects/english/grade-3/second/texts/`
- `/subjects/english/grade-3/second/words/`
- `/subjects/english/grade-5/second/texts/`
- `/subjects/english/grade-5/second/words/`
- `/subjects/little-fox/`
- `/subjects/little-fox/wizard-and-cat/`
- `/subjects/little-fox/wizard-and-cat/once-upon-a-time/`
- `/subjects/little-fox/wizard-and-cat/toms-gift/`
- `/subjects/little-fox/wizard-and-cat/into-the-dark-forest/`
- `/subjects/little-fox/wizard-and-cat/two-new-friends/`
- `/subjects/little-fox/wizard-and-cat/the-palace/`
- `/subjects/little-fox/wizard-and-cat/the-king-and-queen/`

## 公共模板

`assets/js/site-shell.js` 负责生成：
- 站点页头和品牌区。
- 主导航。
- 站点页脚。
- 可选内容页返回上级链接。当前英语课文页、词汇页和 Little Fox 故事页不使用“返回上级”链接，统一通过顶部主导航进入二级页。
- 内容页朗读工具栏。

页面通过占位节点接入公共模板：

```html
<div data-site-header></div>
<div data-reader-tools></div>
<div data-site-footer></div>
```

不是所有页面都需要全部占位节点。首页、英语清单页和 Little Fox 清单页通常只需要 `data-site-header` 和 `data-site-footer`；英语课文页、词汇页和 Little Fox 故事页通常使用 `data-site-header`、`data-reader-tools` 和 `data-site-footer`，不再放 `data-section-back`。

## 普通页面结构

```html
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/css/site.css">
<script src="/assets/js/site-shell.js" defer></script>
<body data-nav="home">
  <div data-site-header></div>
  <main>...</main>
  <div data-site-footer></div>
</body>
```

`data-nav` 的值应对应 `assets/js/site-shell.js` 里的 `site.nav[].id`，用于高亮当前导航。当前主要值是 `home`、`english` 和 `little-fox`。

## 英语课文页和词汇页结构

```html
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/css/site.css">
<script src="/assets/js/site-shell.js" defer></script>
<body data-nav="english">
  <div data-site-header></div>
  <main class="reader-shell">
    ...页面自己的标题、Unit 导航和正文...
    <div data-reader-tools></div>
  </main>
  <div data-site-footer></div>
  <button class="back-top" type="button" id="topButton" aria-label="返回顶部">顶部</button>
  <script src="/assets/js/textbook-reader.js" defer></script>
</body>
```

注意：`site-shell.js` 必须先于 `textbook-reader.js` 加载，因为朗读工具栏里的 `voiceSelect`、`stopButton`、`ttsStatus` 由公共模板生成。

英语课文页正文约定：
- 每个 Unit 使用 `article.reader-unit`。
- 每句英文朗读按钮使用 `button.read-btn`，并在 `data-text` 中保存朗读文本。
- 中文译文使用 `button.translation`。
- 英文句子和译文通过相同的 `data-index` 关联。

英语词汇页正文约定：
- 每个 Unit 使用 `article.reader-unit.vocab-unit`，默认直接展开展示，不使用折叠。
- 词汇表使用 `table.vocab-table`，表头固定为 `English`、`中文`、`音标` 三列。
- 每个词汇行使用 `button.read-btn`，并在 `data-text` 中保存朗读文本。
- 每个词汇行的三列内容都应非空；如果原始资料未提供中文或音标，维护时需要按英文内容补齐，不再使用 `-` 占位。
- 词汇页不引用额外展开/折叠脚本。
- 可选听写模式由 `assets/js/textbook-reader.js` 统一处理；只在页面包含 `data-dictation`、`data-dictation-toggle`、`data-dictation-tray` 标记时启用。目前已用于三年级下学期和五年级下学期单词页。听写面板应放在 `reader-unit-nav` 后面，启用后由 CSS 固定在 Unit 单元栏下方。

## Little Fox 故事页结构

Little Fox 故事页复用课文页的朗读工具和译文显示逻辑：
- 页面使用 `body data-nav="little-fox"`，让顶部主导航高亮 Little Fox。
- 故事正文页使用 `main.reader-shell.story-shell`。
- 每个故事页片段使用 `article.reader-unit.story-page`。
- PDF 插画或页面渲染图放在 `figure.story-figure`，图片路径统一放在 `/assets/images/little-fox/.../`。
- 英文正文仍使用 `button.read-btn` 的 `data-text` 存朗读文本，中文译文使用 `button.translation`，英文句子和译文通过相同 `data-index` 关联。
- 如果 PDF 没有中文译文，维护时按英文内容补齐中文译文。
- 若 PDF 有空白页或版权页，可以不放进正文页；但故事页插画应尽量保留。
- 使用 `english-pdf-story-html` skill 时，PDF 抽取文本只作为原材料；需要结合页面图片、文本坐标和故事上下文整理阅读顺序，不能直接按抽取顺序随意排放。

## 新增或修改页面流程

1. 确认内容归属：学科、系列、年级、学期、内容类型或故事名称。
2. 判断是新增页面、更新已有页面，还是只更新首页入口。
3. 新建或修改对应目录下的 `index.html`。
4. 使用站点根路径引用 CSS/JS 和图片资源。
5. 放置需要的公共模板占位节点。
6. 如果新增英语三级内容页，更新 `subjects/english/index.html` 的清单。
7. 如果新增 Little Fox 故事页，更新对应系列页；如果新增新系列，也更新 `subjects/little-fox/index.html`。
8. 如果新增新的二级入口，更新 `index.html` 的入口；必要时修改 `assets/js/site-shell.js` 的 `site.nav`。
9. 更新 `README.md` 的当前实际页面，若该页面属于主要页面。
10. 更新本文档的“当前目录”“当前页面”和“变更记录”。
11. 按“验证清单”检查。

## 验证清单

维护完成后至少检查：
- `node --check assets/js/site-shell.js`。
- 如改过课文朗读逻辑，执行 `node --check assets/js/textbook-reader.js`。
- 页面里的 `href`、`src` 是否仍为站点根路径或页内锚点。
- 本地静态服务下首页和改动页面是否返回 `200 OK`。
- 如果是英语课文页，检查 Unit 数、朗读按钮数、译文数是否符合预期。
- 如果是英语词汇页，检查 Unit 数、词汇行数、朗读按钮数是否符合预期。
- 如果是 Little Fox 故事页，检查故事页数、插画图片引用、朗读按钮数和译文数是否符合预期。
- 检查中文没有乱码。

## 本地预览

在 `primary-knowledge-site` 目录下运行：

```powershell
python -m http.server 8080
```

打开：

```text
http://127.0.0.1:8080/
```

## Cloudflare 部署

部署到 Cloudflare Pages 时：
- 构建命令：留空。
- 输出目录：项目根目录，即 `primary-knowledge-site`。

## 变更记录

### 2026-06-30

- 使用 `english-pdf-story-html` skill 新增 Little Fox 的 Wizard and Cat 6：The King and Queen 故事朗读页；保留 PDF 封面和 10 页正文插画，跳过版权尾页，并按故事上下文整理正文顺序、补齐中文译文。

- 使用 `english-pdf-story-html` skill 新增 Little Fox 的 Wizard and Cat 5：The Palace 故事朗读页；保留 PDF 封面和 10 页正文插画，跳过版权尾页，并按故事上下文整理正文顺序、补齐中文译文。

- 使用 `english-pdf-story-html` skill 新增 Little Fox 的 Wizard and Cat 4：Two New Friends 故事朗读页；保留 PDF 封面和 10 页正文插画，跳过版权尾页，并按故事上下文整理正文顺序、补齐中文译文。

### 2026-06-29

- 使用 `english-pdf-story-html` skill 新增 Little Fox 的 Wizard and Cat 3：Into the Dark Forest 故事朗读页；保留 PDF 封面和 10 页正文插画，跳过版权尾页，并按故事上下文整理正文顺序、补齐中文译文。
- 使用 `english-pdf-story-html` skill 新增 Little Fox 的 Wizard and Cat 2：Tom's Gift 故事朗读页；保留 PDF 封面和 10 页正文插画，跳过版权尾页，并按文本块坐标与上下文整理正文顺序、补齐中文译文。

- 使用 `english-pdf-story-html` skill 新增 Little Fox 的 Wizard and Cat 三级系列页，以及 Once Upon a Time 故事朗读页；故事页保留 PDF 渲染插画，并按文本坐标和故事上下文整理正文顺序、补齐中文译文。
- 删除此前 Little Fox 旧系列页、旧故事页和对应图片资源；首页与 Little Fox 清单改为指向 Wizard and Cat。
- 顶部主导航新增 `Little Fox` 入口，首页新增 Little Fox 内容入口和扩展卡片。
- 删除英语三年级/五年级课文页和单词词汇页头部的“返回英语”链接，改为依靠顶部主导航返回英语二级页。
- 调整三年级下学期和五年级下学期单词词汇页听写模式：听写面板移到 Unit 单元栏下方，启用后随滚动固定在顶部区域。
- 按 `english-vocabulary-html` skill 新规范复检三年级下学期和五年级下学期单词词汇页：补齐所有缺失音标，移除词汇表音标列的 `-` 占位，并修正三年级页 3 处 OCR/拼接残留。
- 三年级下学期单词词汇页启用听写模式，与五年级下学期单词页保持一致。
- 听写区词卡显示序号，并在删除靠前词卡后自动重排后续序号。
- 五年级下学期单词词汇页新增听写模式试用：点击“听写”展开临时空白区，点击词汇顺序加入，点击已加入词卡删除；刷新后不保留。

### 2026-06-26

- 新增广州英语三年级下册单词词汇页：Unit 1-8，共 227 条词汇、短语和句型；英语清单页增加对应入口。
- 将顶部站点导航的 sticky 定位从内部 `.site-header` 移到外层 `[data-site-header]`，修正 Chrome 页面滚动时主导航消失的问题。
- 新增广州英语五年级下册单词词汇页：Unit 1-12，共 150 个词汇；英语清单页增加对应入口。
- 调整单词页为与课文页一致的直接展开 Unit 列表，并让顶部站点导航在移动端也保持 sticky。
- 新增英语三年级下学期课文页：Unit 1-8，共 102 个朗读条目；首页增加对应入口。
- 根据用户新的维护偏好，将公共页头、导航、页脚和课文页工具栏抽到 `assets/js/site-shell.js`。
- 将页面资源和站内链接统一改为站点根路径，后续以本地静态服务或 Cloudflare 部署环境预览。
- 新增 `AGENTS.md` 作为 Agent 接手维护入口，并重写 `README.md`、`SITE_MAINTENANCE.md` 的阅读顺序和维护说明。
- 调整信息架构：首页为一级页面，英语为二级清单页，具体英语内容为三级页面；顶部导航改为仅保留“首页 / 英语”。
- 根据用户工作流判断，迁移为纯 HTML/CSS/JS 静态站，清理 Astro、Node 依赖、构建产物和临时源码。
- 接入广州英语五年级下册 Unit 1-12 课文，共 163 句。
- 先前创建过 Astro 静态站点原型，后续已废弃。
