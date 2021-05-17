import base64, requests
import hashlib

# 第一届“百度杯”信息安全攻防总决赛 线上选拔赛——Upload
def main():
    a = requests.session()
    b = a.get("http://6ebbbd692cc047ce8ccd326a88f72eb32090a688e6cc4bfa.changame.ichunqiu.com/")
    key1 = b.headers["flag"]
    c = base64.b64decode(key1)
    d = str(c).split(":")
    key = base64.b64decode(d[1])
    body = {"ichunqiu": key}
    f = a.post("http://6ebbbd692cc047ce8ccd326a88f72eb32090a688e6cc4bfa.changame.ichunqiu.com/", data=body)
    print(f.text)
# def captcha():
#     dic = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#
#     for i in range(999999999):
#         h = hashlib.md5(str(i).encode()).hexdigest()[:6]
#         # print(h)
#         # print(i)
#         if h == '3bfd5c':
#             print(i)
#             break
#
# def Captcha():
#
#     for i in range(9999999999):
#     # f = hashlib.md5(str(i).encode()).hexdigest()[:6]
#         h = hashlib.md5(str(i).encode()).hexdigest()[:6]
#         if h == 'c38725':
#          print(i)


#key is not right,md5(key)==="1b4167610ba3f2ac426a68488dbd89be",and the key is ichunqiu***,the * is in [a-z0-9]
# “百度杯”CTF比赛 十月场——fuzzing
def fuzz():
    dict='abcdefghijklmnopqrstuvwxyz0123456789'
    key1='ichunqiu'
    for i in dict:
        for j in dict:
            for k in dict:
                result = hashlib.md5((key1+i+j+k).encode()).hexdigest()
                if(result == "1b4167610ba3f2ac426a68488dbd89be"):
                    print(key1+i+j+k)
# “百度杯”CTF比赛 十月场——hash
def hash():
    hash = 'f9109d5f83921a551cf859f853afe7bb'
    key='123'
    for sign in range(10000000,99999999):
        h = hashlib.md5((str(sign)+key).encode()).hexdigest()
        if(h == hash):
            print(sign)
#
def filehash():
    hash = hashlib.md5()

    filename='/fllllllllllllag'
    cookie_secret="36277246-f3aa-4cea-a784-115ecefa55a2"
    hash.update(filename.encode('utf-8'))
    s1=hash.hexdigest()
    print(hashlib.md5(filename.encode('utf-8')).hexdigest())
    hash = hashlib.md5()
    print(cookie_secret+s1)
    hash.update((cookie_secret+s1).encode('utf-8'))
    print(hash.hexdigest())
# 得到hash值
def gethash():
    str = ''
    hash = hashlib.md5(str.encode()).hexdigest()
    print(hash)

def getFlag():
    key = 'ee70ff'
    # dict='abcdefghijklmnopqrstuvwxyz0123456789'
    for i in range(100000000000):
        a = hashlib.md5(str(i).encode()).hexdigest()[:6]
        if(a==key):
            print(i)
    pass



if __name__ == '__main__':
    # main()
    # captcha()
    # Captcha()
    # fuzz()
    # filehash()
    # getFlag()
    # main()
    hash()