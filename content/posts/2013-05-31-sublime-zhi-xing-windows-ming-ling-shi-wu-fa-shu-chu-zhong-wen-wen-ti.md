title: sublime执行windows命令时无法输出中文问题
category: sublime
tags: sublime, python
Date: 2013-05-31

这是一个很简单的问题，我最近在研究jdk8，使用sublime自定义的编译方式运行，是编译运行的结果显示到sublime控制台上，但是这里如果运行的话会提示 *Decode error* 虽然没有太大的影响但是看着总是很难受，而且有时候也不太方便，所以就自己找出问题解决掉。

解决的方式很简单，按 **ctrl+shift+f** 进入高级搜索，在 **find** 中填入 *Decode error* 在 **where** 中填入sublime的插件目录和要所搜的文件类型，如下：``` D:\SublimeText\Data\Packages,*.py``` 因为我们能确定到要搜索的东西在python的代码文件中，所以这里直接搜索 **.py* 文件即可，等上几秒中就能看到搜索结果，结果如下：

```
Searching 8509 files for "Decode error"

D:\SublimeText\Data\Packages\Default\exec.py:
  181              str = data.decode(self.encoding)
  182          except:
  183:             str = "[Decode error - output not " + self.encoding + "]\n"
  184              proc = None
  185

D:\SublimeText\Data\Packages\GoSublime\gosubl\gs.py:
  672       return (res, 'Unexpected value type')
  673   except Exception as ex:
  674:      return (default, 'Decode Error: %s' % ex)
  675
  676  def json_encode(a):


```

第一個就是我們需要修改的地方，直接上在183行上双击，就能打开文件并定位到需要修改的位置。

从代码上看，sublime是对执行结果进行了解码，使用的编码是默认的编码，我这里默认的编码是 **utf8** 但是windows 中文版命令行执行结果的默认编码是 **gbk** 所以这里解码就会报错，所以我们要做的就是如果这里解码报错，则用gbk在解一次码就行了。

这里的代码就修改成如下的样子：

```python
try:
    str = data.decode(self.encoding)
except:
    str = "[Decode error - output not " + self.encoding + "]\n"
    str = data.decode("gbk")
    proc = None
```

#### 结论
其实这样的做法并不是一个好的解决方案，就和jekyll解决中文问题一样，算是一种暴力的方式，但是暴力的方式通常都是最快最省时间的，但是这样的解决方法也容易埋下隐患。
