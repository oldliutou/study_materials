import hashlib,re
from threading import Thread

# for i in range(99999999999):
#     s = str(i)
#     md5 = hashlib.md5(("0e"+s).encode('utf-8')).hexdigest()
#
#     if(re.match('/^0e\d+$/',md5)):
#
#         print('0e'+str(i))
#         break

def run():
    i = 0
    while True:
        text = '0e{}'.format(i)
        m = hashlib.md5(text.encode('utf-8')).hexdigest()
        print(text,m)
        if m[0:2] == '0e' :
            if m[2:].isdigit():
                print('find it:',text,":",m)
                break
        i +=1
if __name__ == '__main__':
    for i in range(100):
        t = Thread(target=run)
        t.start()

# print(hashlib.md5(("0e141").encode('utf-8')).hexdigest())
# print(hashlib.md5(("0e215962017").encode('utf-8')).hexdigest())
# str = "this_is_the_flag.txt"[::-1]
# print(str)
