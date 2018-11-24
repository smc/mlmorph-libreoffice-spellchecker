# ===== Build settings =====

MLMORPH_VERSION=1.0
MLMORPH_PACKAGENAME:=libreoffice-mlmorph
SRCDIST=README.md LICENSE.txt AUTHORS.md requirements.txt Makefile
EXTENSIONFILES=META-INF pythonpath description.xml lomlmorph.py icon.png mlmorph.components

.PHONY: all build clean bdist sdist

all: clean bdist sdist

bdist: build
	@mkdir -p dist
	cd build/oxt &&	zip -rq ../../dist/$(MLMORPH_PACKAGENAME)-$(MLMORPH_VERSION).oxt $(EXTENSIONFILES)

sdist:
	@mkdir -p dist
	tar -czf dist/$(MLMORPH_PACKAGENAME)-$(MLMORPH_VERSION).tar.gz oxt $(SRCDIST)

build:
	@mkdir -p build
	@cp -rf oxt build/
	@cp -r README.md LICENSE.txt build/
	@pip install --upgrade --target build/oxt/pythonpath -r requirements.txt
	@sed -i -e s/MLMORPH_VERSION/$(MLMORPH_VERSION)/g build/oxt/description.xml

install: bdist
	unopkg add -f dist/$(MLMORPH_PACKAGENAME)-$(MLMORPH_VERSION).oxt

clean:
	@rm -rf build dist