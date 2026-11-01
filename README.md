# Jazz Music in Prewar Japan and Its Concept
### 戦前の日本におけるジャズ音楽とその概念

A master's thesis by **Larry B. Richards Jr.**, submitted to the Department of
Musicology, Faculty of Music, **Tokyo University of the Arts** (東京芸術大学),
enrolled 1990. This repository digitizes the original from a scan into two clean,
rebuildable LaTeX editions: the Japanese original and an English translation.

## Read / download

| Edition | PDF |
| --- | --- |
| 日本語（原文, 48 pp.） | [**pdf/lr_thesis_ja.pdf**](pdf/lr_thesis_ja.pdf) |
| English (42 pp.) | [**pdf/lr_thesis_en.pdf**](pdf/lr_thesis_en.pdf) |

GitHub renders each PDF in the browser (click to read); use the **Download**
button on the file page to save it.

## About the editions

- The source was a scanned copy of the original 1990s typescript. Its text was
  re-typeset faithfully; the five hand-drawn musical examples and the original
  degree-submission / examination routing sheet (論文審査回覧表) are reproduced as
  figures.
- Japanese is set in **Hiragino Mincho ProN** (the family the original used),
  Latin text in a Times-like face, via **LuaLaTeX + luatexja**.
- The English edition is a translation produced by Claude (Anthropic), noted on
  its title page.

## Repository layout

```
pdf/                 the two finished PDFs
latex_ja/            Japanese edition — preamble, title/TOC driver, body, bibliography
latex_en/            English edition  — same structure
figures/             extracted & deskewed musical scores + the approval-sheet facsimile
  orig/              the figures before skew correction (provenance)
transcript/          editable Markdown masters + the Markdown→LaTeX converters
  merged_ja.md       Japanese master text (edit here, then `make regen`)
  merged_en.md       English master text
  md2tex.py          converter: merged_ja.md → latex_ja/body_ja.tex + bib_ja.tex
  md2tex_en.py       converter: merged_en.md → latex_en/body_en.tex + bib_en.tex
  en/GLOSSARY.md     translation terminology & conventions
Makefile             build targets
```

## Building

Requires TeX Live (with `luatexja`) and the Hiragino Mincho ProN font
(`HiraMinProN-W3` / `-W6`), as shipped on macOS.

```sh
make            # build both PDFs into pdf/
make ja         # Japanese only
make en         # English only
make regen      # regenerate body/bib from the Markdown masters, then build
```

To revise wording, edit `transcript/merged_ja.md` (or `merged_en.md`) and run
`make regen`.

## Credits

Original thesis © Larry B. Richards Jr. Examiners: Tsuge Gen'ichi (chief adviser),
Katayama Chikako, Kamisangō Yūkō. Digitization, figure extraction, and the
English translation were done with Claude (Anthropic).
