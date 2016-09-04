# include Makefile.win
include Makefile.in

MDDIR:= markdown
DATADIR:= data
TARGETDIR:= Out

INPUT:= source.md
OUTPUT:= $(shell basename $(INPUT) .md)
CSV:= $(shell cd $(DATADIR); ls *.csv)
TABLES:= $(CSV:%.csv=$(TARGETDIR)/%.tmd)
FILTERED= $(INPUT:%.md=$(TARGETDIR)/%.fmd)
HTML:=$(TARGETDIR)/$(OUTPUT).html
DOCX:=$(TARGETDIR)/$(OUTPUT).docx

.PHONY: docx html filtered tables clean gui

all: mkdir html

gui:
	pyinstaller --noconsole -p python/ gui/main.py --onefile --clean --name tinyI2C$(EXE)

docx: $(DOCX)
$(DOCX): $(HTML)
	$(PANDOC) --reference-docx=$(REFERENCE) $(HTML) -o $(TARGETDIR)/$(OUTPUT).docx; \
	$(PYTHON) $(DOCXPWRTR) -I $(MDDIR)/$(INPUT) -O $(DOCX)

html: $(HTML)

$(HTML): $(TABLES) $(FILTERED)
	$(PANDOC) $(PANFLAGS) --self-contained -thtml5 --template=$(MISC)/github.html \
		$(FILTERED) -o $(HTML)

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
	rm -rf $(TARGETDIR)
	mkdir -p $(TARGETDIR)
