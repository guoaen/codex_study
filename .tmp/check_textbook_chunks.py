"""Intermediate checker for generated textbook JSON.

Purpose: report English chunks that probably contain more than one sentence,
so they can be split into sentence-level read buttons.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


PATTERN = re.compile(r"[.!?]\s+[A-Z(]")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python .tmp/check_textbook_chunks.py content/english/texts/<file>.json")
        return 2

    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    found = 0
    for unit in data.get("units", []):
        for section in unit.get("sections", []):
            for line in section.get("lines", []):
                chunks = line.get("chunks") or [line]
                for chunk in chunks:
                    english = str(chunk.get("english", ""))
                    if PATTERN.search(english):
                        found += 1
                        print(
                            f"{unit.get('id')} | {section.get('heading')} | "
                            f"{line.get('speaker', '')} | {english}"
                        )
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
