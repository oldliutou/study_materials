import requests
from lxml import etree



def src_tiqu(yeshu):

    for i in range(1,int(yeshu)+1):
        print("----------------正在提取第"+str(i)+"页-------------")
        url = 'https://src.sjtu.edu.cn/list/?page='+str(i)
        data = requests.get(url).content
        # print(data.content.decode('utf-8'))
        soup = etree.HTML(data)
        result = soup.xpath('//td[@class=""]/a/text()')
        results = '\n'.join(result)
        resultss = results.split()

        # print(resultss)
        for edu in resultss:
            print(edu)
            with open(r'src_edu.txt','a+',encoding='utf-8') as f:
                f.write(edu+'\n')
                f.close()

if __name__ == '__main__':
    yeshu = input("请输入页数：")
    src_tiqu(yeshu)