title: python 2.7 的参数解析模块 argparse
category: Python
tags: python, code, argparse, python27
Author: Turbidsoul
Date: 2013-09-27
Summary:  今天下午没事，就优化了一下以前写的一些工作上用的小工具，当然大多数都是python写的命令行下的小工具，之前命令行参数都是自己解析，虽然不是什么复杂的事情，但是自己临时写出来的东西毕竟不如人家写出来的好，正好前短时间看到python2.7把 **argparse** 加入到了标准模块中，所以这次对这些工具的代码重构就是使用了 **argparse** 替代自己写的那个简陋名两行解析工具。

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
* `args.start` 和 `args.end` 这样是读取之前在上面用`add_argument`添加的参数，如果要读取没有添加的参数则会抛出一个异常, 例如:

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

* name or flags: 参数名称或者是一个字符串列表，e.g.: `parser.add_argument('-f', '--foo')`
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

* nargs: 这是用来表示这个参数的值的数量。

N，int，是一个整型数字，指定这个参数的值的个数

```pycon
>>> parser = argparse.ArgumentParser(description='argparse test')
... parser.add_argument('--p1', nargs=2)
... parser.print_help()
...
usage: -c [-h] [--p1 P1 P1]

argparse test

optional arguments:
  -h, --help  show this help message and exit
  --p1 P1 P1

```

'?'， 表示0个或者1个

```pycon
>>> parser = argparse.ArgumentParser(description='argparse test')
... parser.add_argument('--p1', nargs='?')
... parser.print_help()
...
usage: -c [-h] [--p1 [P1]]

argparse test

optional arguments:
  -h, --help  show this help message and exit
  --p1 [P1]

```

'*', 表示0个或者多个

```pycon
>>> parser = argparse.ArgumentParser(description='argparse test')
... parser.add_argument('--p1', nargs='*')
... parser.print_help()
...
usage: -c [-h] [--p1 [P1 [P1 ...]]]

argparse test

optional arguments:
  -h, --help          show this help message and exit
  --p1 [P1 [P1 ...]]

```

'+', 和'*'有点相似，表示的是1个或者多个

```pycon
>>> parser = argparse.ArgumentParser(description='argparse test')
... parser.add_argument('--p1', nargs='+')
... parser.print_help()
...
usage: -c [-h] [--p1 P1 [P1 ...]]

argparse test

optional arguments:
  -h, --help        show this help message and exit
  --p1 P1 [P1 ...]

```

argparse.REMAINDER, 这个是表示把其余的参数都聚集成一个list

```pycon
>>> parser = argparse.ArgumentParser(prog='argtest', description='argparse test')
... parser.add_argument('--p1')
... parser.add_argument('p2')
... parser.add_argument('p3', nargs=argparse.REMAINDER)
... parser.print_help()
...
usage: argtest [-h] [--p1 P1] p2 ...

argparse test

positional arguments:
  p2
  p3

optional arguments:
  -h, --help  show this help message and exit
  --p1 P1

>>> parser.parse_args('--p1 a test b c d e'.split())
Namespace(p1='a', p2='test', p3=['b', 'c', 'd', 'e'])
```

* const，表示一个常量,const有三种形，如下面代码：

```pycon
>>> parser = argparse.ArgumentParser(description='argparse test')
... parser.add_argument('--p1', const=1, action='store_const')
... parser.parse_args(["--p1"])
...
Namespace(p1=1)

>>> parser = argparse.ArgumentParser(description='argparse test')
... parser.add_argument('--p1', const=1, action='append_const')
... parser.parse_args("--p1 --p1".split())
...
Namespace(p1=[1, 1])

>>> parser = argparse.ArgumentParser(description='argparse test')
... parser.add_argument('--p1', const=1, nargs='?')
... parser.parse_args("--p1".split())
...
Namespace(p1=1)
```

* default: 默认值，这里值说明一点，这个参数提供一个`argparse.SUPPESS`,如果命令行下没有这个参数，那么就不会有这个参数的属性，具体的区别，请看下面的代码：

