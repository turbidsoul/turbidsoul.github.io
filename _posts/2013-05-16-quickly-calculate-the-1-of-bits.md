---
layout: post
title: "快速计算二进制位1的个数"
description: "快速计算二进制位1的个数"
category: Python
tags: [python, arithmetic]
---
{% include JB/setup %}

昨天在G+上看到的一个算法题: > Returns the number of 1bits in any integer, for example, bits(2) = 1, > bits(3) = 2, bits(4) = 1, bits(5) = 2, bits(6) = 2, bits(7) = 3 我用python简单的实现了一下，实现的还是有点冗长，应该还能优化。

```python
def bits(n):
    t = 2
    f1 = lambda x: 2 * (x / 2)
    f2 = lambda x: x / 2
    if n % 2 == 0:
        if (n / 2) <= 2:
            t = f1
        else:
            t = f2
        return n / t(n) + n % 2
    else:
        if ((n-1) / 2) <= 2:
            t = f1
        else:
            t = f2
        return n / t(n - 1) + n % 2

print bits(2)
print bits(3)
print bits(4)
print bits(5)
print bits(6)
print bits(7)
```

------------

这会中午无事可干，简单的优化了一下，我这回是用字符来处理的。 不知道会不会在数字特别大的时候有问题

```python
def bits(n):
    return sum(int(c) for c in bin(n) if c  == '1')
```

2013-3-5: 再次优化，传入一个数字n，得到1到n每个数字的的2进制1的个数

```python
bits = lambda num:map(lambda n: sum(int(c) for c in bin(n) if c == '1'), [n for n in range(1, num)])
bits(7)
```
