#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Tibor Simon'
AUTHOR_POSITION = 'Engineer and guitarist'
AVATAR = 'img/tibor2.png'

SITENAME = 'Engineering with passion'
SITESUBTITLE = 'Engineering with passion'
SITEURL = ''

GITHUB_URL = 'https://github.com/tiborsimon'
DISQUS_SITENAME = 'tiborsimon'
TWITTER_USERNAME = 'tiborsimonio'

PATH = 'content'
RELATIVE_URLS = False

TIMEZONE = 'Europe/Budapest'

DEFAULT_LANG = 'en'

LOAD_CONTENT_CACHE = False

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Menu settings
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

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
DEFAULT_PAGINATION = 6

USE_OPEN_GRAPH = True
OPEN_GRAPH_FB_APP_ID = 551628881652865

PLUGIN_PATHS = ['plugins']
PLUGINS = []
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
	'img',
    'ajax'
]

EXTRA_PATH_METADATA = {
    'extras/favicon.ico': {'path': 'favicon.ico'},
    'extras/googledc76f0415d29fdd5.html': {'path': 'googledc76f0415d29fdd5.html'},
    'extras/robots.txt': {'path': 'robots.txt'},
    'extras/.htaccess': {'path': '.htaccess'}
}

PDF_PROCESSOR = False

DELETE_OUTPUT_DIRECTORY = True

DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
DISPLAY_CATEGORIES_ON_SIDEBAR = True
DISPLAY_TAGS_ON_SIDEBAR = True

MENUITEMS = [
	['Projects', 'projects'],
	['Log', 'log'],
	['About', '#about']
]

# T H E M E   S E T T I N G S -------------------------------------------------
THEME = "themes/material-resume"

FAVICON = 'favicon.ico'

DISPLAY_ARTICLE_INFO_ON_INDEX = True

BOOTSTRAP_NAVBAR_INVERSE = False

# ABOUT_ME = 'Hello, I am Tibor :)'
# AVATAR = 'images/tibor.png'

HIDE_SIDEBAR = True

SHOW_ARTICLE_CATEGORY = True
SHOW_DATE_MODIFIED  = True
