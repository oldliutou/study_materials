import hashlib

for i in range(9999999999999):
    md5str = hashlib.md5(str(i).encode('utf-8')).hexdigest()
    # print(md5str[:7])
    if(md5str[:7]=='4bf21cd'):
        print("md5:  "+md5str[:7]+' '+str(i))
        break