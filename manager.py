#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2014-07-13 11:33:28
# @Last Modified 2014-07-13
# @Last Modified time: 2014-07-13 13:09:29

import pelicanconf
import click

@click.group()
def cli():
    pass

@cli.command('post', )
@click.option('--title', required=True, help='create post Title')
@click.option('--tags', help='post tags')
@click.option('--catalog', help='post catalog')
@click.option('--slug', help='post to html slug url')
@click.option('--authors', help='post authors')
@click.option('--summary', help='post summary or descritpion')
def post(title, tags, catalog, slug, authurs, summary):
    print(title)


if __name__ == '__main__':
    cli()
