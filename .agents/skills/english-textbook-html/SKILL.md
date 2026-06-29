---
name: english-textbook-html
description: Create interactive HTML study pages from English textbook lessons, unit-based passages, pasted textbook text, OCR text, screenshots, English-only source text, or mixed English and Chinese source material. Use when Codex needs to format English textbook passages, generate missing Chinese translations from English, review or improve Chinese translations, add sentence-level TTS reading, hide or reveal translations, infer speakers in dialogue lessons, create printable and mobile-friendly textbook study pages, or produce reusable English learning HTML for different grades or semesters.
---

# English Textbook HTML

## Purpose

Turn English textbook lesson content into a polished, offline-friendly HTML study page for students. Prioritize readable unit structure, accurate sentence-to-translation mapping, generated Chinese translations when they are missing, click-to-reveal translations, and sentence-level TTS.

## Workflow

1. Inspect the source content first.
   - Identify units, titles, dialogues, prose passages, letters, lists, vocabulary sections, and exercises.
   - Fix obvious encoding artifacts when possible. If Chinese translations are missing, corrupted, incomplete, or unreliable, translate or retranslate from the English instead of leaving blanks or preserving bad text.
   - If the source lacks speaker labels in a dialogue, infer names from context only when clear. Leave neutral narration unlabeled when no reliable speaker exists.

2. Normalize the lesson structure.
   - Keep content grouped by unit.
   - For dialogue lessons, combine consecutive lines by the same speaker unless a line break is needed for meaning or layout.
   - For prose lessons, keep paragraph flow natural, but maintain sentence-level mapping internally.
   - Split into complete English sentences for TTS, not arbitrary visual lines.
   - Ensure every English sentence has a matching Chinese translation before rendering.

3. Review and improve translations.
   - Make Chinese translations natural, accurate, and student-friendly.
   - When the source provides English text but no Chinese translation, generate a Chinese translation from the English sentence or paragraph.
   - Keep translation granularity aligned with English sentence granularity.
   - Avoid over-literal translations when a clearer textbook-style translation is better.
   - Preserve provided credible translations, but fill missing translation entries rather than using placeholders such as `-`, empty strings, or untranslated English.
   - If an item is ambiguous, prefer a conservative translation and mention uncertainty in the final response.

## HTML Requirements

Create a single responsive HTML file unless the user asks for another format.

Required UI behavior:

- Unit navigation near the top.
- A voice selector with one fixed first option: `Google TTS（在线固定）`.
- Append browser/device-provided English voices after the fixed Google TTS option.
- Default to Google TTS.
- One read button after every complete English sentence.
- Translation text is hidden/blurred by default.
- Every complete English sentence must have one corresponding Chinese translation, either supplied by the source or generated from the English when missing.
- Clicking or touching an English sentence reveals only its corresponding translation.
- Clicking or touching a translation also reveals it.
- When focus leaves the revealed translation/line, hide it again.
- Keep translations in the same paragraph/flow as their English paragraph when possible, rather than placing every translation on a new line.
- Add a floating back-to-top button that appears after scrolling.
- Make the page mobile/tablet/desktop responsive and print-friendly.

Recommended implementation pattern:

- Store each unit as structured data, not as raw HTML strings.
- For each sentence, keep `{ speaker, english, translation }` or tuple-equivalent data; do not render an English sentence with an empty translation value.
- Group consecutive items with the same speaker at render time.
- Give English sentence chunks and translation buttons matching `data-index` values inside each paragraph/line.
- On English click, reveal and focus the matched translation; on translation focusout, remove visible/highlight classes.
- Keep the read button click separate from the English click if practical: the button should read, while the sentence click should reveal.

## TTS Pattern

Use the fixed Google TTS option plus local Web Speech API voices.

Google TTS pattern:

```js
const GOOGLE_TTS_VALUE = "__google_tts__";
const url = `https://tts.keepme.xyz/translate_tts?ie=UTF-8&client=tw-ob&q=${encodeURIComponent(text)}&tl=en`;
const audio = new Audio(url);
audio.play();
```

Local TTS pattern:

```js
const voices = window.speechSynthesis.getVoices();
const englishVoices = voices.filter((voice) => /^en/i.test(voice.lang));
const utterance = new SpeechSynthesisUtterance(text);
utterance.rate = 0.86;
window.speechSynthesis.speak(utterance);
```

Implementation rules:

- Stop any current Google audio and any current `speechSynthesis` utterance before starting a new sentence.
- The stop button must stop both audio paths.
- If Google TTS fails because of network or browser policy, show a concise status message suggesting local TTS.
- If no local TTS is available, keep Google TTS usable.

## Output and Versioning

Follow the user's project/output rules. If no project path is specified, put generated artifacts under a same-day `YYYY-MM-DD` directory.

For revisions to an existing output, append a version suffix instead of overwriting the formal deliverable: `_v2`, `_v3`, `_v4`, etc.

Keep useful deliverables:

- Main HTML file.
- Optional preview screenshot if visual QA is performed.

Treat files such as `*_dom.html`, `*_test.html`, and `*_test_dom.html` as validation artifacts, not final deliverables. Mention that they can be deleted if created.

## Validation Checklist

Before final response, validate what is practical:

- JavaScript syntax parses successfully.
- Browser-rendered DOM contains the expected unit count.
- Read button count equals the sentence count.
- Translation item count equals the sentence count.
- No translation item is empty, placeholder-only, or still English when Chinese was missing from the source.
- Voice selector contains the fixed Google TTS option first and local voices after it.
- English-click reveal shows exactly one matching translation.
- Focus leaving the translation hides it again.
- Back-to-top button exists.
- No obvious mojibake remains, such as `鈥`, `檚`, `锛`, `鐪`, or replacement characters.

Final response should include: result summary, output path, validation performed, whether missing Chinese translations were generated, and any limitations such as Google TTS requiring network access.
