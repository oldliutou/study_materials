import csv

from bs4 import BeautifulSoup
import requests

url = 'http://www.xinfadi.com.cn/marketanalysis/0/list/1.shtml'
resp = requests.get(url)
# print(resp.text)

# 解析数据
# 1. 把页面源代码交给BeautifulSoup进行处理，生成bs对象
page= BeautifulSoup(resp.text,"html.parser") #指定HTML解析器
# 2. 从bs对象中查找数据
#  find（标签，属性=值）
#  findall（标签，属性=值）
# table = page.find("table",class_="hq_table")
table = page.find("table",attrs={'class':"hq_table"})
# print(table)
trs = table.find_all("tr")[1:]
f= open("菜价.csv",mode='w')
csvwrite = csv.writer(f)
for tr in trs:
    tds = tr.find_all("td")
    name = tds[0].text
    name1 = tds[1].text
    name2 = tds[2].text
    name3 = tds[3].text
    name4 = tds[4].text
    name5 = tds[5].text
    name6 = tds[6].text
    csvwrite.writerow([name,name1,name2,name3,name4,name5,name6])
    # print(name,name1,name2,name3,name4,name5,name6)