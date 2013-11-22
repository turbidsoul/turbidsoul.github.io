---
layout: post
title: "python logging 模块的 filter"
description: "python logging 模块的 filter"
category: Python
tags: [python, logging, filter, code]
---

前两天同事问我，如果针对不同的IP记录日志，并把更具IP记录到不同的日志文件中，在网上搜了一下这个问题，有很多人都在问，我查了一下python的logging的api，发现有个filter的，这个filter可以根据日志的信息来决定这条日志是否记录到日志文件中，下面来说说如果实现这个功能。

通常我们配置日志都是如下代码：

```python
import logging

logger = logging.getLogger("test")
hdlr = logging.FileHandler('test.log')
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
fmt = logging.Formatter("%(asctime)s  %(levelname)s  Line#%(lineno)d - %(msecs)d - %(message)s")
hdlr.setFormatter(fmt)
logger.info('test 111111')
```

这是我们通常用来配置记录日志到文件的代码，但是如果我们要把日志记根据条件记录到不同的日志文件中就需要用到 **[logging.Filter][1]**

我们可以对上面的代码做一点点的修改，创建一个过滤器，这个过滤器是根据IP进行过滤的，只有IP是创建过滤器时指定的IP才能被记录下来，下面来看看我创建的过滤器:

```python
import logging

class MyFilter(logging.Filter):
    def __init__(self, ip):
        self.ip = ip

    def filter(self, record):
        if record.msg.startswith(self.ip):
            return True
        return False
```

我的过滤器创建好之后就是要把这个过滤器加入到我们的日志处理句柄上，这里我创建了两个Handler，用来存储不同IP的日志，每个Handler添加不同的过滤器，如下:

```python
logger = logging.getLogger("test")
fmt = logging.Formatter("%(asctime)s  %(levelname)s - %(message)s")
hdlr1 = logging.FileHandler('127.0.0.1.log')
hdlr1.addFilter(MyFilter('127.0.0.1'))
hdlr1.setFormatter(fmt)
hdlr2 = logging.FileHandler('192.168.0.2.log')
hdlr2.addFilter(MyFilter('192.168.0.2'))
hdlr2.setFormatter(fmt)


logger.addHandler(hdlr1)
logger.addHandler(hdlr2)
logger.setLevel(logging.INFO)
```

如上代码，对127.0.0.1开头的日志存到127.0.0.1.log文件中，同样192.168.0.2开头的日志存到192.168.0.2.log文件中

