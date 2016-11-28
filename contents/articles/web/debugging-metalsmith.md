---
title: Debugging metalsmith
tags: metalsmith, debug, javascript, plugin, web
date: 2016-10-18
collection: articles
layout: article.html
snippet: Debugging Metalsmith is a bit tricky. You have to write a custom plugin to print out the intermediate data structures passed through the various plugins.
---

During the development of the _current iteration_ of my website core, I have
encountered with the problem of debugging Metalsmith with its plugin system.
Metalsmith is a lightweight static site generator that has a very flexible
plugin system. You can chain together the plugins you like, and Metalsmith
will call them one by one passing the current data structure to them.


This method gives ultimate flexibility but it lacks debuggability. If you
want to see the intermediate data structure that is returned by a plugin
and is about to be passed to the next one, you need to write a custom plugin
to do that. Metalsmith plugins often lacks of any usable documentation so this 
article could be useful too to find out what data they added to the passed data structure.

## Metalsmith's plugin system

## Debug plugin

## Conclusion

