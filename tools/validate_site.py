from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "site-manifest.json"


def fail(message: str) -> None:
    raise AssertionError(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_manifest_pages(manifest: dict) -> list[str]:
    checked = []
    for page in manifest.get("pages", []):
        output = page.get("output")
        if not output:
            continue
        path = ROOT / output
        if not path.exists():
            fail(f"Missing page output: {output}")
        checked.append(output)
    return checked


def check_html_paths() -> int:
    bad = []
    html_files = list(ROOT.rglob("*.html"))
    pattern = re.compile(r'(?:href|src)="([^"]+)"')
    for path in html_files:
        text = read_text(path)
        for match in pattern.finditer(text):
            value = match.group(1)
            if not (
                value.startswith("/")
                or value.startswith("#")
                or value.startswith("http://")
                or value.startswith("https://")
                or value.startswith("mailto:")
            ):
                bad.append(f"{path.relative_to(ROOT)} -> {value}")
    if bad:
        fail("Non-root relative paths found:\n" + "\n".join(bad[:20]))
    return len(html_files)


def check_vocab_source(source: Path) -> tuple[str, int, int]:
    data = json.loads(source.read_text(encoding="utf-8"))
    if data.get("schema") != "english-vocab-page.v1":
        fail(f"Unsupported vocab schema: {source}")
    units = data.get("units", [])
    if not units:
        fail(f"No units in {source}")
    total = 0
    for unit in units:
        for key in ("id", "label", "title"):
            if not str(unit.get(key, "")).strip():
                fail(f"Missing unit {key} in {source}")
        for item in unit.get("items", []):
            total += 1
            for key in ("english", "chinese", "phonetic"):
                if not str(item.get(key, "")).strip():
                    fail(f"Missing {key} in {source} unit {unit.get('id')}")
    output = ROOT / data["output"]
    if not output.exists():
        fail(f"Missing generated vocab output: {data['output']}")
    html = read_text(output)
    article_count = len(re.findall(r'class="reader-unit vocab-unit"', html))
    row_count = len(re.findall(r"<tr>\s*<td>", html))
    read_count = len(re.findall(r'class="read-btn"', html))
    nav_count = len(re.findall(r'<a href="#(?:unit-\d+|review)">', html))
    if article_count != len(units):
        fail(f"{data['output']} article count {article_count} != source units {len(units)}")
    if row_count != total:
        fail(f"{data['output']} row count {row_count} != source items {total}")
    if read_count != total:
        fail(f"{data['output']} read button count {read_count} != source items {total}")
    if nav_count != len(units):
        fail(f"{data['output']} nav count {nav_count} != source units {len(units)}")
    if "data-dictation" not in html:
        fail(f"{data['output']} missing dictation panel")
    if "<details" in html or "data-section-back" in html:
        fail(f"{data['output']} contains disallowed details/back link")
    if "\ufffd" in html:
        fail(f"{data['output']} contains replacement character")
    return (data["output"], len(units), total)


def check_textbook_source(source: Path) -> tuple[str, int, int]:
    data = json.loads(source.read_text(encoding="utf-8"))
    if data.get("schema") != "english-textbook-page.v1":
        fail(f"Unsupported textbook schema: {source}")
    units = data.get("units", [])
    if not units:
        fail(f"No units in {source}")
    total = 0
    for unit in units:
        for key in ("id", "label", "title"):
            if not str(unit.get(key, "")).strip():
                fail(f"Missing unit {key} in {source}")
        for section in unit.get("sections", []):
            if not section.get("lines"):
                fail(f"Empty section in {source} unit {unit.get('id')}")
            for line in section.get("lines", []):
                chunks = line.get("chunks") or [line]
                for chunk in chunks:
                    total += 1
                    for key in ("english", "translation"):
                        if not str(chunk.get(key, "")).strip():
                            fail(f"Missing {key} in {source} unit {unit.get('id')}")
    output = ROOT / data["output"]
    if not output.exists():
        fail(f"Missing generated textbook output: {data['output']}")
    html = read_text(output)
    article_count = len(re.findall(r'<article class="reader-unit"', html))
    read_count = len(re.findall(r'class="read-btn"', html))
    translation_count = len(re.findall(r'class="translation"', html))
    if article_count != len(units):
        fail(f"{data['output']} article count {article_count} != source units {len(units)}")
    if read_count != total:
        fail(f"{data['output']} read button count {read_count} != source chunks {total}")
    if translation_count != total:
        fail(f"{data['output']} translation count {translation_count} != source chunks {total}")
    for unit in units:
        if f'href="#{unit["id"]}"' not in html:
            fail(f"{data['output']} missing nav anchor for {unit['id']}")
    if "data-reader-tools" not in html:
        fail(f"{data['output']} missing reader tools mount")
    if "topButton" not in html:
        fail(f"{data['output']} missing back-to-top button")
    if "<details" in html or "data-section-back" in html:
        fail(f"{data['output']} contains disallowed details/back link")
    if "\ufffd" in html:
        fail(f"{data['output']} contains replacement character")
    return (data["output"], len(units), total)
def main() -> int:
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        pages = check_manifest_pages(manifest)
        html_count = check_html_paths()
        vocab_results = [
            check_vocab_source(path)
            for path in sorted((ROOT / "content" / "english" / "vocab").glob("*.json"))
        ]
        textbook_results = [
            check_textbook_source(path)
            for path in sorted((ROOT / "content" / "english" / "texts").glob("*.json"))
        ]
    except Exception as exc:
        print(f"VALIDATION FAILED: {exc}", file=sys.stderr)
        return 1

    print(f"manifest_pages={len(pages)}")
    print(f"html_files={html_count}")
    for output, units, rows in vocab_results:
        print(f"vocab {output} units={units} rows={rows}")
    for output, units, rows in textbook_results:
        print(f"textbook {output} units={units} chunks={rows}")
    print("VALIDATION OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
