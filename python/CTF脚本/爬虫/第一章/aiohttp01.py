import aiohttp,asyncio

urls=[
    "http://kr.shanghai-jiuxin.com/file/2020/1031/774218be86d832f359637ab120eba52d.jpg",
    "http://kr.shanghai-jiuxin.com/file/2020/1031/191468637cab2f0206f7d1d9b175ac81.jpg",
    "http://kr.shanghai-jiuxin.com/file/2020/1031/d7de3f9faf1e0ecdea27b73139fc8d3a.jpg"
]

async def aiodownload(url):
    name = url.rsplit("/",1)[1]
    # aiohttp.ClientSession() <==> requests
    async with aiohttp.ClientSession() as session:
        async  with session.get(url) as resp:
            # resp.content.read()
            with open("img/"+name,mode="wb") as f:
                f.write(await resp.content.read()) #读取内容是异步的，需要await挂起
    print(name,"搞定")
    pass
async def main():
    tasks = []
    for url in urls:
        tasks.append(aiodownload(url))

    await asyncio.wait(tasks)
    pass

if __name__ == '__main__':
    asyncio.run(main())