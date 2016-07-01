PY?=python3
PELICAN?=pelican
PELICANOPTS=

BASEDIR=.
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py
PUBLISHCONF=$(BASEDIR)/publishconf.py

FTP_HOST=tiborsimon.io
FTP_USER=tiborsim
FTP_TARGET_DIR=public_html

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICANOPTS += --relative-urls
endif

sass:
	@echo ''
	@echo '-> Compiling SASS..'
	sassc $(BASEDIR)/themes/escape-velocity/static/sass/main.scss $(BASEDIR)/themes/escape-velocity/static/css/main.css

delete_output:
	@echo ''
	@echo '-> Delete output directory..'
	rm -rf $(OUTPUTDIR)/*
	cd $(OUTPUTDIR); git checkout CNAME

clean_output:
	@echo ''
	@echo '-> Cleaning up..'

	mv $(OUTPUTDIR)/theme/js/bundle.min.js $(OUTPUTDIR)/theme/bundle.min.js
	rm -rf $(OUTPUTDIR)/theme/js
	mkdir $(OUTPUTDIR)/theme/js
	mv $(OUTPUTDIR)/theme/bundle.min.js $(OUTPUTDIR)/theme/js/bundle.min.js

	mv $(OUTPUTDIR)/theme/css/bundle.min.css $(OUTPUTDIR)/theme/bundle.min.css
	rm -rf $(OUTPUTDIR)/theme/css
	mkdir $(OUTPUTDIR)/theme/css
	mv $(OUTPUTDIR)/theme/bundle.min.css $(OUTPUTDIR)/theme/css/bundle.min.css

compile: delete_output
	@echo ''
	@echo '-> Compiling Pelican..'
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

compile-d: delete_output
	@echo ''
	@echo '-> Compiling Pelican.. [DEBUG]'
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS) -D

bundle:
	@echo ''
	@echo '-> Running gulp tasks..'
	gulp css js
	gulp css-min js-min

local: compile bundle
	@echo ''
	@echo '-> Done!'

local-d: compile-d webpack_bundle clean_output
	@echo ''
	@echo '-> Done!'

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

serve:
ifdef PORT
	cd $(OUTPUTDIR) && $(PY) -m pelican.server $(PORT)
else
	cd $(OUTPUTDIR) && $(PY) -m pelican.server
endif

publish: delete_output
	@echo ''
	@echo '-> Compiling Pelican..'
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS)

publish-d: delete_output
	@echo ''
	@echo '-> Compiling Pelican.. [DEGUG]'
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS) -D

github: publish bundle
	@echo ''
	@echo '-> Pushing to tiborsimon.io..'
	cd $(OUTPUTDIR); git add --all; git commit -m "Site push"; git push
	@echo ''
	@echo '-> Saving pushed site to superproject..'
	git add $(OUTPUTDIR); git commit -m "Site pushed"; git push

github-d: publish-d bundle
	@echo ''
	@echo '-> Pushing to tiborsimon.io..'
	cd $(OUTPUTDIR); git add --all; git commit -m "Site push"; git push
	@echo ''
	@echo '-> Saving pushed site to superproject..'
	git add $(OUTPUTDIR); git commit -m "Site pushed"; git push
