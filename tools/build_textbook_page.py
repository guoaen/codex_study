from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_DIR = ROOT / "content" / "english" / "texts"


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_chunks(data: dict):
    for unit in data.get("units", []):
        for section in unit.get("sections", []):
            for line in section.get("lines", []):
                chunks = line.get("chunks") or [
                    {"english": line.get("english", ""), "translation": line.get("translation", "")}
                ]
                for chunk in chunks:
                    yield unit, section, line, chunk


def item_count(data: dict) -> int:
    return sum(1 for _unit, _section, _line, _chunk in iter_chunks(data))


def validate_data(data: dict, source_path: Path) -> None:
    if data.get("schema") != "english-textbook-page.v1":
        raise ValueError(f"Unsupported schema in {source_path}")
    for key in ("output", "page_title", "description", "kicker", "title", "summary"):
        if not str(data.get(key, "")).strip():
            raise ValueError(f"Missing page {key} in {source_path}")
    if not data.get("units"):
        raise ValueError(f"No units in {source_path}")

    for unit in data["units"]:
        for key in ("id", "label", "title"):
            if not str(unit.get(key, "")).strip():
                raise ValueError(f"Missing unit {key} in {source_path}")
        if not unit.get("sections"):
            raise ValueError(f"No sections in {source_path} unit {unit['id']}")

    for unit, section, _line, chunk in iter_chunks(data):
        english = str(chunk.get("english", "")).strip()
        translation = str(chunk.get("translation", "")).strip()
        if not english:
            raise ValueError(f"Missing English text in {source_path} unit {unit['id']}")
        if not translation:
            heading = section.get("heading", "")
            raise ValueError(f"Missing translation in {source_path} unit {unit['id']} section {heading}")


def read_button(text: str) -> str:
    label = esc(text)
    return (
        f'<button class="read-btn" type="button" title="朗读" '
        f'aria-label="朗读：{label}" data-text="{label}">'
        '<svg viewBox="0 0 20 20" aria-hidden="true">'
        '<path d="M5 3.5v13l11-6.5-11-6.5z"></path>'
        "</svg></button>"
    )


def normalize_line(line: dict) -> list[dict]:
    if line.get("chunks"):
        return line["chunks"]
    return [{"english": line["english"], "translation": line["translation"]}]


def render_line(line: dict) -> str:
    speaker = str(line.get("speaker", "")).strip()
    speaker_html = f'<span class="speaker">{esc(speaker)}:</span>' if speaker else ""
    chunks = normalize_line(line)
    chunk_html = []
    translation_html = []
    for index, chunk in enumerate(chunks):
        english = str(chunk["english"]).strip()
        translation = str(chunk["translation"]).strip()
        chunk_html.append(
            f'<span class="sentence-chunk" data-index="{index}">'
            f'<span class="sentence">{esc(english)}</span>'
            f"{read_button(english)}"
            "</span>"
        )
        translation_html.append(
            f'<button class="translation" type="button" data-index="{index}" '
            'aria-label="显示或隐藏中文译文">'
            f'<span class="translation-text">{esc(translation)}</span>'
            "</button>"
        )

    return (
        '          <div class="reader-line">'
        f'<div class="english-flow">{speaker_html}<span class="utterance-text">{"".join(chunk_html)}</span></div>'
        f'<div class="translations">{"".join(translation_html)}</div>'
        "</div>"
    )


def render_section(section: dict) -> str:
    heading = str(section.get("heading", "")).strip()
    heading_html = f'          <h3 class="reader-section-title">{esc(heading)}</h3>\n' if heading else ""
    lines = "\n".join(render_line(line) for line in section.get("lines", []))
    return f"{heading_html}{lines}"


def render_unit(unit: dict) -> str:
    sections = "\n".join(render_section(section) for section in unit.get("sections", []))
    return f"""      <article class="reader-unit" id="{esc(unit['id'])}">
        <header class="reader-unit-header">
          <p>{esc(unit['label'])}</p>
          <h2>{esc(unit['title'])}</h2>
        </header>
        <div class="reader-unit-body">
{sections}
        </div>
      </article>"""


def render_page(data: dict, source_path: Path) -> str:
    validate_data(data, source_path)
    stats = data.get("stats", {})
    unit_label = stats.get("unit_label", f"{len(data.get('units', []))} 个 Unit")
    item_suffix = stats.get("item_suffix", "句")
    total_items = item_count(data)
    nav = "\n".join(
        f'      <a href="#{esc(unit["id"])}">{esc(unit["label"])}</a>'
        for unit in data.get("units", [])
    )
    units = "\n".join(render_unit(unit) for unit in data.get("units", []))
    rel_source = source_path.relative_to(ROOT).as_posix()

    return f"""<!doctype html>
<!-- Generated from {rel_source} by tools/build_textbook_page.py. Do not edit this file directly. -->
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{esc(data['description'])}">
  <title>{esc(data['page_title'])}</title>
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/css/site.css">
  <script src="/assets/js/site-shell.js" defer></script>
</head>
<body data-nav="english">
  <div data-site-header></div>

  <main class="reader-shell">
    <section class="reader-hero" aria-labelledby="reader-title">
      <div>
        <p class="kicker">{esc(data['kicker'])}</p>
        <h1 id="reader-title">{esc(data['title'])}</h1>
        <p>{esc(data['summary'])}</p>
      </div>
      <div class="reader-stats" aria-label="课文统计">
        <span>{esc(unit_label)}</span>
        <span>{total_items} {esc(item_suffix)}</span>
      </div>
    </section>
    <div data-reader-tools></div>

    <nav class="reader-unit-nav" aria-label="单元导航">
{nav}
    </nav>

    <section class="reader-units" aria-label="课文内容">
{units}
    </section>
  </main>
  <div data-site-footer></div>
  <button class="back-top" type="button" id="topButton" aria-label="返回顶部">顶部</button>
  <script src="/assets/js/textbook-reader.js" defer></script>
</body>
</html>
"""


def build_file(source_path: Path) -> Path:
    data = read_json(source_path)
    target = ROOT / data["output"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_page(data, source_path), encoding="utf-8", newline="\n")
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description="Build English textbook HTML pages from content JSON.")
    parser.add_argument("--all", action="store_true", help="Build every JSON file in content/english/texts.")
    parser.add_argument("sources", nargs="*", help="Specific textbook JSON files to build.")
    args = parser.parse_args()

    if args.all:
        sources = sorted(TEXT_DIR.glob("*.json"))
    else:
        sources = [ROOT / source for source in args.sources]
    if not sources:
        parser.error("Pass --all or one or more source JSON files.")

    for source in sources:
        target = build_file(source)
        print(f"BUILT {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
