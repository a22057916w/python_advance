import requests
import time
import asyncio

url = 'https://www.google.com.tw/'

# since the asyncio must swich between different tasks, there must be a list to contain all the task and info.
# And that is what event loop doing
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
    task = loop.create_task(send_req(url))
    tasks.append(task)

loop.run_until_complete(asyncio.wait(tasks))

print("\nFinished in", time.time() - start_time, "seconds.")
