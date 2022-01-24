import requests
import time

url = 'https://www.google.com.tw/'

start_time = time.time()

def send_req(url):

    t = time.time()
    print("Send a request at",t-start_time,"seconds.")

    res = requests.get(url)

    t = time.time()
    print("Receive a response at",t-start_time,"seconds.")

for i in range(10):
    send_req(url)
    print("*"*20)
print("\nFinished in", time.time() - start_time, "seconds.")
