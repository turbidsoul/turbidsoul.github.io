title: Leibniz公式和Walliz公式估算Pi的值
category: Python
tags: pi, python, leibniz, walliz
Date: 2013-06-08

前两天和同事在聊天的时候说道了 $pi$ 的算法，回家之后在[维基](https://zh.wikipedia.org/wiki/圓周率)上看了一下关于 $pi$ 的公式，正好这回没事干，就用Python实现了两个比较简单的公式，分别是Leibniz 和 Walliz.

## Leibniz

公式如下：

$1 - 1/3 + 1/5 - 1/7 + 1/9 - ... = pi/4$

这个公式也可以用另外一种方式表示：

$pi/4 = sum_{n=0}^{oo} (-1)^n/(2n+1)$

从公式中能看出来，Leibniz是当n趋向于无穷大的时候，计算 $(-1)^n/(2n+1)$的和，用python代码实现如下：

```python
def leibniz_pi(self, n=100):
    reduce(lambda x, y: x + y, [(-1.0) ** x / (2.0 * x + 1.0) for x in xrange(0, n + 1)]) * 4
```


```pycon
>>> leibniz_pi(n=999999)
>>> 3.14159165359
```

## Wallis

公式如下：

$2/1 * 2/3 * 4/3 * 4/5 * 6/5 * 6/7 * 8/7 * 8/9 ... = pi/2$

公式也能如下表示：

$pi/2 = prod_{n=1}^{oo} ((2k)/(2k-1) * (2k)/(2k+1))$

Wallis是一个乘积的运算，计算k从1趋向无穷大的时候 $(2k)/(2k-1) * (2k)/(2k+1)$ 乘积，python代码实现如下：

```python
def wallis_pi(self, n=100):
    return reduce(lambda x, y: x * y, [(2.0 * x / (2.0 * x - 1.0)) * (2.0 * x / (2.0 * x + 1.0)) for x in xrange(1, n + 1)]) * 2
```

```pycon
>>> wallis_pi(n=999999)
>>> 3.14159186819
```

## 结论

两个公式的实现都比较简单，其实对于这类的计算题，只要知道公式现实起来都不会复杂，因为这是把前人智慧的结晶已另外一种方式展现出来，并不是自己的成果，而且我觉得这两个公式的实现代码还有优化的可能，在$n>999999$的时候程序执行的效率明显下降，但是我想就算优化也是有限的，因为$pi$的计算越到后面越是对计算机性能的考验而非算法。

维基上面关$pi$的计算公式还有好多，我也有实验过，但是限于我机子性能的问题，并没有深入下去。维基上也给出了一些更简单的算法，比方说使用反正切函数计算就会更加简单。

**这里我是第一次使用MathJax写数学公式如果有那里错误，请指正出来，我会在最短的时间内修正!**

好了这次先到这里，我要去休息，如果对这些还想有更多的了解，推荐去看一下维基上关于$pi$的介绍。