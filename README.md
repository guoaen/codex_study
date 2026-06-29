# 小学知识点静态站

这是一个纯 HTML/CSS/JS 静态站点，用来展示小学知识点内容。当前主要内容是英语课文朗读、英语单词词汇和 Little Fox 分级阅读故事页面。

`primary-knowledge-site` 是站点根目录，也是部署到 Cloudflare Pages/Worker 时使用的输出目录；本项目不需要构建命令。

## 接手维护前先读

如果这是一个新的会话，或由其它 AI Agent 接手维护，请先按顺序阅读：

1. `AGENTS.md`：Agent 接手规则、必须同步修改的文件、验证要求。
2. `SITE_MAINTENANCE.md`：当前架构、路径约定、页面结构和历史变更。
3. `assets/js/site-shell.js`：如果涉及页头、主导航、页脚或内容页公共朗读工具栏。
4. 本次要修改的具体页面文件。

本项目已把站点维护常用的自建 skills 放在 `.agents/skills/`。在本仓库内启动 Codex 时，应优先使用这些仓库内置 skills，而不是依赖某台电脑上的用户级 `~/.codex/skills`。

## 当前页面层级

- 一级页面：`/` 首页。
- 二级页面：`/subjects/english/` 英语、`/subjects/little-fox/` Little Fox。
- 三级页面：英语具体内容页、Little Fox 系列页，例如 `/subjects/little-fox/wizard-and-cat/`。
- 故事正文页：Little Fox 系列页下的具体故事，例如 `/subjects/little-fox/wizard-and-cat/once-upon-a-time/`。

顶部主导航当前保留：`首页`、`英语`、`Little Fox`。

## 当前实际页面

- `/`：首页。
- `/subjects/english/`：英语内容清单。
- `/subjects/english/grade-3/second/texts/`：英语三年级下学期课文。
- `/subjects/english/grade-3/second/words/`：英语三年级下学期单词词汇。
- `/subjects/english/grade-5/second/texts/`：英语五年级下学期课文。
- `/subjects/english/grade-5/second/words/`：英语五年级下学期单词词汇。
- `/subjects/little-fox/`：Little Fox 分级阅读清单。
- `/subjects/little-fox/wizard-and-cat/`：Wizard and Cat 系列清单。
- `/subjects/little-fox/wizard-and-cat/once-upon-a-time/`：Once Upon a Time 故事朗读页。
- `/subjects/little-fox/wizard-and-cat/toms-gift/`：Tom's Gift 故事朗读页。

## 关键约定

- 公共页头、导航、页脚和内容页朗读工具栏集中在 `assets/js/site-shell.js`。
- 页面资源统一使用站点根路径，例如 `/assets/css/site.css`。
- 不要直接双击 HTML 文件作为正式预览方式；站点根路径需要在 HTTP 服务环境中工作。
- 新增英语内容页后，优先更新 `subjects/english/index.html` 的清单。
- 新增 Little Fox 故事页后，优先更新对应系列页，例如 `subjects/little-fox/wizard-and-cat/index.html`。
- 新增、删除主要页面后，通常需要同步更新 `index.html`、`SITE_MAINTENANCE.md`，必要时更新本 README。

## 本地预览

在 `primary-knowledge-site` 目录运行：

```powershell
python -m http.server 8080
```

然后打开：

```text
http://127.0.0.1:8080/
```

## Cloudflare 部署

部署到 Cloudflare Pages 时：

- 构建命令：留空。
- 输出目录：项目根目录，即 `primary-knowledge-site`。
