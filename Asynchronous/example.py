import requests
import time
import asyncio

url = 'https://www.google.com.tw/'
loop = asyncio.get_event_loop()

start_time = time.time()

async def send_req(url, i):
    print(i)
    t = time.time()

    print("Send a request at",t-start_time,"seconds.")
    res = await loop.run_in_executor(None,requests.get,url)

    print(i)
    t = time.time()
    print("Receive a response at",t-start_time,"seconds.")

tasks = []

for i in range(10):
    task = loop.create_task(send_req(url, i))
    tasks.append(task)

loop.run_until_complete(asyncio.wait(tasks))