```
127.0.0.1 - - [14/May/2013:20:49:13 +0800] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"
127.0.0.1 - - [14/May/2013:20:49:14 +0800] "GET /favicon.ico HTTP/1.1" 404 168 "-" "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"
127.0.0.1 - - [14/May/2013:20:49:14 +0800] "GET /favicon.ico HTTP/1.1" 404 168 "-" "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"
127.0.0.1 - - [14/May/2013:20:49:14 +0800] "GET /favicon.ico HTTP/1.1" 404 168 "-" "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"
127.0.0.1 - - [14/May/2013:20:49:20 +0800] "GET /codemirror.html HTTP/1.1" 200 6783 "-" "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"
127.0.0.1 - - [14/May/2013:20:49:21 +0800] "GET /codemirror/lib/codemirror.css HTTP/1.1" 200 5705 "http://localhost/codemirror.html" "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"
127.0.0.1 - - [14/May/2013:20:49:21 +0800] "GET /codemirror/theme/rubyblue.css HTTP/1.1" 200 1294 "http://localhost/codemirror.html" "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"
127.0.0.1 - - [14/May/2013:20:49:21 +0800] "GET /codemirror/theme/ambiance.css HTTP/1.1" 200 26029 "http://localhost/codemirror.html" "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"
127.0.0.1 - - [14/May/2013:20:49:21 +0800] "GET /codemirror/theme/eclipse.css HTTP/1.1" 200 1050 "http://localhost/codemirror.html" "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"
127.0.0.1 - - [14/May/2013:20:49:21 +0800] "GET /codemirror/theme/ambiance-mobile.css HTTP/1.1" 200 103 "http://localhost/codemirror.html" "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"
127.0.0.1 - - [14/May/2013:20:49:21 +0800] "GET /codemirror/theme/erlang-dark.css HTTP/1.1" 200 1223 "http://localhost/codemirror.html" "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"
127.0.0.1 - - [14/May/2013:20:49:21 +0800] "GET /codemirror/theme/elegant.css HTTP/1.1" 200 593 "http://localhost/codemirror.html" "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"
127.0.0.1 - - [14/May/2013:20:49:21 +0800] "GET /codemirror/theme/blackboard.css HTTP/1.1" 200 1237 "http://localhost/codemirror.html" "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"
127.0.0.1 - - [14/May/2013:20:49:21 +0800] "GET /codemirror/theme/midnight.css HTTP/1.1" 200 1709 "http://localhost/codemirror.html" "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"
127.0.0.1 - - [14/May/2013:20:49:21 +0800] "GET /codemirror/theme/monokai.css HTTP/1.1" 200 1162 "http://localhost/codemirror.html" "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"
127.0.0.1 - - [14/May/2013:20:49:21 +0800] "GET /codemirror/theme/lesser-dark.css HTTP/1.1" 200 1991 "http://localhost/codemirror.html" "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"
127.0.0.1 - - [14/May/2013:20:49:21 +0800] "GET /codemirror/theme/cobalt.css HTTP/1.1" 200 1048 "http://localhost/codemirror.html" "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"
127.0.0.1 - - [14/May/2013:20:49:21 +0800] "GET /codemirror/theme/night.css HTTP/1.1" 200 1129 "http://localhost/codemirror.html" "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0"
  .
  .
  .
192.168.0.2 - - [16/May/2013:21:39:20 +0800] "GET /assets/themes/twitter/css/pygments.css HTTP/1.1" 200 3348 "http://test.turbidsoul.me/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:40:40 +0800] "GET / HTTP/1.1" 304 0 "http://test.turbidsoul.me/pages.html" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:40:40 +0800] "GET /assets/themes/twitter/css/1.4.0/bootstrap.css HTTP/1.1" 304 0 "http://test.turbidsoul.me/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:40:40 +0800] "GET /assets/themes/twitter/css/style.css?body=1 HTTP/1.1" 304 0 "http://test.turbidsoul.me/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:40:40 +0800] "GET /assets/themes/twitter/css/pygments.css HTTP/1.1" 304 0 "http://test.turbidsoul.me/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:40:47 +0800] "GET / HTTP/1.1" 200 4041 "http://test.turbidsoul.me/pages.html" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:40:47 +0800] "GET /assets/themes/twitter/css/1.4.0/bootstrap.css HTTP/1.1" 200 47729 "http://test.turbidsoul.me/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:40:47 +0800] "GET /assets/themes/twitter/css/style.css?body=1 HTTP/1.1" 200 1657 "http://test.turbidsoul.me/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:40:47 +0800] "GET /assets/themes/twitter/css/pygments.css HTTP/1.1" 200 3348 "http://test.turbidsoul.me/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:41:32 +0800] "GET / HTTP/1.1" 200 3768 "http://test.turbidsoul.me/pages.html" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:41:32 +0800] "GET /assets/themes/twitter/css/1.4.0/bootstrap.css HTTP/1.1" 200 47729 "http://test.turbidsoul.me/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:41:32 +0800] "GET /assets/themes/twitter/css/style.css?body=1 HTTP/1.1" 200 1657 "http://test.turbidsoul.me/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:41:32 +0800] "GET /assets/themes/twitter/css/pygments.css HTTP/1.1" 200 3348 "http://test.turbidsoul.me/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:49:24 +0800] "GET / HTTP/1.1" 200 3969 "http://test.turbidsoul.me/pages.html" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:49:24 +0800] "GET /assets/themes/twitter/css/1.4.0/bootstrap.css HTTP/1.1" 200 47729 "http://test.turbidsoul.me/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:49:24 +0800] "GET /assets/themes/twitter/css/pygments.css HTTP/1.1" 200 3348 "http://test.turbidsoul.me/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:49:24 +0800] "GET /assets/themes/twitter/css/style.css?body=1 HTTP/1.1" 200 1657 "http://test.turbidsoul.me/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:49:26 +0800] "GET /java/2013/05/16/spring-configuration-file-and-annotation-load-question HTTP/1.1" 301 184 "http://test.turbidsoul.me/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:49:26 +0800] "GET /java/2013/05/16/spring-configuration-file-and-annotation-load-question/ HTTP/1.1" 200 14041 "http://test.turbidsoul.me/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:49:26 +0800] "GET /assets/themes/twitter/css/1.4.0/bootstrap.css HTTP/1.1" 304 0 "http://test.turbidsoul.me/java/2013/05/16/spring-configuration-file-and-annotation-load-question/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:49:26 +0800] "GET /assets/themes/twitter/css/style.css?body=1 HTTP/1.1" 304 0 "http://test.turbidsoul.me/java/2013/05/16/spring-configuration-file-and-annotation-load-question/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:49:26 +0800] "GET /assets/themes/twitter/css/pygments.css HTTP/1.1" 304 0 "http://test.turbidsoul.me/java/2013/05/16/spring-configuration-file-and-annotation-load-question/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:54:11 +0800] "GET /tags.html HTTP/1.1" 200 9499 "http://test.turbidsoul.me/java/2013/05/16/spring-configuration-file-and-annotation-load-question/" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:54:11 +0800] "GET /assets/themes/twitter/css/1.4.0/bootstrap.css HTTP/1.1" 304 0 "http://test.turbidsoul.me/tags.html" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:54:11 +0800] "GET /assets/themes/twitter/css/style.css?body=1 HTTP/1.1" 304 0 "http://test.turbidsoul.me/tags.html" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
192.168.0.2 - - [16/May/2013:21:54:11 +0800] "GET /assets/themes/twitter/css/pygments.css HTTP/1.1" 304 0 "http://test.turbidsoul.me/tags.html" "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0"
  .
  .
  .
```

这是我的nginx的access.log中的一段日志，我用这段日志来做测试，最终得到的结果和我最初预设的是一样的，我在这里就不再贴出测试的结果，有兴趣的朋友可以自己测试一下。

[1]: http://docs.python.org/2/library/logging.html?highlight=filter#logging.Filter
