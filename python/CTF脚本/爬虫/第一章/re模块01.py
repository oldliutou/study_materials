import re
# findall:匹配字符串中所有的符合正则的内容
list= re.findall(r"\d+","我的电话号是10020,它的电话是12222")
print(list)
# finditer: 匹配字符串所有的内容【返回的是迭代器】
it = re.finditer(r"\d+","我的电话号是10020,它的电话是12222")
for i in it:
    print(i.group())

s=re.search(r"\d+","我的电话号是10020,它的电话是12222")
print(s.group())

s=re.match(r"\d+","10020,它的电话是12222")
print(s)

# 预加载正则表达式
obj = re.compile(r'\d+')
s= obj.finditer("我的电话号是10020,它的电话是12222")
for i in s:
    print(i.group())