#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a primary-knowledge-site Little Fox story page from compact JSON data."""
from __future__ import annotations

import argparse
import datetime as _dt
import html
import json
import re
import shutil
from pathlib import Path
from typing import Any


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def replace_regex(path: Path, pattern: str, replacement: str) -> None:
    text = read_text(path)
    new, count = re.subn(pattern, replacement, text, count=1)
    if count:
        write_text(path, new)


def insert_before(path: Path, marker: str, insert: str) -> None:
    text = read_text(path)
    if insert.strip() in text:
        return
    if marker not in text:
        raise RuntimeError(f"marker not found in {path}: {marker!r}")
    write_text(path, text.replace(marker, insert + marker, 1))


def insert_after(path: Path, marker: str, insert: str) -> None:
    text = read_text(path)
    if insert.strip() in text:
        return
    if marker not in text:
        raise RuntimeError(f"marker not found in {path}: {marker!r}")
    write_text(path, text.replace(marker, marker + insert, 1))


def insert_after_last_matching_line(path: Path, contains: str, insert: str, section_end: str | None = None) -> None:
    text = read_text(path)
    if insert.strip() in text:
        return
    search_text = text if section_end is None or section_end not in text else text[: text.index(section_end)]
    matches = [m for m in re.finditer(rf"^.*{re.escape(contains)}.*$", search_text, re.MULTILINE)]
    if not matches:
        raise RuntimeError(f"line containing {contains!r} not found in {path}")
    pos = matches[-1].end()
    write_text(path, text[:pos] + "\n" + insert.rstrip("\n") + text[pos:])


def line_html(english: str, chinese: str) -> str:
    e = esc(english)
    c = esc(chinese)
    return (
        '          <div class="reader-line"><div class="english-flow"><span class="utterance-text">'
        f'<span class="sentence-chunk" data-index="0"><span class="sentence">{e}</span>'
        f'<button class="read-btn" type="button" title="朗读" aria-label="朗读：{e}" data-text="{e}">'
        '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 3.5v13l11-6.5-11-6.5z"></path></svg>'
        '</button></span></span></div><div class="translations">'
        f'<button class="translation" type="button" data-index="0" aria-label="显示或隐藏中文译文"><span class="translation-text">{c}</span></button>'
        '</div></div>'
    )


def article_html(page: dict[str, Any], story: dict[str, Any]) -> str:
    lines = "\n".join(line_html(en, zh) for en, zh in page["lines"])
    page_id = esc(page["id"])
    label = esc(page["label"])
    title = esc(page["title"])
    image = esc(page["image"])
    page_num = str(page["id"]).rsplit("-", 1)[-1]
    return f'''      <article class="reader-unit story-page" id="{page_id}">
        <header class="reader-unit-header">
          <p>{label}</p>
          <h2>{title}</h2>
        </header>
        <div class="reader-unit-body story-layout">
          <figure class="story-figure">
            <img src="/assets/images/little-fox/{esc(story["series_slug"])}/{esc(story["slug"])}/{image}" alt="{esc(story["series_title"])} {esc(story["title"])} 第 {page_num} 页插画" loading="lazy">
          </figure>
        <div class="story-text">
{lines}
        </div>
        </div>
      </article>'''


def build_story_html(story: dict[str, Any]) -> str:
    pages = story["pages"]
    page_count = len(pages)
    sentence_count = sum(len(page["lines"]) for page in pages)
    nav_links = "\n".join(
        ['      <a href="#cover">封面</a>'] + [f'      <a href="#page-{i}">{i}</a>' for i in range(1, page_count + 1)]
    )
    story_articles = "\n\n".join(article_html(page, story) for page in pages)
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Little Fox {esc(story["level"])} {esc(story["series_title"])} {esc(story["story_number"])} {esc(story["title"])} 英文朗读与中文译文">
  <title>{esc(story["title"])} | {esc(story["series_title"])}</title>
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/css/site.css">
  <script src="/assets/js/site-shell.js" defer></script>
