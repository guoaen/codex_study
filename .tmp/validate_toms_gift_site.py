from pathlib import Path
import re

files = [
    Path('subjects/little-fox/wizard-and-cat/toms-gift/index.html'),
    Path('subjects/little-fox/wizard-and-cat/index.html'),
    Path('subjects/little-fox/index.html'),
    Path('index.html'),
    Path('README.md'),
    Path('SITE_MAINTENANCE.md'),
]
page = files[0]
s = page.read_text(encoding='utf-8')
print('read_btn', s.count('class="read-btn"'))
print('translation', s.count('class="translation"'))
print('articles', s.count('class="reader-unit story-page"'))
imgs = re.findall(r'<img src="([^"]+)"', s)
print('imgs', len(imgs))
missing = [src for src in imgs if src.startswith('/assets/') and not Path(src.lstrip('/')).exists()]
print('missing_images', missing)
for path in files:
    text = path.read_text(encoding='utf-8')
    bad = []
    for token in ['\ufffd', '鑻', '涓', '鈥']:
        if token in text:
            bad.append(token)
    if bad:
        print('bad_text', path, bad)
    hrefs = re.findall(r'\s(?:href|src)="([^"]+)"', text)
    bad_links = [h for h in hrefs if not (h.startswith('/') or h.startswith('#'))]
    if bad_links:
        print('bad_links', path, bad_links)