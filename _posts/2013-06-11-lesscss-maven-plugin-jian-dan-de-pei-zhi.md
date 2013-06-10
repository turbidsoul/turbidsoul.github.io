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

* **configuration.sourceDirectory** 这个节点是要配置less文件所在目录
* **configuration.outputDirectory** 配置的是less文件编译之后生成的css文件所在目录
* **configuration.compress** 说明生成的css文件是否要压缩
* **executions.execution.goals.goal** 很明显，告诉maven在编译的时候执行此插件

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

[1]: https://github.com/alibaba/nginx-http-concat "HTTP Concatenation module for Nginx"
[2]: http://lesscss.org "The Dynamic Stylesheet language"
[3]: https://github.com/marceloverdijk/lesscss-maven-plugin "Official LESS CSS Maven Plugin"
[4]: http://search.maven.org/ "The Search Engine for The Central Repository"