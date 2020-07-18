# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
PYTHON        ?= python
SPHINXOPTS    ?=
SPHINXBUILD   ?= python $(shell which sphinx-build)
PAPER         ?=

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d build/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) source
DEST = build
.PHONY: all help clean html dirhtml pickle json htmlhelp qthelp latex changes linkcheck doctest gitwash gh-pages random_gallery logo

all: html

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html      to make standalone HTML files"
	@echo "  dirhtml   to make HTML files named index.html in directories"
	@echo "  pickle    to make pickle files"
	@echo "  json      to make JSON files"
	@echo "  htmlhelp  to make HTML files and a HTML help project"
	@echo "  qthelp    to make HTML files and a qthelp project"
	@echo "  devhelp   to make HTML files and a Devhelp project"
	@echo "  latex     to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
	@echo "  latexpdf  to make LaTeX files and run them through pdflatex"
	@echo "  changes   to make an overview of all changed/added/deprecated items"
	@echo "  linkcheck to check all external links for integrity"
	@echo "  doctest   to run all doctests embedded in the documentation (if enabled)"
	@echo "  gitwash   to update the gitwash documentation"

clean:
	-rm -rf $(DEST)/*
	-find ./source/auto_examples/* -type f | grep -v blank | xargs rm -f
	-find . -type f -name "*.pyc" | xargs rm -f

logo:
	cd logo; python skfuzzy_logo.py; rm -f ./logo/temp.py
	cd logo; python skfuzzy_icon.py; rm -f ./logo/temp.py

random_gallery:
	@cd source && $(PYTHON) random_gallery.py

html: logo random_gallery gitwash
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(DEST)/html
	@echo
	@echo "Build finished. The HTML pages are in build/html."

dirhtml:
	$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(DEST)/dirhtml
	@echo
	@echo "Build finished. The HTML pages are in build/dirhtml."

pickle:
	$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) $(DEST)/pickle
	@echo
	@echo "Build finished; now you can process the pickle files."

json:
	$(SPHINXBUILD) -b json $(ALLSPHINXOPTS) $(DEST)/json
	@echo
	@echo "Build finished; now you can process the JSON files."

htmlhelp:
	$(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) $(DEST)/htmlhelp
	@echo
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in build/htmlhelp."

qthelp:
	$(SPHINXBUILD) -b qthelp $(ALLSPHINXOPTS) $(DEST)/qthelp
	@echo
	@echo "Build finished; now you can run "qcollectiongenerator" with the" \
	      ".qhcp project file in build/qthelp, like this:"
	@echo "# qcollectiongenerator build/qthelp/scikitfuzzy.qhcp"
	@echo "To view the help file:"
	@echo "# assistant -collectionFile build/qthelp/scikitfuzzy.qhc"

devhelp:
	$(SPHINXBUILD) -b devhelp $(ALLSPHINXOPTS) $(DEST)/devhelp
	@echo
	@echo "Build finished."
	@echo "To view the help file:"
	@echo "# mkdir -p $$HOME/.local/share/devhelp/scikitfuzzy"
	@echo "# ln -s build/devhelp $$HOME/.local/share/devhelp/scikitfuzzy"
	@echo "# devhelp"

changes:
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) $(DEST)/changes
	@echo
	@echo "The overview file is in build/changes."

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(DEST)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in build/linkcheck/output.txt."

doctest:
	$(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) $(DEST)/doctest
	@echo "Testing of doctests in the sources finished, look at the " \
	      "results in build/doctest/output.txt."

gitwash:
	git submodule update --init --recursive
	$(PYTHON) tools/gitwash/gitwash_dumper.py source scikit-fuzzy \
	--project-url=http://scikit-fuzzy.org \
	--project-ml-url=http://groups.google.com/group/scikit-fuzzy \
	--repo-name=scikit-fuzzy \
	--github-user=scikit-fuzzy \
	--source-suffix=.txt
