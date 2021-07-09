import  time
import asyncio
# async def func(): #此时的函数是异步协程函数，此时函数执行得到的是一个协程对象
#     print("wohahah")
async def func1(): #此时的函数是异步协程函数，此时函数执行得到的是一个协程对象
    print("wohahah1")
    # time.sleep(3)
    await asyncio.sleep(3) #异步操作代码
    print("bbbbbb1")
async def func2(): #此时的函数是异步协程函数，此时函数执行得到的是一个协程对象
    print("wohahah2")
    # time.sleep(2)
    await asyncio.sleep(2)
    print("bbbbbb2")
async def func3(): #此时的函数是异步协程函数，此时函数执行得到的是一个协程对象
    print("wohahah3")
    # time.sleep(4)
    await asyncio.sleep(4)
    print("bbbbbb3")
async def main():
    tasks = [
        asyncio.create_task(func1()),
        asyncio.create_task(func2()),
        asyncio.create_task(func3()),

    ]
    await asyncio.wait(tasks)
    pass

if __name__ == '__main__':
    # g= func()
    # asyncio.run(g) #协程程序运行需要asyncio模块的支持
# 协程：当程序遇到了IO操作的时候，可以选择行的切换到其他任务上
# 在微观上是一个任务一个任务的切换，切换条件一般就是IO操作
# 在宏观上，我们能看到的其实是多个任务一起在执行
# 多任务异步操作
    asyncio.run(main())