# include Makefile.win
include Makefile.in

MDDIR:= ../doc
DATADIR:= data
TARGETDIR:= Out
IMAGEDIR:= images

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
PANFLAGS += -M short-hash=`git rev-parse --short HEAD`
PANFLAGS += -M tables=true

.PHONY: docx html filtered tables pdf tex merge gui clean

all: html

docx: $(DOCX)
$(DOCX): $(HTML)
	$(PANDOC) --reference-docx=$(REFERENCE) $(HTML) -o $(DOCX); \
	$(PYTHON) $(DOCXPWRTR) -I $(MDDIR)/$(INPUT) -O $(DOCX)

html: $(HTML)
# $(HTML): $(TARGETDIR) $(TABLES) $(FILTERED) $(TARGETDIR)/$(TARGET).md
$(HTML): tables filtered merge
	$(PANDOC) $(PANFLAGS) --self-contained -thtml5 --template=$(MISC)/github.html \
		$(FILTERED) -o $(HTML)

linking: $(TARGETDIR) $(IMAGEDIR)
	rm -f $(TARGETDIR)/images; \
	cd $(TARGETDIR);\
	ln -s ../images

pdf: linking tex
	cd $(TARGETDIR);\
	xelatex --no-pdf $(TARGET).tex; \
	xelatex $(TARGET).tex

tex: linking merge $(TARGETDIR)/$(TARGET).tex $(TARGETDIR)/$(TARGET).md
$(TARGETDIR)/$(TARGET).tex: $(TARGETDIR)/$(TARGET).md
	$(PANDOC) $(PANFLAGS) --template=$(MISC)/CJK_xelatex.tex --latex-engine=xelatex \
		$(TARGETDIR)/$(TARGET).md -o $(TARGETDIR)/$(TARGET).tex

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
$(IMAGEDIR):
	mkdir -p $(IMAGEDIR)

clean: $(TARGETDIR)
	rm -rf $(TARGETDIR)/*
