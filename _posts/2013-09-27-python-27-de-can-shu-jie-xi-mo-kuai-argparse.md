---
layout: post
title: "python 2.7 的参数解析模块 argparse"
description: "python 2.7 的参数解析模块 argparse"
category: Python
tags: [python, code, argparse, python27]
published: false
---

今天下午没事，就优化了一下以前写的一些工作上用的小工具，当然大多数都是python写的命令行下的小工具，之前命令行参数都是自己解析，虽然不是什么复杂的事情，但是自己临时写出来的东西毕竟不如人家写出来的好，正好前短时间看到python2.7把 **argparse** 加入到了标准模块中，所以这次对这些工具的代码重构就是使用了 **argparse** 替代自己写的那个简陋名两行解析工具。


## 入门

上面已经说了在 **Python 2.7** 中已经内置了这个模块，所以就不用安装了。可以直接使用`import argparse`导入模块使用，我们先看一个简单的例子：

```pycon
>>> import argparse
>>> parser = argparse.ArgumentParser(description='test argparse')
>>> parser.add_argument('-s', '--start', help='start number', type=int, default=1)
>>> parser.add_argument('-e', '--end', help='end number', type=int, default=100)
>>> 
>>> parser.print_help()
usage: arg_test.py [-h] [-s START] [-e END]

test argparse

optional arguments:
  -h, --help            show this help message and exit
  -s START, --start START
                        start number
  -e END, --end END     end number
>>> parser.print_usage()
usage: arg_test.py [-h] [-s START] [-e END]
>>> args = parser.parse_args()
>>> print(args.start)
start: 1
>>> print(args.end)
end: 100
```

简单的说一下这个例子:
* `ArgumentParser` 这是解析器的入口，此链接[argparse#argumentparser-objects][1]关于此class的参数说明。
* `add_argument` 添加具体命令行参数，这是关于此方法[argparse#the-add-argument-method][2]的说明
* `print_help()` 和 `print_usage()` 这是打印帮助信息和usage，就是python xxxx.py -h 只有打印出的那些帮助信息
* `parser.parse_args()` 这是解析命令行参数
* `args.start` 和 `args.end` 这样是读取之前在上面用`add_argument`添加的参数，如果要读取没有添加的参数则会抛出一个一行, 例如: 

```pycon
>>> args.eee
Traceback (most recent call last):
  File "E:\work\python\test\arg_test.py", line 21, in <module>
    print(args.eee)
AttributeError: 'Namespace' object has no attribute 'eee'
```

这是最简单的例子，argparse 还可以定义参数组，必选参数，参数默认值，参数值类型等等，下来我们来慢慢的看这些是如何设置的。

## ArgumentParser

prog：程序名，是usage后面的第一个字符串，就是上面例子的 *arg_test.py* 默认值是 sys.argv[0], 就是python脚本的名字
usage： 程序的用法。即使用`print_usage()`打印出来的信息
epilog：这也是一个帮助文档，但是显示在参数的文档的后面，通常会写一些程序使用例子






[1]: http://docs.python.org/2/library/argparse.html#argumentparser-objects "ArgumentParser objects"
[2]: http://docs.python.org/2/library/argparse.html#the-add-argument-method "The add_argument() method"
