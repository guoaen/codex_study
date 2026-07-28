"""Extract the Chinese grade 6 recitation PDF for the 2026-07-28 site update.

Purpose:
- Read the user-provided network PDF.
- Skip page 1 because it is a signature/check table.
- Save extracted text blocks and rendered page images for review.

This is an intermediate task artifact, not a site runtime file.
"""

from __future__ import annotations

import json
from pathlib import Path

import fitz


PDF_PATH = r"\\192.168.100.221\school\学校资料\郭海翘\10.五年级第二学期\暑假\六年级上册 背诵课文检测表及内容(1).pdf"
ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / ".tmp"
OUTPUT_JSON = TMP / "chinese_grade6_recitation_extracted.json"
IMAGE_PREFIX = "chinese_grade6_recitation_page"


def block_to_dict(block: tuple) -> dict:
    x0, y0, x1, y1, text, block_no, block_type = block
    return {
        "bbox": [round(x0, 2), round(y0, 2), round(x1, 2), round(y1, 2)],
        "text": text.strip(),
        "block_no": block_no,
        "block_type": block_type,
    }


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF_PATH)
    pages = []
    for index, page in enumerate(doc, start=1):
        if index == 1:
            continue
        text = page.get_text("text").strip()
        blocks = [
            block_to_dict(block)
            for block in sorted(page.get_text("blocks"), key=lambda item: (item[1], item[0]))
            if str(block[4]).strip()
        ]
        image_path = TMP / f"{IMAGE_PREFIX}_{index:02d}.png"
        pix = page.get_pixmap(matrix=fitz.Matrix(1.6, 1.6), alpha=False)
        pix.save(image_path)
        pages.append(
            {
                "page": index,
                "width": round(page.rect.width, 2),
                "height": round(page.rect.height, 2),
                "text": text,
                "blocks": blocks,
                "image": str(image_path.relative_to(ROOT)).replace("\\", "/"),
            }
        )
    payload = {
        "source": PDF_PATH,
        "note": "Page 1 skipped by user request because it is a signature/check table.",
        "page_count": doc.page_count,
        "extracted_pages": len(pages),
        "pages": pages,
    }
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"pages={doc.page_count} extracted={len(pages)} output={OUTPUT_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
