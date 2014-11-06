#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os
curdir = os.path.dirname(__file__)

AUTHOR = u'Turbidsoul'
SITENAME = u"Turbidsoul's 小黑屋"
SITEURL = ''
THEME=os.path.join(curdir, 'pelican-sundown')

ARTICLE_PATHS=['content/posts/',]
PAGE_PATHS=['content/pages/',]
OUTPUT_PATH=''

TIMEZONE = 'Asia/Chongqing'
DEFAULT_DATE_FORMAT='%Y年 %B %d日 %a'
SLUG_DATE_FOTMAT='%Y-%m-%d'

DEFAULT_LANG = u'cn'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (("'Turbidsoul's 小黑屋", 'http://blog.turbidsoul.me'),
          ('My Company Site', 'http://www.kaoshidian.com/'),
          ('PyPI', 'https://pypi.python.org'),)

# Social widget
SOCIAL = (('Google+', 'https://plus.google.com/+TurbidsoulChen'),
          ('Github', 'https://github.com/turbidsoul'),
          ('Twitter', 'https://twitter.com/Turbidsoul'),
          ('Facebook', 'https://facebook.com/turbidsoul'),
          ('微博', 'http://weibo.com/turbidsoul'),
          ('Instagram', 'http://instagram.com/turbidsoul'))

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

ARTICLE_URL='posts/{slug}.html'
ARTICLE_SAVE_AS='posts/{slug}.html'

DEFAULT_METADATA = (('Content-Type', 'text/html; charset=utf-8'),)


# STATIC_PATHS = ["content/images", ]
GRV_URL='/content/images/avatar.jpg'
TWITTER_USERNAME='Turbidsoul'
MD_EXTENSIONS = ['codehilite(css_class=highlight)','extra']
PLUGIN_PATHS=[os.path.join(curdir, 'plugins')]
PLUGINS = ['render_math', 'googleplus_comments']

AUTHOR='Turbidsoul Chan'
AUTHOR_EMAIL='sccn.sq@gmail.com'
