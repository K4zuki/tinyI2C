# include Makefile.win
include Makefile.in

MDDIR:= doc
DATADIR:= doc/data
TARGETDIR:= doc/Out
GUIDESIGNDIR:= gui
GUIDESIGN:= $(GUIDESIGNDIR)/tinyI2Cgui.py
GUIBUILDDIR:= build
GUIDISTDIR:= dist
GUIBINARY:= $(GUIDISTDIR)/TinyI2C$(EXE)

INPUT:= README.md
OUTPUT:= $(shell basename $(INPUT) .md)
# CSV:= $(shell cd $(DATADIR); ls *.csv)
TABLES:= $(CSV:%.csv=$(TARGETDIR)/%.tmd)
FILTERED= $(INPUT:%.md=$(TARGETDIR)/%.fmd)
HTML:=$(TARGETDIR)/$(OUTPUT).html
DOCX:=$(TARGETDIR)/$(OUTPUT).docx

PANFLAGS += --toc
PANFLAGS += --listings
PANFLAGS += --number-sections --highlight-style=pygments
PANFLAGS += -M localfontdir=$(FONTDIR)

.PHONY: docx html filtered tables pdf tex merge gui clean

all: mkdir html

gui: $(GUIBINARY)
$(GUIBINARY): $(GUIDESIGN)
	pyinstaller --noconsole -p python/ gui/main.py --onefile --clean --name TinyI2C

$(GUIDESIGN):
	pyuic4 tinyI2C.ui -o $(GUIDESIGN)

docx: $(DOCX)
$(DOCX): $(HTML)
	$(PANDOC) --reference-docx=$(REFERENCE) $(HTML) -o $(TARGETDIR)/$(OUTPUT).docx; \
	$(PYTHON) $(DOCXPWRTR) -I $(MDDIR)/$(INPUT) -O $(DOCX)

html: $(HTML)

$(HTML): $(TABLES) $(FILTERED)
	$(PANDOC) $(PANFLAGS) --self-contained -thtml5 --template=$(MISC)/github.html \
		$(FILTERED) -o $(HTML)

pdf: tex
	xelatex --output-directory=$(TARGETDIR) --no-pdf $(TARGETDIR)/$(TARGET).tex; \
	cd $(TARGETDIR); \
	rm -f ./images; \
	ln -s ../images; \
	xelatex $(TARGET).tex

tex: merge
	$(PANDOC) $(PANFLAGS) --template=$(MISC)/CJK_xelatex.tex --latex-engine=xelatex \
		$(TARGETDIR)/$(TARGET).md -o $(TARGETDIR)/$(TARGET).tex

merge: filtered
	cat $(FILTERED) > $(TARGETDIR)/$(TARGET).md

filtered: tables $(FILTERED)
$(FILTERED): $(MDDIR)/$(INPUT)
	cat $< | $(PYTHON) $(FILTER) --out $@

tables: $(TABLES)
$(TARGETDIR)/%.tmd: $(DATADIR)/%.csv
	$(PYTHON) $(CSV2TABLE) --file $< --out $@ --delimiter ','

mkdir:
	mkdir -p $(TARGETDIR)
	mkdir -p $(DATADIR)
	mkdir -p $(MDDIR)

clean: mkdir
	rm -rf $(TARGETDIR) $(GUIBUILDDIR) $(GUIDISTDIR)
	mkdir -p $(TARGETDIR)
