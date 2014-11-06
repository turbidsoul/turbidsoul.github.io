Title: 使用awk做实时的统计
Category: Linux
Tags: linux, awk
Date: 2014-04-10
Author: Turbidsoul
Summary:  之前头让搞一个24小时内帖子或者视频的点击量，当时为了省事，就随便写了一个，虽然是实时的，但是却没有满足 **24小时内** 这个条件, 数据会在每天0点清零重新计算，前几天被头发现了，所以就只能从新写一个了。

## 缘由 ##

之前头让搞一个24小时内帖子或者视频的点击量，当时为了省事，就随便写了一个，虽然是实时的，但是却没有满足 **24小时内** 这个条件, 数据会在每天0点清零重新计算，前几天被头发现了，所以就只能从新写一个了。

思来想去最后还是决定用`awk`解析日志来完成这个功能，这样最简单。

## 之前的准备 ##

AWK是贝尔实验室1977年搞出来的文本出现神器，所以有必要做个简单的介绍，大家请看这三篇文章:[AWK 简明教程][1], [linux awk 内置函数详细介绍（实例）][2], [awk教程][3]

这三篇文章是前置的知识，有必要简单的看一下，最开始我觉得awk有点麻烦，写了一些之后我发现他和`lua`一样的简单。

## 代码分析 ##

我们的要求是，分别统计出 _thread_, _resource_, _video_, _article_中，没一个的点击量

```awk
BEGIN {
    FS=",;" # 我的日志中的分隔符是 `,;` 所以这里要给`FS` 指定一下，因为默认值是`Tab` 或者 `Space`
    resource = 0
    article = 0
    thread = 0
    video = 0
    count = 0
}

{
    # url的格式是 http://bbs.xxxxxxx.com/thread-nnnnnnn.html 这里的n就是对应模块的id
    split($3, urls, "=") # $3就是取出第三个变量，第三个变量就是我们的url，这里通过if条件配置各个模块，然后对模块进行+1
    url = urls[2]
    if(index(url, "http://bbs.xxxxxxx.com/thread-") == 1) {
        thread += 1
        count += 1

        # 下面三句就是从URL中解析出ID，并放入对应的模块的map中
        split(url, ids, "-")
        split(ids[2], ids2, ".")
        thread_m[ids2[1]] += 1
    }
    else if(index(url, "http://bbs.xxxxxxx.com/resource-") == 1){
        resource += 1
        count += 1
        split(url, ids, "-")
        split(ids[2], ids2, ".")
        resource_m[ids2[1]] += 1
    }
    else if(index(url, "http://bbs.xxxxxxx.com/video-") == 1){
        video += 1
        count += 1
        split(url, ids, "-")
        split(ids[2], ids2, ".")
        video_m[ids2[1]] += 1
    }
    else if(index(url, "http://bbs.xxxxxxx.com/article-") == 1){
        article += 1
        count += 1
        split(url, ids, "-")
        split(ids[2], ids2, ".")
        article_m[ids2[1]] += 1
    }
}

END {
    print "resource:", resource
    for(k in resource_m) {
        print k":"resource_m[k]
    }
    print "article:", article
    for(k in article_m) {
        print k":"article_m[k]
    }
    print "video:", video
    for(k in video_m) {
        print k":"video_m[k]
    }
    print "thread:", thread
    for(k in thread_m) {
        print k":"thread_m[k]
    }
    print "count:", count
}
```

上面的代码中关键的地方都有加注释，这是不完全的代码，只是实现了解析出各个帖子id并统计，并没有限制24小时之内的，但是这并不影响我们对代码的理解.

除了这些以外awk还支持格式化输出，内建函数，内建变量，正则表达式等等

## 总结 ##

awk说他是神器一点都不为过，处理文本的速度很快，至少比python处理起来要快很多，而且我相信只要愿意awk可以完成复杂的统计任务


[1]: http://coolshell.cn/articles/9070.html (AWK 简明教程)
[2]: http://www.cnblogs.com/chengmo/archive/2010/10/08/1845913.html (linux awk 内置函数详细介绍（实例）)
[3]: http://www.colorfuldays.org/linux/good_awk_tutorial/ (很好的awk教程 )
