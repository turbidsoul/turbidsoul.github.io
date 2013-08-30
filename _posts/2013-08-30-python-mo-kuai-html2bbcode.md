---
layout: post
title: "python模块html2bbcode"
description: "python模块html2bbcode"
category: Python
tags: [python, code]
---

公司最近在调整网站的模块，把网站的公告模块去掉，公告的数据移到Discuz做的论坛中，整体功能都很简单，写了一个python脚本，执行一下就能完成数据迁移。在数据迁移的过程中有个小问题，我们公告的正文是用富文本编辑器写的，代码是 _html_ 代码，但是在Discuz中确是用 _bbcode_ 所以就需要对公告正文进行转换，这里就要使用到python的一个模块: **html2bbcode**

#### 安装

执行:`pip install html2bbcode` 安装模块

#### 使用

下面是[bitbucket.org][1]的例子：

```pycon
>>> parser = HTML2BBCode()
>>> str(parser.feed('<ul><li>one</li><li>two</li></ul>'))
'[list][li]one[/li][li]two[/li][/list]'
>>> str(parser.feed('<a href="http://google.com/">Google</a>'))
'[url=http://google.com/]Google[/url]'
>>> str(parser.feed('<img src="http://www.google.com/images/logo.png">'))
'[img]http://www.google.com/images/logo.png[/img]'
>>> str(parser.feed('<em>EM test</em>'))
'[i]EM test[/i]'
>>> str(parser.feed('<strong>Strong text</strong>'))
'[b]Strong text[/b]'
>>> str(parser.feed('<code>a = 10;</code>'))
'[code]a = 10;[/code]'
>>> str(parser.feed('<blockquote>Beautiful is better than ugly.</blockquote>'))
'[quote]Beautiful is better than ugly.[/quote]'
""")
```

#### `<p>` 标签的转换

在使用的时候发现，_html2bbcode_ 不能对`<p>`标签进行转换，我们都知道在富文本编辑器中每一段文字都是用`<p>`包裹的，所以我们需要对`<p>`标签转换成`\n`，请看下面代码：


```python
if not p.map.has_section('p'):
    p.map.add_section('p')
    p.map.set('p', 'start', '\n      ')
    p.map.set('p', 'end', '\n')
```

上面的代码就是添加`<p>`转换配置，我这里，对开始标签做了换行和6个空格，结束标签是一个换行


#### 结论

这其实是一个很简单的python模块，只是一个开始，我准备之后每次都会把使用的python模块写一个简单的介绍


[1]: https://bitbucket.org/amigo/html2bbcode "HTML to BBCode converter"