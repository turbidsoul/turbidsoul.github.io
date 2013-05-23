---
layout: post
title: "jekyll的中文标题转换拼音解决方案"
description: "jekyll的中文标题转换拼音解决方案"
category: jekyll
tags: [jekyll, code]
---

整这个并不是什么刚需，纯粹是怕麻烦，直接把中文转换成拼音更方便一点。

其实很简单，问题是出在Rakefile文件中，请看项目下的Rakefile的第52行：

```ruby
task :post do
  abort("rake aborted: '#{CONFIG['posts']}' directory not found.") unless FileTest.directory?(CONFIG['posts'])
  title = ENV["title"] || "new-post"
  tags = ENV["tags"] || "[]"
  category = ENV['category'] || ""
  slug = title.downcase.strip.gsub(' ', '-').gsub(/[^\w-]/, '')
  begin
    date = (ENV['date'] ? Time.parse(ENV['date']) : Time.now).strftime('%Y-%m-%d')
  rescue Exception => e
    puts "Error - date format must be YYYY-MM-DD, please check you typed it correctly!"
    exit -1
  end
  filename = File.join(CONFIG['posts'], "#{date}-#{slug}.#{CONFIG['post_ext']}")
  if File.exist?(filename)
    abort("rake aborted!") if ask("#{filename} already exists. Do you want to overwrite?", ['y', 'n']) == 'n'
  end
  
  puts "Creating new post: #{filename}"
  open(filename, 'w') do |post|
    post.puts "---"
    post.puts "layout: post"
    post.puts "title: \"#{title.gsub(/-/,' ')}\""
    post.puts 'description: ""'
    post.puts "category: "
    post.puts "tags: []"
    post.puts "---"
    post.puts "{% include JB/setup %}"
  end
end # task :post
```

这是Rakefile中关于post的那段代码：`slug = title.downcase.strip.gsub(' ', '-').gsub(/[^\w-]/, '')`，我们只需要在行代码之前加入对标题的转换就可以。

汉字转拼音我用的是[hz2py](https://github.com/elvuel/hz2py),使用`gem install hz2py`就可以安装，使用也很简单：

```ruby
require 'hz2py'

Hz2py.do('听说使用hz2py可以使jekyll支持中文标题，并转换成拼音', :join_with => '-', :to_simplified => true)

# 输出结果
# ting-shuo-shi-yong-hz2py-ke-yi-shi-jekyll-zhi-chi-zhong-wen-biao-ti-,-bing-zhuan-huan-cheng-pin-yin
```

我们只需要把这段代码加入到Rakefile中，就可以了，打开Rakefile在头部加入hz2py，即：`require 'hz2py'`,在`slug = title.downcase.strip.gsub(' ', '-').gsub(/[^\w-]/, '')`上面加上`slug = Hz2py.do(title.encode('utf-8'), :join_with => '-', :to_simplified => true)`就可以了，下面是我修改所的代码片段，请输入被注释框起来的部分：

```ruby
task :post do
  abort("rake aborted: '#{CONFIG['posts']}' directory not found.") unless FileTest.directory?(CONFIG['posts'])
  title = ENV["title"] || "new-post"
  tags = ENV["tags"] || "[]"
  category = ENV['category'] || ""
  #--------------------------------------------------------------------------------------
  slug = Hz2py.do(title.encode('utf-8'), :join_with => '-', :to_simplified => true)
  slug = slug.downcase.strip.gsub(' ', '-').gsub(/[^\w-]/, '')
  #--------------------------------------------------------------------------------------
  begin
    date = (ENV['date'] ? Time.parse(ENV['date']) : Time.now).strftime('%Y-%m-%d')
  rescue Exception => e
    puts "Error - date format must be YYYY-MM-DD, please check you typed it correctly!"
    exit -1
  end
  filename = File.join(CONFIG['posts'], "#{date}-#{slug}.#{CONFIG['post_ext']}")
  if File.exist?(filename)
    abort("rake aborted!") if ask("#{filename} already exists. Do you want to overwrite?", ['y', 'n']) == 'n'
  end
  
  puts "Creating new post: #{filename}"
  open(filename, 'w') do |post|
    post.puts "---"
    post.puts "layout: post"
    post.puts "title: \"#{title.gsub(/-/,' ')}\""
    post.puts 'description: ""'
    post.puts "category: "
    post.puts "tags: []"
    post.puts "---"
    post.puts "{% include JB/setup %}"
  end
end # task :post
```