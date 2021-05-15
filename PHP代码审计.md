# PHP代码审计

## 刷题遇到的函数

 ```php
isset():检测变量是否已设置并且非 null
strpos():查找字符串首次出现的位置
error_reporting(v):设置应该报告何种 PHP 错误,当v=0时，关闭所有PHP错误报告
header():发送原生 HTTP 头
curl_init():初始化 CURL 会话
curl_setopt():设置 cURL 传输选项
curl_exec():执行 cURL 会话
ord():函数返回字符串的首个字符的 ASCII 值
die():等同于exit(), 输出一个消息并且退出当前脚本
==:比较两个参数的值
====:会比较两个变量的类型
exec():执行一个外部程序
preg_match ( string $pattern , string $subject [, array &$matches [, int $flags = 0 [, int $offset = 0 ]]] ):搜索 subject 与 pattern 给定的正则表达式的一个匹配。
var_dump():打印变量的相关信息
$GLOBALS:引用全局作用域中可用的全部变量
file(): 把整个文件读入一个数组中
file_get_contents():将整个文件读入一个字符串
unserialize():对单一的已序列化的变量进行操作，将其转换回 PHP 的值
gzuncompress():解压被压缩的字符串
base64_decode():base64解码
show_source(): 别名 highlight_file():语法高亮一个文件
array_merge(): 合并一个或多个数组
in_array(search,array,type):搜索数组中是否存在指定的值
mb_substr():获取部分字符串
mb_strpos():查找字符串在另一个字符串中首次出现的位置
require(): require 和 include 几乎完全一样，除了处理失败的方式不同之外。require 在出错时产生 E_COMPILE_ERROR 级别的错误。换句话说将导致脚本中止而 include 只产生警告（E_WARNING），脚本会继续运行
range():根据范围创建数组，包含指定的元素
mt_rand():生成更好的随机数
substr(string $string , int $start , int $length = ?):返回字符串的子串，开始位置从0计算
preg_replace():执行一个正则表达式的搜索和替换
str_replace():子字符串替换
chr ( int $ascii ) : string 返回指定的字符
random():
addslashes():会在单引号‘,双引号“,反斜杠\以及NULL前添加反斜杠进行转义\，该函数常用于为存储在数据库中的字符串以及数据库查询语句准备字符串。				
strstr():搜索字符串在另一字符串中的第一次出现。
var_dump():打印变量的相关信息
scandir():列出指定路径中的文件和目录
global:声明了全局变量
getenv():获取一个环境变量的值
intval(): 获取变量的整数值
is_numeric(): 检测变量是否为数字或数字字符串
md5(string $string,bool $binary=false):string ：计算字符串的MD5散列值，如果可选的 binary 被设置为 true，那么 md5 摘要将以 16 字符长度的原始二进制格式返回。 
get_defined_funcations():
ctype_alpha():

 ```

**执行运算符：**

>    PHP 支持一个执行运算符：反引号（`）。注意这不是单引号！PHP    将尝试将反引号中的内容作为 shell 命令来执行，并将其输出信息返回（即，可以赋给一个变量而不是简单地丢弃到标准输出）。使用反引号运算符“``”的效果与函数    [shell_exec()](https://www.php.net/manual/zh/function.shell-exec.php) 相同。    

```
 <?php
 $output = `ls -al`;
 echo "<pre>$output</pre>";
 ?> 
