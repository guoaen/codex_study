# 小学知识点静态站

这是一个纯 HTML/CSS/JS 静态站点，用来展示小学知识点内容。当前主要内容是语文背诵资料、英语课文朗读、英语单词词汇、英语语法专题和 Little Fox 分级阅读故事页面。

`primary-knowledge-site` 是站点根目录，也是部署到 Cloudflare Pages/Worker 时使用的输出目录；本项目不需要构建命令。

## 接手维护前先读

如果这是一个新的会话，或由其它 AI Agent 接手维护，请先按顺序阅读：

1. `AGENTS.md`：Agent 接手规则、必须同步修改的文件、验证要求。
2. `SITE_MAINTENANCE.md`：当前架构、路径约定、页面结构和历史变更。
3. `SITE_FRAMEWORK.md`：AI Agent 轻量维护框架，尤其是英语单词词汇页和已纳入框架课文页的 JSON 源数据、生成脚本。
4. `assets/js/site-shell.js`：如果涉及页头、主导航、页脚或内容页公共朗读工具栏。
5. 本次要修改的具体页面文件。

本项目已把站点维护常用的自建 skills 放在 `.agents/skills/`。在本仓库内启动 Codex 时，应优先使用这些仓库内置 skills，而不是依赖某台电脑上的用户级 `~/.codex/skills`。

## 当前页面层级

- 一级页面：`/` 首页。
- 二级页面：`/subjects/chinese/` 语文、`/subjects/english/` 英语、`/subjects/little-fox/` Little Fox。
- 三级页面：语文具体内容页、英语具体内容页、Little Fox 系列页，例如 `/subjects/chinese/grade-6/first/recitation/`、`/subjects/little-fox/wizard-and-cat/`。
- 故事正文页：Little Fox 系列页下的具体故事，例如 `/subjects/little-fox/wizard-and-cat/once-upon-a-time/`。

顶部主导航当前保留：`首页`、`语文`、`英语`、`Little Fox`。

## 当前实际页面

- `/`：首页。
- `/subjects/chinese/`：语文内容清单。
- `/subjects/chinese/grade-6/first/recitation/`：语文六年级上册背诵资料。
- `/subjects/english/`：英语内容清单。
- `/subjects/english/grade-3/second/texts/`：英语三年级下学期课文。
- `/subjects/english/grade-3/second/words/`：英语三年级下学期单词词汇。
- `/subjects/english/grade-4/first/words/`：英语四年级上学期单词词汇。
- `/subjects/english/grade-5/second/texts/`：英语五年级下学期课文。
- `/subjects/english/grade-5/second/words/`：英语五年级下学期单词词汇。
- `/subjects/english/grade-6/first/texts/`：英语六年级上学期课文。
- `/subjects/english/grade-6/first/words/`：英语六年级上学期单词词汇。
- `/subjects/english/grammar/tenses/`：小学英语四大常用时态语法专题。
- `/subjects/english/grammar/comparative-superlative/`：英语比较级和最高级语法专题。
- `/subjects/little-fox/`：Little Fox 分级阅读清单。
- `/subjects/little-fox/wizard-and-cat/`：Wizard and Cat 系列清单。
- `/subjects/little-fox/wizard-and-cat/once-upon-a-time/`：Once Upon a Time 故事朗读页。
- `/subjects/little-fox/wizard-and-cat/toms-gift/`：Tom's Gift 故事朗读页。
- `/subjects/little-fox/wizard-and-cat/into-the-dark-forest/`：Into the Dark Forest 故事朗读页。
- `/subjects/little-fox/wizard-and-cat/two-new-friends/`：Two New Friends 故事朗读页。
- `/subjects/little-fox/wizard-and-cat/the-palace/`：The Palace 故事朗读页。
- `/subjects/little-fox/wizard-and-cat/the-king-and-queen/`：The King and Queen 故事朗读页。

## 关键约定

- 公共页头、导航、页脚和内容页朗读工具栏集中在 `assets/js/site-shell.js`。
- 页面资源统一使用站点根路径，例如 `/assets/css/site.css`。
- 不要直接双击 HTML 文件作为正式预览方式；站点根路径需要在 HTTP 服务环境中工作。
- 英语单词词汇页和部分英语课文页已纳入 AI Agent 轻量生成框架：词汇源数据在 `content/english/vocab/`，课文源数据在 `content/english/texts/`，生成脚本分别是 `tools/build_vocab_page.py` 和 `tools/build_textbook_page.py`，入口清单由 `site-manifest.json` 和 `tools/build_indexes.py` 维护。
- 新增语文内容页后，通常需要同步更新 `subjects/chinese/index.html`、`site-manifest.json`、首页入口和公共导航。
- 新增英语内容页后，优先更新 `site-manifest.json`，再运行 `tools/build_indexes.py` 重建 `subjects/english/index.html` 清单。
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
