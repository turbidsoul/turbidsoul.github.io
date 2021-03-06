title: markdown：简单，轻量级的文档标记语言
category: Markdown
tags: markdown
Date: 2012-09-16


最近喜欢喜欢上了markdown这东西，我觉得他简单，轻量级，易学，是非常适合开发人员用来写文档的工具，也尝试用他写了一些文档，配合这网上找的好的css样式，写出来的文档还是很漂亮和整洁的！

先简单介绍一些Markdown:

Markdown是文档标记，他的表示方式更加简单，让人容易理解和记忆。这是markdown项目的主页:[http://daringfireball.net/projects/markdown/][markdown]


Markdown是用pl写的，不过很多其他语言都有他的实现：

* Python: markdown, markdown2, [misaka](http://misaka.61924.nl/)等， 可以通过easy_install安装
* Java: [markdownj](http://code.google.com/p/markdownj/)

 同时markdown也有一些不错的编辑器：

1. markdownPad：这个需要安装.net，笔者试用过一下，感觉还不错，但是在保存上还有一点瑕疵，让我觉得很不舒服。
2. retext：这是用Python+Qt实现的一个工具，足够小巧，也够轻量级，足够初学者使用
3. MaHua在线markdown编辑器：
4. sublime2: 在sublime2中安装Markdown，Markdown Preview，Markdown Slideshow这三个，当然安装前两个就已经够了，后面这个是我后来装上去，可以用来做HTML的PPT也很方便。

笔者自己使用的是sublime2，所以这里我多说几句：

在sublime2下安装markdown这是markdown的语法包。

Markdown Preview这个是生成HTML文件预览，可以直接在浏览器中看，也可以在sublime2中生成HTML代码，笔者对这个插件做了简单的修改可以让他对应不同的theme，当然这是css都是我在网上搜罗的，笔者是个纯粹的程序猿，对css神马的完全是只能简单修改，让笔者去写那就没有指望了，笔者修改的代码会在稍后介绍，这里先给出插件的下载连接[[Markdown Preview](https://docs.google.com/open?id=0B1L569wdo3IkQ19aeFdkWGtMZWc)]。

Markdown Slideshow也是生成预览的，但是他生成的是PPT形式的，可以用它来做一些HTML的PPT也是一个不错的选择，不过我还没时间研究这个。

本来想简单说下markdown的语法的，但是后来想想没有必要，在[GitHub](https://github.com/)上有个开源项目[Markdown-Syntax-CN](https://github.com/riku/Markdown-Syntax-CN) 这个项目是从 [http://markdown.tw/ ][markdowntw]fork来的，里面有很详细的语法介绍，当然如果你感兴趣也可以fork之后加入自己的东西在Pull Requests，也可以对项目进行校对等。

**本来还有些要说的，但是写道这里觉得应该说的都说了，剩下的可以在google上搜索到，我在这里吹的天花乱坠的都不如去自己试试，感觉一下是否真的好，我一直坚持的是discover，自己去发现，觉得好，然后接推荐给别人。**

[markdown]: http://daringfireball.net/projects/markdown/
[markdowntw]: http://markdown.tw/
