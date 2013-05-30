---
layout: post
title: "jekyll模版的中文问题"
description: "jekyll模版的中文问题"
category: Jekyll
tags: [jekyll, ruby, code]
---

今天在给blog添加[Creative Commons](http://creativecommons.org/licenses/by/3.0/cn/)(简称CC)时，发现在jekyll的模版中不能加入中文。大概看了一下build时报的错，可以确定应该和jekyll不能发带有中文的文章的问题是一样的，不过出问题的地方不一样。

#### jekyll不能发有中文的文章

出问题的地方是在convertible.rb#31 行：

```ruby
self.content = File.read(File.join(base, name), :encoding => "utf-8")
```

如上面的代码在最后加入编码参数，以utf8读取文件即可，即用上面的代码替换原来的代码就可以了

#### jekyll模版不能包含中文

这问题出在 tags/include.rb#23 行：

```ruby
source = File.read(@file, :encoding => "utf-8")
```

同样的方式，替换原来的代码即可。


#### 结论

同样的问题，应该都可以用同样的方式解决，jekyll作者应该并没有在这里考虑中文的问题，不过我们可以自己解决这个问题，如果有更新jekyll最新版，记得也要改响应的问题位置的相关编码问题。