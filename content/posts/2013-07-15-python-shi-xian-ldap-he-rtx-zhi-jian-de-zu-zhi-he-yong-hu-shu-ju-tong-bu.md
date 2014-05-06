title: python实现ldap和rtx之间的组织和用户数据同步
category: python
tags: python, ldap, rtx, win32com
Date: 2013-07-15



最近公司正在准备使用 **AD** ( **[Activate Directory][]** )服务来进行公司员工的帐号管理，这样就避免不了需要对AD的帐号和[RTX][]的帐号和组织关系进行同步，所以才有了这篇文章。

#### Python-Ldap

[Python-Ldap][]是python用来操作ldap的模块，可以对ldap进行查询，添加，修改，删除等操作，如下代码：

```python
ldap_host = "127.0.0.1"
ldap_port = 389
ldap_who = "turbidsoul.me\\test"
ldap_cred = "test"
ldap_baseondn = "OU=XXXX,DC=turbidsoul,DC=me"
l = ldap.open(ldap_host, ldap_port)
    l.simple_bind_s(ldap_who, ldap_cred)
    result_id = l.search(ldap_baseondn, ldap.SCOPE_SUBTREE, "(object=organizationalUnit)", None)
    depart_map = {}
    while True:
        result_type, result_data = l.result(result_id, 0)
        if result_data == []:
            break

        if result_type == ldap.RES_SEARCH_ENTRY:
            name, attrs = result_data[0]
            depart_map[get_dept_path_by_dn(name)] = attrs
```


上面这段代码就是ldap的连接，查询代码，我简单的解释一下：

* ldap_host: AD服务器的地址
* ldap_port：AD服务器的端口，默认是389
* ldap_who：管理员的帐户，注意：这里必须是要域+用户名，也就是代码中的那种写法
* ldap_cred: 管理员密码
* ldap_baseondn: 这是查询的基，也就是说在查询的时候，查询的范围是啥，通常情况下，OU这里用该都是公司的名称或者顶级部门

`(object=organizationalUnit)`: 过滤参数，我这里指明的是值查询组织，如果是`(object=user)`则是查询用户

`ldap.open(ldap_host, ldap_port)`: 连接AD服务器

`l.simple_bind_s(ldap_who, ldap_cred)`: bind用户名和密码，

`l.search(ldap_baseondn, ldap.SCOPE_SUBTREE, "(object=organizationalUnit)"`:查询并获得一个结果ID;
第一个参数，就是我们要查询的基DN，这里也可以是具体的一个子部门，例如: `OU=开发组,OU=技术部,OU=XX公司,DC=turbidsoul,DC=me`;第二个参数，查询的范围，有三个值， *SCOPE_BASE* (基数：查询指定DN，也就是在DN中指定的那个，就只查这DN的)， *SCOPE_ONELEVEL* (一级：查询指定DN下的一级子目录，不会查子目录的子目录)， *SCOPE_SUBTREE* (子树：查询指定DN下的所有目录，包括指定DN)

下来就是利用循环取出数据，这里的`name`就是DN，`attrs`就是DN的属性集合。

下来看一下如何添加或者修改属性值：

```python
old = {"jobno": attrs['jobno']}
new = {"jobno": str(jobno)}
ml = modlist.modifyModlist(old, new)
l.modify_s(dn, ml)
```

* old: 指就原属性，如果原属性不存在，这里给个空字符串即可，`""`
* new: 需要修改的新值

我这里使用的jobno并不是ad的默认就有的属性是自己后来添加的扩展属性，至于如何添加扩展属性，請参照这篇文章[AD扩展属性定义][ad_extend_prop]

#### RTX

我通过python-ldap从AD中读取到数据，现在需要把他写道RTX中，在这里我遇到了一个问题，当时并没有仔细去看rtx sdk文档，只是想当然的以为直接用python操作数据，来进行数据同步，但是后来发现，数据虽然同步成功了，但是rtx客户端并不能从服务器抓取到新用户的信息，包括基本资料和详细资料等。

使用上面的方法，算是走到死胡同，同事的一句话让我想到我可以用过windows的com接口实现数据的同步，python下实现调用windows的com接口的模块是[win32com][](这个网站有，pywin32编译好的安装包，根据自己的python版本下载安装即可)。

我们来看一段测试代码：

```python
import win32com.client
import xml.etree.cElementTree as et

rootobj = win32com.client.Dispatch("RTXSAPIRootObj.RTXSAPIRootObj")

print(rootobj.QueryUserState('lp'))
print(rootobj.QueryUsersByState('online'))


um = rootobj.UserManager
print(um.GetUserBasicInfo("test")[0])
dm = rootobj.DeptManager
print(dm.GetUserDepts("test"))

dept_xml = et.fromstring(dm.GetUserDepts('test').encode('utf8'))
print(dept_xml.find('Department').attrib['Name'])

print(dm.IsDeptExist("XX公司\\技术部".decode('utf8').encode('gb2312')))
print(dm.IsDeptExist("开发组".decode('utf8').encode('gb2312')))
print(dm.IsDeptExist("XX公司\\技术部\\开发组".decode('utf8').encode('gb2312')))
print(dm.IsDeptExist("XX公司\\技术部\\美工组".decode('utf8').encode('gb2312')))
print(dm.GetChildDepts("XX公司\\技术部".decode('utf8').encode('gb2312')))
print(dm.GetUserDepts("test"))
```

代码很清晰，我们先加载了RTXSAPIRootObj.RTXAPIRootObj这个组件，这是rtx的api的跟对象（rtx文档中是这么说的，我觉得好别扭），具体有什么方法，請参照rtx文档。

