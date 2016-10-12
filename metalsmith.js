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
var linkcheck       = require('metalsmith-linkcheck')


metalsmith(__dirname)
  .source('src')
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
    },
    moment: require('moment')
  }))
  .use(collections({
    articles: {
      pattern: 'articles/**/*.md',
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
	.use(tags({
    handle: 'tags',
    path:'tags/:tag.html',
    layout:'tag.html',
    sortBy: 'date',
    reverse: true,
    skipMetadata: false,
    slug: {mode: 'rfc3986'}
  }))
  .use(permalinks())
  .use(discoverHelpers({
    directory: 'helpers',
    pattern: /\.js$/
  }))
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
  .destination('build')
  // .use(linkcheck({
  //   verbose: true
  // }))
  .build(function (err) {
    if (err) {
      throw err;
    }
  })
