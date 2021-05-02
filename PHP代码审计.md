# PHP代码审计

## 常用函数

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
 ```









## 代码审计的思路和流程

