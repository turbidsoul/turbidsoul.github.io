#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os
curdir = os.path.dirname(__file__)

AUTHOR = u'Turbidsoul'
SITENAME = u"Turbidsoul's 小黑屋"
SITEURL = ''
THEME=os.path.join(curdir, 'pelican-sundown')

ARTICLE_DIR='posts/'
PAGE_DIR='pages/'
OUTPUT_PATH=''

TIMEZONE = 'Asia/Chongqing'
DEFAULT_DATE_FORMAT='%Y年 %B %d日 %a'

DEFAULT_LANG = u'cn'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Turbidsoul\'s 小黑屋', 'http://blog.turbidsoul.me'),
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


STATIC_PATHS = ["images", ]
GRV_URL='/images/avatar.jpg'
TWITTER_USERNAME='Turbidsoul'


PLUGIN_PATH= os.path.join(curdir, 'pelican-plugins')
PLUGINS = ['gravatar', 'googleplus_comments']


AUTHOR_EMAIL='sccn.sq@gmail.com'
