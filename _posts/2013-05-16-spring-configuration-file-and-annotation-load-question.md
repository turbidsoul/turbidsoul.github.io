---
layout: post
title: "Spring配置文件加载的疑问和annotation加载的问题"
description: "Spring配置文件加载的疑问和annotation加载的问题"
category: Java
tags: [java, sprint, annotation]
---

Spring配置文件加载的疑问和annotation加载的问题
==============================================

前几天在做一个异步的模块，简单点说就是上传文件后，后台异步解析，前台定时请求解析的日志，并显示，算是一个实时的给用户看到解析的情况和日志，很简单的一个工作，但是我却遇到了一个让我郁闷了2天的问题。

问题的起因是在我做完所有工作后发现异步没有执行，也就是说文件的解析方法是同步运行的，也就是说先解析文件，解析完毕后在返回页面，页面才能请求到解析的日志，但是这会已经解析完了文件，没有达打到之前的需求。

这 里先简单的说下Spring异步的用法，Spring异步的用法很简单，在需要异步的方法加上annotation  `@Async` 声明自方法是异步调用的，同时还要在方法所在类上加上annotation `@Service`或`@Component` 在Spring在加载的时候可以扫描到这个类，然后需要在配置文件中加入`<task:annotation-driven />`，这样就可以在Spring启动的时候，将异步处理器加入全局中，并在调用到有@Async的时候，异步调用。

上面简单说了下如何配置Spring异步，现在我说下我的问题，问题很简单就是配置类Spring 异步，并且确定配置正确，但是异步配置没有起效！问什么呢？我百思不得其解，没有办法，那就debug跟踪Spring的源代码。

在 debug的了几次之后，见到那的了解了Spring配置文件加载的方式，很简单，先加载`application-context.xml`文件，然后根据 文件在去扫描class的注解，比方说在Spring 3.0中加入的`@Autowired` 当Spring扫描到了这个注解，就会在全局的注解处理器（我是这么理解的，其实就是以*AnnotationBeanPostProcessor结尾的 类），而异步的处理是在声明了`<task:annotation-driven />`就会把`AsyncAnnotationBeanPostProcessor`加入到全局的注解处理器中，当遇到了声明了@Async的时候，这个 处理器就会生效，并且进行异步的调用。（我这里说的很简单，其实Spring这里不是这么简单，我是跟了2，30次之后才看明白的，如果有兴趣可以自己跟 踪一下。）

我在跟中的过程中发现`<task:annotation-driven />`生效了，并且把`AsyncAnnotationBeanPostProcessor`加入了全局处理器中，但是在调用的时候却没有这个处理器，我 很疑惑。我检查了一边配置文件，并且看了下web.xml文件，发现我们的web.xml配置是这样的:

```xml
<!-- The definition of the Root Spring Container shared by all Servlets and Filters -->
    <context-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>
                /WEB-INF/spring/root-context.xml
                /WEB-INF/spring/application-context.xml
                /WEB-INF/spring/application-context-shiro.xml
            <!--
            /WEB-INF/spring/application-content-schedule.xml -->
        </param-value>
    </context-param> 
    <listener>
        <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
    </listener>
    <!-- Processes application requests -->
    <servlet>
        <servlet-name>appServlet</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>
                /WEB-INF/spring/appServlet/servlet-context.xml
            </param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>
```

从上面的配置文件可以看出，我们配了两个Spring ，一个是用ContextLoaderListener加载，另一个是靠DispatcherServlet加载，但是在上面的注释用说明了，这两个是可 以互相共享的，也就是说两个是可以互相引用的，事实确实是这样，但是为什么我没法异步呢？

待着这个疑惑我做了一个试验，写了一个测试用例，在测试用例中是这样的:

```java
public class SpringAsyncTest {
    AbstractApplicationContext ctx = new ClassPathXmlApplicationContext("root-context.xml");
 
    @Test
    public void asyncTest() throws Exception {
        IImportMng mng = (IImportMng) ctx.getBean("importMng");
        Future<String> result = mng.testAsync("innate");
        System.out.println("SpringAsyncTest.asyncTest() - 测试结束");
        while (!"stop".equals(result.get())) {
            System.out.println("SpringAsyncTest.asyncTest() - " + mng.getLogAndClear("innate"));
        }
    }
}
```

从上面可以清除看到，我是直接在家的root-context.xml，在root中import了application- context.xml，异步的的配置就在application-context.xml运行之后发现，没有问题，异步执行完全正确，这个测试用例也验 证了我的一个想法，两个Spring Context是可以互相共享，但是确实相对独立的，为了进一步验证我的想法，我在action中，写了一个测试例子，没有用@Autowired注入进 来的，而是使用了WebApplicationContext， 即:`WebApplicationContextUtils.getWebApplicationContext(request.getSession().getServletContext());`， 用它得到Spring Context，然后直接异步方法，保存，运行，结果正确！这样就完全确认了我的想法是正确的，虽然两个Spring Context是可以共享的但是两个Spring的配置和加载确实相对独立的，也就是说ContextLoaderListener和 DispatcherServlet两个都会把配置文件声明要加载的东西加载一边，当这个其中一个没有的时候就会去另一个里面查找（这个我没有确认，只是 我猜测的，因为工作忙，这个问题上已经耽误太多时间，所以就没有继续下去。)，当这个里面有就不会去另一个里面找。

所以，我把配置启动异步 的配置，换到了servlet-context.xml中（也就就是DispatcherServlet），并删掉原来异步配置（这里一定要保证在整个系统中`<task:annotation-driven />`只能出现一次，如果出现两次，或者被加载了两次，Spring就会抛出一个异常指示这个东西只能加载一次），再次重启服务器，上传文件，OK， 成功了！