```

## 正则表达式

> 正则表达式(regular expression)描述了一种字符串匹配的模式（pattern），可以用来检查一个串是否含有某种子串、将匹配的子串替换或者从某个串中取出符合某个条件的子串等。
### 普通字符

普通字符包括没有显式指定为元字符的所有可打印和不可打印字符。这包括所有大写和小写字母、所有数字、所有标点符号和一些其他符号。

| 字符   | 描述                                                         |
| ------ | ------------------------------------------------------------ |
| [ABC]  | 匹配 [...] 中的所有字符，例如 [aeiou] 匹配字符串 "google runoob taobao" 中所有的 e o u a 字母。 |
| [^ABC] | 匹配`除了` [...] 中字符的所有字符，例如 \[^aeiou] 匹配字符串 "google runoob taobao" 中除了 e o u a 字母的所有字母。 |
| [A-Z]  | [A-Z] 表示一个区间，匹配所有大写字母，[a-z] 表示所有小写字母。 |
| [\s\S] | 匹配所有。`\s 是匹配所有空白符`，包括换行，`\S 非空白符`，不包括换行。 |
| \w     | 匹配字母、数字、下划线。等价于 [A-Za-z0-9_]                  |

### 特殊字符

所谓特殊字符，就是一些有特殊含义的字符，如上面说的 `runoo*b` 中的 `*`，简单的说就是表示任何字符串的意思。如果要查找字符串中的 `*` 符号，则需要对 `*` 进行转义，即在其前加一个 \，runo\\*ob 匹配字符串 **runo\*ob**。

许多元字符要求在试图匹配它们时特别对待。若要匹配这些特殊字符，必须首先使字符"转义"，即，将反斜杠字符\ 放在它们前面。下表列出了正则表达式中的特殊字符：

| 特别字符 | 描述                                                         |
| -------- | ------------------------------------------------------------ |
| $        | 匹配输入`字符串的结尾位置`。如果设置了 RegExp 对象的 Multiline 属性，则 $ 也匹配 '\n' 或 '\r'。要匹配 $ 字符本身，请使用 \$。 |
| ( )      | 标记一个子表达式的开始和结束位置。子表达式可以获取供以后使用。要匹配这些字符，请使用 \( 和 \)。 |
| *        | 匹配前面的子表达式`零次或多次`。要匹配 * 字符，请使用 \*。   |
| +        | 匹配前面的子表达式`一次或多次`。要匹配 + 字符，请使用 \+。   |
| .        | 匹配除`换行符 \n 之外的任何`单字符。要匹配 . ，请使用 \. 。  |
| ?        | 匹配前面的子表达式`零次或一次`，或指明一个非贪婪限定符。要匹配 ? 字符，请使用 \?。 |
| ^        | `匹配输入字符串的开始位置`，除非在方括号表达式中使用，当该符号在方括号表达式中使用时，表示不接受该方括号表达式中的字符集合。要匹配 ^ 字符本身，请使用 \^。 |
| \|       | 指明`两项之间的一个选择`。要匹配 \|，请使用 \|。             |
| {        | 标记`限定符表达式的开始`。要匹配 {，请使用 \{。              |

### 限定符

限定符用来指定正则表达式的一个给定组件必须要出现多少次才能满足匹配。有 * 或 + 或 ? 或 {n} 或 {n,} 或 {n,m} 共6种。

正则表达式的限定符有：

| 字符  | 描述                                                         |
| ----- | ------------------------------------------------------------ |
| *     | 匹配前面的子表达式零次或多次。例如，zo* 能匹配 "z" 以及 "zoo"。* 等价于{0,}。 |
| +     | 匹配前面的子表达式一次或多次。例如，'zo+' 能匹配 "zo" 以及 "zoo"，但不能匹配 "z"。+ 等价于 {1,}。 |
| ?     | 匹配前面的子表达式零次或一次。例如，"do(es)?" 可以匹配 "do" 、 "does" 中的 "does" 、 "doxy" 中的 "do" 。? 等价于 {0,1}。 |
| {n}   | n 是一个非负整数。匹配确定的 n 次。例如，'o{2}' 不能匹配 "Bob" 中的 'o'，但是能匹配 "food" 中的两个 o。 |
| {n,}  | n 是一个非负整数。至少匹配n 次。例如，'o{2,}' 不能匹配 "Bob" 中的 'o'，但能匹配 "foooood" 中的所有 o。'o{1,}' 等价于 'o+'。'o{0,}' 则等价于 'o*'。 |
| {n,m} | m 和 n 均为非负整数，其中n <= m。最少匹配 n 次且最多匹配 m 次。例如，"o{1,3}" 将匹配 "fooooood" 中的前三个 o。'o{0,1}' 等价于 'o?'。请注意在逗号和两个数之间不能有空格。 |

更多语法：[正则表达式中各种字符的含义 - 一个农夫 - 博客园 (cnblogs.com)](https://www.cnblogs.com/afarmer/archive/2011/08/29/2158860.html)



## CTF中PHP常用知识点（重点）

### PHP超全局变量

PHP中的许多预定义变量都是“超全局的”，这意味着它们在一个脚本的全部作用域中都是可用的。在函数或方法中无需执行global $variable;就可以访问它们。

这些超全局变量是：

+ $GLOBALS
+ $_SERVER
+ $REQUEST
+ $_POST
+ $_GET
+ $_FILES
+ $_ENV
+ $_COOKIE
+ $_SESSION

### PHP的弱类型比较问题

+ 前言

  在ctf比赛中，不止一次出现了PHP弱类型的题目，借此想总结一下PHP弱类型以及绕过方式

+ 知识介绍

  PHP中有两种比较的符号 `==` 与`===`

  ~~~php
  <?php
  	$a==$b;
  	$a===$b;
  ?>
  ~~~

  `===`在进行比较的时候，会先判断两种字符串的类型是否相等，在比较值

  `==`在进行比较的时候，会先将字符串类型转化成相同，再比较

  > 如果比较一个数字和字符串或者比较涉及到数字内容的字符串，则字符串会被转换成数值并且比较按照数值来进行

**这里明确了说如果一个数值和字符串进行比较的时候，会将字符串转换成数值**

```php
 <?php
 var_dump("admin"==0);  //true
 var_dump("1admin"==1); //true
 var_dump("admin1"==1) //false
 var_dump("admin1"==0) //true
 var_dump("0e123456"=="0e4456789"); //true 
 ?>  //上述代码可自行测试
