---
layout: post
title: "python 3.3.2 mingw gcc 4.7.1 安装misaka模块时编译报错"
description: "python 3.3.2 mingw gcc 4.7.1 安装misaka模块时编译报错"
category: Python
tags: [python, python33, mingw, gcc]
---


今天安装在 **python3.3.2** 下安装 **misaka**  编译的时候报出了一个编译错误 *gcc: error: unrecognized command line option '-mno-cygwin'*

解决的办法很简单，在 **gcc 4.7** 不支持 **-mno-cygwin** 选项，所以我们只需要把这个选项在编译的时候去掉就行了。

但是在那里去掉呢？python负责编译的模块是 **distutils** 这个包，在这个模块下有个 **cygwinccompiler.py** 文件，打开在297行：

```python
self.set_executables(compiler='gcc -mno-cygwin -O -Wall',
                     compiler_so='gcc -mno-cygwin -mdll -O -Wall',
                     compiler_cxx='g++ -mno-cygwin -O -Wall',
                     linker_exe='gcc -mno-cygwin ',
                     linker_so='%s %s %s'
                                % (self.linker_dll, shared_option,
                                   entry_point))
```


把代码中的 **-mno-cygwin** 去掉即可。