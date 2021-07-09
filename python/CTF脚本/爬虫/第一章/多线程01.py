from threading import Thread
def func(name):
    for i in range(1000):
        print(name,i)

if __name__ == '__main__':
    for i  in range(13):
        t = Thread(target=func,args=("子线程"+str(i),))
        t.start()
    for i in range(1000):
        print("main",i)