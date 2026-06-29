#!/usr/bin/env python3
"""Extract text and rendered page images from an illustrated story PDF."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


def import_fitz():
    try:
        import fitz  # PyMuPDF
    except Exception as exc:  # pragma: no cover - environment-specific message
        raise SystemExit(
            "PyMuPDF is required. Install/use an environment with the 'fitz' module available."
        ) from exc
    return fitz


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True, help="Source PDF path")
    parser.add_argument("--out", required=True, help="Output directory for extracted assets")
    parser.add_argument("--scale", type=float, default=2.0, help="Render scale; 2.0 is usually enough for web pages")
    parser.add_argument(
        "--blank-byte-threshold",
        type=int,
        default=12000,
        help="Rendered PNG byte size at or below this value is treated as blank when text is empty",
    )
    parser.add_argument(
        "--skip-blank-pages",
        action="store_true",
        help="Do not save rendered PNGs for pages guessed to be blank",
    )
    return parser.parse_args()


def pixmap_looks_blank(pix, threshold: int = 250, max_dark_ratio: float = 0.001) -> bool:
    """Return True when a pixmap is effectively white/blank."""
    samples = pix.samples
    if not samples:
        return True
    step = max(1, len(samples) // 100000)
    checked = 0
    dark = 0
    for value in samples[::step]:
        checked += 1
        if value < threshold:
            dark += 1
    return checked == 0 or (dark / checked) <= max_dark_ratio


def save_pixmap(pix, image_path: Path) -> int:
    if image_path.exists():
        try:
            image_path.unlink()
        except PermissionError as exc:
            raise SystemExit(
                f"Cannot overwrite existing image: {image_path}. Close viewers or use a fresh --out directory."
            ) from exc
    pix.save(image_path)
    return image_path.stat().st_size


def main() -> int:
    args = parse_args()
    fitz = import_fitz()

    pdf_path = Path(args.pdf).expanduser().resolve()
    out_dir = Path(args.out).expanduser().resolve()
    image_dir = out_dir / "images"
    out_dir.mkdir(parents=True, exist_ok=True)
    image_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    matrix = fitz.Matrix(args.scale, args.scale)
    text_blocks: list[str] = [f"source: {pdf_path}", f"pages: {doc.page_count}"]
    pages: list[dict[str, object]] = []

    for index, page in enumerate(doc, 1):
        text = page.get_text("text").strip()
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        width = pix.width
        height = pix.height
        blank_by_pixels = not text and pixmap_looks_blank(pix)
        image_name = f"page-{index:02d}.png"
        image_path = image_dir / image_name

        if args.skip_blank_pages and blank_by_pixels:
            image_bytes = 0
            kept_image = None
            likely_blank = True
        else:
            image_bytes = save_pixmap(pix, image_path)
            kept_image = f"images/{image_name}"
            likely_blank = blank_by_pixels or (not text and image_bytes <= args.blank_byte_threshold)

        text_blocks.append(f"--- page {index} chars {len(text)} ---")
        text_blocks.append(text)
        pages.append(
            {
                "page": index,
                "chars": len(text),
                "text": text,
                "image": kept_image,
                "image_bytes": image_bytes,
                "width": width,
                "height": height,
                "likely_blank": likely_blank,
            }
        )

    (out_dir / "extracted-text.txt").write_text("\n".join(text_blocks), encoding="utf-8")
    (out_dir / "pages.json").write_text(
        json.dumps({"source": str(pdf_path), "page_count": doc.page_count, "pages": pages}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"out": str(out_dir), "pages": doc.page_count}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())