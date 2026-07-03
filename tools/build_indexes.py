from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "site-manifest.json"
ENGLISH_INDEX = ROOT / "subjects" / "english" / "index.html"


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def render_card(page: dict) -> str:
    card = page["card"]
    return f"""        <a class="content-card is-ready" href="{esc(page['route'])}">
          <span>{esc(card['eyebrow'])}</span>
          <strong>{esc(card['title'])}</strong>
          <small>{esc(card['summary'])}</small>
        </a>"""


def render_english_index(manifest: dict) -> str:
    english_pages = [
        page
        for page in manifest["pages"]
        if page.get("subject") == "english" and page.get("card")
    ]
    english_pages.sort(key=lambda page: page.get("order", 9999))
    cards = "\n".join(render_card(page) for page in english_pages)
    return f"""<!doctype html>
<!-- Generated from site-manifest.json by tools/build_indexes.py. Do not edit the card list directly. -->
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="英语学习内容清单">
  <title>英语 | 小学知识点</title>
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/css/site.css">
  <script src="/assets/js/site-shell.js" defer></script>
</head>
<body data-nav="english">
  <div data-site-header></div>
  <main class="home-shell">
    <section class="hero-panel" aria-labelledby="page-title">
      <p class="kicker">学科入口</p>
      <h1 id="page-title">英语</h1>
      <p class="page-summary">当前收录英语课文朗读和单词词汇内容。先选择年级、学期和内容类型，再进入对应学习页面。</p>
    </section>

    <section class="content-section" aria-labelledby="english-content">
      <div class="section-head">
        <div>
          <p class="kicker">英语内容</p>
          <h2 id="english-content">现有清单</h2>
        </div>
      </div>
      <div class="content-list">
{cards}
      </div>
    </section>
  </main>
  <div data-site-footer></div>
</body>
</html>
"""


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ENGLISH_INDEX.write_text(render_english_index(manifest), encoding="utf-8", newline="\n")
    print(f"BUILT {ENGLISH_INDEX.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
