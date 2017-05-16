---
title: Copying the content of code blocks
tags: tools, javascript, metalsmith, config
date: 2017-05-16
collection: articles
layout: article.html
snippet: Many code highlighter plugins offers the feature of copying the highlighted text from them to help out the readers. In this article I am going to show you how I implemented the same feature in my static Metalsmith-based blog.
---

First thing first, we are going to need a way to access the visitors clipboard. I find a pure javascript library [clipboard.js](https://clipboardjs.com/) for the purpose.

Integrating _clipboard.js_ is easy. You can put your code in a html tag, name it with and id, then pass that id to a button that has the class that the library is expecting for, and thats it.

```Basic_example_copied_from_the_documentation
<!-- Target -->
<textarea id="bar">Mussum ipsum cacilds...</textarea>

<!-- Trigger -->
<button class="btn" data-clipboard-action="cut" data-clipboard-target="#bar">
    Cut to clipboard
</button>
```
I initialized the library to look for elements with the `copy-btn` class on them. This can be configured with the initialization code.

```
<script>
  const clipboard = new Clipboard('.copy-btn');
</script>
```

In case of a static website that is generated from a Markdown file there is a bit of an issue. You don't want to bother naming each code snippet with a unique name, and to create the necessary button for them. You want all of these task happen automatically in compile time.

## Generating the code blocks

Since I use [Markdown-it](https://github.com/markdown-it/markdown-it) as a Markdown engine for my site, I integrated the code block generator code in to the exposed highlighter API of the library. You can give the library a function that will be called with the raw string and the optional language identifier on code block render request. You can generate your own version of html embedded code, and you can simply return it as a string. The html escaping has to be done manually.

``` Integrating_the_code_block_renderer_to
const md = new MarkdownIt({
  highlight: renderCode
})
```

The `renderCode` function will be used as a code block renderer.

```
let renderCode = function(str, info) {
  const id = getId()
  const title = info.replace(/_/g, " ")
  let front = '<pre>'
  const back = `<button class="copy-btn" title="Copy code to clipboard" data-clipboard-target="#${id}">&#xe9b8;</button><code id="${id}">${escapeHtml(str)}</code></pre>`
  if (title.length > 0)
    front += `<div class="code-title">${title}</div>`
  return front + back
}
```

There are two issues we have to solve:

1. The language keyword can only be a single word as __markdown-it__ parses it.
1. We have to generate unique identifiers for all of the code blocks.

The fisrt isse is solved by the third line. We simply use _underscore_ separated titles in the language keyword field, and then we replace the _underscores_ with spaces. This is a simple but effective hack though.

The second issue is a bit more harder. We need a semi unique identifier to solve it. The identifier only has to be unique for an article. I solved this issue by generating a 100 character long random hash for each code.

```
let getId = function() {
  let text = "";
  const possible = "abcdefghijklmnopqrstuvwxyz";
  for( let i=0; i < 100; i++ )
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  return text;
}
```

The 100 characters will ensure that I will be able to write pretty long articles and having a pretty good confidence that there will be no interference with the generated identifiers.

The rest of the `renderCode` function is self explanatory. If there was a language keyword in the code block, we will add that too to the generated code. Of course, I am using a standard escape function to escape unwanted characters.

```
let escapeHtml = function(unsafe) {
  return unsafe
   .replace(/&/g, "&amp;")
   .replace(/</g, "&lt;")
   .replace(/>/g, "&gt;")
   .replace(/"/g, "&quot;")
   .replace(/'/g, "&#039;")
}
```

With a little bit of CSS, the embedded code block is looking good:

```Style_for_the_code_blocks
pre code {
  background: radial-gradient(circle at top right, #5b747e, #0d1a1e 1200px);
  color: #e9e8e8;
  width: var(--content-width);
  display: block;
  position: relative;
  left: - $content-padding;
  overflow-x: auto;
  font-size: 0.8em;
  line-height: 1.4em;
  padding: 12px 25px;
  box-shadow: inset 0px 7px 11px -7px rgba(35, 30, 30, 0.8);
  border-left: solid 5px #3d7287;
}

.code-title {
  background-color: var(--main-color);
  color: white;
  position: relative;
  width: var(--content-width);
  left: - $content-padding;
  padding: 4px 0 1px;
  padding-left: $content-padding;
  font-size: 90%;
}

.copy-btn {
  font-family: 'icomoon';
  position: relative;
  float: right;
  margin: -12px;
  z-index: 3;
  top: 24px;
  opacity: 0;
  transition: $default-transition;
  background-color: transparent;
  border: none;
  color: #e9e8e8;
  cursor: pointer;
}

.copy-btn::before {
  content: "Copied!";
  padding-right: 6px;
  font-family: "Lato","proxima-nova","Helvetica Neue",Arial,sans-serif;
  font-size: 90%;
  opacity: 0;
  transition: $default-transition;
}

button:focus {outline:0;}

pre:hover .copy-btn {
  opacity: 1;
}
```
The button will be only visible if the user hovers over to the code block. Nice and elegant solution.


# Feedback to the user

I think it is pretty important to give a feedback about an action in any case. So I implemented the feedback system for the result of the copy command.

_Clipboard.js_ has an exposed event API as well. The official example like this:

```
var clipboard = new Clipboard('.btn');

clipboard.on('success', function(e) {
    console.info('Action:', e.action);
    console.info('Text:', e.text);
    console.info('Trigger:', e.trigger);

    e.clearSelection();
});

clipboard.on('error', function(e) {
    console.error('Action:', e.action);
    console.error('Trigger:', e.trigger);
});
```
That indicates, that we have access to the triggering button after the copy action fired. In this way, we can insert here our feedback animations as follows:

```
<script>
  const clipboard = new Clipboard('.copy-btn');
  clipboard.on('success', function(e) {
      e.clearSelection();
      e.trigger.classList.add("copy-success");
      setTimeout(function() {
        e.trigger.classList.remove("copy-success");
      }, 1500);
      console.log(e);
  });
  clipboard.on('error', function(e) {
      alert('Copy failed :(')
      console.log(e);
  });
</script>
```

By redefining the trigger button's `:before` selector in the `copy-success` class, we can display a message about the successful copy action to the user.

```
.copy-btn::before {
  content: "Copied!";
  padding-right: 6px;
  font-family: "Lato","proxima-nova","Helvetica Neue",Arial,sans-serif;
  font-size: 90%;
  opacity: 0;
  transition: $default-transition;
}

.copy-success::before {
  content: "Copied!";
  padding-right: 6px;
  font-family: "Lato","proxima-nova","Helvetica Neue",Arial,sans-serif;
  font-size: 90%;
  opacity: 1;
  transition: $default-transition;
}
```

The only drawback of this method, is that in this form, it can only display a single message. This is not the best case, but we can heavily assume, that the weakest part of the system, the id assingment, will be strong enough to not to have any problems with it.

# Conclusion

Implementing a one-click-copy code block is not hard with the right tools.

