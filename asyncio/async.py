import requests
import time
import asyncio

url = 'https://www.google.com.tw/'

#建立一個Event Loop
loop = asyncio.get_event_loop()

start_time = time.time()

async def send_req(url):
    t = time.time()
    print("Send a request at",t-start_time,"seconds.")

    res = await loop.run_in_executor(None,requests.get,url)

    t = time.time()
    print("Receive a response at",t-start_time,"seconds.")

tasks = []

for i in range(10):
    # 這個函數會接收一個coroutine object，並包裝成一個Task對象，同時把這個Task註冊到這個Event loop中等待執行。
    task = loop.create_task(send_req(url))
    tasks.append(task)


# loop.run_until_complete(coroutine)
# 這個函數顧名思義，就是讓註冊參數裡的任務並執行，等到任務完成就關閉Event Loop

# asyncio.wait(tasks)
# 這函數的用處在於把兩個example1和example2的兩個協程對象包成一個大的協程對象，就是把兩個小任務包成一個大任務。
loop.run_until_complete(asyncio.wait(tasks))

print("\nFinished in", time.time() - start_time, "seconds.")
