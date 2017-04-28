---
title: Metalsmith enchanced tag handling
tags: metalsmith, javascript, plugin, web
date: 2017-04-27
collection: articles
layout: article.html
snippet: The existing tag management plugins are not the bests..
---


```
let enhanceTags = () => {
  return (files, metalsmith, done) => {
    let metadata = metalsmith.metadata()

    // Adding url to the tag list of files..
    for (let file in files) {
      let target = files[file]
      if (target.tags) {
        for (let tag in target.tags) {
          let data = target.tags[tag]
          data.url = metadata.baseUrl + '/tag/' + data.slug + '/'
        }
      }
    }

    // Restructuring tags metadata field..
    let enhancedTags = {
      tagsByName: [],
      tagsByCount: []
    }
    for (tag in metadata.tags) {
      let urlSafe = metadata.tags[tag].urlSafe
      let files = []
      for (let item of metadata.tags[tag]) {
        files.push(item)
      }
      enhancedTags.tagsByName.push({
        tag,
        urlSafe,
        files,
        count: files.length,
        url: metadata.baseUrl + '/tag/' + urlSafe + '/'
      })
      enhancedTags.tagsByCount.push({
        tag,
        urlSafe,
        files,
        count: files.length,
        url: metadata.baseUrl + '/tag/' + urlSafe + '/'
      })
    }
    enhancedTags.tagsByCount.sort((a, b) => {
      return b.count == a.count ? ((a.urlSafe < b.urlSafe) ? -1 : (a.urlSafe > b.urlSafe) ? 1 : 0) : b.count - a.count
    })
    enhancedTags.tagsByName.sort((a, b) => {
      return (a.urlSafe < b.urlSafe) ? -1 : (a.urlSafe > b.urlSafe) ? 1 : 0
    })
    metadata.enhancedTags = enhancedTags
    done()
  }
}
```
