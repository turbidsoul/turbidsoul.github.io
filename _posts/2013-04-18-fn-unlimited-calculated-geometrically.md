---
layout: post
title: "fn实现无限计算等比级数"
description: "fn实现无限计算等比级数"
category: Python
tags: [python, arithmetic, functional]
---


今天看InfoQ上的一篇关于 [Fn.py](http://www.infoq.com/cn/articles/fn.py-functional-programming-python) 的文章，Fn中的Stream可以实现无限序列，例如文章中的代码：

```python
f = Stream()
fib = f << [0, 1] << map(lambda x, y: x + y, f, drop(1, f))
```

这是实现了一个无限的斐波那契数列，我根据这个实现了一个等比级数，等比级数的公式是f = b^(n-1), b是基数，n=1 f=1, n>=2 f=b^(n-1)。

我实现的方法使用了生成器：

```python
def geo_sequence(b):
    n = 2
    while 1:
        yield b ** (n - 1)
        n += 1
```

如上面代码，这是一个无限循环的生成器，每次调用next的时候都会得到下一个等比级数


```python
gs = geo_sequence(3)
print gs.next() # output 3
print gs.next() # output 9
print gs.next() # output 27
print gs.next() # output 81
```

如何使用Stream实现无限序列呢？很简单，如下：

```python
f = Stream()
f << geo_sequence(3)
print f[3]
print list(f[:5])
print list(f[3:5])
print list(f[5:10])
```

output:

```pycon
>>> 81
>>> [3, 9, 27, 81, 243]
>>> [81, 243]
>>> [729, 2187, 6561, 19683, 59049]
```

就这样！ 