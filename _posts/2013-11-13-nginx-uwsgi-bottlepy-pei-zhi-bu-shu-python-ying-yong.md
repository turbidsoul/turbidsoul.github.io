---
layout: post
title: "nginx,uwsgi,bottlepy配置部署python应用"
description: "nginx,uwsgi,bottlepy配置部署python应用"
category: Python
tags: [nginx, uwsgi, python, web, bottlepy]
---

这几天一直在写一个用户行为分析出席清晰代码的工具，我的本意是想把这个用python做成一个独立的应用，但是这么做其实是比较麻烦和有一定难度的，因为用户的行为分析是和要我们主数据库结合做的，如果做成独立应用的话需要从主库中找出大量的数据，这样会影响效率，所以就把用户端分析和cms系统做到以前，前期的日志清洗和数据初期简单的分析做到一个python实现的一个离线工具，这个不是我这篇blog的重点，这次的重点是如何使用nginx，uwsgi，python部署web应用，这只是这次工作的题外话，但是我认为这是这个用户行为分析模块将来的方向，所以研究留用计数备忘和初期探索。


## 搭建环境 ##

因为uwsgi没有windows版的，所以这次是在linux下做的测试，我在虚拟机上装了arch linux。

`pacman -S python nginx`
`pip install uwsgi bottlepy`

arch linux 默认python应该是3.3.2，所以需要安装*pythonbrew*然后在来安装2.7.5,至于pythonbrew如何安装，请自行搜索，安装其实很简单。至于nginx默认是支持uwsgi，所以不需要特别安装其他的插件。

