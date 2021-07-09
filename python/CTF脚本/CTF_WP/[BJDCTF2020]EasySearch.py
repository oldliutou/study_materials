import hashlib

for i in range(10000000000):
    # print(i)
    md5 = hashlib.md5(str(i).encode("utf-8")).hexdigest()
    print(md5)
    # if(md5[:6] == '6d0bc1'):
    #     print(md5[:6])
    #     print(i)
    #     pass
# md5 = hashlib.md5(str(1).encode("utf-8")).hexdigest()
# print(md5[:6])

# md5 = hashlib.md5(str(1).encode("utf-8")).hexdigest()
# print(md5)
# if(md5[:6] == '6d0bc1'):
#    print(md5[:6])
#    # print(i)