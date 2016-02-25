#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

SITENAME = 'Engineering with passion'
SITEURL = ''

AUTHOR = 'Tibor Simon'
AUTHOR_POSITION = 'Engineer and guitarist'
AVATAR = 'images/tibor4.jpg'
DISQUS_SITENAME = 'tiborsimon'

PATH = 'content'
RELATIVE_URLS = False

LOAD_CONTENT_CACHE = False

USE_FOLDER_AS_CATEGORY = True

# Permalink settings
ARTICLE_PATHS = ['articles']
ARTICLE_URL = '{category}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{slug}/index.html'

PAGE_PATHS = ['pages']
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'


# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

USE_PAGER = True
PAGINATED_DIRECT_TEMPLATES = ('archives',)
DEFAULT_PAGINATION = 8

TAG_CLOUD_SORTING = 'alphabetically'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['tag_cloud', 'neighbors', 'series', 'summary', 'portfolio']
#PLUGINS = ['tspr', 'summary', 'tag_cloud', 'series', 'figure-generator', 'json-search-system', 'bootstrapify']
#PLUGINS = ['tspr', 'summary', 'json-search-system', 'bootstrapify']

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'daily',
        'indexes': 'daily',
        'pages': 'weekly'
    }
}

# SITELOGO = 'images/tiborsimon-logo-300.png'
# HIDE_SITENAME = True

STATIC_PATHS = [
	'extras',
	'images',
    'ajax'
]

EXTRA_PATH_METADATA = {
    'extras/favicon.ico': {'path': 'favicon.ico'},
    'extras/googledc76f0415d29fdd5.html': {'path': 'googledc76f0415d29fdd5.html'},
    'extras/robots.txt': {'path': 'robots.txt'},
    'extras/.htaccess': {'path': '.htaccess'}
}

PDF_PROCESSOR = False

# T H E M E   S E T T I N G S -------------------------------------------------
THEME = "themes/escape-velocity"

FAVICON = 'favicon.ico'

# JINJA FILTERS ---------------------------------------------------------------
import math

def middle_index(content, *args):
    return math.ceil(len(content)/2)

def category_count(articles, cat):
    return len([article for article in articles if article.category == cat])

JINJA_FILTERS = {
    'middle_index': middle_index,
    'category_count': category_count
}
