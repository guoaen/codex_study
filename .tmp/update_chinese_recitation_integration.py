"""Integrate the Chinese grade 6 recitation pages into the static site.

Purpose:
- Update shared navigation and homepage entry.
- Register Chinese pages in the manifest.
- Update README and SITE_MAINTENANCE for the 2026-07-28 task.

This is an intermediate task artifact, not a site runtime file.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        return text
    return text.replace(old, new, 1)


def update_site_shell() -> None:
    path = "assets/js/site-shell.js"
    text = read(path)
    text = text.replace(
        'footer: "小学知识点静态站 · 当前包含首页、英语清单页、英语内容页和 Little Fox 分级阅读页",',
        'footer: "小学知识点静态站 · 当前包含首页、语文、英语和 Little Fox 学习内容",',
    )
    if '{ id: "chinese", label: "语文", href: "/subjects/chinese/" }' not in text:
        text = text.replace(
            '      { id: "home", label: "首页", href: "/" },\n      { id: "english", label: "英语", href: "/subjects/english/" },',
            '      { id: "home", label: "首页", href: "/" },\n      { id: "chinese", label: "语文", href: "/subjects/chinese/" },\n      { id: "english", label: "英语", href: "/subjects/english/" },',
        )
    write(path, text)


def update_home() -> None:
    path = "index.html"
    text = read(path)
    text = text.replace(
        "当前站点保留最基础的静态结构：首页作为一级入口，英语和 Little Fox 作为二级入口，具体学习内容页面按清单继续下钻。后续新增内容时，会按维护记录继续补充。",
        "当前站点保留最基础的静态结构：首页作为一级入口，语文、英语和 Little Fox 作为二级入口，具体学习内容页面按清单继续下钻。后续新增内容时，会按维护记录继续补充。",
    )
    chinese_card = """        <a class="content-card is-ready" href="/subjects/chinese/">
          <span>语文</span>
          <strong>六年级上册背诵资料</strong>
          <small>已整理课文片段、古诗词、文言文和日积月累，共 7 个单元 18 项内容</small>
        </a>
