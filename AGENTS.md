# Agent 维护入口

这个文件是给 Codex 或其它 AI Agent 接手维护本站点时的入口说明。开始任何站点维护前，先按顺序阅读：

1. `README.md`：确认站点用途、预览方式和部署方式。
2. `SITE_MAINTENANCE.md`：确认当前架构、路径约定、页面结构和历史变更。
3. `assets/js/site-shell.js`：如果涉及页头、导航、页脚、课文页公共工具栏，必须先看这里。
4. 相关页面文件：例如 `index.html`、`subjects/english/index.html` 或 `subjects/.../index.html`。

## 当前项目判断

- 本站点是纯静态 HTML/CSS/JS，不使用 Astro、Node 构建、打包器或组件框架。
- `primary-knowledge-site` 是部署根目录，也是本地预览时的站点根目录。
- 当前页面层级是：首页为一级页面，英语为二级页面，具体英语内容为三级页面。
- 顶部主导航只保留一级/二级入口：`首页` 和 `英语`。
- 页面资源和站内链接统一使用站点根路径，例如 `/assets/css/site.css`。
- 不以双击 HTML 文件作为正式预览方式；使用本地静态服务或 Cloudflare Pages/Worker 预览。

## 修改规则

- 顶部站点导航的 sticky 样式在 `assets/css/site.css` 的 `[data-site-header]` 上，`.site-header` 只负责内部布局，不要改回内部 header。
- 修改导航、品牌标题、页脚或课文页公共朗读工具栏时，只改 `assets/js/site-shell.js`，不要逐页复制维护。
- 新增英语内容页后，通常需要同步更新：
  - `subjects/english/index.html` 的英语清单。
  - `SITE_MAINTENANCE.md` 的当前目录、当前页面和变更记录。
  - `README.md` 的当前实际页面，若新增的是主要页面。
- 新增新的主学科时，通常需要同步更新：
  - `index.html` 的学科入口。
  - `assets/js/site-shell.js` 的 `site.nav`，如果该学科应该出现在主导航。
  - `SITE_MAINTENANCE.md` 和必要的 README 说明。
- 英语课文页和词汇页继续复用 `assets/js/textbook-reader.js` 提供朗读能力，并保留 `data-reader-tools`、`topButton`、`voiceSelect` 等约定。
- 如用户明确要求使用 `english-textbook-html` skill 生成英语课文页，必须先读取该 skill 的说明，再开始整理页面。

## 验证规则

维护完成后至少检查：

- 相关 JS 文件语法，例如 `node --check assets/js/site-shell.js`。
- 页面里的 `href`、`src` 是否仍为站点根路径或页内锚点。
- 本地服务下首页和改动页面是否返回 `200 OK`。
- 若是英语课文页，检查 Unit 数、朗读按钮数、译文数是否符合预期。

## 本地预览

在 `primary-knowledge-site` 目录运行：

```powershell
python -m http.server 8080
```

然后打开：

```text
http://127.0.0.1:8080/
```