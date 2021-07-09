import requests
import re
import csv
url = 'https://movie.douban.com/top250'
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
}
res = requests.get(url,headers=header)
page_content=res.text
# print(page_content)
# 解析数据
obj = re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)'
                 r'</span>.*?<p class="">.*?<br>(?P<year>.*?)&nbsp.*?'
                 r'<span class="rating_num" property="v:average">(?P<score>.*?)</span>.*?'
                 r'<span>(?P<num>.*?)人评价</span>', re.S)
result = obj.finditer(page_content)
f= open("data.csv",mode='w')
csvwrite = csv.writer(f)
for i in result:
    # print(i.group("name"))
    # print(''.join(i.group("year").split()))
    # print(i.group("score"))
    # print(i.group("num"))
    dic = i.groupdict()
    # dic['name'] = dic['year'].encode('utf-8')
    dic['year'] = ''.join(dic['year'].split())
    csvwrite.writerow(dic.values())
print('over!!!')