</head>
<body data-nav="little-fox">
  <div data-site-header></div>

  <main class="reader-shell story-shell">
    <section class="reader-hero" aria-labelledby="reader-title">
      <div>
        <p class="kicker">Little Fox · {esc(story["level"])} · {esc(story["series_title"])} {esc(story["story_number"])}</p>
        <h1 id="reader-title">{esc(story["title"])}</h1>
        <p>英文逐句朗读 | 中文译文点击显示 | PDF 插画保留</p>
      </div>
      <div class="reader-stats" aria-label="故事统计">
        <span>{page_count} 页故事</span>
        <span>{sentence_count} 句正文</span>
      </div>
    </section>
    <div data-reader-tools></div>

    <nav class="reader-unit-nav" aria-label="故事页面导航">
{nav_links}
    </nav>

    <section class="reader-units story-units" aria-label="故事正文">
      <article class="reader-unit story-page" id="cover">
        <header class="reader-unit-header">
          <p>Cover</p>
          <h2>{esc(story["title"])}</h2>
        </header>
        <div class="reader-unit-body story-layout">
          <figure class="story-figure">
            <img src="/assets/images/little-fox/{esc(story["series_slug"])}/{esc(story["slug"])}/cover.png" alt="{esc(story["series_title"])} {esc(story["story_number"])} {esc(story["title"])} PDF 封面" loading="lazy">
          </figure>
        </div>
      </article>

{story_articles}
    </section>
  </main>
  <div data-site-footer></div>

  <button class="back-top" type="button" id="topButton" aria-label="返回顶部">顶部</button>
  <script src="/assets/js/textbook-reader.js" defer></script>
</body>
</html>
'''


def copy_assets(story: dict[str, Any], asset_source: Path, project: Path) -> Path:
    target = project / "assets" / "images" / "little-fox" / story["series_slug"] / story["slug"]
    target.mkdir(parents=True, exist_ok=True)
    mapping = [("page-01.png", "cover.png")]
    mapping.extend((f"page-{i + 1:02d}.png", f"page-{i:02d}.png") for i in range(1, len(story["pages"]) + 1))
    for source_name, target_name in mapping:
        src = asset_source / source_name
        if not src.exists():
            raise FileNotFoundError(src)
        shutil.copy2(src, target / target_name)
    return target


def update_site(story: dict[str, Any], project: Path) -> None:
    pages = story["pages"]
    sentence_count = sum(len(page["lines"]) for page in pages)
    route = f'/subjects/little-fox/{story["series_slug"]}/{story["slug"]}/'
    asset_route = f'assets/images/little-fox/{story["series_slug"]}/{story["slug"]}/'
    page_file = f'subjects/little-fox/{story["series_slug"]}/{story["slug"]}/index.html'
    story_label = f'{story["series_title"]} {story["story_number"]}'
    today = story.get("date") or _dt.date.today().isoformat()

    series_page = project / "subjects" / "little-fox" / story["series_slug"] / "index.html"
    if route not in read_text(series_page):
        card = f'''        <a class="content-card is-ready" href="{route}">
          <span>{esc(story_label)}</span>
          <strong>{esc(story["title"])}</strong>
          <small>{len(pages)} 页故事 · {sentence_count} 句正文 · 英文朗读 · 中文译文点击显示 · PDF 插画保留</small>
        </a>
