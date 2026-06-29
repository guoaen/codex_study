from pathlib import Path
import html
import shutil

ROOT = Path.cwd()
UTF8 = "utf-8"

story_slug = "toms-gift"
story_title = "Tom's Gift"
series_title = "Wizard and Cat"
level = "Level 3"
story_no = 2
asset_dir = ROOT / "assets/images/little-fox/wizard-and-cat" / story_slug
page_dir = ROOT / "subjects/little-fox/wizard-and-cat" / story_slug
source_images = ROOT / ".tmp/tom-s-gift-assets/images"

pages = [
    {
        "id": "page-1",
        "label": "Page 1",
        "title": "A New Royal Wizard",
        "image": "page-01.png",
        "lines": [
            ("Tom wanted to be the new royal wizard.", "汤姆想成为新的皇家巫师。"),
            ("So did everyone else.", "其他人也都想。"),
            ("But only one wizard could try out.", "但只有一名巫师可以去试一试。"),
            ("“I will pick the best wizard soon,” said Master Wizard.", "“我很快就会选出最好的巫师。”大法师说。"),
        ],
    },
    {
        "id": "page-2",
        "label": "Page 2",
        "title": "Practice",
        "image": "page-02.png",
        "lines": [
            ("Tom practiced lots of magic spells.", "汤姆练习了许多魔法咒语。"),
            ("The other wizards practiced too.", "其他巫师也在练习。"),
        ],
    },
    {
        "id": "page-3",
        "label": "Page 3",
        "title": "A Gift Appears",
        "image": "page-03.png",
        "lines": [
            ("One day Master called all the wizards.", "一天，大法师把所有巫师都叫来。"),
            ("“Each wizard must make a gift appear,” he said.", "“每位巫师都必须变出一份礼物。”他说。"),
            ("“I will pick the best gift—and the best wizard.”", "“我会选出最好的礼物，也选出最好的巫师。”"),
        ],
    },
    {
        "id": "page-4",
        "label": "Page 4",
        "title": "Walter Laughs",
        "image": "page-04.png",
        "lines": [
            ("Walter laughed. “Tom can’t make a gift appear!”", "沃尔特笑了。“汤姆变不出礼物！”"),
            ("Other wizards laughed too.", "其他巫师也笑了。"),
            ("Tom frowned.", "汤姆皱起了眉头。"),
        ],
    },
    {
        "id": "page-5",
        "label": "Page 5",
        "title": "Fancy Gifts",
        "image": "page-05.png",
        "lines": [
            ("Wizards made fancy cakes and candy appear.", "巫师们变出了漂亮的蛋糕和糖果。"),
            ("Golden coins and pens appeared too.", "金币和笔也出现了。"),
        ],
    },
    {
        "id": "page-6",
        "label": "Page 6",
        "title": "Red Socks",
        "image": "page-06.png",
        "lines": [
            ("Then Tom lifted his wand.", "然后汤姆举起了魔杖。"),
            ("“I’ll give everyone red socks with dots!”", "“我要送给每个人一双带点点的红袜子！”"),
            ("Poof!", "砰！"),
        ],
    },
    {
        "id": "page-7",
        "label": "Page 7",
        "title": "Red Spots",
        "image": "page-07.png",
        "lines": [
            ("“You fool!” cried Walter.", "“你这个笨蛋！”沃尔特叫道。"),
            ("“You gave us red spots!”", "“你给了我们红点点！”"),
            ("“We all have chicken pox!” said another wizard.", "“我们全都得了水痘！”另一个巫师说。"),
        ],
    },
    {
        "id": "page-8",
        "label": "Page 8",
        "title": "Go To The Palace",
        "image": "page-08.png",
        "lines": [
            ("“Everyone is sick but you, Tom,” said Master.", "“大家都病了，只有你没事，汤姆。”大法师说。"),
            ("“You must go to the palace.”", "“你必须去王宫。”"),
            ("“I will do my best, Master!” said Tom.", "“我会尽力的，大法师！”汤姆说。"),
        ],
    },
    {
        "id": "page-9",
        "label": "Page 9",
        "title": "Where Is The Palace?",
        "image": "page-09.png",
        "lines": [
            ("Tom got his sack and hurried away.", "汤姆拿起他的袋子，匆忙离开了。"),
            ("A minute later he was back.", "一分钟后，他又回来了。"),
            ("“Master?” asked Tom. “Where is the palace?”", "“大法师？”汤姆问。“王宫在哪里？”"),
            ("Master sighed and gave Tom a map.", "大法师叹了口气，给了汤姆一张地图。"),
        ],
    },
    {
        "id": "page-10",
        "label": "Page 10",
        "title": "The Dark Forest",
        "image": "page-10.png",
        "lines": [
            ("“You must go through the Dark Forest,” warned Master.", "“你必须穿过黑暗森林。”大法师提醒说。"),
            ("“It is very dangerous. Make sure you stay on the path!”", "“那里非常危险。一定要沿着路走！”"),
            ("Tom took the map and headed for the Dark Forest.", "汤姆拿着地图，朝黑暗森林走去。"),
        ],
    },
]

