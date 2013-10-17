---
layout: post
title: "使用selenium进行web测试入门和使用WebDriver开发web测试代码入门"
description: "使用selenium进行web测试入门和使用WebDriver开发web测试代码入门"
category: Selenium
tags: [selenium, python, java, webdriver, test, code]
draft: true
---

前段时间我们头在搞一个分布式测试，使用的就是 **Selenium** 可以坑太多，最后应该是放弃了，因为我没见到回音，说实话这东西是bug挺多，而且在firefox上的版本兼容也有很大的问题，不过这不是我们讨论的问题，我们这里要讨论的是使用它来做简单的web测试。

## Selenium 入门 ##

#### 安装 ####

我使用的是 Firefox Aurora 现在的版本就是ff26,这下面是正常的，我不知道在每日编译版下是否正常，虽然我机子上也安装了，但是并没有在起下面做个测试，不过应该是没有问题的。

在 [about:addons](about:addons) 或者 [http://addons.mozilla.org/](http://addons.mozilla.org/) 上搜索 *selenium* 点击安装，安装的时候同时还会附带安装几个其他的插件，这些都是 Selenium 的一些附属插件，我在之后的会有介绍。

安装完之后可以在 `菜单 >> 工具 >> Selenium IDE` 打开或者在 *附加组建栏* 点击 Selenium IDE 按钮打开，如何附加组建栏没有，请自行添加。




