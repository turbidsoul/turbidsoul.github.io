---
layout: post
title: "lesscss maven plugin简单的配置"
description: "lesscss maven plugin简单的配置"
category: Maven
tags: [lesscss, maven, java]
---

这其实是一个很简单的问题，本来并不打算写成一片文章的，因为这个文件和另外一个问题是一起的，就是我们在nginx上做css和js文件合并时遇到的，不过在这之前我还遇到了另外一个问题，就是我们开发环境是windows7，而nginx下有个静态文件合并的模块: **http\_concat\_module** ，是[淘宝][1]开源的，这个模块并不是nginx标准模块，所以要使用它需要自己重新编译nginx，具体如何编译我需要一段一点时间整理一下，在之后的文章中会写出来。

至于为什么要使用[less][2]是因为使用了 **http\_concat\_module** 之后css中文件的一些路径出现了错误，需要为css文件设置一些变量，其实使用maven的插件也可以进行变量替换，但是这样只能在maven打包的时候才能起作用，对于开发来说就不行，因为开发必须要求在编译的时候就生效。所以就需要使用maven的另一个插件[lesscss-maven-plugin][3]，这个插件的作用就是在编译的时候就能把less转换成css，这样做对我们最大的好处就是需要修改的地方是最少的，而且能一劳永逸的解决这个问题。

现在我们来说说这个插件如何配置：

#### 添加插件

```xml
<plugin>
    <groupId>org.lesscss</groupId>
    <artifactId>lesscss-maven-plugin</artifactId>
    <version>1.3.3</version>
</plugin>
```

插件添加好后，就能在 _pom.xml_  `plugins` 节点下多出上面的代码

##### 配置插件

```xml
<plugin>
    <groupId>org.lesscss</groupId>
    <artifactId>lesscss-maven-plugin</artifactId>
    <version>1.3.3</version>
    <configuration>
        <sourceDirectory>${project.basedir}/src/main/webapp/less</sourceDirectory>
        <outputDirectory>${project.build.directory}/${project.build.finalName}/css</outputDirectory>
        <compress>true</compress>
    </configuration>
    <executions>
        <execution>
            <goals>
                <goal>compile</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

现在我来解释一下：

* **sourceDirectory** 这个节点是要配置less文件所在目录
* **outputDirectory** 配置的是less文件编译之后生成的css文件所在目录
* **compress** 说明生成的css文件是否要压缩
* **lessJs** 指定一个Less.js文件，默认是插件包中自带的但是版本是1.1.3，如果需要使用最新的那就要指定一个less.js文件
* **force** 当这个值为`true`的时候插件就会强制编译less文件，否则就会在css文件不存在或者源文件有修改的时候才会编译less文件为css文件，默认值是`false`
* **inlcudes** 指定需要编译的文件，默认是{"**\/*.less"}
* **expludes** 指定不需要编译的文件。
* **encoding** 输入css文件的编码，默认是${project.build.sourceEncoding}

下面来看一下运行结果：

less文件：

```css
@color: #4D926F;

#header {
  color: @color;
}
h2 {
  color: @color;
}
```

生成的css文件：

```css
#header{color:#4d926f;}
h2{color:#4d926f;}
```

#### 结论

使用less的目的其实一个，就是为了一劳永逸的解决css文件中对图片引用的地址问题，需要同时兼顾开发和生产环境，当然less的功能并不是只有这一个，他有很多很炫的特性，也能简化css的开发。

--------

2012-6-15 夜 添加

今天对这篇文章最了一些修改，主要是上次写的有些仓促，并没有写清楚，另外是下面需要补充一些东西。

这个插件并不能使用maven的变量过滤，这个在github上也有人提出过[issue 10][5]，是十个月之前提出来的，但是作者并没有给出回复。其实也正常，这个和maven的编译打包过程有关，maven的filter是在package之前compile之后进行的，而且这个插件是在compile是进行less文件编译的，所以它是无法处理的。

但是也不是完全没有办法，我查看了源代码发现它是直接文件对文件的操作，我们可以在这之前先对less文件进行变量替换，然后在进行编译，这样也可以。但是我觉得这样的操作很奇怪，怎么看怎么不舒服。

还有另外一个插件[wro4j][6]，这个插件的功能更为强大，支持css，js合并，压缩，less文件编译，合并，压缩等等丰富的功能，也支持自定义的processor但是如果要实现上面说的应该也要自己实现processor，我并没有看到官方文档或者jboss上介绍，而且官方文档关于less的内容太少，而且做到这里，发现我们的项目使用less之后需要变动的东西太多，主要来自css书写的问题，很多时候为了兼容ie，写了一些非标准的css代码，修改成less之后需要话大量的时间去修正，所以就放弃了less，还是决定采用之前的方案处理。

这里有一个关于wro4j的例子，有兴趣的朋友可以看一下：
[https://github.com/jbosstools/m2e-wro4j/wiki/Sample-twitter-bootstrap-project][7]

[1]: https://github.com/alibaba/nginx-http-concat "HTTP Concatenation module for Nginx"
[2]: http://lesscss.org "The Dynamic Stylesheet language"
[3]: https://github.com/marceloverdijk/lesscss-maven-plugin "Official LESS CSS Maven Plugin"
[4]: http://search.maven.org/ "The Search Engine for The Central Repository"
[5]: https://github.com/marceloverdijk/lesscss-maven-plugin/issues/10 "Add 'filtering' configuration option to allow use ${..} variables in .less files"
[6]: http://code.google.com/p/wro4j/ "Web Resource Optimizer for Java"
[7]: https://github.com/jbosstools/m2e-wro4j/wiki/Sample-twitter-bootstrap-project