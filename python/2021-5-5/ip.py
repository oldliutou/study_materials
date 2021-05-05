import socket,os,time,sys,nmap
from whois import whois
#ip查询
def ip_check(url):
    ip = socket.gethostbyname(url)
    print(ip)

# whois查询
def whois_check(url):
    data = whois(url)
    print(data)

# 域名反查ip

def dns2ip(url,port):
    ip = socket.getaddrinfo(url,port)
    print(ip)
# 识别目标是否存在CDN
# 采用nslookup执行结果进行返回IP解析数目判断
def nslookup_T(url):
    # cdn_data = os.system("nslookup "+url)
    cdn_data = os.popen("nslookup "+url)
    cdn_datas = cdn_data.read()
    x = cdn_datas.count('.')
    if(x>7):
        print("cdn存在")
    else:
        print("cdn不存在")
    print(x)
# 端口扫描
# 1.原生态，自写socket协议tcp、udp扫描
# 2.调用第三方模块
# 3.调用系统工具脚本执行
def scan_port():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    result = server.connect_ex(("www.xiaodi8.com",8080))
    if result==0:
        print("port Open!")
    else:
        print("port Close!")
# 内网扫描
def nmap_Demo():
    nm = nmap.PortScanner()
    data = nm.scan("www.xiaodi8.com",'80,8888','-sV')
    print(data)



if __name__ == '__main__':
    # dns2ip("www.baidu.com",80)
    # nslookup_T("www.xiaodi8.com")
    # scan_port()
    # whois_check('www.baidu.com')
    # print(whois('www.xiaodi8.com'))

    # check = sys.argv[1]
    # url=sys.argv[2]
    # if check=='all':
    #     whois_check(url)
    #     print(whois(url))
    nmap_Demo()