'''
        insert_before(series_page, "      </div>\n    </section>", card)

    little_fox = project / "subjects" / "little-fox" / "index.html"
    replace_regex(little_fox, r"已收录 \d+ 篇故事 · PDF 插画保留 · 支持逐句朗读", f"已收录 {story['story_number']} 篇故事 · PDF 插画保留 · 支持逐句朗读")

    home = project / "index.html"
    home_text = read_text(home)
    home_pattern = rf"已收录 {re.escape(story['series_title'])} 1-\d+：([^<]+)"
    match = re.search(home_pattern, home_text)
    if match and story["title"] not in match.group(1):
        titles = match.group(1) + "、" + story["title"]
        home_text = re.sub(home_pattern, f"已收录 {story['series_title']} 1-{story['story_number']}：{titles}", home_text, count=1)
        home_text = re.sub(r"已添加 \d+ 篇故事", f"已添加 {story['story_number']} 篇故事", home_text, count=1)
        write_text(home, home_text)

    readme = project / "README.md"
    readme_line = f"- `{route}`：{story['title']} 故事朗读页。\n"
    if readme_line.strip() not in read_text(readme):
        insert_before(readme, "\n## 关键约定", readme_line)

    maintenance = project / "SITE_MAINTENANCE.md"
    replace_regex(maintenance, r"最后更新：\d{4}-\d{2}-\d{2}", f"最后更新：{today}")
    asset_line = f"- `{asset_route}`：{story['title']} 由 PDF 渲染出的封面和故事页插画。\n"
    if asset_line.strip() not in read_text(maintenance):
        insert_after_last_matching_line(maintenance, f"assets/images/little-fox/{story['series_slug']}/", asset_line, "\n- `subjects/english/index.html`")
    page_line = f"- `{page_file}`：{story['title']} 故事朗读页。\n"
    if page_line.strip() not in read_text(maintenance):
        insert_after_last_matching_line(maintenance, f"subjects/little-fox/{story['series_slug']}/", page_line, "\n\n## 当前页面")
    route_line = f"- `{route}`\n"
    if route_line.strip() not in read_text(maintenance):
        insert_before(maintenance, "\n## 公共模板", route_line)
    change = f"- 使用 `english-pdf-story-html` skill 新增 Little Fox 的 {story_label}：{story['title']} 故事朗读页；保留 PDF 封面和 {len(pages)} 页正文插画，跳过版权尾页，并按故事上下文整理正文顺序、补齐中文译文。\n\n"
    if change.strip() not in read_text(maintenance):
        text = read_text(maintenance)
        marker = f"### {today}\n\n"
        if marker in text:
            insert_after(maintenance, marker, change)
        else:
            insert_after(maintenance, "## 变更记录\n\n", f"### {today}\n\n{change}")


def normalize_story(story: dict[str, Any]) -> dict[str, Any]:
    pages = []
    for index, page in enumerate(story["pages"], start=1):
        normalized_lines = []
        for line in page["lines"]:
            if not isinstance(line, list) or len(line) != 2:
                raise ValueError(f"page {index} line must be [english, chinese]: {line!r}")
            normalized_lines.append((str(line[0]), str(line[1])))
        pages.append(
            {
                "id": page.get("id", f"page-{index}"),
                "label": page.get("label", f"Page {index}"),
                "title": page.get("title", f"Page {index}"),
                "image": page.get("image", f"page-{index:02d}.png"),
                "lines": normalized_lines,
            }
        )
    story = dict(story)
    story["pages"] = pages
    for key in ["title", "slug", "series_title", "series_slug", "level", "story_number"]:
        if key not in story:
            raise KeyError(key)
    return story


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=".", help="primary-knowledge-site root")
    parser.add_argument("--data", required=True, help="story JSON file")
    parser.add_argument("--asset-source", required=True, help="directory containing rendered PDF page-XX.png images")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    story = normalize_story(json.loads(Path(args.data).read_text(encoding="utf-8")))
    asset_target = copy_assets(story, Path(args.asset_source), project)
    page_target = project / "subjects" / "little-fox" / story["series_slug"] / story["slug"] / "index.html"
    write_text(page_target, build_story_html(story))
    update_site(story, project)
    print(json.dumps({"page": str(page_target.relative_to(project)), "assets": str(asset_target.relative_to(project))}, ensure_ascii=False))


if __name__ == "__main__":
    main()