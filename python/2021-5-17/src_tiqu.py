import time


import requests
from lxml import etree




def src_tiqu(yeshu):
# //获取学校+漏洞类型
    for i in range(1,int(yeshu)+1):
        print("----------------正在提取第"+str(i)+"页-------------")
        url = 'https://src.sjtu.edu.cn/list/?page='+str(i)
        data = requests.get(url).content
        # print(data.content.decode('utf-8'))
        soup = etree.HTML(data)
        result = soup.xpath('//td[@class=""]/a/text()')

        results = '\n'.join(result)
        resultss = results.split()
        # print(results)
        # print(resultss)
        for edu in resultss:
            # print(edu)
            with open(r'src_edu.txt','a+',encoding='utf-8') as f:
                f.write(edu+'\n')
                f.close()

#获取学校名称
def schoolname (yeshu):
    for i in range(1,int(yeshu)+1):
        print("----------------正在提取第" + str(i) + "页-------------")
        url = 'https://src.sjtu.edu.cn/rank/firm/?page='+ str(i)
        data = requests.get(url).content
        # print(data.content.decode('utf-8'))
        soup = etree.HTML(data)
        result = soup.xpath('//td[@class="am-text-center"]/a/text()')
        for i in result:
            print(i)
            with open(r'name_edu.txt','a+',encoding='utf-8') as f:
                f.write(i+'\n')
                f.close()
        # results = '\n'.join(result)
        # resultss = results.split()
        # print(resultss)
        # for

# 获取学校域名
# url = https://cn.bing.com/search?q=大学名称
def school_webname():
    url = 'https://cn.bing.com/search?q='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51'
        # 'Cookie'
    }
    for schoolstr in open('name_edu.txt',encoding='utf-8'):
        r = requests.get(url+schoolstr,headers=headers)
        # r = requests.get(url+"山东大学",headers=headers)
        # print(r.content.decode('utf-8'))
        data = etree.HTML(r.text)
        result = data.xpath('//li[@class="b_algo"]/h2/a[@target="_blank"]/@href')

        for j in result:
            if('baike' in j ):
                # time.sleep(0.5)
                result.remove(j)
                # print(result)
        print("==================》》"+ schoolstr +result[0])
        with open(r'webname_edu.txt', 'a+', encoding='utf-8') as f:
            f.write(result[0] + '\n')
            f.close()

if __name__ == '__main__':
    # yeshu = input("请输入页数：")
    # src_tiqu(yeshu)
    # schoolname(yeshu)
    school_webname()