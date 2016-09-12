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

INPUT:= TITLE.md
TARGET = NXPemulatesNXP

CSV:= $(shell cd $(DATADIR); ls *.csv)
TABLES:= $(CSV:%.csv=$(TARGETDIR)/%.tmd)
FILTERED= $(INPUT:%.md=$(TARGETDIR)/%.fmd)
HTML:=$(TARGETDIR)/$(TARGET).html
DOCX:=$(TARGETDIR)/$(TARGET).docx

PANFLAGS += --toc
PANFLAGS += --listings
PANFLAGS += --number-sections --highlight-style=pygments
PANFLAGS += -M localfontdir=$(FONTDIR)
PANFLAGS += -M css=$(MISC)/github_css/github.css

.PHONY: docx html filtered tables pdf tex merge gui clean

all: mkdir html

gui: $(GUIBINARY)
$(GUIBINARY): $(GUIDESIGN)
	pyinstaller --noconsole -p python/ gui/main.py --onefile --clean --name TinyI2C

$(GUIDESIGN):
	pyuic4 tinyI2C.ui -o $(GUIDESIGN)

docx: $(DOCX)
$(DOCX): $(HTML)
	$(PANDOC) --reference-docx=$(REFERENCE) $(HTML) -o $(DOCX); \
	$(PYTHON) $(DOCXPWRTR) -I $(MDDIR)/$(INPUT) -O $(DOCX)

html: $(HTML)
# $(HTML): $(TARGETDIR) $(TABLES) $(FILTERED) $(TARGETDIR)/$(TARGET).md
$(HTML): tables filtered merge
	$(PANDOC) $(PANFLAGS) --self-contained -thtml5 --template=$(MISC)/github.html \
		$(FILTERED) -o $(HTML)

pdf: tex
	cd $(TARGETDIR); \
	rm -f ./images; \
	ln -s ../images; \
	xelatex $(TARGET).tex

tex: merge $(TARGETDIR)/$(TARGET).tex $(TARGETDIR)/$(TARGET).md
$(TARGETDIR)/$(TARGET).tex: $(TARGETDIR)/$(TARGET).md
	$(PANDOC) $(PANFLAGS) --template=$(MISC)/CJK_xelatex.tex --latex-engine=xelatex \
		$(TARGETDIR)/$(TARGET).md -o $(TARGETDIR)/$(TARGET).tex; \
	xelatex --output-directory=$(TARGETDIR) --no-pdf $(TARGETDIR)/$(TARGET).tex

merge: $(TARGETDIR) filtered $(TARGETDIR)/$(TARGET).md
$(TARGETDIR)/$(TARGET).md:
	cat $(FILTERED) > $(TARGETDIR)/$(TARGET).md

filtered: $(MDDIR) tables $(FILTERED)
$(FILTERED): $(MDDIR)/$(INPUT)
	cat $< | $(PYTHON) $(FILTER) --out $@

tables: $(TARGETDIR) $(DATADIR) $(TABLES)
$(TARGETDIR)/%.tmd: $(DATADIR)/%.csv
	$(PYTHON) $(CSV2TABLE) --file $< --out $@ --delimiter ','

$(TARGETDIR):
	mkdir -p $(TARGETDIR)
$(DATADIR):
	mkdir -p $(DATADIR)
$(MDDIR):
	mkdir -p $(MDDIR)

clean: $(TARGETDIR)
	rm -rf $(TARGETDIR)/* $(GUIBUILDDIR)/* $(GUIDISTDIR)/*
