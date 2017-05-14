---
title: My Markdown setup
tags: markdown, tools, javascript, metalsmith, config
date: 2017-05-14
collection: articles
layout: article.html
snippet: For my site I use a highly customised Markdown configuration for the articles. Let me show you the details.
---

This will be an [external-link](https://google.com) and this will be an [internal-link](/#about). Thats is.

# Figure system

@[img](1#Test figure 1.#160#tibor2017-600.jpg)

@[img](2#Test figure 2.#160#tibor2017-600.jpg)

@[img](3#Test figure 3.#160#tibor2017-600.jpg)


``` Figure_syntax
@[img](1#Test figure 1.#160#tibor2017-600.jpg)

@[img](2#Test figure 2.#160#tibor2017-600.jpg)

@[img](3#Test figure 3.#160#tibor2017-600.jpg)
```

# Divider

@[divider](My first divider)

@[divider](My second divider)

``` Divider_syntax
@[divider](My first divider)

@[divider](My second divider)
```

# Message boxes

## Success box

::: success
This is a success message.
:::

``` Success_box_syntax
::: success
This is a success message.
:::
```

## Info box

::: info
This is a info message.
:::

``` Info_box_syntax
::: info
This is a info message.
:::
```

## Warning box

::: warning
This is a warning message.
:::

``` Warning_box_syntax
::: warning
This is a warning message.
:::
```

## Danger box

::: danger
This is a danger message.
:::

``` Danger_box_syntax
::: danger
This is a danger message.
:::
```
