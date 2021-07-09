import time
from concurrent.futures import ThreadPoolExecutor
import requests
from lxml import etree
import csv
f = open("新发地菜价.csv",mode="w",encoding="gbk")
csvwriter = csv.writer(f)
def down_one_page(url):
    resp = requests.get(url)
    html = etree.HTML(resp.text)
    table = html.xpath("/html/body/div[2]/div[4]/div[1]/table")[0]
    trs = table.xpath("./tr[position()>1]")
    for tr in trs:
        txt = tr.xpath("./td/text()")
        # 对数据做简单的处理：\\ /去掉
        txt = (i.replace("\\","").replace("/","") for i in txt)
        csvwriter.writerow(txt)
        # print(list(txt))
    time.sleep(0.5)

    print(url+ "   over!!!")


if __name__ == '__main__':
    # for i in range(1,1000):
    #     down_one_page(f"http://www.xinfadi.com.cn/marketanalysis/0/list/{i}.shtml") #效率低下

    with ThreadPoolExecutor(50) as t:
        for i in range(1,1000):
            t.submit(down_one_page,f"http://www.xinfadi.com.cn/marketanalysis/0/list/{i}.shtml")

    print("全部下载完毕")