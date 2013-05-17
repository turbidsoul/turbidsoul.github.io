---
layout: post
title: "Sublime2插件Emmet和SublimeV8冲突 "
description: "Sublime2插件Emmet和SublimeV8冲突 "
category: Sublime2
tags: [sublime2, emmet, sublimev8]
---

Zencode很久没有更新，最近在github上看到Zencode的作者[sergeche](https://github.com/sergeche)把Zencode更名为Emmet，并增加了很多新功能.

刚好下午左右没什么事情，就安装了Emmet并卸载了Zencode,可以怎么都没有效果，打开sublime的控制台看了下， 每次按Tab键的时候都会出现下图的错误:

![emmet.png](asets/images/emmet.png)

百思不得其解，最后没办法上Github向[sergeche](https://github.com/sergeche)求助，他告诉我说是SublimeV8引起的， 在移除SublimeV8之后果然问题解决，当然具体什么原因呢，我就不自己陈述了，sergeche给了解释：Issue204

好吧我承认我偷懒了，Emmet的新功能就自己出研究吧。