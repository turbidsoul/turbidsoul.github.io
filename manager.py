#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2014-07-13 11:33:28
# @Last Modified 2014-10-26
# @Last Modified time: 2015-08-17 22:29:18

import os

import click
from click import secho
import pelicanconf
from pypinyin import slug as pyslug
from datetime import date
import jieba

md_template = """Title: {title}
Date: {create_date}
Modified: {modified_date}
Category: {category}
Tags: {tags}
Slug: {slug}
Authors: {authors}
Summary: {summary}

"""

rst_template = """{title}
####################

:date: {create_date}
:modified: {modified_date}
:tags: {tags}
:category: {category}
:slug: {slug}
:authors: {authors}
:summary: {summary}

"""

@click.group(context_settings={'help_option_names':['-h', '--help']})
def cli():
    pass

@cli.command('post', short_help="create post file")
@click.option('--title', required=True, help='create post Title')
@click.option('--tags', help='post tags', multiple=True)
@click.option('--category', help='post category')
@click.option('--slug', help='post to html slug url')
@click.option('--authors', default=[pelicanconf.AUTHOR], help='post authors',
              multiple=True, required=True)
@click.option('--summary', help='post summary or descritpion')
@click.option('--ext', default='md', type=click.Choice(['md', 'rst']),
              help='post file type is md or rst')
def post(title, tags, category, slug, authors, summary, ext):
    '''
    Create post file the ext is markdown or rst

    This post file contains title, tags, category, authors, slug, summary
    '''
    post_dir = os.path.join(pelicanconf.curdir, pelicanconf.ARTICLE_PATHS[0])
    post_name = date.today().strftime(pelicanconf.SLUG_DATE_FOTMAT) + "-" +\
                pyslug(jieba.cut(title), errors='ignore') + '.' + ext
    post_path = os.path.join(post_dir, post_name)
    if os.path.exists(post_path):
        secho('Post file [%s] is exists.' % post_name, fg='red')
        return
    template = md_template
    date_line = date.today().strftime('%Y-%m-%d')
    meta = {
        "title": str(title),
        "tags": ", ".join(tags),
        "category": category if category else '',
        "slug": slug if slug else os.path.splitext(post_name)[0] + '.html',
        "authors": ", ".join(authors),
        "summary": summary if summary else "",
        "create_date": date_line,
        "modified_date": date_line,
    }
    if ext == 'rst':
        template = rst_template
        meta['title'] += "\n" + ("#" * len(meta['title']))

    secho('Create [%s] post:' % ext, fg='cyan')
    secho("\n".join(["  " + k + ":" + (v if v else '') for k, v in meta.items()]), fg='cyan')
    print(meta)
    with open(post_path, 'w', encoding='utf8') as post_file:
        post_file.write(template.format(**meta))
    secho('Create post [%s] success!' % post_name, fg='green')


    

if __name__ == '__main__':
    cli()
