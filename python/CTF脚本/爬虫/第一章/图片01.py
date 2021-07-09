import requests
from bs4 import BeautifulSoup
import time
url = "https://www.umei.net/bizhitupian/weimeibizhi/"
resp = requests.get(url)
resp.encoding='utf-8'
# print(resp.text)
main_page = BeautifulSoup(resp.text,"html.parser")
alist = main_page.find("div",class_="TypeList").find_all("a")
# print(alist)
for a in alist:
    href = a.get('href')
    # print(href)
    child_page_resp  = requests.get("https://www.umei.net"+href)
    # print(url+href)
    child_page_resp.encoding="utf-8"
    child_page_resp_text = child_page_resp.text

    child_page = BeautifulSoup(child_page_resp_text,"html.parser")
    p = child_page.find("p",align="center")
    img = p.find("img")
    src = img.get("src")
    # 下载图片
    img_resp = requests.get(src)

    img_name = src.split("/")[-1]
    with open("img/"+img_name,mode="wb") as f:
        f.write(img_resp.content)

        pass
    print("over!!!"+img_name)
    time.sleep(0.5)
print("all_over!")
