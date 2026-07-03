from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_PAGES = [
    {
        "input": "subjects/english/grade-3/second/words/index.html",
        "output": "content/english/vocab/grade-3-second.json",
        "id": "english-grade-3-second-words",
        "route": "/subjects/english/grade-3/second/words/",
    },
    {
        "input": "subjects/english/grade-4/first/words/index.html",
        "output": "content/english/vocab/grade-4-first.json",
        "id": "english-grade-4-first-words",
        "route": "/subjects/english/grade-4/first/words/",
    },
    {
        "input": "subjects/english/grade-5/second/words/index.html",
        "output": "content/english/vocab/grade-5-second.json",
        "id": "english-grade-5-second-words",
        "route": "/subjects/english/grade-5/second/words/",
    },
]


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def first_match(pattern: str, text: str, default: str = "") -> str:
    match = re.search(pattern, text, re.S)
    return clean_text(match.group(1)) if match else default


def parse_stats(hero: str) -> dict[str, str]:
    spans = [clean_text(item) for item in re.findall(r"<span>(.*?)</span>", hero, re.S)]
    unit_label = spans[0] if spans else ""
    item_suffix = "条"
    if len(spans) > 1:
        item_suffix = re.sub(r"^\d+\s*", "", spans[1]).strip() or item_suffix
    return {"unit_label": unit_label, "item_suffix": item_suffix}


def parse_unit_suffix(header_text: str) -> str:
    match = re.search(r"·\s*\d+\s*(.+)$", header_text)
    return match.group(1).strip() if match else "条"


def parse_page(config: dict[str, str]) -> dict:
    source_path = ROOT / config["input"]
    text = source_path.read_text(encoding="utf-8")
    hero = first_match(r"(<section class=\"reader-hero\"[\s\S]*?</section>)", text)
    hero_raw_match = re.search(r"<section class=\"reader-hero\"[\s\S]*?</section>", text, re.S)
    hero_raw = hero_raw_match.group(0) if hero_raw_match else ""

    units = []
    unit_item_suffix = "条"
    articles = re.findall(
        r"<article class=\"reader-unit vocab-unit\" id=\"([^\"]+)\">([\s\S]*?)</article>",
        text,
    )
    for unit_id, body in articles:
        header_text = first_match(r"<header class=\"reader-unit-header\">\s*<p>(.*?)</p>", body)
        title = first_match(r"<h2>(.*?)</h2>", body)
        label = header_text.split("·", 1)[0].strip() if header_text else unit_id
        if len(units) == 0:
            unit_item_suffix = parse_unit_suffix(header_text)

        items = []
        rows = re.findall(r"<tbody>([\s\S]*?)</tbody>", body)
        row_text = rows[0] if rows else ""
        for row in re.findall(r"<tr>([\s\S]*?)</tr>", row_text):
            cells = re.findall(r"<td(?: class=\"phonetic\")?>([\s\S]*?)</td>", row)
            if len(cells) != 3:
                continue
            english = first_match(r"<span>(.*?)</span>", cells[0])
            chinese = clean_text(cells[1])
            phonetic = clean_text(cells[2])
            if not english:
                continue
            items.append({"english": english, "chinese": chinese, "phonetic": phonetic})

        units.append({"id": unit_id, "label": label, "title": title, "items": items})

    return {
        "schema": "english-vocab-page.v1",
        "id": config["id"],
        "source_note": f"Imported from {config['input']}",
        "route": config["route"],
        "output": config["input"],
        "title": first_match(r"<h1 id=\"reader-title\">(.*?)</h1>", text),
        "page_title": first_match(r"<title>(.*?)</title>", text),
        "description": first_match(r"<meta name=\"description\" content=\"([^\"]*)\"", text),
        "kicker": first_match(r"<p class=\"kicker\">(.*?)</p>", hero_raw),
        "summary": first_match(r"<h1 id=\"reader-title\">.*?</h1>\s*<p>(.*?)</p>", hero_raw),
        "stats": parse_stats(hero_raw),
        "unit_item_suffix": unit_item_suffix,
        "dictation": "data-dictation" in text,
        "units": units,
    }


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Import existing vocabulary HTML pages into content JSON.")
    parser.add_argument("--all-current", action="store_true", help="Import the current known vocabulary pages.")
    args = parser.parse_args()
    if not args.all_current:
        parser.error("Only --all-current is supported for this migration helper.")

    for config in DEFAULT_PAGES:
        data = parse_page(config)
        target = ROOT / config["output"]
        write_json(target, data)
        item_count = sum(len(unit["items"]) for unit in data["units"])
        print(f"WROTE {target.relative_to(ROOT)} units={len(data['units'])} items={item_count}")


if __name__ == "__main__":
    main()