READ_ICON = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 3.5v13l11-6.5-11-6.5z"></path></svg>'

def esc(value: str) -> str:
    return html.escape(value, quote=True)

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding=UTF8, newline="\n")

def reader_line(en: str, zh: str) -> str:
    return (
        '          <div class="reader-line"><div class="english-flow"><span class="utterance-text">'
        f'<span class="sentence-chunk" data-index="0"><span class="sentence">{esc(en)}</span>'
        f'<button class="read-btn" type="button" title="朗读" aria-label="朗读：{esc(en)}" data-text="{esc(en)}">{READ_ICON}</button>'
        '</span></span></div><div class="translations">'
        f'<button class="translation" type="button" data-index="0" aria-label="显示或隐藏中文译文"><span class="translation-text">{esc(zh)}</span></button>'
        '</div></div>'
    )

def article(page: dict) -> str:
    lines = "\n".join(reader_line(en, zh) for en, zh in page["lines"])
    img_src = f"/assets/images/little-fox/wizard-and-cat/{story_slug}/{page['image']}"
    return f'''      <article class="reader-unit story-page" id="{esc(page["id"])}">
        <header class="reader-unit-header">
          <p>{esc(page["label"])}</p>
          <h2>{esc(page["title"])}</h2>
        </header>
        <div class="reader-unit-body story-layout">
          <figure class="story-figure">
            <img src="{esc(img_src)}" alt="Wizard and Cat Tom's Gift 第 {esc(page["label"].split()[-1])} 页插画" loading="lazy">
          </figure>
        <div class="story-text">
{lines}
        </div>
        </div>
      </article>'''

def build_story_html() -> str:
    page_count = len(pages)
    line_count = sum(len(p["lines"]) for p in pages)
    nav = ['      <a href="#cover">封面</a>'] + [f'      <a href="#{p["id"]}">{i}</a>' for i, p in enumerate(pages, 1)]
    articles = "\n\n".join(article(p) for p in pages)
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Little Fox Level 3 Wizard and Cat 2 Tom's Gift 英文朗读与中文译文">
  <title>Tom's Gift | Wizard and Cat</title>
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/css/site.css">
  <script src="/assets/js/site-shell.js" defer></script>
</head>
<body data-nav="little-fox">
  <div data-site-header></div>

  <main class="reader-shell story-shell">
    <section class="reader-hero" aria-labelledby="reader-title">
      <div>
        <p class="kicker">Little Fox · Level 3 · Wizard and Cat 2</p>
        <h1 id="reader-title">Tom's Gift</h1>
        <p>英文逐句朗读 | 中文译文点击显示 | PDF 插画保留</p>
      </div>
      <div class="reader-stats" aria-label="故事统计">
        <span>{page_count} 页故事</span>
        <span>{line_count} 句正文</span>
      </div>
    </section>
    <div data-reader-tools></div>

    <nav class="reader-unit-nav" aria-label="故事页面导航">
{chr(10).join(nav)}
    </nav>

    <section class="reader-units story-units" aria-label="故事正文">
      <article class="reader-unit story-page" id="cover">
        <header class="reader-unit-header">
          <p>Cover</p>
          <h2>Tom's Gift</h2>
        </header>
        <div class="reader-unit-body story-layout">
          <figure class="story-figure">
            <img src="/assets/images/little-fox/wizard-and-cat/{story_slug}/cover.png" alt="Wizard and Cat 2 Tom's Gift PDF 封面" loading="lazy">
          </figure>
        </div>
      </article>