```

> 1 观察上述代码，"admin"==0 比较的时候，会将admin转化成数值，强制转化,由于admin是字符串，转化的结果是0自然和0相等
> 2 "1admin"==1 比较的时候会将1admin转化成数值,结果为1，而“admin1“==1 却等于错误，也就是"admin1"被转化成了0,为什么呢？？
> 3 "0e123456"=="0e456789"相互比较的时候，会将0e这类字符串识别为科学技术法的数字，0的无论多少次方都是零，所以相等

对于上述的问题我查了php手册

> 
> 当一个字符串被当作一个数值来取值，其结果和类型如下:如果该字符串没有包含' . ' , ' e ', ' E' 并且其数值值在整形的范围之内，该字符串被当作int来取值，其他所有情况下都被作为float来取值，**该字符串的开始部分决定了它的值，如果该字符串以合法的数值开始，则使用该数值，否则其值为0。**
> 

```php
 <?php
 $test=1 + "10.5"; // $test=11.5(float)
 $test=1+"-1.3e3"; //$test=-1299(float)
 $test=1+"bob-1.3e3";//$test=1(int)
 $test=1+"2admin";//$test=3(int)
 $test=1+"admin2";//$test=1(int)
 ?>
```

所以就解释了“admin1”==1 ---->False的原因

[php 弱类型总结 +实战](https://www.cnblogs.com/Mrsm1th/p/6745532.html)

### PHP断言（assert）

[PHP断言（ASSERT)的用法 - 菜问 - 博客园 (cnblogs.com)](https://www.cnblogs.com/nixi8/p/7147122.html)

### PHP读取目录下文件的方法

**scandir():读取文件和目录，以数组形式存储**

**print_r():输出**

~~~php
<?php
$dir = "/images/";

// Sort in ascending order - this is default
$a = scandir($dir);

// Sort in descending order
$b = scandir($dir,1);

print_r($a);
print_r($b);
?>
~~~

结果：

~~~php
Array
(
[0] => .
[1] => ..
[2] => cat.gif
[3] => dog.gif
[4] => horse.gif
[5] => myimages
)
Array
(
[0] => myimages
[1] => horse.gif
[2] => dog.gif
[3] => cat.gif
[4] => ..
[5] => .
)
~~~

### preg_match绕过

`preg_match`用于执行正则匹配。返回pattern的匹配次数。它的值是0次（不匹配）或1次，因为preg_match（）在一次匹配后将会停止搜索。preg_match_all()不同与此，它会一直搜索subject直到到达结尾。如果发生错误preg_match（）返回FALSE。

+ 语法

~~~php
int preg_match ( string $pattern , string $subject [, array &$matches [, int $flags = 0 [, int $offset = 0 ]]] )
~~~

**搜索 subject 与 pattern 给定的正则表达式的一个匹配。**

参数说明：

​		$pattern: 要搜索的模式，字符串形式。

​		$subject: 输入字符串。

​		$matches: 如果提供了参数matches，它将被填充为搜索结果。 $matches[0]将包含完整模式匹配到的文本， 				$matches[1] 将包含第一个捕获子组匹配到的文本，以此类推。

​		$flags：flags 可以被设置为以下标记值：

​				PREG_OFFSET_CAPTURE: 如果传递了这个标记，对于每一个出现的匹配返回时会附加字符串偏移量(相对于目标字符串的)。 注意：这会改变填充到matches参数的数组，使其每个元素成为一个由 第0个元素是匹配到的字符串，第1个元素是该匹配字符串 在目标字符串subject中的偏移量。

​			offset: 通常，搜索从目标字符串的开始位置开始。可选参数 offset 用于 指定从目标字符串的某个未知开始搜索(单位是字节)。

+ 返回值

  返回 pattern 的匹配次数。 它的值将是 0 次（不匹配）或 1 次，因为 preg_match() 在第一次匹配后 将会停止搜索。preg_match_all() 不同于此，它会一直搜索subject 直到到达结尾。 如果发生错误preg_match()返回 FALSE。

+ 实例

  [PHP preg_match() 函数 | PHP 教程 - 码农教程 (codercto.com)](https://www.codercto.com/courses/d/852.html)

### PHP中sha1()函数和MD5()函数的绕过

```php
sha1($_GET['name']) === sha1($_GET['password'])
```

这两个函数比较时，由于无法处理数组，两边都会返回false，则相等，所以playload为?name[]=1&password[]=2。







RCE过滤绕过

反序列化







## 代码审计的思路和流程





