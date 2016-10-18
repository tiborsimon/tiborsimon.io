NODE := node_modules
HIGHLIGHT_STYLE := hopscotch

PHONY: all metalsmith copy

all: metalsmith copy

metalsmith:
	node metalsmith.js

copy:
	cp ./node_modules/highlight.js/styles/$(HIGHLIGHT_STYLE).css ./publish/assets/highlight.css
