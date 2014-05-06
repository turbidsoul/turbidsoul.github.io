title: Nginx实现文件下载自动打包成zip文件
category: Nginx
tags: nginx, python
Author: Turbidsoul
Date: 2014-01-26

## 来源和介绍 ##

问题的来源是需要对已有的资料在下载的时候进行添加广告，但是对于doc文件操作麻烦的情况，采用在下载的时候将广告文件和资料一起打包成zip文件.

在apache服务器中有个mod_zip的模块就是完成这个功能，同样nginx有大神已经实现了这个模块，我们只需要拿来用就可以了:[mod_zip](https://github.com/evanmiller/mod_zip)

## 应用 ##

此模块并不是nginx的默认模块所以需要用户自己编译安装。

安装完成之后，不需要修改任何nginx的任何配置，完成打包都在服务点返回的信息中，下面请看我用python实现的示例：

```python
from bottle import run, route, response
@route('/download')
def download():
    response.set_header('X-Archive-Files', 'zip')
    response.set_header('Content-Type', 'application/octet-stream')
    response.set_header('X-Accel-Chareset', 'utf-8')
    response.set_header('Content-Disposition', r"attachment; filename*=test.zip")
    return """618792700 135 /test.lua 4.lua
3521768339 2865 /ngx_openresty-1.4.2.8/README 5.txt"""
if __name__ == '__main__':
    run(host='192.168.1.196', port=9000, debug=True, reloader=True)
```

这里需要主意两点：

1. response.set_header('X-Archive-Files', 'zip') 这一行就是告诉nginx需要打包成zip文件
2. 就是return返回的那个多行字符串,这里是告诉nginx都要打包那些文件，一行表示一个文件，这里一共四个字段，按顺序依次是 CRC32校验值， 文件大小，源文件路径，打包之后的文件名。

对于第二点还需要在说明一下：

* CRC32的校验值并不是必须的，如果没有可以用'-'代替，但不能什么都不写
* 原文件的路径是相对nginx设置的路径的绝对路径，即就是nginx的root设置的路径，如果没有设置那就是/*/nginx/html这个路径。
* nginx中设置root的时候需要把放置在location外面，放置里面是无法生效的。
* 如果源文件的路径是错误的，那么会产生一个404错误或者下载下来的文件无法解压的损坏文件。
