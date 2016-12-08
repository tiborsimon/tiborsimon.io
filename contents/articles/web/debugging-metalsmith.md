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
will call them one by one passing the current data structure to them. This 
functional approach makes it hard to understand at first, since there are no visible 
variables you can look at during execution.


## Debug plugin

In order to peek into the data structure, you need to write a small plugin with the 
required metalsmith plugin interface like so:

```
let monitor = () => {
  return (files, metalsmith, done) => {
    // console.log(metalsmith._metadata.enhancedTags)
    done()
  }
}

...

metalsmith(__dirname)
  .source('contents')
  .use(monitor())
  .destination('publish')
  .build(function (err) {
    if (err) {
      throw err;
    }
  })
```

With this small plugin, you are be able to log out any data structure you want by inserting it to the plugin chain.
