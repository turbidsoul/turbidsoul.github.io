title: 如何配置在nginx和cas上配置ssl？
category: Nginx
tags: nginx, cas, ssl, java, https
Date: 2013-05-08

公司准备对登录服务采用https，而登录服务采用的是cas，前段的是用nginx代理， 所以就有了之后的几个问题。

**主要碰到了下面3个问题** ：

1. nginx中配置ssl
2. cas中开启ssl
3. java中导入证书

---------------------------------------------

首先是生成我们的证书，我使用的是openssl：

1. 首先是生成私钥： openssl genrsa -out server.key
2. 接下来要生成CSR文件： openssl req -new -key server.key -out server.csr
3. 最后就是生成证书文件： openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

这里有我一个笔记是openssl的简单教程：[openssl简单教程](https://www.evernote.com/shard/s25/sh/233c0eda-2f70-4756-8907-50dc0bff82c2/92861a2bd473f1d703bcead620080d27)

------------------------------------------

生成证书后，就可以配置nginx了，打开nginx.conf，加入以下几行:

```nginx
listen                 443 ssl;
ssl                    on;
ssl_certificate        login.cert;
ssl_certificate_key    login.key;
```

加入这几行配置后，重载nginx， nginx上ssl就可以生效了，这时用普通的http访问会无法访问， 必须使用https访问，第一次访问firefox会提示证书不信任。

----------------------------------------------

接下来是在cas中开启ssl的支持，虽然这一步很简单，但是具体我也不甚了解，因为cas是其他同事负责的， 我只是按照他说的去做，所以我说的文件路径或者文件名和cas的原生项目会有不通。接下来我简单说以下如何配置：

先找到`WEB-INFO/spring-configuration`下的配置文件, `ticketGrantingTicketCookieGenerator.xml` 和 `warnCookieGenerator.xml`

打开文件 `ticketGrantingTicketCookieGenerator.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xmlns:p="http://www.springframework.org/schema/p"
   xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.0.xsd">
    <description>
        Defines the cookie that stores the TicketGrantingTicket.  You most likely should never modify these (especially the "secure" property).
        You can change the name if you want to make it harder for people to guess.
    </description>
    <bean id="ticketGrantingTicketCookieGenerator" class="org.jasig.cas.web.support.CookieRetrievingCookieGenerator"
        p:cookieSecure="false"
        p:cookieMaxAge="-1"
        p:cookieName="CASTGC"
        p:cookiePath="/cas" />
</beans>
```

修改`p:cookieSecure="false"`的值为`true`

打开`warnCookieGenerator.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xmlns:p="http://www.springframework.org/schema/p"
   xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.0.xsd">
   <description>
   This Spring Configuration file describes the cookie used to store the WARN parameter so that a user is warned whenever the CAS service
   is used.  You would modify this if you wanted to change the cookie path or the name.
   </description>

   <bean id="warnCookieGenerator" class="org.jasig.cas.web.support.CookieRetrievingCookieGenerator"
      p:cookieSecure="false"
      p:cookieMaxAge="-1"
      p:cookieName="CASPRIVACY"
      p:cookiePath="/cas" />
</beans>
```

修改`p:cookieSecure="false"` 的值为`true`。

修改这两个之后就可以把cas的包放入tomcat中启动tomcat。

经过上面两部其实按正常情况下已经可以访问了，但是在登录的时候， 进入cas的登录页面进行登录，登录成功后返回的时候会抛出异常，对于这个异常我不甚理解， 但是我在google上所有得到的结果是这时java的一个bug，不过已经给出了解决方法.

下载下面的代码： [InstallCert.java](https://gist.github.com/turbidsoul/5506661)

<script src="https://gist.github.com/turbidsoul/5506661.js"></script>

编译之后使用使用下面命令执行以下：`java InstallCert cas.xxxxx.com`

https://login.xxxx.com 是你配置了ssl的服务的那个域名

执行完后会在当前目录下生成jssecacerts的文件，把文件copy到`jdk1.7.0_10\jre\lib\security`目录下 重新启动服务即可。或者在java的启动参数中加入`-Djavax.net.ssl.trustStore=F:/work/Java/jssecacerts`, 重新启动也是可行的，我使用的后面这个方法，前面的那个我没有测试，不过应该不会有问题。

到这里就算是把ssl配置完成了，其实并没有什么复杂的东西，就是最后java这个问题让我找了很常时间。 最后在java的社区中找到解决办法，可以这个类的源码文件的下载链接还失效了，在google中找了半天才找到个完整的。
