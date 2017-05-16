---
title: My Markdown setup
tags: markdown, tools, javascript, metalsmith, config
date: 2017-05-14
collection: articles
layout: article.html
snippet: I use a highly customised Markdown engine for my blog. It is backed up by the javascript based pluggable Markdown-it engine. In this article I am going to show you all the features it has.
---

I use the [Markdown-it](https://github.com/markdown-it/markdown-it) engine to implement the feature set I find useful to have for my articles:

1. Easy to use figures with indexing and referencing.
1. Code snippets with optional titles and the ability to copy the cope with one button.
1. External link handling.
1. Section dividers with optional titles.
1. Message boxes.
1. Anchor links.

I used the following software components:


| Package | Version | Description |
|:--------|:--------|:------------|
|[markdown-it](https://www.npmjs.com/package/markdown-it) | _8.3.1_ | Core engine. |
|[markdown-it-anchor](https://www.npmjs.com/package/markdown-it-anchor) | _4.0.0_ | Anchor links for header. |
|[markdown-it-container](https://www.npmjs.com/package/markdown-it-container) | _2.0.0_ | Custom containers with predefined classes. |
|[markdown-it-custom-block](https://www.npmjs.com/package/markdown-it-custom-block) | _0.1.0_ | Custom blocks with custom renderers. |
|[markdown-it-external-links](https://www.npmjs.com/package/markdown-it-external-links) | _0.0.6_ | External link handling. |
|[markdown-it-footnote](https://www.npmjs.com/package/markdown-it-footnote) | _3.0.1_ | Footnote system. |

Since I am using [Metalsmith](http://www.metalsmith.io/) for my blog, I was implemented the custom Markdown system as a __Metalsmith plugin__ with a few helper function. The sources for the whole system can be found on my [site's GitHub repository](https://github.com/tiborsimon/site).

---

# Figure system

My __figure system__ uses the [markdown-it-custom-block](https://www.npmjs.com/package/markdown-it-custom-block) plugin to define the necessary custom renderer function as follows:

```
const md = new MarkdownIt()
md.use(mdCustomBlock, {
  img (raw) {
    const [index, alt, width, url] = raw.split('#')
    return `<figure id="fig${index}">
      <img width=${width} src="/assets/images/${url}" alt="${alt}">
      <figcaption>Fig ${index}: ${alt}</figcaption>
    </figure>`
  }
})
```

That code snippet will define a custom `@[img](index#title#width#image_url)` block that can be used to insert figures. This one-liner will result the following html code:

```
<figure id="fig${index}">
  <img width=${width} src="/assets/images/${image_url}" alt="${title}">
  <figcaption>Fig ${index}: ${title}</figcaption>
</figure>
```

Using a bit of CSS wizardry will create automatic wrapper-less borders around the image blocks:

```
figure {
  position: relative;
  border: none;
  border-bottom: 1px solid palette(Black, Dividers);
  width: var(--content-width);
  left: - $content-padding;
  margin: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  img {
    max-width: 740px;
    margin: 20px 0px 8px;
  }
  figcaption {
    font-size: 0.9em;
    font-style: italic;
    margin-bottom: 10px;
  }
}
:not(figure)+figure {
  border-top: 1px solid palette(Black, Dividers);
}
```

## Figures example

The following markup will be rendered as a figure group containing three images. Each images will have its own _figure id_, title, and a hidden anchor `/#fig<number>` link for later references.

@[img](1#Test figure 1.#160#tibor2017-600.jpg)

@[img](2#Test figure 2.#160#tibor2017-600.jpg)

@[img](3#Test figure 3.#160#tibor2017-600.jpg)


``` Figure_syntax
@[img](1#Test figure 1.#160#tibor2017-600.jpg)

@[img](2#Test figure 2.#160#tibor2017-600.jpg)

@[img](3#Test figure 3.#160#tibor2017-600.jpg)
```

---

# Divider

Similarly to the figures, the dividers also implemented with the [markdown-it-custom-block](https://www.npmjs.com/package/markdown-it-custom-block) plugin.

```
const md = new MarkdownIt()
md.use(mdCustomBlock, {
  divider (text) {
    return `<div class="divider">${text}</div>`
  }
})
```

## Divider example

@[divider](My first divider)

@[divider](My second divider)

``` Divider_syntax
@[divider](My first divider)

@[divider](My second divider)
```
---

# Message boxes

I like to use message boxes to highlight sime important sections.

::: success
This is a success message.
:::

::: info
This is a info message.
:::

::: warning
This is a warning message.
:::

::: danger
This is a danger message.
:::

``` Message_box_syntax
::: success
This is a success message.
:::

::: info
This is a info message.
:::

::: warning
This is a warning message.
:::

::: danger
This is a danger message.
:::
```

