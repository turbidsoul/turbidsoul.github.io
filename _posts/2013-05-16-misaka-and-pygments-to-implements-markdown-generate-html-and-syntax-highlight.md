---
layout: post
title: "Misaka+pygments实现markdown生成html页面并语法高亮"
description: "Misaka+pygments实现markdown生成html页面并语法高亮"
category: Python
tags: [python, misaka, pygments, markdown]
---
{% include JB/setup %}


## 来由
最近新blog开发到文章页面生成这块，看上了GFM这样的方式，使用markdown编辑页面，也很适合程序猿。使用富文本编辑始终太重量级，并不适合程序猿写文章，所以我也很推崇jekyll，用他来写文章、blog确实很geek也很舒适。

经过几次简单的测试，最后决定使用`Misaka`+`pygments`，下面我简单说一下实现方法。

## 开始之前
我的测试例子中使用到了三个包，分别是 web.py , Misaka , pygments ,如果在开始之前需要使用pip安装这三个包

### Web.py
[Web.py][webpy]是python的一个轻量级web框架，我只是简单的使用了一下，有兴趣的人可以去它的[官网][webpy],它的官方有一个[中文教程][webpy_tutorial]说的很详细。

我这里使用他做一个简单的web服务：

```python
class Index(object):
    def GET(self):
        return "Hello World!"
urls = (
    '/', 'Index'
)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
```

### Misaka

[Misaka][misaka]是一个Markdown的解析工具包，他的Github地址：[https://github.com/FSX/misaka][misaka_github]

Misaka的官网上也有他的[教程][misaka_tutorial]，我在这里只是简单的举个例子，说明一下：

```python
import misaka as m

print m.html('A ~~complex~~ simple example.', extensions=m.EXT_STRIKETHROUGH)
# <p>A <del>complex</del> simple example.</p>

print m.html('The 2^(nd) ~~complex~~ simple example.', 
        extensions=m.EXT_STRIKETHROUGH | m.EXT_SUPERSCRIPT)
# <p>The 2<sup>nd</sup> <del>complex</del> simple example.</p>

print m.html('The 3^(nd) ~~complex~~ <i>simple</i> example.',
        extensions=m.EXT_STRIKETHROUGH | m.EXT_SUPERSCRIPT,
        render_flags=m.HTML_SKIP_HTML)
# <p>The 3<sup>nd</sup> <del>complex</del> simple example.</p>
```

* 上面这三个例子就是misaka的最基本用法。

### pygments

pygments是python的语法高亮工具包，它提供了语法样式 `pygments.styles`,关于styles文档请查看[http://pygments.org/docs/styles/][pygments_styles]

昨天无事可作的时候 把[jekyll][jekyll]的一个主题minimum的样式写成Style,代码如下：

{% gist 5567214 %}

同时它也支持很多语言，具体支持什么语言请参照[Support Language][pygments_lang]

pygments提供一个工具,pygmentize用于生成Style的css文件，但是我不知道这个工具能不能通过css文件生成Style，所以上面的那个Style是我自己手敲的 T_T !

pygmentize的用法：`pygmentize -S default -f html > style.css` 这样就能生成指定的Style的css样式文件

> 命令中的default是Style的名字，你可以在`pygments/styles`下看到

下面的这段代码就是，使用使用`misaka`+`pygments`实现的解析代码

```python
# -*- coding: utf8 -*-
import misaka as m
from misaka import Markdown, HtmlRenderer, SmartyPants
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

# Create a custom renderer


class BleepRenderer(HtmlRenderer, SmartyPants):

    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % text.strip()
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)

# And use the renderer
renderer = BleepRenderer()
md = m.Markdown(renderer,
                extensions=m.EXT_FENCED_CODE | m.EXT_NO_INTRA_EMPHASIS)

print md.render("""
## Title 1

```python
def foo():
    pass

print 'Hello World'
```
""")
```

运行之后生成下面的HTML：

```html
    <h2>
        Title 1
    </h2>
    <div class="highlight">
        <pre>
            <span class="k">
                def
            </span>
            <span class="nf">
                foo
            </span>
            <span class="p">
                ():
            </span>
            <span class="k">
                pass
            </span>
            <span class="k">
                print
            </span>
            <span class="s">
                &#39;Hello World&#39;
            </span>
        </pre>
    </div>
```

加入使用pygmentize生成的样式文件，就能看到语法高亮了。

下面是我的完整代码：

```python
# -*- coding: utf8 -*-

import web
import misaka as m
from misaka import Markdown, HtmlRenderer, SmartyPants
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


class SyntaxHighlightRenderer(HtmlRenderer, SmartyPants):

    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>' % text.strip()
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter(
            linenos=True, style="vim", title="%s code" % lang)
        return highlight(text, lexer, formatter)


class Index(object):
    html_tempalte = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test Page</title>
    <style>
    %s

    pre {
        font-family: Consolas;
    }
    </style>
</head>
<body>
    %s
</body>
</html>
"""

    def GET(self):
        rndr = SyntaxHighlightRenderer()
        formatter = HtmlFormatter(style="minimum")
        md = Markdown(rndr, extensions=m.EXT_FENCED_CODE | m.EXT_NO_INTRA_EMPHASIS)
        result = md.render('''
## Title 1
-------
```python
class Test(object):
    """Test"""
    def __init__(self, arg):
        super(Test, self).__init__()
        self.arg = arg

    def hello(self, name="world"):
        return "hello,", world

t = Test()
print t.hello()
print t.hello("Turbidsoul")
```

```java
public class Test {
    public static void main(String... args) {
        System.out.println("Hello World!");
    }
}
```

```pycon
>>> a = 'foo'
>>> print a
foo
>>> 1 / 0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: integer division or modulo by zero
```
''')
        result = self.html_tempalte % (
            formatter.get_style_defs('.highlight'), result)
        return result


urls = (
    '/', 'Index'
)


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()

```

> 在命令下运行: `python test.py 1234`之后使用 [http://localhost:1234](http://localhost:1234))就能访问,并且看到结果

[webpy]: http://webpy.org "web.py"
[webpy_tutorial]: http://webpy.org/docs/0.3/tutorial.zh-cn "web.py tutorial"
[misaka]: http://misaka.61924.nl/ "Misaka"
[misaka_github]: https://github.com/FSX/misaka "Misaka Github"
[misaka_tutorial]: http://misaka.61924.nl/manual/ "Misaka Tutorial"
[pygments]: http://pygments.org/ "Pygments"
[pygments_style]: http://pygments.org/docs/styles/ "Pygments Style Document"
[pygments_lang]: http://pygments.org/languages/ "Pygments Support Language"
[jekyll]: http://jekyllrb.com/ "Jekyll"