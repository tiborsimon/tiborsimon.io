var metalsmith      = require('metalsmith')
var markdown        = require('metalsmith-markdown')
var highlighter     = require('highlighter')
var layouts         = require('metalsmith-layouts')
var permalinks      = require('metalsmith-permalinks')
var collections     = require('metalsmith-collections')
var define          = require('metalsmith-define')
var pagination      = require('metalsmith-pagination')
var snippet         = require('metalsmith-snippet')
var date            = require('metalsmith-build-date')
var assets          = require('metalsmith-assets')
var compress        = require('metalsmith-gzip')
var sitemap         = require('metalsmith-mapsite')
var discoverHelpers = require('metalsmith-discover-helpers')
var tags            = require('metalsmith-tags')
var drafts          = require('metalsmith-drafts')

if (process.argv[2] === 'production') {
  var BASEURL = 'https://tiborsimon.io'
} else {
  var BASEURL = 'http://localhost:8000'
}

var generateUrl = function(baseurl) {
  return function (files, metalsmith, done) {
    for (var file in files) {
      var target = files[file]
      target.url = baseurl + '/' + target.path + '/'
      if (target.tags) {
        for (var tag in target.tags) {
          var data = target.tags[tag]
          data.url = baseurl + '/tags/' + data.slug + '/'
        }
      }
    }
    done()
  }
}

metalsmith(__dirname)
  .source('content')
  .use(drafts())
  .use(date())
  .use(define({
    blog: {
      url: 'https://tiborsimon.io',
      title: 'Tibor Simon',
      description: 'Hello world.'
    },
    owner: {
      url: 'https://tiborsimon.io',
      name: 'Tibor Simon'
    }
  }))
  .use(collections({
    articles: {
      sortBy: 'date',
      reverse: true
    },
    portfolio: {
      sortBy: 'date',
      reverse: true
    }
  }))
  .use(pagination({
    'collections.articles': {
      perPage: 5,
      first: 'index.html',
      path: 'page/:num/index.html',
      layout: 'index.html'
    }
  }))
  .use(markdown({
    gfm: true,
    tables: true,
    highlight: highlighter()
  }))
  .use(snippet({
    maxLength: 300
  }))
  .use(permalinks())
  .use(discoverHelpers({
    directory: 'helpers',
    pattern: /\.js$/
  }))
  .use(tags({
    handle: 'tags',
    path:'tags/:tag/index.html',
    pathPage: 'tags/:tag/:num/index.html',
    perPage: 6,
    layout:'tag.html',
    sortBy: 'date',
    reverse: true,
    skipMetadata: false,
    slug: {mode: 'rfc3986'}
  }))
  .use(generateUrl(BASEURL))
  .use(layouts({
    engine: 'handlebars',
    partials: 'partials',
    directory: 'layouts'
  }))
  .use(assets({
    source: './assets',
    destination: './assets'
  }))
  // .use(compress())
  .use(sitemap({
    hostname: 'https://tiborsimon.io',
    changefreq: 'daily'
  }))
  .destination('publish')
  .build(function (err) {
    if (err) {
      throw err;
    }
  })