其实也可以通过`pacman -S uwsgi`来安装但是这个是不支持python的，所以需要用户pip安装uwsgi，才能支持python至于[bottlepy](http://bottlepy.org/docs/dev/)我就不多说了，请查看其文档。

## 配置 ##

#### Bottle ####

bottlepy 其实也就是我们的服务端代码，我们这里就简单的一个`Hello World!`

```python
from bottle import run, route, default_app

@route('')
def index():
    return "Hello World!"

if __name__ == '__main__':
    run(host='127.0.0.1', port=9000)
else:
    application = default_app()

```

这就是bottle的代码，很简单，if部分的代码就是普通的main方法运行,而else部分的代码就是我们要和uwsgi对接的代码，这样写就可以了

#### uWSGI ####

我们先来看看http的运行方式，在终端输入`uwsgi --http 192.168.56.101:9000 --wsgi-file app.py`,如果能看到下面的输出就算是运行成功了：

```
*** Starting uWSGI 1.9.19 (32bit) on [Tue Nov 19 23:55:07 2013] ***
compiled with version: 4.8.2 on 14 November 2013 00:18:09
os: Linux-3.11.6-1-ARCH #1 SMP PREEMPT Sat Oct 19 00:29:46 CEST 2013
nodename: localhost
machine: i686
clock source: unix
pcre jit disabled
detected number of CPU cores: 1
current working directory: /opt/openresty/nginx/app
detected binary path: /root/.pythonbrew/pythons/Python-2.7.5/bin/uwsgi
uWSGI running as root, you can use --uid/--gid/--chroot options
*** WARNING: you are running uWSGI as root !!! (use the --uid flag) ***
*** WARNING: you are running uWSGI without its master process manager ***
your processes number limit is 3965
your memory page size is 4096 bytes
detected max file descriptor number: 1024
lock engine: pthread robust mutexes
thunder lock: disabled (you can enable it with --thunder-lock)
uWSGI http bound on 192.168.56.101:9000 fd 4
spawned uWSGI http 1 (pid: 6504)
uwsgi socket 0 bound to TCP address 127.0.0.1:56423 (port auto-assigned) fd 3
Python version: 2.7.5 (default, Nov 13 2013, 23:45:52)  [GCC 4.8.2]
*** Python threads support is disabled. You can enable it with --enable-threads ***
Python main interpreter initialized at 0x94ab820
your server socket listen backlog is limited to 100 connections
your mercy for graceful operations on workers is 60 seconds
mapped 64024 bytes (62 KB) for 1 cores
*** Operational MODE: single process ***
WSGI app 0 (mountpoint='') ready in 0 seconds on interpreter 0x94ab820 pid: 6503 (default app)
*** uWSGI is running in multiple interpreter mode ***
spawned uWSGI worker 1 (and the only) (pid: 6503, cores: 1)
```

这样我们就能在浏览器中输入 `http://192.168.56.101:9000` 之后就能看到`Hello World!`


我们除了使用http方式也可以使用socket或者tcp的方式，对于TCP的方式其实在启动http的时候tcp的就已经启动了，我们可以在启动的日志当中看到这样一句：
`uwsgi socket 0 bound to TCP address 127.0.0.1:56423 (port auto-assigned) fd 3`
这一句就是告诉我们已经把socket绑定到了 tcp地址`127.0.0.1:56423`上，这样也就可以通过nginx配置之后访问，具体的配置我在后面说明。

不过这样启动tcp后面的端口是随机的每次启动都会变化，不适合我们部署，所以我们需要把他配置固定的，所以就需要使用如下的命令:
`uwsgi -s 127.0.0.1:9000 --wsgi-file app.py`，这样之后每次启动的端口都是一样的，但是http就不会在启动了。

而socket的方式和tcp启动的方式参数出差不多，之后把http地址方程一个socket文件的地址：`uwsgi -s ~/app.socket --wsgi-file app.py`，在启动日志中看到`uwsgi socket 0 bound to UNIX address /root/app.socket fd 3` 这一句说明我们socket的地址了

#### nginx ####

在nginx可以使用http反向代理，只需要在nginx里面配置`proxy_pass`代理使用http启动的uwsgi，具体的我就不再多说了。

下面我们来说说socket连接在nginx中如何配置的：

1. 如果uwsgi是`uwsgi -s 127.0.0.1:9000 --wsgi-file app.py`启动的，那就需要在nginx里如下配置

```nginx
location / {
    include uwsgi_params;
    uwsgi_pass 127.0.0.1:9000;
}
```


重载你的nginx，然后访问一下看看是不是成功了。

2. 如果我们使用`uwsgi -s /var/run/app.socket --wsgi-file app.py`， 在nginx中的配置是没有大的变化的，如下:

```nginx
location / {
    include uwsgi_params;
    uwsgi_pass unix:///var/run/app.socket;
}
```

重载nginx之后，看看是不是和上面说的的几种方式一样

不过在这里需要注意的就是如果是使用的socket文件，那么文件的路径就需要注意，不能是随便什么路径，如果是随便的一个路径的话，可能会有下面的错误：

```
2013/11/21 23:17:59 [error] 552#0: *13 connect() to unix:///root/app.socket failed (111: Connection refused) while connecting to upstream, client: 192.168.56.1, server: xxxx.xxxxxx.com, request: "GET / HTTP/1.1", upstream: "uwsgi://unix:///root/app.socket:", host: "xxxx.xxxxxx.com"
```

所以我在这里路径写成`/var/run/x.socket` 是这个路径下的就不会有问题,关于这个问题这里有个帖子应该能解决问题[Trouble with uwsgi + nginx][1]

另外如果错误中有 `13: Permission denied` 这个错误，那可能是在nginx的配置文件中没有声明用户，或者用户没权限，我这里是用root用户登录的，所以在nginx最上面加了`user root;`

## 结论 ##

uwsgi自创了一个uwsgi协议，与wsgi、fcgi不同，据说uwsgi的速度是fcgi的10倍，我没有那个环境测试。uwsgi旨在为分布式部署提供一套解决方案，他支持很多语言，也同时可以使用c,c++等来开发插件，我使用他纯粹是为了在我的VPS上部署我的python应用。


[1]: http://mediadrop.net/community/topic/trouble-with-uwsgi-nginx (Trouble with uwsgi + nginx)
