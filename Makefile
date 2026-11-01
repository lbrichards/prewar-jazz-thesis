# Build both editions with LuaLaTeX. Requires TeX Live (luatexja) and the
# Hiragino Mincho ProN font (HiraMinProN-W3/W6), as on macOS.
#
#   make            build both PDFs into pdf/
#   make ja         build the Japanese edition only
#   make en         build the English edition only
#   make regen      regenerate body_*/bib_* from the Markdown masters, then build
#   make clean      remove LaTeX intermediates

LATEXMK = latexmk -lualatex -interaction=nonstopmode -halt-on-error

.PHONY: all ja en regen clean
all: ja en

ja:
	cd latex_ja && $(LATEXMK) thesis_ja.tex
	cp latex_ja/thesis_ja.pdf pdf/lr_thesis_ja.pdf

en:
	cd latex_en && $(LATEXMK) thesis_en.tex
	cp latex_en/thesis_en.pdf pdf/lr_thesis_en.pdf

# Rebuild the generated body_*/bib_* .tex from the editable Markdown masters.
regen:
	cd transcript && python3 md2tex.py && python3 md2tex_en.py
	$(MAKE) all

clean:
	cd latex_ja && latexmk -C >/dev/null 2>&1 || true
	cd latex_en && latexmk -C >/dev/null 2>&1 || true
	rm -f latex_ja/*.png latex_en/*.png
