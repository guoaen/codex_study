---
name: english-pdf-story-html
description: Create or update static HTML reader pages from illustrated English story PDFs, leveled readers, Little Fox PDFs, or similar PDF picture books. Use when Codex needs to extract PDF text, preserve page illustrations, reconstruct article or dialogue reading order from visual/story context, generate missing Chinese translations, build sentence-level TTS/translation HTML pages, add Little Fox or story-series hierarchy pages, update primary-knowledge-site navigation/list pages, and validate image-backed reader pages.
---

# English PDF Story HTML

## Overview

Create illustrated English reader pages from PDF stories. Preserve the PDF artwork as page images, extract or transcribe the English text, reconstruct the correct reading order from visual and story context, add Chinese translations when missing, and integrate the result into a static HTML/CSS/JS site that already has shared navigation and reader tooling.

This skill is designed for `primary-knowledge-site`, but the extraction and page-assembly workflow can be adapted to similar static sites.

## Workflow

1. Read the target site's maintenance docs before editing. For `primary-knowledge-site`, read `AGENTS.md`, `README.md`, `SITE_MAINTENANCE.md`, then inspect `assets/js/site-shell.js`, `assets/css/site.css`, and one existing reader page.
2. Copy the source PDF into a local temp/work directory. If the PDF is on a network share or outside the sandbox, request the needed permission and never modify the original PDF.
3. Extract text and render page images. Prefer the bundled script `scripts/extract_pdf_story_assets.py`; use other PDF tools only if the script cannot handle the file.
4. Decide which rendered pages belong in the published story. Keep cover and story illustration pages. Skip genuinely blank pages and optional copyright/back-matter pages unless the user asks to keep them.
5. Reconstruct the article or dialogue order from the rendered page image and story context. Treat extracted text as raw material, not as final order.
6. Build a story data model before writing HTML: page id, label, title, image filename, ordered English lines, Chinese translations, and alt text.
7. For `primary-knowledge-site` Little Fox stories, prefer the bundled JSON-driven builder `scripts/build_little_fox_story_page.py` after extraction. Use a temporary generator script only when the builder cannot express the needed page.
8. Generate missing Chinese translations from the English text when the PDF does not provide them. Keep translations natural, concise, and suitable for primary-school readers.
9. Create or update the site hierarchy. For Little Fox content, use a second-level page such as `/subjects/little-fox/`, a series page such as `/subjects/little-fox/wizard-and-cat/`, and a story page below the series.
10. Copy final images into a stable asset folder using site-root paths, for example `/assets/images/little-fox/<series>/<story>/page-01.png`.
11. Update shared navigation, homepage cards, list pages, README, and maintenance docs when the page hierarchy changes.
12. Validate the result before reporting completion.
13. After successful validation, delete the `.tmp` scratch directory created for the task. Before deleting, resolve the path and confirm it is inside the current project root and contains only task-specific temporary PDFs, extracted assets, and generation/validation scripts. If `.tmp` contains unrelated user files or shared scratch data, do not delete it; report what remains.

## PDF Extraction

Use the helper script from this skill directory:

```powershell
python "<english-pdf-story-html-skill-dir>\scripts\extract_pdf_story_assets.py" `
  --pdf "C:\path\to\story.pdf" `
  --out ".tmp\story-assets" `
  --scale 2 `
  --skip-blank-pages
```

The script creates:

- `images/page-XX.png`: rendered PDF pages.
- `extracted-text.txt`: readable text grouped by page.
- `pages.json`: page metadata, character counts, image sizes, and blank-page guesses.

If text extraction returns empty text for story pages, inspect the rendered images and use OCR or manual transcription. Do not invent English text.

## Reading And Dialogue Order

PDF text extraction often follows internal object order, not the order a child should read the page. Never paste extracted lines into the HTML blindly.

Use this process for each page:

- Inspect the rendered page image when the page has speech bubbles, captions, panels, separated text boxes, or unusual layout.
- Follow visual reading order first: panel sequence, top-to-bottom and left-to-right layout for English pages, speech-bubble placement, bubble tails, character gaze, and caption placement.
- Follow story logic when visual order is ambiguous: question before answer, interruption before response, teacher instruction before student apology, cause before consequence, pronoun references after their antecedents.
- Rejoin words or sentences split by PDF line wrapping, for example `I taught Snooks a` + `new trick!` becomes one sentence.
- Split incorrectly combined extraction blocks into separate dialogue turns when the page clearly has multiple speakers or bubbles.
- If extracted order conflicts with the image or the dialogue logic, reorder the text to match the intended reading sequence.
- If speaker names are not printed, do not invent labels unless the site pattern requires them. Use the dialogue order itself and keep lines separate.
- If a sequence cannot be determined after inspecting image and context, preserve the safest visible order and mention the uncertainty in the final reply or ask the user for the page/order.

Before writing HTML, read the ordered English lines aloud mentally. The sequence should sound like a coherent story, not a dump of PDF text objects.

## Primary Knowledge Site Builder

For repeated Little Fox story additions in `primary-knowledge-site`, avoid rewriting a full HTML generator. Create a compact `.tmp/<story>.json` story model and run the bundled builder:

