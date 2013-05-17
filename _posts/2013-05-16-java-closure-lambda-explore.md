---
layout: post
title: "java8的闭包Lambda语句小探 "
description: "java8的闭包Lambda语句小探 "
category: Java
tags: [java, lambda, closure, code]
---

java8的闭包Lambda语句小探
=========================

这是我上个礼拜相对较闲的时候自己做的简单测试，应为那天正好在oschina上看到jdk1.8发布了开发者预览版，正好左右没事，就去下了一个，实验了一下java 的闭包。

java 闭包，也就是Lambda表达式，和python中的lambda是一样的，语法也挺相似：

```java
String result = (String name) -> "Hello, " + name + "!";
```


下面我们来看个具体的例子：

首先定义一个接口:

```java
interface Lamb {
    String str(String name);
}
```

之后我们就能在main方法中写下面的代码，编译并运行：

```java
Lamb str = (String name) -> "Hello, " + name;
System.out.println(str.str("aaa"));
```

运行结果：
`Hello, aaa`
上面是最简单的hello world！

在看一个多参数的例子:

```java
interface MathLamb {
    int add(int x, int y);
}

// main方法
MathLamb ml = (int x, int y) -> x + y;
System.out.println(ml.add(1, 2));
```

运行结果：
`3`

当然除了使用自定义的接口也可以使用jdk自带的接口，我用了一个java.util.Comparable<T>接口，做一个简单的字符串排序：

具体接口请参看java.util.Comparable<T>官方文档。

下面是，lambda语句的实现:

```java
// 定义一个字符串List，乱序添加一下简单字符串
List<String> l = new ArrayList<>();
l.add("2");
l.add("3");
l.add("5");
l.add("1");
l.add("4");
l.add("6");
l.add("8");
l.add("7");

// lambda 语句,第二个参数，本来可以是一个Comparable匿名实现，这里用了一个Lambda语句
Collections.sort(l, (String s1, String s2) -> {return s1.compareTo(s2);});

// 打印结果
for (String s : l) {
    System.out.print(s + " ");
}
System.out.println();
```

运行结果：

1 2 3 4 5 6 7 8

这三个例子都很简单，但是最近几天都比较忙，没有时间继续研究下去，有点可惜！