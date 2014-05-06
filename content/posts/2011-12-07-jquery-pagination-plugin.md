title: Jquery分页插件
category: jquery
tags: jquery, javascript, code
Date: 2011-12-07

我们头不让我们使用外面的页面特效脚本，因为页面加载的时候使用太多的不相关页面会影响页面加载的速度。so，只能自己动手去写一个分页插件。

今天没有在公司，没有截到效果图，不过没有关系，我可以说一下我的实现思路，我会在后面把效果图补上。

这个插件有两个主要方法refresh_data和refresh_num_bar，这两个方法是用来刷新，首页，末页，上一页，下一页，以及在这些中间的数字按钮的样式变化。

首先是refresh_data：

```javascript
var refresh_data = function($data, cur_page) {
    $data.find('.peak_comment_li').each(function() {
        $(this).find('#peak_comment_count').peak({
            url: $(this).find("#peak_comment_url").val(),
            msgbox: options['msgbox'],
            peakTagId: "peak_comment_d_count"
        });
        $(this).find('.reply_comment_btn').bind('click', function(event) {
            $(this).parent().parent().find(".reply_comment_li").show();
        });
        $(this).find('.cancel_comment_btn').bind('click', function(event) {
            $(this).parent().hide();
        });
    });

    $('#content_comment_more > dl').remove();
    $('#content_comment_more').append($data);
    if (cur_page == 1) {
        $prev_page.find('a').remove();
        $prev_page.text('上一页');
        $prev_page.addClass('disabled');
        $prev_page.unbind('click');
        $next_page.text('');
        var a = $('<a></a>');
        a.text("下一页");
        $next_page.append(a);
        $next_page.removeClass('disabled');
        $next_page.bind('click', next_page_click);
        refresh_num_bar(cur_page);
    } else if (cur_page == max_page) {
        $next_page.find('a').remove();
        $next_page.text('下一页');
        $next_page.addClass('disabled');
        $next_page.unbind('click');
        $prev_page.text('');
        var a = $('<a></a>');
        a.text("上一页");
        $prev_page.append(a);
        $prev_page.removeClass('disabled');
        $prev_page.bind('click', prev_page_click);
        refresh_num_bar(cur_page);
    } else {
        $prev_page.find('a').remove();
        $prev_page.text('');
        var a_prev = $('<a></a>');
        a_prev.text("上一页");
        $prev_page.append(a_prev);
        $prev_page.removeClass('disabled');
        $prev_page.unbind('click');
        $prev_page.bind('click', prev_page_click);

        refresh_num_bar(cur_page);

        $next_page.find('a').remove();
        $next_page.text('');
        var a_next = $('<a></a>');
        a_next.text("下一页");
        $next_page.append(a_next);
        $next_page.removeClass('disabled');
        $next_page.unbind('click');
        $next_page.bind('click', next_page_click);
    }
};
```

这个方法是为首页，末页和上下页绑定click事件，并调用refresh_num_bar修改数字按钮的样式，重新生成数字按钮，并绑定事件
下面的是refresh_num_bar 方法的代码：

```javascript
var refresh_num_bar = function(cur_page) {
    $num_page_bar.find(".num_page").remove();
    var n = max_page < 9 ? max_page : 9;
    var k = -4;
    for (var i = 1; i <= n; i++) {
                // 这里是用来在当前页是倒数第三页，且显示的按钮是最后一个按钮的时候，把它显示出來
        if (max_page - cur_page == 3 && i == 9) {
            var a = $("<a class='num_page'>" + max_page + "</a>");
            a.bind("click", {
                pageNum: max_page
            }, num_page_click);
            $num_page_bar.append(a);
        }

        if (cur_page + k > max_page) {
                     // 如果当前页是+k已经超过最大页的时候忽略当前循环，但是这个会造成当前那个页是倒数第三页且是最后一个按钮时，
                     // 会造成最后一个按钮无法显示出來，所以在前面的条件是加入这个按钮                     continue;
        }


        if (cur_page - 1 < 5 && cur_page == i) {
            $num_page_bar.append("<span class='num_page current'>" + cur_page + "</span>");
        } else if (cur_page - 1 >= 5 && i == 2) {
            var a = $("<a class='num_page'>...</a>");
            var pageNum = cur_page - 10 <= 0 ? 1 : cur_page - 10;
            a.bind("click", {
                pageNum: pageNum
            }, num_page_click);
            $num_page_bar.append(a);
        } else if (max_page - cur_page >= 5 && i == 8) {
            var a = $("<a class='num_page'>...</a>");
            var pageNum = cur_page + 10 > max_page ? max_page : cur_page + 10;
            a.bind("click", {
                pageNum: pageNum
            }, num_page_click);
            $num_page_bar.append(a);
        } else if (i == 9 && cur_page != max_page) {
            var a = $("<a class='num_page'>" + max_page + "</a>");
            a.bind("click", {
                pageNum: max_page
            }, num_page_click);
            $num_page_bar.append(a);
        } else if (cur_page - 1 >= 5 && i >= 3 && i <= 7) {
            if (k == 0) {
                $num_page_bar.append("<span class='num_page current'>" + cur_page + "</span>");
            } else {
                var a = $("<a class='num_page'>" + (cur_page + k) + "</a>");
                a.bind("click", {
                    pageNum: (cur_page + k)
                }, num_page_click);
                $num_page_bar.append(a);
            }

        } else if (i < 5) {
            var a = $("<a class='num_page'>" + i + "</a>");
            a.bind("click", {
                pageNum: i
            }, num_page_click);
            $num_page_bar.append(a);
        } else if (i > 5) {
            if (cur_page + k < max_page && cur_page + k > i) {
                var a = $("<a class='num_page'>" + (cur_page + k) + "</a>");
                a.bind("click", {
                    pageNum: (cur_page + k)
                }, num_page_click);
                $num_page_bar.append(a);
            }
        }
                                // 下面的这段代码是输出前5个按钮的样式正常显示
        if (cur_page == 3 && i == 5) {
            var a = $("<a class='num_page'>" + i + "</a>");
            a.bind("click", {
                pageNum: i
            }, num_page_click);
            $num_page_bar.append(a);
        }

        if (cur_page == 4 && i >= 5 && i <= 6) {
            var a = $("<a class='num_page'>" + i + "</a>");
            a.bind("click", {
                pageNum: i
            }, num_page_click);
            $num_page_bar.append(a);
        }

        if (cur_page == 5 && i >= 6 && i <= 7) {
            var a = $("<a class='num_page'>" + i + "</a>");
            a.bind("click", {
                pageNum: i
            }, num_page_click);
            $num_page_bar.append(a);
        }


        k++;
    }
};
```


其实这是我现在第一次做web前端开发，并真正的接触jquery和javascript所以问题还很多，这个插件应该还有很多可以优化和修改的地方，但是以我现在的水平只能做到这样了！
