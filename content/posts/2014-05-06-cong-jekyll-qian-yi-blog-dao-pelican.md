Title: 从Jekyll迁移blog到pelican
Date: 2014-04-30
Tags: pelican, jekyll
Category: Pelican
Summary: 这次是一次小的迁移，其实也就是把blog生成器从`jekyll`切换到了`pelican`

这次是一次小的迁移，其实也就是把blog生成器从`jekyll`切换到了`pelican`

至于为什么呢，主要是工作忙，从jekyll升级到2.0之后，在本地就不能测试运行，而且还有各种编码问题，一直没有时间去收拾。
另外一个原因就是我现在主要使用的是`python`做开发，所以使用pelican更加的顺手一些。

---------------------------------

从jekyll到pelican并没有什么特别的地方，主要有两点需要改动的：

* 是所有的post文件的头需要变化，如下：
```markdown
---
layout: news_item
title: "Jekyll 1.0.0 Released"
date: "2013-05-06 02:12:52 +0200"
author: parkr
version: 1.0.0
categories: [release]
---
```
```markdown
title: 关于读书
category: 闲聊
tags: 闲聊, math, code, programer, developer
Author: Turbidsoul
Date: 2013-07-29
```
上面的是jekyll，下面的是pelican

* 是注意文件的生成路径，pelican默认是把文件生成到output中，我这里dev环境下是在output中，但是publish下确实直接在根目录下，这样目录看着有点乱，但是我喜欢这样子

这次这个还只能算是半成品，因为评论还没有想好用那个，不过我可能考虑用国内的评论系统，还在考虑中。。。。。
