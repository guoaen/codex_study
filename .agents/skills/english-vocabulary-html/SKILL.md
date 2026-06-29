---
name: english-vocabulary-html
description: Create and update unit-based English vocabulary and word-list HTML study pages from pasted text, screenshots/OCR text, existing HTML, spreadsheets, or mixed English-Chinese-phonetic source material. Use when Codex needs to add or maintain English 单词/词汇/短语/句型 pages for primary-knowledge-site or similar static HTML/CSS/JS sites, including three-column English/中文/音标 vocabulary tables, generated missing Chinese meanings or phonetics, TTS read buttons, dictation mode, site navigation entries, and maintenance documentation.
---

# English Vocabulary HTML

## Purpose

Create static English vocabulary study pages that match the existing `primary-knowledge-site` style: unit navigation, three-column `English / 中文 / 音标` vocabulary tables, per-row TTS buttons, temporary dictation mode, and clear maintenance records.

Use this skill for vocabulary, word, phrase, and sentence-pattern pages. Use broader textbook-page skills only for full lesson texts, dialogues, or sentence-by-sentence translation pages.

## Workflow

1. Inspect the project before editing.
   - Read `README.md`, `SITE_MAINTENANCE.md`, and the target subject page such as `subjects/english/index.html`.
   - Read an existing vocabulary page first, preferably `subjects/english/grade-5/second/words/index.html`.
   - Read `assets/js/textbook-reader.js` and `assets/css/site.css` if changing shared behavior or styles.

2. Normalize the vocabulary source.
   - Group by Unit and preserve source order.
   - Treat words, phrases, fixed expressions, and sentence patterns as vocabulary rows.
   - Every vocabulary row must have three visible columns: `English`, `中文`, and `音标`.
   - English is required. Do not create a vocabulary row when the English item is missing or cannot be recovered from the source.
   - If Chinese is provided, use the provided Chinese exactly except for obvious OCR spacing or punctuation cleanup.
   - If Chinese is missing, add a concise, student-friendly Chinese meaning based on the English item.
   - If phonetics are provided, use the provided phonetics exactly except for obvious OCR cleanup.
   - If phonetics are missing, add common learner-friendly phonetics based on the English item. Keep one transcription style consistent within the page, preferably IPA wrapped in slashes such as `/ɡet ʌp/`.
   - For multi-word phrases, add phrase-level phonetics when practical. For sentence patterns with blanks or ellipses, add the spoken parts clearly and keep placeholders readable.
   - Preserve useful notes such as plural forms or grammar hints in the Chinese meaning.
   - Convert obvious OCR punctuation issues, but do not silently change uncertain content.
   - Mention materially generated or uncertain Chinese/phonetic additions in the final response.

3. Create or update the page.
   - Use site-root asset paths such as `/assets/css/site.css` and `/assets/js/textbook-reader.js`.
   - Use the shared site shell instead of copying header/footer HTML.
   - Do not add a `data-section-back` “返回英语” link on English content pages; the top navigation already links to `/subjects/english/`.
   - Use the same vocabulary page structure as the current site.
   - Do not use `<details>` or folded Unit sections unless the user explicitly asks.
   - Keep Google TTS/local TTS handled by `assets/js/textbook-reader.js`; do not embed duplicate TTS scripts in the page.

4. Integrate the page.
   - Add the page link to `subjects/english/index.html` when creating a new vocabulary page.
   - Update `README.md` if the current actual page list changes.
   - Always update `SITE_MAINTENANCE.md` for new pages, structure changes, shared JS/CSS changes, and count changes.

5. Validate before final response.
   - Check JS syntax if shared scripts changed.
   - Check Unit count, row count, read button count, and dictation markers.
   - Check that every vocabulary row has non-empty English, Chinese, and phonetic cells.
   - Check site-root paths.
   - Check local HTTP `200 OK` if a local static server is available.

## Page Contract

For `primary-knowledge-site`, place vocabulary pages at:

```text
subjects/english/grade-{grade}/second/words/index.html
```

Use this head/body shell:

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="广州英语三年级下册 Unit 1-8 单词词汇、短语和句型">
  <title>三年级下学期英语单词 | 小学知识点</title>
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/css/site.css">
  <script src="/assets/js/site-shell.js" defer></script>
</head>
<body data-nav="english">
  <div data-site-header></div>
  <main class="reader-shell vocab-shell">
    ...hero, reader tools, unit nav, dictation panel, vocabulary units...
  </main>
  <div data-site-footer></div>
  <button class="back-top" type="button" id="topButton" aria-label="返回顶部">顶部</button>
  <script src="/assets/js/textbook-reader.js" defer></script>
</body>
</html>
```

## Hero And Tools

Use a compact hero with grade/semester/type, title, summary, and stats:

```html
<section class="reader-hero" aria-labelledby="reader-title">
  <div>
    <p class="kicker">三年级 · 下学期 · 单词</p>
    <h1 id="reader-title">广州英语三年级下册单词词汇</h1>
    <p>Unit 1-8 | 按单元整理 | 支持逐词朗读</p>
  </div>
  <div class="reader-stats" aria-label="词汇统计">
    <span>8 个 Unit</span>
    <span>227 条</span>
  </div>
</section>

<div data-reader-tools></div>
```

Place dictation mode after `reader-unit-nav` for vocabulary pages in this site, so the active tray can stay sticky below the Unit navigation:

```html
<section class="dictation-panel" data-dictation aria-label="听写模式">
  <div class="dictation-toolbar">
    <button class="dictation-toggle" type="button" data-dictation-toggle aria-expanded="false" aria-pressed="false" aria-controls="dictationTray">听写</button>
  </div>
  <div class="dictation-tray" id="dictationTray" data-dictation-tray hidden tabindex="-1" aria-label="听写词汇"></div>
