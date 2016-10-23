---
title: Debugging metalsmith
tags: metalsmith, website, debug
date: 2016-10-18
collection: articles
layout: article.html
draft: true
---

During the development of the current iteration of my website core, I have
encountered with the problem of debugging Metalsmith with its plugin system.
Metalsmith is a lightweight static site generator that has a very flexible
plugin system. You can chain together the plugins you like, and Metalsmith
will call them one by one passing the current data structure to them.

This method gives ultimate flexibility but it lacks debuggability. If you
want to see the intermediate data structure that is returned by a plugin
and is about to be passed to the next one, you need to write a custom plugin
to do that. Hacking logging printouts into existing plugin function is not an
option for me.

## Metalsmith's plugin system

## Debug plugin

## Conclusion

