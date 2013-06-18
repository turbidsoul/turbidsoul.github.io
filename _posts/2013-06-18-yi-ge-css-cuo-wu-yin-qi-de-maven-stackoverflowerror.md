---
layout: post
title: "一个css错误引起的maven StackOverflowError"
description: "一个css错误引起的maven StackOverflowError"
category: Java
tags: [java, maven, css]
published: false
---

这个问题是我的一个失误造成的，这是上一片文章的后续，我在使用正则做文本替换的时候没有注意到，这个正则在主干上是正常的，但是在分支上执行的时候使一行css少了一个引号，这个问题在浏览器中是暴露不出来的，之后在maven打包的时候对文件做压缩的时候才会出现，下面我们来看看是什么样的问题。


