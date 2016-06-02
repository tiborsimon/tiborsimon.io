#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

SITENAME = 'Engineering with passion'
SITEURL = ''

TIMEZONE = 'Europe/Budapest'

DEFAULT_DATE_FORMAT = '%a %d %B %Y'

AUTHOR = 'Tibor Simon'
AVATAR = 'images/tibor4.jpg'
DISQUS_SITENAME = 'tiborsimon'

SITE_TITLE = 'Tibor Simon - Engineering with Passion'

DESCRIPTION = 'A blog and portfolio about programming, engineering, electronics and music. Tibor, the host, is a graduated electrical engineer from Budapest.'
SHORT_DESCRIPTION = 'A blog and portfolio about programming, engineering, electronics and music.'

PATH = 'content'
RELATIVE_URLS = False

LOAD_CONTENT_CACHE = False


# Permalink settings
ARTICLE_PATHS = ['articles']
ARTICLE_URL = 'blog/{category}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{category}/{slug}/index.html'

PAGE_PATHS = ['pages']
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

USE_PAGER = True
PAGINATED_DIRECT_TEMPLATES = ('archives',)
DEFAULT_PAGINATION = 8

TAG_CLOUD_SORTING = 'alphabetically'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['tag_cloud', 'series', 'summary', 'portfolio', 'neighbors', 'minify']

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

STATIC_PATHS = [
	'extras',
	'images'
]

EXTRA_PATH_METADATA = {
    'extras/favicon.ico': {'path': 'favicon.ico'},
    'extras/googledc76f0415d29fdd5.html': {'path': 'googledc76f0415d29fdd5.html'},
    'extras/lillus-and-tibcsi.html': {'path': 'lillus-and-tibcsi.html'},
    'extras/robots.txt': {'path': 'robots.txt'}
}

PDF_PROCESSOR = False

# T H E M E   S E T T I N G S -------------------------------------------------
THEME = "themes/rhythm"
FAVICON = 'favicon.ico'

# JINJA FILTERS ---------------------------------------------------------------
import math
import time

def middle_index(content, *args):
    return math.ceil(len(content)/2)

def category_count(articles, cat):
    return len([article for article in articles if article.category == cat])

def get_date(a):
    return time.strftime("%Y-%m-%d %H:%M")

JINJA_FILTERS = {
    'middle_index': middle_index,
    'category_count': category_count,
    'get_date': get_date
}
