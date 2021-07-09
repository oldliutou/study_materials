import requests

url = 'https://fanyi.baidu.com/sug'
s = input("请输入你要查询的单词：")
data = {
    'kw': s
}
reps = requests.post(url,data)
print(reps.json()) #将服务器返回的内容直接处理成json数据