{articles}
    </section>
  </main>
  <div data-site-footer></div>

  <button class="back-top" type="button" id="topButton" aria-label="返回顶部">顶部</button>
  <script src="/assets/js/textbook-reader.js" defer></script>
</body>
</html>
'''

def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding=UTF8)
    if old not in text:
        if new in text:
            return
        raise ValueError(f"pattern not found in {path}: {old[:80]!r}")
    write_text(path, text.replace(old, new, 1))

def insert_after(path: Path, anchor: str, insertion: str) -> None:
    text = path.read_text(encoding=UTF8)
    if insertion.strip() in text:
        return
    if anchor not in text:
        raise ValueError(f"anchor not found in {path}: {anchor[:80]!r}")
    write_text(path, text.replace(anchor, anchor + insertion, 1))

# Copy final image assets. Keep cover and 10 story pages; skip PDF copyright page 12.
asset_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(source_images / "page-01.png", asset_dir / "cover.png")
for i in range(1, 11):
    shutil.copy2(source_images / f"page-{i+1:02d}.png", asset_dir / f"page-{i:02d}.png")

write_text(page_dir / "index.html", build_story_html())

series = ROOT / "subjects/little-fox/wizard-and-cat/index.html"
new_card = '''
        <a class="content-card is-ready" href="/subjects/little-fox/wizard-and-cat/toms-gift/">
          <span>Wizard and Cat 2</span>
          <strong>Tom's Gift</strong>
          <small>10 页故事 · 30 句正文 · 英文朗读 · 中文译文点击显示 · PDF 插画保留</small>
        </a>'''
insert_after(series, '''        <a class="content-card is-ready" href="/subjects/little-fox/wizard-and-cat/once-upon-a-time/">
          <span>Wizard and Cat 1</span>
          <strong>Once Upon a Time</strong>
          <small>10 页故事 · 33 句正文 · 英文朗读 · 中文译文点击显示 · PDF 插画保留</small>
        </a>''', new_card)

replace_once(ROOT / "subjects/little-fox/index.html", "已收录 1 篇故事 · PDF 插画保留 · 支持逐句朗读", "已收录 2 篇故事 · PDF 插画保留 · 支持逐句朗读")
replace_once(ROOT / "index.html", "已收录 Wizard and Cat 1：Once Upon a Time", "已收录 Wizard and Cat 1-2：Once Upon a Time、Tom's Gift")
replace_once(ROOT / "index.html", "已添加 1 篇故事", "已添加 2 篇故事")

readme = ROOT / "README.md"
insert_after(readme, "- `/subjects/little-fox/wizard-and-cat/once-upon-a-time/`：Once Upon a Time 故事朗读页。", "\n- `/subjects/little-fox/wizard-and-cat/toms-gift/`：Tom's Gift 故事朗读页。")

maint = ROOT / "SITE_MAINTENANCE.md"
insert_after(maint, "- `assets/images/little-fox/wizard-and-cat/once-upon-a-time/`：Once Upon a Time 由 PDF 渲染出的封面和故事页插画。", "\n- `assets/images/little-fox/wizard-and-cat/toms-gift/`：Tom's Gift 由 PDF 渲染出的封面和故事页插画。")
insert_after(maint, "- `subjects/little-fox/wizard-and-cat/once-upon-a-time/index.html`：Once Upon a Time 故事朗读页。", "\n- `subjects/little-fox/wizard-and-cat/toms-gift/index.html`：Tom's Gift 故事朗读页。")
insert_after(maint, "- `/subjects/little-fox/wizard-and-cat/once-upon-a-time/`", "\n- `/subjects/little-fox/wizard-and-cat/toms-gift/`")
insert_after(maint, "### 2026-06-29", "\n\n- 使用 `english-pdf-story-html` skill 新增 Little Fox 的 Wizard and Cat 2：Tom's Gift 故事朗读页；保留 PDF 封面和 10 页正文插画，跳过版权尾页，并按文本块坐标与上下文整理正文顺序、补齐中文译文。")

print({"story_page": str(page_dir / "index.html"), "assets": str(asset_dir), "pages": len(pages), "lines": sum(len(p["lines"]) for p in pages)})