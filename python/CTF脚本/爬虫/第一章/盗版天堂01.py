import  requests,re
url = "https://dytt89.com"
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66'
}
resp = requests.get(url,verify=False,headers=header)
resp.encoding = 'gb2312'
# print(resp.text)
# 拿到ul里的li
obj1 = re.compile(r'2021必看热片.*?<ul>(?P<ul>.*?)</ul>',re.S)
obj2 = re.compile(r"<a href='(?P<href>.*?)'",re.S)
result1 = obj1.finditer(resp.text)
for it in result1:
    ul = it.group("ul")
    # print(ul)
    result2 = obj2.finditer(ul)

    for itt in result2:
        print(itt.group("href"))