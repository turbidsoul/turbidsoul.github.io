---
layout: post
title: "一个css错误引起的maven StackOverflowError"
description: "一个css错误引起的maven StackOverflowError"
category: Java
tags: [java, maven, css]
published: true
---

这个问题是我的一个失误造成的，这是上一片文章的后续，我在使用正则做文本替换的时候没有注意到，这个正则在主干上是正常的，但是在分支上执行的时候使一行css少了一个引号，这个问题在浏览器中是暴露不出来的，之后在maven打包的时候对文件做压缩的时候才会出现，下面我们来看看是什么样的问题。

我们项目使用的是 [yuicompressor-maven-plugin][1] 做js和css的压缩，在压缩的过程中出现了下面的错误：

```
---------------------------------------------------
constituent[0]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/aether-api-1.13.1.jar
constituent[1]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/aether-connector-wagon-1.13.1.jar
constituent[2]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/aether-impl-1.13.1.jar
constituent[3]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/aether-spi-1.13.1.jar
constituent[4]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/aether-util-1.13.1.jar
constituent[5]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/commons-cli-1.2.jar
constituent[6]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/maven-aether-provider-3.0.4.jar
constituent[7]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/maven-artifact-3.0.4.jar
constituent[8]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/maven-compat-3.0.4.jar
constituent[9]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/maven-core-3.0.4.jar
constituent[10]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/maven-embedder-3.0.4.jar
constituent[11]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/maven-model-3.0.4.jar
constituent[12]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/maven-model-builder-3.0.4.jar
constituent[13]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/maven-plugin-api-3.0.4.jar
constituent[14]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/maven-repository-metadata-3.0.4.jar
constituent[15]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/maven-settings-3.0.4.jar
constituent[16]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/maven-settings-builder-3.0.4.jar
constituent[17]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/plexus-cipher-1.7.jar
constituent[18]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/plexus-component-annotations-1.5.5.jar
constituent[19]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/plexus-interpolation-1.14.jar
constituent[20]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/plexus-sec-dispatcher-1.3.jar
constituent[21]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/plexus-utils-2.0.6.jar
constituent[22]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/sisu-guava-0.9.9.jar
constituent[23]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/sisu-guice-3.1.0-no_aop.jar
constituent[24]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/sisu-inject-bean-2.3.0.jar
constituent[25]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/sisu-inject-plexus-2.3.0.jar
constituent[26]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/wagon-file-2.2.jar
constituent[27]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/wagon-http-2.2-shaded.jar
constituent[28]: file:/E:/opensource/apache/maven-2.2.1.RELEASE/lib/wagon-provider-api-2.2.jar
---------------------------------------------------
Exception in thread "main" java.lang.StackOverflowError
        at java.util.regex.Pattern$Loop.match(Pattern.java:4683)
        at java.util.regex.Pattern$GroupTail.match(Pattern.java:4615)
        at java.util.regex.Pattern$BranchConn.match(Pattern.java:4466)
        at java.util.regex.Pattern$CharProperty.match(Pattern.java:3694)
        at java.util.regex.Pattern$Branch.match(Pattern.java:4502)
        at java.util.regex.Pattern$GroupHead.match(Pattern.java:4556)
        at java.util.regex.Pattern$Loop.match(Pattern.java:4683)
        at java.util.regex.Pattern$GroupTail.match(Pattern.java:4615)
```

google了一下，有过类似的问题，但是并不完全一样，而且我们项目中并没有使用别的一些插件，所以不会是网上说的哪些问题。

我们项目有主干和一个分支，主干上是没有问题，问题只在分支上出现，当时替换的时候使用的是同一个正则，在主干上既然正常了，分支上应该也不会有问题，所以我觉得正则应该也不会有问题。

我用sublime的diff插件比对了两个项目的 *pom.xml* 也没有差别，本来想用windiff比较两个项目下，style文件的差别，但是放弃了，一是文件还是比较多的，而且两个项目在样式上已经有了一些差别，这样比较很难看出问题所在。

不过maven为我们提供了调试参数 **-X** 输入 `mvn yuicompressor:compress -X` maven就会打印出调试信息：

```
[DEBUG] compress file :F:\work\work1\old_ksdfront\src\main\webapp\resources\style\share\layout.css to F:\work\work1\old_ksdfront\targe
rces\style\share\layout.css
[DEBUG] only compress if input file is younger than existing output file
[DEBUG] use a temporary outputfile (in case in == out)
[DEBUG] start compression
[DEBUG] end compression
[INFO] layout.css (12088b) -> layout.css (10582b)[87%]
###############################################################################
[DEBUG] compress file :F:\work\work1\old_ksdfront\src\main\webapp\resources\style\share\page.css to F:\work\work1\old_ksdfront\target\
es\style\share\page.css
[DEBUG] only compress if input file is younger than existing output file
[DEBUG] use a temporary outputfile (in case in == out)
[DEBUG] start compression
###############################################################################
---------------------------------------------------
```

看我用 *#* 框出的几行和＃之上的只讲有什么差别，从`[DEBUG] start compression` 之后 就没有了，也就是说在业所page.css文件的时候报错了，这样文件就简单了，我需要检查一下这个page.css文件。

我在此用diff比较了两个项目下的page.css文件的差别，唯一可能引起错的地方之后一个：

```css
.new-commentsIco {background: url(/resources/style/images/share/share_c.png") -189px -509px; padding-left: 15px;}
```

url之后的链接少了一个 "**"**",我加上引号之后在运行插件压缩css文件，这次成功了。看来问题就是出在这里。

#### 结论

这个问题并不是一定会一定出现，可能需要特性的环境，我并没有做详细的求证，但是我昨晚在家里的时候就准备写这篇文章，但是我发现我用同样的方式是无法重现问题，可能是我家里的只用了一个css文件，而公司的项目css和js文件会比较多的原因造成的，我并不清楚，写这篇文章的目的只是给遇到这类问题的人提醒，凡事要小心，谨慎，细心和耐心，问题本身并不是什么高深问题，但是我却花了一下午的时间，检查了所有可能出问题的地方，刚开始的时候有些浮躁，并没有去注意这些细节上的问题，但是在两三个小时之后才发现这样并不能解决问题，去洗了个脸，清醒一下，回来沉下心仔细的重新整理一下，其实很快就能解决问题。



[1]: https://github.com/davidB/yuicompressor-maven-plugin "yuicompressor-maven-plugin"