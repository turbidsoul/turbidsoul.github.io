title: sublime插件emmet启动失败
category: Sublime
tags: sublime, python, emmet
Date: 2013-06-05

最近发现我的sublime的emmet失效，查看了控制台，发现在sublime启动的失败，启动的时候报了如下的错误：

```pycon
Traceback (most recent call last):
  File ".\sublime_plugin.py", line 62, in reload_plugin
  File ".\emmet-plugin.py", line 710, in <module>
    init()
  File ".\emmet-plugin.py", line 101, in init
    update_settings()
  File ".\emmet-plugin.py", line 231, in update_settings
    ctx.js()
  File ".\emmet\context.py", line 178, in js
    self.eval_js_file(f)
  File ".\emmet\context.py", line 235, in eval_js_file
    self.js().eval(self.read_js_file(file_path, resolve_path), name=file_path, line=0, col=0)
Boost.Python.ArgumentError: Python argument types in
    JSContext.eval(JSContext, str)
did not match C++ signature:
    eval(class CContext {lvalue}, class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >)
```

看着错误对着代码看了半天有点莫名其妙，就跑去[Github][]上找找看有没有解决的办法，还别说真有一哥们遇到了同样的问题，[Emmet Issue #320][1]，Emmet的作者也对这个Issue给了解释和解决办法：

> For some reason, you have outdated PyV8 package. Try to quit ST editor, manually remove PyV8 folder from Packages and start ST again: it should load recent PyV8 package automatically

大意就是说PyV8的版本过低，需要升级，解决的办法就是关闭sublime并删除sublime插件目录下的PyV8，然后在重启，重启之后sublime就会自动下载PyV8，下载好之后就能正常使用了。




[Github]: https://github.com/sergeche/emmet-sublime/ "Emmet (ex-Zen Coding) for Sublime Text"
[1]: https://github.com/sergeche/emmet-sublime/issues/320 "emmet fails on startup"
