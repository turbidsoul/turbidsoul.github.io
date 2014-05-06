title: python实现morse编码与解码
category: Python
tags: python, morse, code
Date: 2013-06-04

写这个完全是闲着无聊，看了一片趣文[趣文：表白后女生发给我一串五层加密的密码](http://blog.jobbole.com/40628/?utm_source=rss&utm_medium=rss&utm_campaign=draft-created-on-20130531-at-1028-am) 这篇文章来源自百度贴吧的的有一个帖子[传送门](http://tieba.baidu.com/f?kz=529691897)，文章的内容还是很欢乐的。

言归正传，[Morse Code](http://zh.wikipedia.org/zh/%E6%91%A9%E5%B0%94%E6%96%AF%E7%94%B5%E7%A0%81) 的算法是根据维基得来的，说白了就是键值对，编码解码也都是按照键值对进行匹配的。

编码如下：

```python
__morse_code__ = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
    'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
    'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
    'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',

    '1': ['.----', '.-'], '2': ['..---', '..-'], '3': ['...--', '...-'], '4': ['....-', '....-'], '5': ['.....', '.'],
    '6': ['-....', '-....'], '7': ['--...', '-...'], '8': ['---..', '-..'], '9': ['----.', '-.'], '0': ['-----', '-'],

    '.': '.-.-.-', ':': '---...', ',': '--..--', ';': '-.-.-.', '?': '..--..', '=': '-...-', "'": '.---.',
    '/': '-..-.', '!': '-.-.--', '-': '-....-', '_': '..--.-', '"': '.-..-.', '(': '-.--.', ')': '-.--.-',
    '$': '...-..-', '&': '.-...', '@': '.--.-.'
}
```

编码没有什么特别的，不过对于数字有两种编码，长码和短码，长码是五位，短码少的是2位最长是5位，上面的代码中0位上的是长码、1位上的是短码。

在解码的时候需要键值翻转，如下：

```python
__de_morse_code__ = {}

for c in __morse_code__:
    if type(__morse_code__[c]) == list:
        for _c in __morse_code__[c]:
            __de_morse_code__[_c] = c
        continue
    __de_morse_code__[__morse_code__[c]] = c
```

我们来看一下上面那篇趣文中的morse电码：

```
****-/*—-/—-*/****-/****-/*—-/—**/*—-/****-/*—-/-****/***–/****-/*—-/—-*/**—/-****/**—/**—/***–/–***/****-/
```

标准的编码是用`.`和`-`表示 *Dit* 和 *Dah* 上面的编码写成标准的形式如下：

```
....-/.----/----./....-/....-/.----/---../.----/....-/.----/-..../...--/....-/.----/----./..---/-..../..---/..---/...--/--.../....-
```

编码和解码的代码如下：

```python
def morse_encode(data):
    data = data.upper()
    encoded = []
    for c in data:
        if type(__morse_code__[c]) == list:
            encoded.append(__morse_code__[c][0])
        else:
            encoded.append(__morse_code__[c])
    return "/".join(encoded)


def morse_decode(data):
    codes = data.split("/")
    result = []
    for code in codes:
        if code:
            result.append(__de_morse_code__[code])
    return "".join(result)
```

代码很简单，并没有什么特别的，测试代码和运行结果：

```python
result = morse_encode('4194418141634192622374')
print(result)

result = morse_decode(result)
print(result)

result = morse_decode('....-/.----/----./....-/....-/.----/---../.----/....-/.----/-..../...--/....-/.----/----./..---/-..../..---/..---/...--/--.../....-')
print(result)
```

```pycon
>>> ....-/.----/----./....-/....-/.----/---../.----/....-/.----/-..../...--/....-/.----/----./..---/-..../..---/..---/...--/--.../....-
>>> 4194418141634192622374
>>> 4194418141634192622374
```

上面的就是运行结果，下面有两个关于morse的应用：

<iframe src="//zh.wikipedia.org/wiki/File:TVB_News_Theme_Song_Extract.ogg?embedplayer=yes" width="220" height="23" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>

[Morse Code Translation and Copy Practice](http://www.omnicron.com/~ford/java/NMorse.html)
