---
layout: post
title: "开发jquery插件"
description: ""
category: jquery
tags: [jquery, javascript, code]
---

开发一个jquery 插件
===================

 公司网站首页广告位需要一个鼠标悬浮切换的特效，但是公司不让使用jquery已经实现过的特效，而公司的这方面的高手又没有时间做，所以只能自己去实现一个这样的特效插件。

 下面是先说下JQuery 插件大概的结构:

```javascript
// 这里这个匿名函数，是为了避免冲突
(function($){
  // 为JQuery 附加一个新的方法
  $.fn.extend({
    //这里需要开发的插件的名字
    fv_adv: function(){
      // 这里就是插件的具体实现代码
    },
    ……
    // 这里可以继续增加插件
  });
})(jQuery);
 ```


 本来想把代码大概的说下的，但是觉得这个插件很简单，没有什么值得特别说说的，jquery的 插件结构就项上面说的那样，一个插件名，对应一个具体的实现，在function里写插件的具体代码，这些东西在网上被人都快说烂了，但是我觉得有些说的 实在不清晰，至少我没看明白，我在这里不像说太多的，有时候对于程序员来说具体的代码，比一本书更管用！

 源代码：[jquery_plugin.7z](http://www.rayfile.com/zh-cn/files/b82a5e82-1a71-11e1-88b6-0015c55db73d/)