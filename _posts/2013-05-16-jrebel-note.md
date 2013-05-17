---
layout: post
title: "JRebel小记"
description: "JRebel小记"
category: Java
tags: [java, jrebel]
---




>首先我先承认我标题党了，其实完全算不上简述，只是我这两天使用JRebel的一点心得吧。 当然我用的是盗版啦，谁让我有一个高富帅的心却是一个吊丝的命呢。 至于如何破解什么的请自己到网上搜索。

进入正题，我使用的是 eclipse 4.2+RunJettyRun(jetty当然是8喽)+JRebel5.1 ，不过我用的破解的JRebel是5.0的， 直接覆盖，完全没问题。

首先说一下如何在通过RunJettyRun使用JRebel,其实很简单，只需要在启动的配置的 Arguments > VM Arguments 中加入 “${jrebel_args}”就可以了， 这样在启动的时候就能看到JRebel启动：

    [2012-12-15 22:32:17] 
    [2012-12-15 22:32:17] #############################################################
    [2012-12-15 22:32:17] 
    [2012-12-15 22:32:17]  JRebel 5.0.0 (201206080930)
    [2012-12-15 22:32:17]  (c) Copyright ZeroTurnaround OU, Estonia, Tartu.
    [2012-12-15 22:32:17] 
    [2012-12-15 22:32:17]  Over the last 1 days JRebel prevented 
    [2012-12-15 22:32:17]  at least 2 redeploys/restarts saving you about 0.1 hours.
    [2012-12-15 22:32:17] 
    [2012-12-15 22:32:17]  This product is licensed to Unlimited
    [2012-12-15 22:32:17]  For FUN! Unlimited! Enjoy!
    [2012-12-15 22:32:17] 
    [2012-12-15 22:32:17]  The following plugins are disabled at the moment: 
    [2012-12-15 22:32:17]  * Apache MyFaces plugin (set -Drebel.myfaces_plugin=true to enable)
    [2012-12-15 22:32:17]  * Click plugin (set -Drebel.click_plugin=true to enable)
    [2012-12-15 22:32:17]  * JRuby Plugin (set -Drebel.jruby_plugin=true to enable)
    [2012-12-15 22:32:17]  * Jersey plugin (set -Drebel.jersey_plugin=true to enable)
    [2012-12-15 22:32:17]  * Oracle ADF Core plugin (set -Drebel.adf_core_plugin=true to enable)
    [2012-12-15 22:32:17]  * Oracle ADF Faces plugin (set -Drebel.adf_faces_plugin=true to enable)
    [2012-12-15 22:32:17]  * Seam-Wicket plugin (set -Drebel.seam_wicket_plugin=true to enable)
    [2012-12-15 22:32:17]  * WebObjects plugin (set -Drebel.webobjects_plugin=true to enable)
    [2012-12-15 22:32:17] 
    [2012-12-15 22:32:17] #############################################################
    [2012-12-15 22:32:17] 
    [2012-12-15 22:32:17] 
    [2012-12-15 22:32:17] JRebel: A newer version '5.1.1' is available for download 
    [2012-12-15 22:32:17] JRebel: from http://www.zeroturnaround.com/jrebel/upgrade/
    [2012-12-15 22:32:17] 

当看到上面的信息就说明JRebel已经启动成功了，也就是说现在JRebel已经生效了。

这样你可以去修改一下代码，当然你不会立即看到效果，因为JRebel是延迟加载的，也就是说当你运行到需要加载这个类的时候才会加载， 也就是在控制台上能看到下面的输出：

    [2012-12-15 22:37:43] JRebel: Reloading class 'cn.is.servlet.TestServlet'.

有了这句输出表示所修改的代码已经生效，当然如果修改的类里引用了很多其他的类的实例，在重新加载这个类的时候就会把这些类也加载一次， 如果这次操作还包含其他的一些操作，例如登录的权限验证，而修改的代码引用了和权限有关的类，比方说用户（User）， 那么JRebel也会把和User有关的类加载，加载的顺序和操作的顺序是一样的。

如果在项目中使用的Spring或者Hibernate，可能还可以看到Spring或者Hibernate实体的加载日志，因为Spring和Hibernate的plugin默认是打开的。 在最上面发的日志中，能看到那些日志没有打开，但是看不到那些日志已经打开了，如果在要关闭Spring和Hibernate需要在VM Arguments中才入两个参数， -Drebel.spring_plugin=false, -Drebel.hiberate_plugin=false 加入这两个参数之后，就会在启动的未开启Plugin中看到。

对于这类的热加载插件，还有另外一个就是DCEVM，个人觉得也不错，可惜已经两年没有更新了，只支持jdk1.6和jdk1.7-ea-b139之前的版，对于最新的完全无法使用。

DCEVM和JRebel的区别在于：

* DCEVM是JVM的插件，修改了jvm.dll，从虚拟机入手，效率上来说我觉得比JRebel好快， 但是缺点是如果加载的类有通过Spring注入的实例，很可能会变成null，因为类被重新实例话，但是不是通过Spring实例的， 所以没有为里面引用的其他类进行实例。这个问题并不是一定的，但是我曾经出现过这个问题，而且还不只一次，但是我没有细究， 可以肯定的是对于静态变量等是没有办法重新加载的。

* 而JRebel是从ClassLoader入手的，JRebel在加载的时候会加载这类引用到的所有实例，这样就不会出现DCEVM中出现的问题， 而JRebel也有自己的问题，在某些时候修改的代码次数过多虎抛出一个异常，但是这个异常貌似并没有影响到不能运行，需要重新启动的情况， 也可能是我的类结构比较简单，所以没有影响，因为在网上搜到的别人的文章中有提到过这个异常，但是也没有说会有什么影响。

总的来说JRebel比DCEVM功能更全面，也强大，毕竟是商业软件，且价格不菲，如果环境允许的情况下还是花点钱买个正版的， 毕竟使用盗版也不是什么好事情，而且使用正版也是对软件作者的支持
