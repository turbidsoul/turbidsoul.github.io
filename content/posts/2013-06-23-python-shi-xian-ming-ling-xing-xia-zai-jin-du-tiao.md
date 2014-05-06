title: python实现命令行下载进度条
category: python
tags: python, cmd, ftp, progressbar
Date: 2013-06-23

这是昨晚下班之后同事问我的一个问题，不过当时已经7点，如果在不出公司就会赶不上最后一趟公交车，所以就给同事说回家研究研究礼拜一给他答案，昨晚无事就看了一下。

#### 需要用到的模块

* 使用 **pip** 安装progressbar `pip install progressbar`
* 这里我是从ftp上下载一个或者多个文件，所以我们要用到 **ftplib**。这是python的标准模块，在代码前导入即可
* 我在最后要把代码编译成exe文件所以要用 **py2exe** `pip install py2exe`

#### 原理

我们先来看一下progressbar的是原理，如下代码：

```python
import sys
import time

for x in xrange(0,51):
    sys.stdout.write("Computing: [%s%s] %i%%\r" % ('#' * x , '-' * (50 - x) , x * 2))
    sys.stdout.flush()
    time.sleep(0.02)
```

上面这段代码运行之后的结果：

```pycon
Computing: [##################################################] 100%
```

这是最简单的命令行进度条，只是通过循环向stdio输出进度条，每0.02s向控制台输出，每次都会从新计算#和-的个数，这样就会变化成我们欲行代码时看到的效果，也可以在上面加入对文件传输的速度和文件下载速度的显示，就能做成类似progressbar那样的效果。

#### progressbar的使用

progressbar使用非常简单，如下代码：

```python
from progressbar import ProgressBar
import time

p = ProgressBar(maxval=100).start()
for x in xrange(1,101):
    p.update(x)
    time.sleep(0.1)
p.finish()
```

```pycon
Computing: [##############################>-------------------] 60%
```

**常用数据描述符**

* maxval: 设置progressbar的最大值，我们也可以通过 `p.maxval` 在出程序运行的过程中得到这个值，
* currval: 这个表示的是当前值，可以通过 `p.currval`
* widgets：配置progressbar进度条样式的时候会用到这个，我会在后面介绍

这三个是我代码中用到的，还有很多，可以参考progress文档或者代码

#### 完整代码

{% gist 5844112 %}

这段代码接受4个参数，分别是ftp地址，用户名，密码和需要下载的文件（多个文件使用,分割）

1. 首先和ftp建立连接，并使用循环一个一个的对文件进行处理
2. 通过ftp的size命令得到文件的大小，并把这个值做为progressbar的maxval
3. 下来就是设置进度条的样式，在上面我就说过这个是通过widget实现的。
    * `Percetage()` 显示进度的百分比
    * `Bar(marker='*', left='[', right=']')` 设置进度条的标记符
    * `ETA()` 剩余时间
    * `FileTransferSpeed()` 显示文件的传输速度
4. 现在就是要进行文件传输，并在传输的过程修正进度条，ftp.retrbinary提供了callback，那就只需要在callback中进行更新进度条，并把数据写入本地的文件中
5. 关闭连接

最后就是要编程成exe文件向，我使用的py2exe,如下：

```python
# -*- coding: utf8 -*-


from distutils.core import setup
import py2exe


setup(console=["ftp_download.py"], zipfile=None)

```

应为是命令行工具，所以使用的console，zipfile=表示把python*.zip文件打入exe中。

在cmd下运行如下命令`python ftp_download_exe.py py2exe -b 1`

* ftp_download_exe.py就是上面那段代码保存后的文件
* `-b 1` 表示把所有文件都编译到一个exe文件中，这样我们就只有一个exe文件不会在依赖其他的文件

编译完了之后在dist目录下就是表一好的文件，ftp_download.exe,我们运行一下看看效果： `ftp_download.exe 127.0.0.1 test test PbSetup60.exe,VIDEO0006.mp4`


```
Download [PbSetup60.exe]: 100% [********************] Time: 0:00:05   1.69 MB/s
Download [VIDEO0006.mp4]:  20% [****                ] ETA:  0:00:09   2.24 MB/s
```