</section>
```

`textbook-reader.js` handles the behavior: clicking vocabulary terms in dictation mode appends numbered chips, clicking chips deletes them, and deleting earlier chips renumbers later chips. `assets/css/site.css` keeps the active dictation panel sticky below the Unit navigation. Do not persist dictation content across reloads.

## Unit Navigation

Use sticky Unit navigation with page anchors:

```html
<nav class="reader-unit-nav" aria-label="单元导航">
  <a href="#unit-1">Unit 1</a>
  <a href="#unit-2">Unit 2</a>
</nav>
```

Match anchor IDs with each Unit article: `id="unit-1"`, `id="unit-2"`, and so on.

## Vocabulary Table Markup

Use one `article.reader-unit.vocab-unit` per Unit:

```html
<article class="reader-unit vocab-unit" id="unit-1">
  <header class="reader-unit-header">
    <p>Unit 1 · 23 个词汇/短语</p>
    <h2>Get Up</h2>
  </header>
  <div class="vocab-table-wrap">
    <table class="vocab-table">
      <thead>
        <tr><th>English</th><th>中文</th><th>音标</th></tr>
      </thead>
      <tbody>
        <tr>
          <td>
            <div class="vocab-word">
              <span>get up</span>
              <button class="read-btn" type="button" title="朗读" aria-label="朗读：get up" data-text="get up"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 3.5v13l11-6.5-11-6.5z"></path></svg></button>
            </div>
          </td>
          <td>起床</td>
          <td class="phonetic">/ɡet ʌp/</td>
        </tr>
      </tbody>
    </table>
  </div>
</article>
```

Rules:
- Put the spoken English in `data-text`.
- Use `data-text` without markup and without Chinese.
- Keep a `button.read-btn` for every vocabulary row.
- Count vocabulary rows by `<tr>` rows in `<tbody>`, not by Unit headers.
- Escape HTML-sensitive characters in English, Chinese, and phonetic text.
- Prefer `...` in English pattern text only when the source uses blanks or ellipses.
- Do not use `-` or an empty muted placeholder for missing Chinese or phonetics unless the English item is genuinely not pronounceable; if that rare case occurs, call it out in the final response.

## Shared JS/CSS Contract

Reuse these shared files:
- `assets/js/site-shell.js`: header, nav, footer, back link, voice selector, stop button.
- `assets/js/textbook-reader.js`: read buttons, TTS, translation behavior for text pages, dictation mode for vocabulary pages, back-to-top.
- `assets/css/site.css`: reader layout, vocabulary tables, sticky navigation, dictation styles.

When adding dictation to a vocabulary page, only add the `data-dictation` panel if the shared CSS/JS already supports it. If not, implement support once in shared files and document it in `SITE_MAINTENANCE.md`.

## Content Quality

- Preserve provided English, Chinese, and phonetic content whenever it is credible.
- Fill missing Chinese meanings and phonetics instead of leaving blanks.
- Keep generated Chinese meanings concise and suitable for primary-school learners.
- Keep generated phonetics consistent across the page and avoid mixing IPA, respelling, and dictionary variants without a reason.
- Do not translate source content loosely when a concise textbook-style Chinese meaning exists.
- Keep source unit titles if available.
- If a source image has left/right cards for the same Unit, merge them into one Unit in source order: words first if the source presents them first, then phrases/sentence patterns.
- If a phrase and a single word duplicate meaning, keep both when both appear in the source.
- Mention any uncertain OCR, translation, phonetic transcription, or interpretation in the final response.

## Maintenance Updates

For a new vocabulary page, update:

- `subjects/english/index.html`: add a content card.
- `README.md`: add the page under current actual pages if it is a major page.
- `SITE_MAINTENANCE.md`: update current directory, current pages, vocabulary page conventions if changed, and the dated change log.

Do not add a concrete grade/semester page to the top site nav. Top nav should remain high-level, such as `首页` and `英语`.

## Validation Checklist

Run practical checks before final response:

```powershell
node --check assets\js\site-shell.js
node --check assets\js\textbook-reader.js
```

Check the new/updated vocabulary page:

```powershell
$html = [System.IO.File]::ReadAllText('subjects\english\grade-3\second\words\index.html', [System.Text.Encoding]::UTF8)
[regex]::Matches($html, 'class="reader-unit vocab-unit"').Count
[regex]::Matches($html, 'class="read-btn"').Count
[regex]::Matches($html, '<details\b').Count
$html.Contains('data-dictation')
```

Check that vocabulary table rows have three meaningful columns:

```powershell
$rows = [regex]::Matches($html, '<tbody>[\s\S]*?</tbody>') | ForEach-Object { [regex]::Matches($_.Value, '<tr>[\s\S]*?</tr>') } | ForEach-Object { $_ }
$badRows = foreach ($row in $rows) {
  $cells = [regex]::Matches($row.Value, '<td[^>]*>([\s\S]*?)</td>')
  if ($cells.Count -ne 3 -or ($cells | Where-Object { ($_.Groups[1].Value -replace '<[^>]+>', '').Trim() -eq '' })) { $row.Value }
}
$badRows.Count
```

Check root paths:

```powershell
$files = Get-ChildItem -Recurse -Filter *.html
Select-String -Path $files.FullName -Pattern '(href|src)="(?!/|#|https?:|mailto:)'
```

Check local HTTP when a server is running:

```powershell
curl.exe -I http://127.0.0.1:8080/subjects/english/grade-3/second/words/
```

Final response must include result summary, output paths, validation performed, and any limitations such as Google TTS requiring network access.