"""
    if 'href="/subjects/chinese/"' not in text:
        text = text.replace('      <div class="content-list">\n', '      <div class="content-list">\n' + chinese_card, 1)
    text = text.replace("<small>待添加</small>", "<small>已添加六年级上册背诵资料</small>", 1)
    write(path, text)


def update_manifest() -> None:
    path = ROOT / "site-manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["updated"] = "2026-07-28"
    pages = data.setdefault("pages", [])
    existing = {page.get("id") for page in pages}
    new_pages = [
        {
            "id": "chinese-index",
            "type": "subject-index",
            "title": "语文",
            "route": "/subjects/chinese/",
            "output": "subjects/chinese/index.html",
            "managed": "manual",
        },
        {
            "id": "chinese-grade-6-first-recitation",
            "type": "chinese-recitation",
            "subject": "chinese",
            "title": "六年级上册背诵资料",
            "route": "/subjects/chinese/grade-6/first/recitation/",
            "output": "subjects/chinese/grade-6/first/recitation/index.html",
            "managed": "manual",
            "order": 610,
            "card": {
                "eyebrow": "六年级 · 上学期 · 背诵",
                "title": "六年级上册背诵资料",
                "summary": "7 个单元 · 18 项背诵内容 · 不含 PDF 第 1 页签名表格",
            },
        },
    ]
    insert_at = 2
    for page in reversed(new_pages):
        if page["id"] not in existing:
            pages.insert(insert_at, page)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_readme() -> None:
    path = "README.md"
    text = read(path)
    text = text.replace(
        "当前主要内容是英语课文朗读、英语单词词汇、英语语法专题和 Little Fox 分级阅读故事页面。",
        "当前主要内容是语文背诵资料、英语课文朗读、英语单词词汇、英语语法专题和 Little Fox 分级阅读故事页面。",
    )
    text = text.replace(
        "二级页面：`/subjects/english/` 英语、`/subjects/little-fox/` Little Fox。",
        "二级页面：`/subjects/chinese/` 语文、`/subjects/english/` 英语、`/subjects/little-fox/` Little Fox。",
    )
    text = text.replace(
        "三级页面：英语具体内容页、Little Fox 系列页，例如 `/subjects/little-fox/wizard-and-cat/`。",
        "三级页面：语文具体内容页、英语具体内容页、Little Fox 系列页，例如 `/subjects/chinese/grade-6/first/recitation/`、`/subjects/little-fox/wizard-and-cat/`。",
    )
    text = text.replace(
        "顶部主导航当前保留：`首页`、`英语`、`Little Fox`。",
        "顶部主导航当前保留：`首页`、`语文`、`英语`、`Little Fox`。",
    )
    if "/subjects/chinese/" not in text:
        text = text.replace(
            "- `/`：首页。\n",
            "- `/`：首页。\n- `/subjects/chinese/`：语文内容清单。\n- `/subjects/chinese/grade-6/first/recitation/`：语文六年级上册背诵资料。\n",
            1,
        )
    if "新增语文内容页后" not in text:
        text = text.replace(
            "- 新增英语内容页后，优先更新 `site-manifest.json`，再运行 `tools/build_indexes.py` 重建 `subjects/english/index.html` 清单。\n",
            "- 新增语文内容页后，通常需要同步更新 `subjects/chinese/index.html`、`site-manifest.json`、首页入口和公共导航。\n- 新增英语内容页后，优先更新 `site-manifest.json`，再运行 `tools/build_indexes.py` 重建 `subjects/english/index.html` 清单。\n",
            1,
        )
    write(path, text)


def update_maintenance() -> None:
    path = "SITE_MAINTENANCE.md"
    text = read(path)
    text = text.replace("最后更新：2026-07-10", "最后更新：2026-07-28")
    text = text.replace(
        "当前站点除英语内容外，也包含 Little Fox 分级阅读内容。",
        "当前站点包含语文、英语和 Little Fox 分级阅读内容。",
    )
    text = text.replace(
        "二级页面：`/subjects/english/` 英语、`/subjects/little-fox/` Little Fox。",
        "二级页面：`/subjects/chinese/` 语文、`/subjects/english/` 英语、`/subjects/little-fox/` Little Fox。",
    )
    text = text.replace(
        "三级页面：英语具体内容页、Little Fox 系列页，例如 `/subjects/little-fox/wizard-and-cat/`。",
        "三级页面：语文具体内容页、英语具体内容页、Little Fox 系列页，例如 `/subjects/chinese/grade-6/first/recitation/`、`/subjects/little-fox/wizard-and-cat/`。",
    )
    text = text.replace(
        "顶部主导航只保留一级/二级入口：`首页`、`英语`、`Little Fox`。",
        "顶部主导航只保留一级/二级入口：`首页`、`语文`、`英语`、`Little Fox`。",
    )
    if "`subjects/chinese/index.html`" not in text:
        text = text.replace(
            "- `subjects/english/index.html`：英语二级清单页。\n",
            "- `subjects/chinese/index.html`：语文二级清单页。\n- `subjects/chinese/grade-6/first/recitation/index.html`：语文六年级上册背诵资料页。\n- `subjects/english/index.html`：英语二级清单页。\n",
            1,
        )
    if "- `/subjects/chinese/`" not in text:
        text = text.replace(
            "- `/`\n",
            "- `/`\n- `/subjects/chinese/`\n- `/subjects/chinese/grade-6/first/recitation/`\n",
            1,
        )
    text = text.replace(
        "当前主要值是 `home`、`english` 和 `little-fox`。",
        "当前主要值是 `home`、`chinese`、`english` 和 `little-fox`。",
    )
    if "新增语文内容页" not in text:
        text = text.replace(
            "8. 如果新增英语三级内容页，更新 `site-manifest.json`，再运行 `tools/build_indexes.py` 生成 `subjects/english/index.html` 清单。\n",
            "8. 如果新增语文内容页，更新 `subjects/chinese/index.html`、`site-manifest.json`，必要时更新首页入口和公共导航。\n9. 如果新增英语三级内容页，更新 `site-manifest.json`，再运行 `tools/build_indexes.py` 生成 `subjects/english/index.html` 清单。\n",
            1,
        )
        text = text.replace(
            "9. 如果新增 Little Fox 故事页，更新对应系列页；如果新增新系列，也更新 `subjects/little-fox/index.html`。\n10. 如果新增新的二级入口，更新 `index.html` 的入口；必要时修改 `assets/js/site-shell.js` 的 `site.nav`。\n11. 更新 `README.md` 的当前实际页面，若该页面属于主要页面。\n12. 更新本文档的“当前目录”“当前页面”和“变更记录”。\n13. 按“验证清单”检查。",
            "10. 如果新增 Little Fox 故事页，更新对应系列页；如果新增新系列，也更新 `subjects/little-fox/index.html`。\n11. 如果新增新的二级入口，更新 `index.html` 的入口；必要时修改 `assets/js/site-shell.js` 的 `site.nav`。\n12. 更新 `README.md` 的当前实际页面，若该页面属于主要页面。\n13. 更新本文档的“当前目录”“当前页面”和“变更记录”。\n14. 按“验证清单”检查。",
            1,
        )
    changelog = """### 2026-07-28

- 新增语文二级入口和六年级上册背诵资料页：从指定 PDF 跳过第 1 页签名表格后整理第 2-7 页内容，按 7 个单元、18 项背诵内容排版，不启用语音朗读。

"""
    if "### 2026-07-28" not in text:
        text = text.replace("## 变更记录\n\n", "## 变更记录\n\n" + changelog, 1)
    write(path, text)


def main() -> None:
    update_site_shell()
    update_home()
    update_manifest()
    update_readme()
    update_maintenance()
    print("UPDATED Chinese recitation integration")


if __name__ == "__main__":
    main()