UserManager和DeptManager分别是用户管理对象和部门管理对象，至于具体的还是請参照rtx文档，如何使用就如上面的代码一样，方法名的调用直接和rtx的api文章方法名一样，不过rtx的api有两种参数，in和out，我们传入的只是in参数，out的返回值，所以不需要管他，rtx有些返回值是xml，所以这里使用的cElementTree来处理。


#### Shiro和Ldap的整合

本来并没有打算写这一段，但是写道这里了，我想也会有人在这里遇到问题，所以我就简单的说一下。

首先我们先来看一下在Spring中shiro的配置：

```xml
<bean id="shiroLdapRealm" class="me.turbidsoul.permission.ShiroLdapRealm">
    <property name="contextFactory.url" value="ldap://127.0.0.1:389"/>
    <property name="contextFactory.systemUsername" value="CN=administrator,DC=isoushi,DC=cn"/>
    <property name="contextFactory.systemPassword" value="123456"/>
</bean>
```

配置很简单，但是需要给三个参数，分别是，ldap服务器的连接地址，ldap服务器的用户名和密码，这里用户名是用了DN的方式，其实在上面python也可以用这样的方式，接下来看一下java中如何实现的：

```java
public class ShiroLdapRealm extends JndiLdapRealm {
    @Autowired
    private UserDAO userDao;

    @Override
    protected AuthenticationInfo queryForAuthenticationInfo(AuthenticationToken token, LdapContextFactory ldapContextFactory) throws NamingException {
        UsernamePasswordToken uptoken = (UsernamePasswordToken) token;
        Object username = token.getPrincipal();

        if(username == null) {
            throw new AccountException("Null usernames are not allowed by this realm.");
        }

        Object password = token.getCredentials();

        if(password == null) {
            throw new AccountException("Null password are not allowed by this realm.");
        }

        User curuser = userDao.findUniq("loginName", username);

        if(curuser == null) {
            throw new AccountException("Can't not find user[" + username.toString() + "] in system." );
        }

        if(StringUtils.isBlank(curuser.getDn())) {
            throw new AccountException("This user[" + username.toString() + "] has not ldap server." );
        }

        LdapContext ctx = null;
        try {
            ctx = ldapContextFactory.getLdapContext(curuser.getDn(), password);
        } catch(Exception e) {
            throw new AccountException("Ldap auth failure!");
        } finally {
            LdapUtils.closeContext(ctx);
        }

        return createAuthenticationInfo(token, username, password, ctx);
    }


    @Override
    protected AuthenticationInfo doGetAuthenticationInfo(AuthenticationToken token) throws AuthenticationException {
        try {
            return this.queryForAuthenticationInfo(token, getContextFactory());
        } catch (NamingException e) {
            throw new AccountException(e);
        }
    }
}
```

代码很简单，就是当用户登录的时候，Shiro拦截到，并把用户的token传到`queryForAuthenticationInfo`或者`doGetAuthenticationInfo`两个方法中，在方法中得到用户的登录名和密码，使用登录名查到用户的DN，然后在代码用DN和密码创建`LdapContext`，最后在返回返回`AuthenticationInfo`即可

这里需要注意两点：

* 一定会用到DN，所以要么自己可以在本地拼出DN，要么就直接像我这样直接把DN冗余到本地库中。
* 当我们在代码中使用`SecurityUtils.getSubject().getPrincipal()`获取用户对象的时候，返回的只是一个用户名，不想JDBC的方式获取的是用户的对象。

#### 结论

在这次的开发工作中，其实费了不少时间，有快一个礼拜，其中有两天多的时候都卡在的编码的问题上，说起来挺可笑也挺无奈，ad对编码的问题支持的还算不错，rtx就不行了，他使用的mdb数据库，windows下是gb2312而在python中我使用了utf8，所以在和rtx交互的时候需要把字符串的编码，进行转码，如：`"中文编码".decode('utf8').encode('gb2312')`

其次耗费时间的是，我花了一些时间，研究为什么直接操作数据库并不能是rtx客户端读取到用户资料，为此我还用 **Wireshark** 进行了抓包，发现并不似rtx本身配置的问题，因为通过抓包分析得到rtx本身并没有问题，我想应该就是我在操作数据库上存在问题，但是又想不到是那里的问题。在后来使用com接口操作时候，对比了两种方式操作数据库之后数据库的变化，让我发现，问题出在sys_sysconfig这张表上，这张表里有两个字段 *UserVersion* 和 *DeptVersion* 两个这两个字段记录的是上一次更新数据之后sys_user和rtx_dept两个表数据的最后版本变化，在这两个表里也同样存在这两个对应的字段 *UserVersion* 和 *Version* 记录了没个记录的版本号，rtx客户端会更新版本号大于等于sys_sysconfig中记录的版本号，我尝试修改版本号来测试，得到的结果和我猜测的是一样的。但是我并不知道使用com接口操作是不是还有修改其他的数据，因为这里完全是黑盒，而且在rtx的官网也看到推荐使用api操作，直接操作数据库可能会造成数据库的不一致。

但在数据同步并不是这上面说的使用UserManager和DeptManager这两个对象来操作，也可以使用ElementTree配成xml，使用rtx提供的方法导入也可以，这样的方法效率要比上面的方法更快，不过我并没有看到一个完成的XML例子，所以并没有采用这种方法。


[Activate Directory]: https://zh.wikipedia.org/wiki/Active_Directory "Active Directory"
[RTX]: http://rtx.tencent.com/rtx/index.shtml "RTX"
[Python-Ldap]:http://www.python-ldap.org/ "LDAP client API for Python"
[ad_extend_prop]: http://docs.tidyinfo.com/?p=309 "AD扩展属性定义"
[win32com]: http://www.lfd.uci.edu/~gohlke/pythonlibs/ "Unofficial Windows Binaries for Python Extension Packages"
