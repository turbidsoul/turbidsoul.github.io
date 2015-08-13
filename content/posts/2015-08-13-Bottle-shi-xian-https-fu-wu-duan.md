Title: Bottle实现https服务端
Date: 2015-08-13
Modified: 2015-08-13
Category: Python
Tags: python,ssl,https,bottle
Slug: 2015-08-13-Bottle-shi-xian-https-fu-wu-duan.html
Authors: Turbidsoul Chan
Summary: 最近在研究**OAuth2**，在回调的时候需要一个`https`，因为就是一个简单的demo所以懒的去编译配置nginx，就用bottle服务端使用Python些了一个简单的SSL服务。

## 2 TO 3 ##

年前转了`Python3`所以之后使用的环境都是Python34甚至可能是Python35，因为实在是对`Python27`之前的版本的编码问题很蛋疼。

最近在研究**OAuth2**，在回调的时候需要一个`https`，因为就是一个简单的demo所以懒的去编译配置nginx，就用bottle服务端使用Python些了一个简单的SSL服务。

## 代码 ##

其实代码中除了`bottle`其他的并没有使用第三方的库，我们都知道bottle推荐使用`cherrypy` 不过我还是使用Python自己写了一个简单的ssl服务器，因为足够简单和轻量级。


```python
import ssl
from bottle import redirect, request, route, run, ServerAdapter, app, static_file
from wsgiref.simple_server import WSGIRequestHandler, make_server

class QuietHandler(WSGIRequestHandler):

    def log_request(*args, **kwargs):
        pass


class SslWsgiRefServer(ServerAdapter):

    def run(self, handler):
        if self.quiet:
            self.options['handler_class'] = QuietHandler
        server = make_server(self.host, self.port, handler, **self.options)
        server.socket = ssl.wrap_socket(server.socket,  certfile='server.crt', keyfile='server.key', server_side=True)
        server.serve_forever()


if __name__ == '__main__':
    srv = SslWsgiRefServer(host='localhost', port=443)
    run(app=SessionMiddleware(app(), session_opts), server=srv, reloader=True)

```

上面的代码就是ssl服务的实现，非常的简单，一共就不到10多代码。其中**keyfile**和**certfile**是密钥文件，使用**openssl**可以生成，具体如何生成请看我在evernote上的从[顽石的日志](brooks.wang.blog.163.com)收集的笔记[http://www.evernote.com/l/ABkjPA7aL3BHVokHUNwL_4LCkoYaK9Rz8dc/](http://www.evernote.com/l/ABkjPA7aL3BHVokHUNwL_4LCkoYaK9Rz8dc/)


## 最后说点啥？ ##

最近一年基本没根心过blog，主要是三个原因：

1. 第一是其实一直有写，但是总是觉得自己写的不够，写着写着就废了.
2. 第二是父亲第二次心脏病发住院，跟着姥姥身体也越来越差，被接到我家来住，有点忙
3. 第三是在找女朋友。
