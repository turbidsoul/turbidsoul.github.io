---
layout: post
title: "IText中文处理问题！！！ "
description: "IText中文处理问题！！！ "
category: Java
tags: [itext, java, code]
---


> 这篇文章是很早之前写的，是我在去第一个公司的时候遇到的问题

这里说的IText中文处理问题，是指两种生成PDF文档是对中文处理的问题：

1. 是直接通过从数据库查询或者自己拼接中文字符串生成PDF文档。
2. 第二种是将一个HTML文档转换成PDF文档时的中文处理。

首先说第一种：
    这种很简单，我们只需为加上这样一句：

```java
BaseFont bf = BaseFont.createFont("STSong-Light","UniGB-UCS2-H",BaseFont.NOT_EMBEDDED);
```
在之后的给Document添加节点是为Paragraph设置字体时设置成BF就可以，如下：

```java
document.add(new Paragraph("混沌之神", new Font(bf)));
```

源码：

```java
/**
 * 生成PDF文件解决中文的例子
 *
 * @throws DocumentException
 * @author <b>Innate Solitary</b><br />
 *         创建时间：<b>2008-6-4 下午09:47:37</b><br />
 * @throws IOException
 */
public static void pdfWriter() throws DocumentException, IOException {
    Document document = new Document();
    PdfWriter.getInstance(document, new FileOutputStream("g:\\Hello.pdf"));
    BaseFont bf = BaseFont.createFont("STSong-Light,Bold", "UniGB-UCS2-H",
            BaseFont.NOT_EMBEDDED);
    document.open();
    document.add(new Paragraph("混沌之神", new Font(bf)));
    document.add(new Paragraph("混沌之神", new Font(bf)));
    document.close();
}
```


第二种有个要求是你给的HTML文档必须XHTML文档，格式必须正确，不正确就会报解析HTML文件错误。
我在解决这个问题的时候在网上看到有人给的解决方法是修改IText中的SAXiTextHandler类的源码，在里面加上一句设置BaseFont的一句话，我测试了这样确实可行，同时也想提出这个解决方法的人致敬，他对IText理解很深入。

我们经理找到一个不用修改源码的解决方法，方法如下：

```java
 /**
  * 将HTML文档转换成PDF文档的中文处理的例子
  *
  * @throws Exception
  * @author <b>Innate Solitary</b><br />
  *         创建时间：<b>2008-6-5 下午09:41:22</b><br />
  */
public static void html2pdf() throws Exception {
    String htmlPath = "g:\\test.html";
    Document doc = new Document();
    BaseFont bf = BaseFont.createFont("STSong-Light,Bold", "UniGB-UCS2-H",
            BaseFont.NOT_EMBEDDED);
    SAXParser parser = SAXParserFactory.newInstance().newSAXParser();
    PdfWriter.getInstance(doc, new FileOutputStream("g:\\test.pdf"));
    SAXmyHtmlHandler saxHandler = new SAXmyHtmlHandler(doc, bf);
    parser.parse(new File(htmlPath), saxHandler);
}
```


上面的是源码，我将源码解释一下。
IText之所以会在处理HTML转换PDF是出错，是因为他的内部没有设置中文编码的字体转换，
即没有这三句：

```java
BaseFont bf = BaseFont.createFont("STSong-Light", "UniGB-UCS2-H", BaseFont.NOT_EMBEDDED);
SAXmyHtmlHandler saxHandler = new SAXmyHtmlHandler(doc, bf);
parser.parse(new File(htmlPath), saxHandler);
```
所以我们只需要将代码改成上面那样，就可以解决中文问题。
这里的SAXParser 是标准的DOM内的SAX解析器，没有测试其他的XML解析器可以处理这里不