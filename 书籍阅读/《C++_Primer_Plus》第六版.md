# 第二章 开始学习C++
#进行中 

> 本章内容:
> ![](picture/《C++_Primer_Plus》第六版.assets/image-20230909174330536.png)
## 进入C++
```Cpp
#include <iostream>

int main() {
	using namespace std;
	cout << "Come up ***";
	cout << endl;
	cout << "You wont regret it!";
	//cin.get();
	return 0;
}

```

### main()函数

![](picture/《C++_Primer_Plus》第六版.assets/image-20230909175450246.png)

**在C++中，不能省略语句结尾的分号！**

![](picture/《C++_Primer_Plus》第六版.assets/image-20230909180013534.png)

![](picture/《C++_Primer_Plus》第六版.assets/image-20230909180506369.png)

### c++注释

C++的注释：
+ //
+ /*  */

### C++预处理器和iostream文件

![](picture/《C++_Primer_Plus》第六版.assets/image-20230909181211314.png)

### 头文件名

![](picture/《C++_Primer_Plus》第六版.assets/image-20230909181922436.png)


### 名称空间

![](picture/《C++_Primer_Plus》第六版.assets/image-20230909182611384.png)



### 使用cout进行C++输出

![](picture/《C++_Primer_Plus》第六版.assets/image-20230909205335648.png)



### C++源代码的格式化


## C++语句

~~~cpp
#include <iostream>

int main1(void) {
	using namespace std;
	int num;
	cout << "Hello World!" << endl << "please input number:";
	cin >> num;
	num = num + 2;
	cout << "number is " << num <<" ! " << endl;

	return 0;
}
~~~

### 声明语句和变量

![](picture/《C++_Primer_Plus》第六版.assets/image-20230909210140578.png)

