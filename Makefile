PY?=python
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

help:
	@echo 'Makefile for a pelican Web site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make html                           (re)generate the web site          '
	@echo '   make clean                          remove the generated files         '
	@echo '   make regenerate                     regenerate files upon modification '
	@echo '   make publish                        generate using production settings '
	@echo '   make serve [PORT=8000]              serve site at http://localhost:8000'
	@echo '   make serve-global [SERVER=0.0.0.0]  serve (as root) to $(SERVER):80    '
	@echo '   make devserver [PORT=8000]          start/restart develop_server.sh    '
	@echo '   make stopserver                     stop local server                  '
	@echo '   make ssh_upload                     upload the web site via SSH        '
	@echo '   make rsync_upload                   upload the web site via rsync+ssh  '
	@echo '   make dropbox_upload                 upload the web site via Dropbox    '
	@echo '   make ftp_upload                     upload the web site via FTP        '
	@echo '   make s3_upload                      upload the web site via S3         '
	@echo '   make cf_upload                      upload the web site via Cloud Files'
	@echo '   make github                         upload the web site via gh-pages   '
	@echo '                                                                          '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html   '
	@echo 'Set the RELATIVE variable to 1 to enable relative urls                    '
	@echo '                                                                          '

sass:
	@echo ''
	@echo '-> Compiling SASS..'
	sassc $(BASEDIR)/themes/escape-velocity/static/sass/main.scss $(BASEDIR)/themes/escape-velocity/static/css/main.css

clean_output:
	@echo ''
	@echo '-> Cleaning up..'
	rm -rf $(OUTPUTDIR)/theme/sass
	mv $(OUTPUTDIR)/theme/js/bundle.min.js $(OUTPUTDIR)/theme/bundle.min.js
	rm -rf $(OUTPUTDIR)/theme/js
	mkdir $(OUTPUTDIR)/theme/js
	mv $(OUTPUTDIR)/theme/bundle.min.js $(OUTPUTDIR)/theme/js/bundle.min.js

compile:
	@echo ''
	@echo '-> Compiling Pelican..'
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

compile-d:
	@echo ''
	@echo '-> Compiling Pelican.. [DEBUG]'
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS) -D

webpack_bundle:
	@echo ''
	@echo '-> Generating Webpack js bundle..'
	@webpack

html: sass compile webpack_bundle clean_output
	@echo ''
	@echo '-> Done!'

html-d: sass compile-d webpack_bundle clean_output
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

publish:
	@echo ''
	@echo '-> Compiling Pelican..'
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS)

publish-d:
	@echo ''
	@echo '-> Compiling Pelican.. [DEGUG]'
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS) -D

ftp: sass publish webpack_bundle clean_output
	@echo ''
	@echo '-> Uploading via FTP..'
	lftp ftp://$(FTP_USER)@$(FTP_HOST) -e "set ftp:ssl-allow no; mirror -R $(OUTPUTDIR) $(FTP_TARGET_DIR) -p; quit"

ftp-d: sass publish-d webpack_bundle clean_output
	@echo ''
	@echo '-> Uploading via FTP.. [DEGUG]'
	lftp ftp://$(FTP_USER)@$(FTP_HOST) -e "set ftp:ssl-allow no; mirror -R $(OUTPUTDIR) $(FTP_TARGET_DIR) -p; quit"
