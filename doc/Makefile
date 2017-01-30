include Makefile.in

REQ = 'Requirements -\n'
REQ += '\033[92m'
REQ += 'pandoc'
REQ += '\033[0m'
REQ += 'to convert Markdown to TeX/html\n\033[0m'
REQ += '\033[92m'
REQ += 'XeLaTeX'
REQ += '\033[0m'
REQ += 'to convert TeX to PDF\n\033[0m'
REQ += '\033[92m'
REQ += 'pyYAML(via pip)'
REQ += '\033[0m'
REQ += 'to convert yaml to json waveform file \n\033[0m'
REQ += '\033[92m'
REQ += 'WAVEDROM+PhantomJS(via npm)'
REQ += '\033[0m'
REQ += 'to convert JSON to waveform png\n\033[0m'
REQ += '\033[92m'
REQ += 'rsvg-convert(via librsvg)'
REQ += '\033[0m'
REQ += 'to convert SVG to PNG\n\033[0m'

MDDIR:= ../doc
DATADIR:= data
TARGETDIR:= Out
IMAGEDIR:= images
WAVEDIR:= waves
BITDIR:= bitfields

INPUT:= TITLE.md
TARGET = NXPemulatesNXP

CSV:= $(shell cd $(DATADIR); ls *.csv)
TABLES:= $(CSV:%.csv=$(TARGETDIR)/%.tmd)

WAVEYAML:= $(shell cd $(DATADIR)/$(WAVEDIR); ls *.yaml)
PYWAVEOPTS:= -c
PYWAVEOPTS += 'import sys, yaml, json; \
							json.dump(yaml.load(sys.stdin), sys.stdout, indent=4)'
WAVEJSON:= $(WAVEYAML:%.yaml=$(TARGETDIR)/%.wavejson)
WAVEPNG:= $(WAVEYAML:%.yaml=$(IMAGEDIR)/$(WAVEDIR)/%.png)

BITYAML:= $(shell cd $(DATADIR)/$(BITDIR); ls *.yaml)
BITJSON:= $(BITYAML:%.yaml=$(TARGETDIR)/%.bitjson)
BITPNG:=  $(BITYAML:%.yaml=$(IMAGEDIR)/$(BITDIR)/%.png)
# rsvg-convert alpha.svg --format=png --output=sample_rsvg.png

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

MARKDOWN = $(shell ls $(MDDIR)/*.md)

.PHONY: docx html filtered tables pdf tex merge clean linking

all: html

help:
	@echo $(REQ)"\033[0m"

docx: $(DOCX)
$(DOCX): $(HTML)
	$(PANDOC) --reference-docx=$(REFERENCE) $(HTML) -o $(DOCX); \
	$(PYTHON) $(DOCXPWRTR) -I $(MDDIR)/$(INPUT) -O $(DOCX)

html: $(HTML)
$(HTML): $(TARGETDIR)/$(TARGET).md
	$(PANDOC) $(PANFLAGS) --self-contained -thtml5 --template=$(MISC)/github.html \
		$(FILTERED) -o $(HTML)

pdf: $(TARGETDIR)/$(IMAGEDIR) $(TARGETDIR)/$(TARGET).tex
	cd $(TARGETDIR);\
	xelatex --no-pdf $(TARGET).tex; \
	xelatex $(TARGET).tex

linking: $(TARGETDIR)/$(IMAGEDIR)
$(TARGETDIR)/$(IMAGEDIR):
	rm -f $(TARGETDIR)/$(IMAGEDIR); \
	cd $(TARGETDIR);\
	ln -s ../$(IMAGEDIR)

tex: merge $(TARGETDIR)/$(TARGET).tex
$(TARGETDIR)/$(TARGET).tex: $(TARGETDIR)/$(TARGET).md
	$(PANDOC) $(PANFLAGS) --template=$(MISC)/CJK_xelatex.tex --latex-engine=xelatex \
		$(TARGETDIR)/$(TARGET).md -o $(TARGETDIR)/$(TARGET).tex

merge: filtered $(TARGETDIR)/$(TARGET).md
$(TARGETDIR)/$(TARGET).md: $(FILTERED)
	cat $(FILTERED) > $(TARGETDIR)/$(TARGET).md

filtered: tables $(FILTERED)
$(FILTERED): $(MDDIR)/$(INPUT) $(MARKDOWN) $(TABLES) $(WAVEPNG) $(BITPNG)
	cat $< | $(PYTHON) $(FILTER) --mode tex --out $@

tables: $(TABLES)
$(TARGETDIR)/%.tmd: $(DATADIR)/%.csv
	$(PYTHON) $(CSV2TABLE) --file $< --out $@ --delimiter ','

wavedrom: $(WAVEDIR) $(WAVEPNG)
$(IMAGEDIR)/$(WAVEDIR)/%.png: $(TARGETDIR)/%.wavejson
ifneq ($(OS),Windows_NT)
	phantomjs $(WAVEDROM) -i $< -p $@
else
	touch $@
endif

bitfield: $(BITDIR) $(BITPNG)
$(IMAGEDIR)/$(BITDIR)/%.png: $(TARGETDIR)/%.bitjson
	$(BITFIELD) --input $< --vspace 80 --hspace 640 --lanes 1 --bits 8 > $<.svg
	$(RSVG) $<.svg --format=png --output=$@

yaml2json: $(WAVEDIR) $(BITDIR) $(WAVEJSON) $(BITJSON)
$(TARGETDIR)/%.wavejson: $(DATADIR)/$(WAVEDIR)/%.yaml
	if [ ! -e $(IMAGEDIR)/$(WAVEDIR) ]; then mkdir -p $(IMAGEDIR)/$(WAVEDIR); fi
	$(PYTHON) $(PYWAVEOPTS) < $< > $@

$(TARGETDIR)/%.bitjson: $(DATADIR)/$(BITDIR)/%.yaml
	if [ ! -e $(IMAGEDIR)/$(BITDIR) ]; then mkdir -p $(IMAGEDIR)/$(BITDIR); fi
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
	mkdir -p $(IMAGEDIR)/$(WAVEDIR)
$(BITDIR):
	mkdir -p $(IMAGEDIR)/$(BITDIR)

clean: $(TARGETDIR)
	rm -rf $(TARGETDIR)/*
	rm -rf $(IMAGEDIR)/$(WAVEDIR)/
	rm -rf $(IMAGEDIR)/$(BITDIR)/
