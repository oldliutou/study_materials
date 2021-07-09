from lxml import etree
import  requests
url = "https://beijing.zbj.com/search/f/?type=new&kw=saas"
resp = requests.get(url)
# print(resp.text)
# 解析
html = etree.HTML(resp.text)
divs = html.xpath("/html/body/div[6]/div/div/div[2]/div[5]/div[1]/div")
for div in divs: #每一个服务商的信息
    price = div.xpath("./div/div/a[1]/div[2]/div[1]/span[1]/text()")[0].strip("¥")
    title = "saas".join(div.xpath("./div/div/a[1]/div[2]/div[2]/p/text()"))
    com_name = div.xpath("./div/div/a[2]/div[1]/p/text()")
    add = div.xpath("./div/div/a[2]/div[1]/div/span/text()")
    print(title)