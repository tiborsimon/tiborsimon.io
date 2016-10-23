NODE:=./node_modules/.bin/
HIGHLIGHT_STYLE := hopscotch
HIDE:=@

YELLOW:=$(shell tput setaf 3)
RESET:=$(shell tput sgr0)

PHONY: all metalsmith css copy

all: metalsmith copy css

metalsmith:
	@echo "$(YELLOW)-> Compiling metalsmith..$(RESET)"
	$(HIDE)node metalsmith.js

css:
	@echo "$(YELLOW)-> Compiling CSS..$(RESET)"
	$(HIDE)$(NODE)node-sass scss/main.scss publish/css/compiled.css 1>/dev/null
	$(HIDE)cat ./node_modules/normalize.css/normalize.css \
		         ./node_modules/highlight.js/styles/$(HIGHLIGHT_STYLE).css \
						 ./publish/css/compiled.css > publish/css/style.css
	$(HIDE)cp -a ./node_modules/highlight.js/styles/$(HIGHLIGHT_STYLE).css ./publish/assets/highlight.css

copy:
	@echo "$(YELLOW)-> Copying Assets..$(RESET)"
	$(HIDE)cp -avR ./assets ./publish/assets
