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

#### ArgumentParser

prog：程序名，是usage后面的第一个字符串，就是上面例子的 *arg_test.py* 默认值是 sys.argv[0], 就是python脚本的名字.

usage： 程序的用法。即使用`print_usage()`打印出来的信息.

epilog：这也是一个帮助文档，但是显示在参数的文档的后面，通常会写一些程序使用例子.

formatter_class：帮助文档的格式化，有三个值，`RawDescriptionHelpFormatter`、`RawTextHelpFormatter`、`ArgumentDefaultsHelpFormatter`，前两其实差不多，都会保持文档的格式，所不同的是第一个会对超长的参数文档进行 **wrap**，第二个不会。第三个参数就不会保持文档的格式了，但是他会显示出参数的默认者等信息，如下：

```pycon
# RawDescriptionHelpFormatter
usage: python arg_test.py [-h] [-s START] [-e END]

Please do not mess up this text!
--------------------------------
    I have indented it
    exaclty the way
    I want it

optional arguments:
  -h, --help            show this help message and exit
  -s START, --start START
                        start number aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
                        aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
  -e END, --end END     end number

test argparse after

# RawTextHelpFormatter
usage: python arg_test.py [-h] [-s START] [-e END]

Please do not mess up this text!
--------------------------------
    I have indented it
    exaclty the way
    I want it

optional arguments:
  -h, --help            show this help message and exit
  -s START, --start START
                        start number aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
  -e END, --end END     end number

test argparse after

# ArgumentDefaultsHelpFormatter
usage: python arg_test.py [-h] [-s START] [-e END]

Please do not mess up this text! -------------------------------- I have
indented it exaclty the way I want it

optional arguments:
  -h, --help            show this help message and exit
  -s START, --start START
                        start number aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
                        aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa (default: 1)
  -e END, --end END     end number (default: 100)

test argparse after
```

上面就是三种formatter_class的表现

prefix_chars：参数前缀，默认是`-`。不过要注意的是，如果改成其他的符号，那么在使用`add_argument()` 方法添加参数的时候，参数的前缀要写成和prefix_chars一样，这里是可以声明多个前缀的。

常用的参数就这些，剩下的几个并不是很常用，所以就不一一介绍，有兴趣的可以看一下官方的文档了解一下

#### add_argument() ####

* name or flags: 参数名称或者是一个字符串列表，e.g.: `parser.add_argument('-f', --foo')`
* action: 指定参数的处理方式。

```pycon
>>> parser = argparse.ArgumentParser()
... parser.add_argument('--p1', action='store_true') # 指定参数默认存储为True
... parser.add_argument('--p2', action='store_false') # 指定参数默认存储为False
... parser.parse_args('--p1 --p2'.split())
...
Namespace(p1=True, p2=False, p3=True)

>>> parser = argparse.ArgumentParser(prog='arg_test')
... parser.add_argument('--p3', action='append')
... parser.parse_args('--p3 1 --p3 2'.split())
...
Namespace(p3=['1', '2'], types=None, v=None)

>>> parser = argparse.ArgumentParser(prog='arg_test')
... parser.add_argument('--str', dest='types', action='append_const', const=str)
... parser.add_argument('--int', dest='types', action='append_const', const=int)
... parser.parse_args('--str --int'.split())
...
Namespace(types=[<type 'str'>, <type 'int'>], v=None)

>>> parser = argparse.ArgumentParser(prog='arg_test')
... parser.add_argument('-v', action='count')
... parser.parse_args(['--version'])
...
arg_test 1.0

```

上面的是 **argparse** 为我们提供的预设一些action，当然也可以自定义action,  例如下面的代码：

```pycon
>>> class MyAction(argparse.Action):
...     def __call__(self, parser, namespace, values, option_string=None):
...         print('%r, %r, %r' % (namespace, values, option_string))
...         setattr(namespace, self.dest, values)
... parser = argparse.ArgumentParser()
... parser.add_argument('--p1', action=MyAction)
... parser.add_argument('p2', action=MyAction)
... args = parser.parse_args('1 --p1 2'.split())
...
Namespace(p1=None, p2=None), '1', None
Namespace(p1=None, p2='1'), '2', '--p1'

>>> args
Namespace(p1='2', p2='1')

```


[1]: http://docs.python.org/2/library/argparse.html#argumentparser-objects "ArgumentParser objects"
[2]: http://docs.python.org/2/library/argparse.html#the-add-argument-method "The add_argument() method"