```powershell
python .agents\skills\english-pdf-story-html\scripts\build_little_fox_story_page.py `
  --project . `
  --data .tmp\<story>.json `
  --asset-source .tmp\<story>-assets\images
```

The JSON must include `title`, `slug`, `series_title`, `series_slug`, `level`, `story_number`, and `pages`. Each page needs `title` and `lines`, where each line is `[english, chinese]`. The builder copies `page-01.png` as `cover.png`, maps story pages from `page-02.png` onward, writes the story HTML, and updates the homepage, Little Fox list, series page, README, and `SITE_MAINTENANCE.md` idempotently.

Use targeted context reads for unchanged repeated work: inspect the series page, one recent story page header/body sample, and relevant CSS selectors instead of loading full CSS or every existing story page.
## HTML Generation On Windows

When generating pages with large HTML strings, avoid passing big templates through `python -c`, long PowerShell command arguments, or nested quoted one-liners. Windows command-line parsing can strip or reinterpret quotes inside HTML attributes, JavaScript, SVG snippets, and apostrophes, causing broken generated files or failed scripts.

Use this safer pattern:

1. Put the page data and HTML-generation code in a temporary script file such as `.tmp/generate_<story_slug>_site.py`.
2. Write output files from that script using UTF-8 without BOM and explicit newline handling.
3. Execute the script as a file: `python .tmp\generate_<story_slug>_site.py`.
4. Run validation after generation before deleting or ignoring the temporary script.

This rule is especially important when the generated HTML contains:

- Chinese text or translations.
- Smart quotes, apostrophes, em dashes, SVG markup, or HTML attributes with quoted values.
- Large lists of story pages, reader lines, image references, or translation buttons.

Small one-line inspections with `python -c` are fine. Do not use `python -c` for large generated HTML or multi-page site-writing scripts.

## HTML Page Pattern

Use existing site classes and scripts instead of creating a separate UI system:

```html
<body data-nav="little-fox">
  <div data-site-header></div>
  <main class="reader-shell story-shell">
    <section class="reader-hero" aria-labelledby="reader-title">...</section>
    <div data-reader-tools></div>
    <nav class="reader-unit-nav" aria-label="故事页面导航">...</nav>
    <section class="reader-units story-units" aria-label="故事正文">
      <article class="reader-unit story-page" id="page-1">
        <header class="reader-unit-header">...</header>
        <div class="reader-unit-body story-layout">
          <figure class="story-figure">
            <img src="/assets/images/.../page-01.png" alt="..." loading="lazy">
          </figure>
          <div class="story-text">
            <div class="reader-line">...</div>
          </div>
        </div>
      </article>
    </section>
  </main>
  <div data-site-footer></div>
  <button class="back-top" type="button" id="topButton" aria-label="返回顶部">顶部</button>
  <script src="/assets/js/textbook-reader.js" defer></script>
</body>
```

For each ordered English line:

- Put the visible sentence in `.sentence`.
- Put the same clean text in the read button's `data-text`.
- Add a matching `.translation` button.
- Use matching `data-index` values when a single line has multiple sentence chunks.

## Site Integration Rules

- Use site-root URLs for all internal `href` and `src` values: `/assets/...`, `/subjects/...`.
- Keep shared header/nav/footer in `assets/js/site-shell.js`; do not paste nav HTML into individual pages.
- Add a top navigation item only for a major second-level entry the user expects to access directly.
- Do not add old “返回英语” style links when the top navigation already gives the needed route.
- If adding Little Fox content, update `subjects/little-fox/index.html`. If adding a new story in an existing series, update only that series page unless the homepage copy also needs to change.
- Keep story-page CSS in the shared stylesheet when it can be reused by future PDF stories.

## Translation Guidance

- If Chinese is present in the source, preserve it unless it is clearly OCR-corrupted.
- If Chinese is missing, translate from English. Favor simple, child-friendly Chinese over overly literal phrasing.
- Keep names consistent across the story.
- Preserve classroom/story context and punctuation such as questions and exclamations.
- Translate after the English order has been reconstructed, so Chinese follows the same story logic.

## Validation Checklist

Run these checks before finishing:

- `node --check assets/js/site-shell.js` if navigation or shell changed.
- `node --check assets/js/textbook-reader.js` if reader behavior changed.
- Count `.read-btn` and `.translation`; they should match for the story text.
- Count story page articles and image references; every referenced image must exist.
- Review at least ambiguous dialogue pages against rendered images to confirm the English line order follows story logic.
- Search for Unicode replacement characters and common mojibake fragments; the search should return no unexpected matches.
- Check all local `href` and `src` values are site-root paths or page anchors.
- Verify changed pages return `200 OK` under a local static server.
- When practical, render a browser screenshot to confirm images, sticky nav, and layout appear.

Final replies should summarize changed files, output URLs, validation results, and any limitations such as OCR uncertainty, ambiguous dialogue order, skipped blank/copyright pages, or temporary generation scripts left in the workspace. Do not paste the full copyrighted story text into chat; point to the local page instead.