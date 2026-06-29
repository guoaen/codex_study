import fitz
from pathlib import Path
pdf = Path('.tmp/tom-s-gift-source/tom-s-gift.pdf')
doc = fitz.open(pdf)
for pno in range(1, 11):
    page = doc[pno]
    print(f'--- PDF page {pno+1} story/page {pno} ---')
    blocks = page.get_text('blocks')
    blocks = [b for b in blocks if b[4].strip() and not b[4].strip().isdigit()]
    blocks.sort(key=lambda b: (round(b[1], 1), round(b[0], 1)))
    for b in blocks:
        x0, y0, x1, y1, text, *_ = b
        clean = ' / '.join(line.strip() for line in text.splitlines() if line.strip())
        print(f'({x0:.1f},{y0:.1f})-({x1:.1f},{y1:.1f}) {clean}')