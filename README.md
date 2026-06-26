# 小学知识点静态站

这是一个纯 HTML/CSS/JS 静态站点，用来展示小学知识点内容。当前主要内容是英语课文朗读页面和单词词汇页面。

`primary-knowledge-site` 是站点根目录，也是部署到 Cloudflare Pages/Worker 时使用的输出目录；本项目不需要构建命令。

## 接手维护前先读

如果这是一个新的会话，或由其它 AI Agent 接手维护，请先按顺序阅读：

1. `AGENTS.md`：Agent 接手规则、必须同步修改的文件、验证要求。
2. `SITE_MAINTENANCE.md`：当前架构、路径约定、页面结构和历史变更。
3. `assets/js/site-shell.js`：如果涉及页头、主导航、页脚或英语内容页公共工具栏。
4. 本次要修改的具体页面文件。

## 当前页面层级

- 一级页面：`/` 首页。
- 二级页面：`/subjects/english/` 英语。
- 三级页面：具体英语内容页。

顶部主导航当前只保留：`首页`、`英语`。

## 当前实际页面

- `/`：首页。
- `/subjects/english/`：英语内容清单。
- `/subjects/english/grade-3/second/texts/`：英语三年级下学期课文。
- `/subjects/english/grade-3/second/words/`：英语三年级下学期单词词汇。
- `/subjects/english/grade-5/second/texts/`：英语五年级下学期课文。
- `/subjects/english/grade-5/second/words/`：英语五年级下学期单词词汇。

## 关键约定

- 公共页头、导航、页脚和内容页朗读工具栏集中在 `assets/js/site-shell.js`。
- 页面资源统一使用站点根路径，例如 `/assets/css/site.css`。
- 不要直接双击 HTML 文件作为正式预览方式；站点根路径需要在 HTTP 服务环境中工作。
- 新增英语内容页后，优先更新 `subjects/english/index.html` 的清单。
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