```pycon
>>> parser = argparse.ArgumentParser(description='argparse test')
... parser.add_argument('--p1', default=argparse.SUPPRESS)
... parser.parse_args("--p1 1".split())
...
Namespace(p1='1')

>>> parser = argparse.ArgumentParser(description='argparse test')
... parser.add_argument('--p1', default=argparse.SUPPRESS)
... parser.parse_args("".split())
...
Namespace()

>>> parser = argparse.ArgumentParser(description='argparse test')
... parser.add_argument('--p1')
... parser.parse_args("".split())
...
Namespace(p1=None)

```

* type: 参数类型，也就是声明参数的类型，例如int,file(分为读和写，表示的方式不同),也可以自定义

```pycon
>>> parser = argparse.ArgumentParser(description='argparse test')
... parser.add_argument('--source', type=file)
... parser.add_argument('--target', type=argparse.FileType('w'))
... parser.parse_args("--p1 1 --source source.txt --target target.txt".split())
...
Namespace(p1=1, source=<open file 'source.txt', mode 'r' at 0x0496E6A8>, target=<open file 'target.txt', mode 'w' at 0x0496E548>)


>>> def upper(s):
...     if not s.isupper():
...         raise argparse.ArgumentTypeError('%r not a upper letter' % s)
...     return s
... parser = argparse.ArgumentParser(prog='argtest')
... parser.add_argument('--p1', type=upper)
... parser.parse_args('--p1 A'.split())
...
Namespace(p1='A')

>>> def upper(s):
...     if not s.isupper():
...         raise argparse.ArgumentTypeError('%r not a upper letter' % s)
...     return s
... parser = argparse.ArgumentParser(prog='argtest')
... parser.add_argument('--p1', type=upper)
... parser.parse_args('--p1 a'.split())
...
usage: argtest [-h] [--p1 P1]
argtest: error: argument --p1: 'a' not a upper letter

```

* choices: 提供给参数一组可选择的值，
```pycon
>>> parser = argparse.ArgumentParser(prog='argtest')
... parser.add_argument('--p1', choices=[1,2,3])
... parser.add_argument('--p2', choices=range(1, 10, 2))
... parser.print_help()
...
usage: argtest [-h] [--p1 {1,2,3}] [--p2 {1,3,5,7,9}]

optional arguments:
  -h, --help        show this help message and exit
  --p1 {1,2,3}
  --p2 {1,3,5,7,9}

```

* required: 为True时，表示这个参数是必须的，默认是False
* help: 参数的说明描述，当值为`argparse.SUPPRESS`时，这个参数在参数说明中不显示
* metavar: 对于这个参数我不知道如何解释，可以看一下他的[官方文档][3]和下面的代码应该就能理解。

```pycon
>>> parser = argparse.ArgumentParser(prog='argtest')
... parser.add_argument('-s', '--start')
... parser.add_argument('-e', '--end', metavar='over')
... parser.add_argument('--p3', metavar=['p1', 'p2'])
... parser.print_help()
...
usage: argtest [-h] [-s START] [-e over] [--p3 ['p1', 'p2']]

optional arguments:
  -h, --help            show this help message and exit
  -s START, --start START
  -e over, --end over
  --p3 ['p1', 'p2']
```

* dest 允许用户提供一个自定义的属性名，如下代码：

```pycon
>>> parser = argparse.ArgumentParser(prog='argtest')
... parser.add_argument('-s', '--start', dest='ss')
... parser.print_help()
...
usage: argtest [-h] [-s SS]

optional arguments:
  -h, --help         show this help message and exit
  -s SS, --start SS

>>> parser.parse_args('-s a'.split())
... Namespace(ss='a')
```


## 结论

argparse 还有很多其他功能，我这里之说了连个最常用的，当然我的小工具里也就用了这么多，如果还有兴趣可以自己试一试，python本身确实提供了很多不错的模块，有时候完全没有必要舍本逐末。

[1]: http://docs.python.org/2/library/argparse.html#argumentparser-objects "ArgumentParser objects"
[2]: http://docs.python.org/2/library/argparse.html#the-add-argument-method "The add_argument() method"
[3]: http://docs.python.org/2/library/argparse.html#metavar "metavar"
