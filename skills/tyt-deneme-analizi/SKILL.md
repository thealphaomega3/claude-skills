---
name: tyt-deneme-analizi
description: Turn a Turkish student's TYT (or similar YKS/LGS) exam-tracking Excel sheet into a rich, designed, Turkish-language visual analysis page published as an Artifact. The sheet has topic rows, one column per mock exam (deneme), "X" marks for missed questions, and a per-subject "toplam" row of correct answers. Use this whenever the user points at a "TAKİP" / "TYT AYRINTI" style xlsx, asks to graph or visualize a student's deneme results, wants subject or topic progress over time, most-missed konular, or a general overview (karne) of a student's exam year, even if they only say "grafiğe dök", "görselleştir" or "bu öğrencinin denemelerini analiz et".
---

# TYT deneme analizi

Turns the tracking sheet into a designed Turkish page. Two styles ship with the skill; pick with `--style`:

- `optik` (default): "Bir Yılın Optiği". Optik-form look, pink drop-out ink + pencil graphite. Built for long histories (100+ exams, several period blocks).
- `defter`: "Deneme Defteri". Kareli defter in light theme, yazı tahtası in dark theme, hand-drawn charts via rough.js, çetele (tally) marks and red-pen X map. Built for short or current sheets (roughly 5-40 exams, one block). Sections: karne cards, a hand-drawn radar comparing each subject's first half vs second half of exams (the stand-in for first vs last period when there is only one block) + sticky notes, per-subject hand-drawn line charts with value labels, full-exam stacked bars + per-exam success line, tally of most-missed topics, X map of topic x exam.

If the user asks for "a different style", do not reuse either template as is: design a new one from scratch (new concept, fonts, palette), keep the same data model, and save it as `assets/template-<name>.html` with a matching `--style` choice.

The page and all copy are in Turkish.

## What the optik page contains

- Header strip styled like an optik form: exam count, missed questions, best full exam /120.
- Hero: every exam as a bubble column, every subject as a row; fill = success, pink = under 70%.
- A. Karne: radar of first vs last period per subject, key numbers, 4 finding cards.
- B. Genel gelişim: per-exam Türkçe+Mat+Fen total (/100) with rolling average, full /120 rings where all 9 subjects exist, plus field-level (Türkçe, Matematik, Fen, Sosyal) period lines.
- C. One small chart per subject: each exam as a dot, 9-exam rolling average, first-to-last delta chip.
- D. Topic x period heatmap (tabs per subject): missed questions per 10 exams.
- E. Top 16 most-missed topics and a 1-dot-per-question waffle of all misses.
- F. Publisher difficulty dot plot (only for exams where a publisher is written).

## Sheet model (read this before trusting any number)

- Sheets vary: an older one had 7 blocks and 193 exams, a newer "TAKİP TASLAK" draft had 1 filled block, 18 exams, no sosyal, and math only in the first 6 exams. The builder handles both; a subject may cover only some exams.
- Each column is ONE full TYT exam shared by all subjects. A blank subject cell in a column means that subject was not recorded for that exam. The user corrected this once: never count subject-rows as separate exams.
- The sheet has several side-by-side blocks. Each block begins with a label column (topic names). Blocks are treated as chronological periods D1..Dn, left to right, because the sheet has no dates. Say this assumption on the page and in the reply.
- A subject's "total" row holds integer correct counts. Columns with float totals are block averages ("ORTA") and are skipped.
- "X", "XX", "XXX" in a topic cell = that many questions missed. Wrong and blank are not separated, so show doğru, never net.
- Free text inside a subject's cells ("3D", "APOT", "MSÜ", "mebi") is the publisher.

## Workflow

1. Find the file (usually `~/Downloads/TAKİP TYT ....xlsx`; list with `ls ~/Downloads | grep -i tak`). The tab is typically named "TYT AYRINTI".
2. openpyxl is usually missing. Make a venv in the scratchpad: `python3 -m venv v && v/bin/pip -q install openpyxl`.
3. Run the builder. It auto-detects label columns, total rows, subjects, average columns, publishers, and normalizes topic names:
   ```bash
   v/bin/python ~/.claude/skills/tyt-deneme-analizi/scripts/build_page.py "<xlsx>" "<workdir>/tyt-optik.html" --json data.json
   ```
   Pass `--sheet "<name>"` if the tab name differs.
4. Read the printed summary and sanity-check it: exam count ≈ number of exam columns, 9 subjects named, per-period percentages plausible, TYT maxima (Tür 40, Mat 40, Fiz 7, Kim 7, Biy 6, Tar/Coğ/Fel/Din 5). A `warn: could not name section` line means a subject was not recognized; extend `SUBJECT_HINTS` in the script. Unmapped topic labels pass through as written; add ugly ones to `CANON`.
5. Review the copy. Optik: the finding cards in `fillStats()`; defter: `lede` and the sticky notes in `drawKarne()`. Four optik cards name specific topics (paragraf in Türkçe, problemler and olasılık in matematik, optik and dalgalar in fizik) because they were true for the original student. If the summary shows a different story, rewrite those cards and the `lede` text from the actual top misses and biggest deltas. Keep claims checkable against the data.
6. Look once at the rendered page. The Artifact skeleton is added at publish time, so for a local preview wrap the file in `<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>…</body></html>` and serve it with a tiny `python3 -m http.server` preview (file:// URLs may be refused). Check for clipped labels at the right edges of the heatmap and publisher chart.
7. Publish with the Artifact tool (`icon: "chart"`, one-sentence Turkish description). Reply in Turkish with the link, what each section shows, 3-4 headline findings, and the assumptions (period order, doğru not net, subjects that stop being tracked).

## Style rules for this user

- All page copy and the reply in Turkish, natural phrasing, Turkish number format (`36,7`, `%94`, `1.673`).
- No em dash anywhere, use "-".
- Within a style, keep its identity. Optik: Big Shoulders Display / Onest / IBM Plex Mono, ink `#C8365C`. Defter: Caveat / Kalam / Atkinson Hyperlegible, ballpoint blue, red pen, highlighters. Subject colors stay fixed across styles (Türkçe orange, Matematik blue, fen teal/violet/green, sosyal earth tones).
- Check that any new font has a `latin-ext` subset on Google Fonts, or Turkish letters (ş ğ ı İ) fall back.

## Files

- `scripts/build_page.py`: xlsx → JSON → HTML. Its docstring restates the sheet model.
- `assets/template-optik.html`: optik page (D3 7.9.0 from cdnjs). Data goes in at `__DATA__`.
- `assets/template-defter.html`: defter page (rough.js 4.6.6 from jsdelivr; colors are resolved from CSS tokens at draw time and everything redraws on theme change, because SVG attributes cannot read `var()`). Its lede and sticky notes name geometri, paragraf, biyoloji and fen from the first sheet it was made for; rewrite them in step 5 like the optik findings.
- Trend words ("yükseliyor", "düşüyor") must agree across charts: the defter page only calls a trend when the regression slope and the first-half vs second-half change point the same way and the change is at least 3 points. With few exams a slope alone is usually noise.
- Every chart derives from the JSON, so a new sheet only needs the copy review in step 5.
