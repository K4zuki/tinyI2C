# include Makefile.win
include Makefile.in

MDDIR:= ../doc
DATADIR:= data
TARGETDIR:= Out
IMAGEDIR:= images
WAVEDIR:= images/waves

INPUT:= TITLE.md
TARGET = NXPemulatesNXP

CSV:= $(shell cd $(DATADIR); ls *.csv)
TABLES:= $(CSV:%.csv=$(TARGETDIR)/%.tmd)

WAVEYAML:= $(shell cd $(DATADIR); ls *.yaml)
PYWAVEOPTS:= -c
PYWAVEOPTS +=	'import sys, yaml, json; \
							json.dump(yaml.load(sys.stdin), sys.stdout, indent=4)'
WAVEJSON:= $(WAVEYAML:%.yaml=$(TARGETDIR)/%.json)
WAVEPNG:= $(WAVEYAML:%.yaml=$(WAVEDIR)/%.png)

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

.PHONY: docx html filtered tables pdf tex merge clean linking

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

filtered: $(MDDIR) tables wavedrom $(FILTERED)
$(FILTERED): $(MDDIR)/$(INPUT)
	cat $< | $(PYTHON) $(FILTER) --out $@

tables: $(TARGETDIR) $(DATADIR) $(TABLES)
$(TARGETDIR)/%.tmd: $(DATADIR)/%.csv
	$(PYTHON) $(CSV2TABLE) --file $< --out $@ --delimiter ','

wavedrom: $(DATADIR) $(WAVEDIR) yaml2json $(WAVEPNG)
$(WAVEDIR)/%.png: $(TARGETDIR)/%.json
	phantomjs $(WAVEDROM) -i $< -p $@

yaml2json: $(WAVEJSON)
$(TARGETDIR)/%.json: $(DATADIR)/%.yaml
	$(PYTHON) $(PYWAVEOPTS) < $< > $@

$(TARGETDIR):
	mkdir -p $(TARGETDIR)
$(DATADIR):
	mkdir -p $(DATADIR)
$(MDDIR):
	mkdir -p $(MDDIR)
$(IMAGEDIR):
	mkdir -p $(IMAGEDIR)
$(WAVEDIR):
	mkdir -p $(WAVEDIR)

clean: $(TARGETDIR)
	rm -rf $(TARGETDIR)/* $(WAVEDIR)/
