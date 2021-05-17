import threading
from queue import Queue
from time import sleep

import requests

# pre_str='abcmlyx'
# hou_str='0123456789'
# for i in pre_str:
#     for j in pre_str:
#         pre = i+j+'ctf'
#         for a in hou_str:
#             for b in hou_str:
#                 for c in hou_str:
#                     print(pre+a+b+c)
#                     with open(r'ctf_str.txt', 'a+', encoding='utf-8') as f:
#                         f.write(pre+a+b+c + '\n')
#                         f.close()
def bp():
    url='http://353e7b03144049c18a362f7dd41d8832df76c8b4bcec4b49.changame.ichunqiu.com/js/'
    try:
        for i in open('ctf_str.txt'):
            i = i.replace('\n','')
            html = requests.get(url+i+'.js').status_code
            if(html==200):
                print(i)
            # sleep(0.5)
            print(url+i+'.js'+"         "+str(html))
    except :
        pass
if __name__ == '__main__':

    # q = Queue()
    #
    # for each in range(300):
    #     t = threading.Thread(target=bp)
    #     t.daemon = True
    #     t.start()

    # q.join()
    bp()