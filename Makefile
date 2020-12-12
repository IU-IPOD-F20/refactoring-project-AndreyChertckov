#-----------------------------------------------------
# Some usefull instructions...
#
BIBLIO=biblio.bib
#-----------------------------------------------------

all: README.html README.pdf

README.html: README.adoc
	asciidoctor -a toc=left README.adoc

README.pdf: README.adoc
	asciidoctor-pdf README.adoc

todos: 
	@echo "========================================"
	@echo "==> Generating the list of today's totos"
	grep "^fix " README.adoc 

check: 
	@echo "========================================"
	@echo "==> checking the fix "
	mvn test
	gradle test
	ruby tests/testfix0.rb README.adoc 
	ruby tests/checkModel.rb docs/classDiagam.plantuml 

badge:
	@echo "========================================"
	@echo "==> generating coverage badge "
	mvn clean install
	mvn io.github.handofgod94:jacoco-cov-badge-maven-plugin:1.1.0:badge
	
clean:
	rm -rf target
	rm -rf build
	rm .DS_Store
	rm -rf out
