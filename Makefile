ifeq ($(OS),Windows_NT)
MAKE= make-4.1_64bit.exe
else
MAKE= make
endif
MDDIR:= doc
GUIDESIGNDIR:= gui
GUIDESIGN:= $(GUIDESIGNDIR)/tinyI2Cgui.py
GUIBUILDDIR:= build
GUIDISTDIR:= dist
GUIBINARY:= $(GUIDISTDIR)/TinyI2C$(EXE)
.PHONY: gui pdf html clean

all: html

gui: $(GUIBINARY)
$(GUIBINARY): $(GUIDESIGN)
	pyinstaller --noconsole -p python/ gui/main.py --onefile --clean --name TinyI2C

$(GUIDESIGN):
	pyuic4 tinyI2C.ui -o $(GUIDESIGN)

html:
	cd $(MDDIR); \
	$(MAKE) html

pdf:
	cd $(MDDIR); \
	$(MAKE) pdf

clean: $(TARGETDIR)
	rm -rf $(GUIBUILDDIR)/* $(GUIDISTDIR)/*; \
	cd $(MDDIR); \
	$(MAKE) clean
