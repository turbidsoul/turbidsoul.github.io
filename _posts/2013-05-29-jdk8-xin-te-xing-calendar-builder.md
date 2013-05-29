---
layout: post
title: "JDK8新特性 Calendar.Builder"
description: "JDK8新特性 Calendar.Builder"
category: Java
tags: [java, jdk8]
published: true
---

5月23号，Oracle 发布了 jdk8 **M7** 版，这是一个[Feature Complete](http://openjdk.java.net/projects/jdk8/milestones#Feature_Complete)，就是说它已经把所有特性和功能都加入。在翻看 **M7** 的文档时发现了 [*Locale.Builder*][locale_buidler] ，在jdk7的时候加入过一个类似的：[*Locale.Builder*][locale_buidler], 下面我们来看看 [*Calendar.Builder*][calendar_builder]。

#### 允许单语句设置

允许使用 [`set(int, int)`][method_set] 方法，为指定的Field设置值，如下：

```java
import java.util.Calendar;
import java.text.SimpleDateFormat;
import static java.util.Calendar.*;

public static String testSingleStatement() {
    Calendar cal = new Calendar.Builder()
        .set(YEAR, 2013)
        .set(MONTH, MAY)
        .set(DATE, 29)
        .set(HOUR, 8)
        .set(MINUTE, 46)
        .set(SECOND, 40)
        .build();
    System.out.println(stringifyCalendar(cal));
}

public static String stringifyCalendar(Calendar cal) {
    SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
    return sdf.format(cal.getTime());
}
```

#### 允许设置Date和Time

除了[`set(int, int)`][method_set] 这样的方法外，还有还有一些更多参数的方法如：[`setDate(int, int, int)`][method_setdate]，[`setTimeOfDay(int, int, int)`][method_settimeofday] 下面我们来看一个例子：

```java
public static void testSingleStatements2() {
    Calendar cal = new Calendar.Builder()
        .setDate(2013, MAY, 29)
        .setTimeOfDay(14, 1, 25)
        .build();
    System.out.println(stringifyCalendar(cal));
}
```

#### 允许通过Calendar Field设置值

除了上面的两种方法外还可以使用[`setFields(int...)`][method_setfields], 如下：

```java
public static void testSingleStatements3() {
    Calendar cal = new Calendar.Builder()
        .setFields(YEAR, 2013, MONTH, MAY, DATE, 29, HOUR, 14, MINUTE, 25, SECOND, 30)
        .build();
    System.out.println(stringifyCalendar(cal));
}
```

#### 通过Calendar.Builder 转换 Instant 到 Calendar

[Instant][instant] 也是jdk8的新特性，它是[java.time.*][java_time] 下的类，有兴趣的可以区查看一下官方文档，我会在过段时间，研究了之后在发一篇这个包的介绍文章，下面看一下之后的代码:

```java
public static void testSingleStatements4() {
    Calendar cal = new Calendar.Builder()
        .setInstant(Instant.now().toEpochMilli())
        .build();
        System.out.println(stringifyCalendar(cal));
}
```

#### 结论

对于java的日期时间API一直都是被人吐槽的对象，虽然`Calendar.Builder`对写大量关于日期时间相关代码的压力还是有所减少，但是还是觉得不甚如人意，我还是很希望Java对日期时间API的调整更加方便使用，因为每次使用现有的API都忍不住像吐槽一下。

[method_set]: http://download.java.net/jdk8/docs/api/java/util/Calendar.Builder.html#set(int,%20int) "set(int, int)"
[method_setdate]: http://download.java.net/jdk8/docs/api/java/util/Calendar.Builder.html#setDate(int,%20int,%20int) "setDate(int, int, int)"
[method_settimeofday]: http://download.java.net/jdk8/docs/api/java/util/Calendar.Builder.html#setTimeOfDay(int,%20int,%20int) "setTimeOfDay(int, int, int)"
[calendar_builder]: http://download.java.net/jdk8/docs/api/java/util/Calendar.Builder.html "Calendar.Builder"
[locale_buidler]: http://download.java.net/jdk8/docs/api/java/util/Locale.Builder.html "Locale.Builder"
[method_setfields]: http://download.java.net/jdk8/docs/api/java/util/Calendar.Builder.html#setFields(int...) "setFields(int...)"
[instant]: file:///F:/work/Java/doc/docs/api/index.html "Instant"
[java_time]: http://download.java.net/jdk8/docs/api/java/time/package-summary.html "java.time.*"