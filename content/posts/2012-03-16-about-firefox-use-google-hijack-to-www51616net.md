title: 关于firefox中使用google搜索被劫持到www5.1616.com的解决办法！
category: firefox
tags: firefox, google
Date: 2012-03-16

这个问题也是我今天早上发现的，搜索东西的时候发现先进入www5.1616.net然后在跳转到google中，感觉像是被劫持了，于是我就在 google上搜索了www5.1616.net发现很多人都有这个问题，而且但是绝大多数都认为是DNS被劫持的问题，但是我觉得不是这样，因为很多人 都和我的情况一样，出现问题的只有他一个，同一局域网下的别人都正常，同一社区下的只有个别的人有这个问题，并不是大面积出现，而且我只有Firefox 有问题，chrome和IE9都正常，所以我肯定是firefox的问题。

后面我有简单的试了几次，发现https下不存在这种现象所以我象应该是他修改我的某些search相关文件，其实在firefox中和search有关的文件就几个，常用的人也都知道：

1. {Profiles}/searchplugins/*.xml
2. {app_root}/searchplugins/*.xml
3. {Profiles}/search.json
4. {Profiles}/search.sqlite
5. {Profiles}/extensions/cehomepage@mozillaonline.com/searchplugins/*.xml

总共就这5个吧，我知道的只有这些.

其实我本来并没有想到会是这几个地方，但是看了月光在2010年5月的一片名为[《Google支持HTTPS加密搜索》](http://www.williamlong.info/archives/2186.html)文章，才想到这点上的。

在网上有些文章说需要删除search.json和search.sqlite，其实不用。先打开search.json，可以格式化一下，看着清楚，直接搜索google，找到后向下拖，看到有下面的代码:

```json
{
    "params": [
        {
            "name": "q",
            "value": "{searchTerms}"
        },
        {
            "name": "id",
            "value": "1157"
        },
        {
            "name": "type",
            "value": "21"
        }
    ],
    "rels": [],
    "template": "http://www5.1616.net/q.php"
}
```

删除这段就可以，记得把上面的逗号也删掉啊！

然 后进入，上面列出第五点下，打开google.xml，把url的属性template修改会原来的值,即 为:http://www.google.com/search然后保存就行了，然后重启firefox，再试试应该已经解决了问题，可能这不是唯一的解 决办法，但是是一个根除的办法，我还没有找到是什么东西修改了这些文件，我也喜欢有人能找到这个东西，并更不出来！

**在上面月光的文章中已经说了google已经启动了https所以我也希望大家都使用https上网，这样更安全一点。**
