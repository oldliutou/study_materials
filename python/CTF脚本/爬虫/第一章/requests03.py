import requests

url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0%2C10&tags=%E7%94%B5%E5%BD%B1&start=22'
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
}
res = requests.get(url,headers=header)
print(res.json())
res.close()