---
layout: post
title: "Python实现排列和组合"
description: "Python实现排列和组合 "
category: Python
tags: [python, arithmetic]
---


无事可做用python实现的的排列和组合的算法，顺便也复习以下2.7中yield的用法

```python
# coding: utf8


def perm(items, n=None):
    if n is None:
        n = len(items)
    for i in range(len(items)):
        v = items[i:i + 1]
        if n == 1:
            yield v
        else:
            _items = items[:i] + items[i + 1:]
            for p in perm(_items):
                yield v + p


def comp(items, n=None):
    if n is None:
        n = len(items) - 1
    for i in range(len(items)):
        v = items[i:i + 1]
        if n == 1:
            yield v
        else:
            _items = items[i + 1:]
            for p in comp(_items, n - 1):
                yield v + p

for x in perm('123'):
    print(x)

print('-' * 20)

for x in comp('123', 2):
    print(x)
```