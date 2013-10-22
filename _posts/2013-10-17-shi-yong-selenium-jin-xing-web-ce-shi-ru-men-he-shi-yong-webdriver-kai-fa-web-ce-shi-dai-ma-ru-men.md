---
layout: post
title: "使用selenium进行web测试入门和使用WebDriver开发web测试代码入门"
description: "使用selenium进行web测试入门和使用WebDriver开发web测试代码入门"
category: Selenium
tags: [selenium, python, java, webdriver, test, code]
published: true
---

前段时间我们头在搞一个分布式测试，使用的就是 **Selenium** 可以坑太多，最后应该是放弃了，因为我没见到回音，说实话这东西是bug挺多，而且在firefox上的版本兼容也有很大的问题，不过这不是我们讨论的问题，我们这里要讨论的是使用它来做简单的web测试。

## Selenium 入门 ##

#### 安装 ####

我使用的是 Firefox Aurora 现在的版本就是ff26,这下面是正常的，我不知道在每日编译版下是否正常，虽然我机子上也安装了，但是并没有在起下面做个测试，不过应该是没有问题的。

在 [about:addons](about:addons) 或者 [http://addons.mozilla.org/](http://addons.mozilla.org/) 上搜索 *selenium* 点击安装，安装的时候同时还会附带安装几个其他的插件，这些都是 Selenium 的一些附属插件，我在之后的会有介绍。

安装完之后可以在 `菜单 >> 工具 >> Selenium IDE` 打开或者在 *附加组建栏* 点击 Selenium IDE 按钮打开，如何附加组建栏没有，请自行添加。

![Selenium IDE 界面](/file/images/selenium1.jpg "Selenium IDE")

上图就是 Selenium IDE 界面，图最右边的红色圆形按钮就是录制按钮，一般在打开的时候这个那就就是按下的，所以可以直接录制。

录制的方式很简单，当点击录制按钮之后就可以在网站的页面向普通浏览网页一样操作，Selenium会自动记录下操作我已经做了简单的几次点击操作，下面使我录制下来的代码：

```html
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head profile="http://selenium-ide.openqa.org/profiles/test-case">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<link rel="selenium.base" href="http://www.kaoshidian.com/" />
<title>New Test</title>
</head>
<body>
<table cellpadding="1" cellspacing="1" border="1">
<thead>
<tr><td rowspan="1" colspan="3">New Test</td></tr>
</thead><tbody>
<tr>
    <td>open</td>
    <td>/</td>
    <td></td>
</tr>
<tr>
    <td>click</td>
    <td>css=div.wrap</td>
    <td></td>
</tr>
<tr>
    <td>clickAndWait</td>
    <td>link=课程中心</td>
    <td></td>
</tr>
<tr>
    <td>clickAndWait</td>
    <td>xpath=(//a[contains(text(),'专业课一对一')])[2]</td>
    <td></td>
</tr>
<tr>
    <td>clickAndWait</td>
    <td>xpath=(//a[contains(text(),'微直播')])[2]</td>
    <td></td>
</tr>
<tr>
    <td>clickAndWait</td>
    <td>link=精彩视频</td>
    <td></td>
</tr>

</tbody></table>
</body>
</html>
```

上面的代码就是录制后的代码，是html代码，当然也可以按照在这样的方法写出来，复制到Selenium中也是可以运行的。

运行的方法很简单，菜单 Actions -> Play entire test suite 就会把录制的脚本运行一边，同时我们也能在浏览器上看到运行的结果。

Selenium可以完成我们在浏览器上的所有操作，因为它就是模拟我们浏览器的操作，所以登录等操作也是没有问题的。这就是Selenium的几本操作，更加复杂的可以自己去探索.

Selenium也可以把录制的宏导出成其他代码，比如java,ruby,php,python,C#,XML等，导出的方法很简单，在菜单中的 文件 -> Export Test Case 就可以看到导出的选项，但是要要导出这些代码，是需要有扩展支持的，一般这些扩展在安装 Selenium IDE 的时候都会提示一起安装，如果在这里没有看到的花，可以在[http://addons.mozilla.org](http://addons.mozilla.org/)搜索，然后安装，重启firefox之后就可以了

## Python ##

如何得到python 的测试代码呢？有两种，第一个就是通过Selenium中提供的导出的方法直接导出，另外一个就是自己编写python代码了。

从Selenium可以导出两种，一种是基于`Webdriver`，另外一个就是基于`Remote Control`：

```python
# webdriver #

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class TestWebdriver(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.kaoshidian.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_webdriver(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_css_selector("div.wrap").click()
        driver.find_element_by_link_text(u"课程中心").click()
        driver.find_element_by_xpath(u"(//a[contains(text(),'专业课一对一')])[2]").click()
        driver.find_element_by_xpath(u"(//a[contains(text(),'微直播')])[2]").click()
        driver.find_element_by_link_text(u"精彩视频").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

#########################################################

# Remote Control #

from selenium import selenium
import unittest, time, re

class test_remote(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*firefox x:/xxxxxxx/Mozilla Firefox/firefox.exe", "http://www.kaoshidian.com/")
        self.selenium.start()

    def test_test_remote(self):
        sel = self.selenium
        sel.open("/")
        sel.click("css=div.wrap")
        sel.click(u"link=课程中心")
        sel.wait_for_page_to_load("30000")
        sel.click(u"xpath=(//a[contains(text(),'专业课一对一')])[2]")
        sel.wait_for_page_to_load("30000")
        sel.click(u"xpath=(//a[contains(text(),'微直播')])[2]")
        sel.wait_for_page_to_load("30000")
        sel.click(u"link=精彩视频")
        sel.wait_for_page_to_load("30000")

    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()


```

在运行这段代码之前，需要安装selenium的python包 `pip install selenium`,如果安装的时候出现`error: invalid command 'egg_info'`这个错误，则需要升级`Setuptools`,运行`pip install -upgrade setuptools`进行升级，如果运行代码的时候，虽然浏览器启动起来了但是没有打开网站之类的情况，则需要升级selenium或者降低安装的浏览器版本，可能是当前安装的版本太低了，和机子上的安装的浏览器版本不兼容。

运行结果如下:
```
C:\Users\Turbidsoul\Desktop>python test_webdriver.py
.
----------------------------------------------------------------------
Ran 1 test in 27.629s

OK
```
对于Remote Control方式，在运行之前需要下载[selenium-server-standalone-<version>.jar](https://code.google.com/p/selenium/downloads/list),下载完成后，在命令行下运行`java -jar selenium-server-standalone-<version>.jar` 启动服务，启动成功后能看下如下信息：

```
十月 21, 2013 11:20:28 下午 org.openqa.grid.selenium.GridLauncher main
信息: Launching a standalone server
3:20:30.219 INFO - Java: Oracle Corporation 21.0-b17
3:20:30.221 INFO - OS: Windows 7 6.1 x86
3:20:30.229 INFO - v2.37.0, with Core v2.37.0. Built from revision a7c61cb
3:20:30.339 INFO - Default driver org.openqa.selenium.iphone.IPhoneDriver registration is skipped: registration capabilities Capabilities [{platform=AC, browserName=iPad, version=}] does not match with current platform: VISTA
3:20:30.356 INFO - Default driver org.openqa.selenium.iphone.IPhoneDriver registration is skipped: registration capabilities Capabilities [{platform=AC, browserName=iPhone, version=}] does not match with current platform: VISTA
3:20:30.407 INFO - RemoteWebDriver instances should connect to: http://127.0.0.1:4444/wd/hub
3:20:30.408 INFO - Version Jetty/5.1.x
3:20:30.409 INFO - Started HttpContext[/selenium-server/driver,/selenium-server/driver]
3:20:30.410 INFO - Started HttpContext[/selenium-server,/selenium-server]
3:20:30.410 INFO - Started HttpContext[/,/]
3:20:30.553 INFO - Started org.openqa.jetty.jetty.servlet.ServletHandler@a450bb
3:20:30.553 INFO - Started HttpContext[/wd,/wd]
3:20:30.558 INFO - Started SocketListener on 0.0.0.0:4444
3:20:30.559 INFO - Started org.openqa.jetty.jetty.Server@314585
```

现在可以运行，Remote Control 那段代码，运行的时候会新打开两个firefox窗口，一个显示当前运行情况的控制台信息，另外一个就是现在我们网站页面，并且可以在运行 *selenium-server-standalong-<version>.jar* 的窗口看到如下信息：

```
23:36:03.707 INFO - creating new remote session
23:36:03.765 INFO - Allocated session c096289dc3174e68b7be194a7bd27447 for http://www.kaoshidian.com/, launching...
jar:file:/E:/opensource/selenium/selenium-server-standalone-2.37.0.jar!/customProfileDirCUSTFFCHROME
23:36:03.925 INFO - Preparing Firefox profile...
23:36:08.889 INFO - Launching Firefox...
23:36:15.537 INFO - Got result: OK,c096289dc3174e68b7be194a7bd27447 on session c096289dc3174e68b7be194a7bd27447
23:36:15.543 INFO - Command request: open[/, True] on session c096289dc3174e68b7be194a7bd27447
23:36:19.860 INFO - Got result: OK on session c096289dc3174e68b7be194a7bd27447
23:36:19.866 INFO - Command request: click[css=div.wrap, ] on session c096289dc3174e68b7be194a7bd27447
23:36:19.889 INFO - Got result: OK on session c096289dc3174e68b7be194a7bd27447
23:36:19.893 INFO - Command request: click[link=课程中心, ] on session c096289dc3174e68b7be194a7bd27447
23:36:19.926 INFO - Got result: OK on session c096289dc3174e68b7be194a7bd27447
23:36:19.931 INFO - Command request: waitForPageToLoad[30000, ] on session c096289dc3174e68b7be194a7bd27447
23:36:21.832 INFO - Got result: OK on session c096289dc3174e68b7be194a7bd27447
23:36:21.838 INFO - Command request: click[xpath=(//a[contains(text(),'专业课一对一')])[2], ] on session c096289dc3174e68b7be194a7bd27447
23:36:21.870 INFO - Got result: OK on session c096289dc3174e68b7be194a7bd27447
23:36:21.876 INFO - Command request: waitForPageToLoad[30000, ] on session c096289dc3174e68b7be194a7bd27447
23:36:25.504 INFO - Got result: OK on session c096289dc3174e68b7be194a7bd27447
23:36:25.509 INFO - Command request: click[xpath=(//a[contains(text(),'微直播')])[2], ] on session c096289dc3174e68b7be194a7bd27447
23:36:25.528 INFO - Got result: OK on session c096289dc3174e68b7be194a7bd27447
23:36:25.534 INFO - Command request: waitForPageToLoad[30000, ] on session c096289dc3174e68b7be194a7bd27447
23:36:28.735 INFO - Got result: OK on session c096289dc3174e68b7be194a7bd27447
23:36:28.740 INFO - Command request: click[link=精彩视频, ] on session c096289dc3174e68b7be194a7bd27447
23:36:28.767 INFO - Got result: OK on session c096289dc3174e68b7be194a7bd27447
23:36:28.773 INFO - Command request: waitForPageToLoad[30000, ] on session c096289dc3174e68b7be194a7bd27447
23:36:30.402 INFO - Got result: OK on session c096289dc3174e68b7be194a7bd27447
23:36:30.408 INFO - Command request: testComplete[, ] on session c096289dc3174e68b7be194a7bd27447
23:36:30.409 INFO - Killing Firefox...
23:36:30.613 INFO - Got result: OK on session c096289dc3174e68b7be194a7bd27447
```

上面显示的就是运行成功每一步之后服务端控制台显示的信息，如果没有出现这类情况而是出现一下的信息：

```
23:24:44.930 INFO - Command request: getNewBrowserSession[*firefox3, http://www.kaoshidian.com/, ] on session null
23:24:44.931 INFO - creating new remote session
23:24:44.936 INFO - Got result: Failed to start new browser session: java.lang.RuntimeException: java.lang.RuntimeException: Firefox 3 could not be found in the path!
Please add the directory containing ''firefox.exe'' to your PATH environment
variable, or explicitly specify a path to Firefox 3 like this:
*firefox3 c:\blah\firefox.exe on session null
```

则是因为没有在环境变量中配置firefox的路径，不过这里不需要在环境变量里配置，只需要在`selenium("localhost", 4444, "*firefox x:/xxxxxx/Mozilla Firefox/firefox.exe", "http://www.kaoshidian.com/")` 声明即可，一般通过selenium生成的代码这里是 `selenium("localhost", 4444, "*chrome", "http://www.kaoshidian.com/")` 所以这里需要注意修改一下。

## Java ##

Selenium导出的是也是分为Webdriver和Remote Control 两种，同时也基于junit3和4，在这里我就只做一个Webdriver的例子。

我们先创建一个maven项目，然后在`pom.xml`文件中加入关于selenium的声明：

```xml
<dependency>
    <groupId>org.seleniumhq.selenium</groupId>
    <artifactId>selenium-java</artifactId>
    <version>2.37.1</version>
</dependency>
```

这里我不得不吐槽一下，这玩意居然依赖了这么多包，太坑爹。

下来就是用Selenium IDE 导出java的测试代码：

```java
package com.example.tests;

import java.util.regex.Pattern;
import java.util.concurrent.TimeUnit;
import org.junit.*;
import static org.junit.Assert.*;
import static org.hamcrest.CoreMatchers.*;
import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.Select;

public class SeleniumTest {
  private WebDriver driver;
  private String baseUrl;
  private boolean acceptNextAlert = true;
  private StringBuffer verificationErrors = new StringBuffer();

  @Before
  public void setUp() throws Exception {
    driver = new FirefoxDriver();
    baseUrl = "http://www.kaoshidian.com/";
    driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
  }

  @Test
  public void test() throws Exception {
    driver.get(baseUrl + "/");
    driver.findElement(By.cssSelector("div.wrap")).click();
    driver.findElement(By.linkText("课程中心")).click();
    driver.findElement(By.xpath("(//a[contains(text(),'专业课一对一')])[2]")).click();
    driver.findElement(By.xpath("(//a[contains(text(),'微直播')])[2]")).click();
    driver.findElement(By.linkText("精彩视频")).click();
  }

  @After
  public void tearDown() throws Exception {
    driver.quit();
    String verificationErrorString = verificationErrors.toString();
    if (!"".equals(verificationErrorString)) {
      fail(verificationErrorString);
    }
  }

  private boolean isElementPresent(By by) {
    try {
      driver.findElement(by);
      return true;
    } catch (NoSuchElementException e) {
      return false;
    }
  }

  private boolean isAlertPresent() {
    try {
      driver.switchTo().alert();
      return true;
    } catch (NoAlertPresentException e) {
      return false;
    }
  }

  private String closeAlertAndGetItsText() {
    try {
      Alert alert = driver.switchTo().alert();
      String alertText = alert.getText();
      if (acceptNextAlert) {
        alert.accept();
      } else {
        alert.dismiss();
      }
      return alertText;
    } finally {
      acceptNextAlert = true;
    }
  }
}

```

上面的代码运行的是偶可能会跑错，指示说没有指定firefox的路径，所以我们需要指定一下路径，方法很简单，就是修改创建driver实例的地方，`new FirefoxDriver(new FirefoxBinary(new File("x:\\xxxxxxxxxxx\\Mozilla Firefox\\firefox.exe")), new FirefoxProfile());` 这样在运行就可以了，运行之后就能看到我们之前在运行python一样的结果。

至于Remote Control我就不在这里在多说了，有兴趣的朋友可以自己去试一下，和python的Remote Control差不多的。

## 结论 ##

Selenium其实还有支持很多，比如Ruby,PHP,Perl,Hashel,Javascript,Objective-C等语言，也支持Chrome,Opera,IE等主流的浏览器，不过在兼容性上我没发给出确切的答案，因为没有做过测试，但是我们头做这个的分布式测试时候，倒是深有体会。同时也在支持在android和iOS上的测试，在功能上还是很全面的，操作也简单，是web测试中上佳的选择。
