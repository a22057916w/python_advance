## Asynchronous
Basiclly, the asynchronous programming can discribe in the following concept:
* **Event Loop**
* **Event**
* **CallBack**

### Event Loop
Since the `asynchronous process` must swich between different tasks. There must be a list to maintain all the tasks and info, which is what a **Event loop** doing.

### Event and CallBack
If there is a asynchronous process, it must register to a **Eventloop** like `Event : CallBack`, then the **EventLoop** would iterate throught the registered process like `for` doing.
<br><br>
If a **Event** is happening, the **EventLoop** would invoke the **CallBack**, and stop listening the event.

![](https://github.com/a22057916w/python_advance/blob/main/.meta/eventloop1.png)
<br><br>
![](https://github.com/a22057916w/python_advance/blob/main/.meta/eventloop2.png)
<br><br>
![](https://github.com/a22057916w/python_advance/blob/main/.meta/eventloop3.png)
<br><br>

**Take the Following Code for Example:**
```
import asyncio
loop = asyncio.get_event_loop() # create a Event Loop

async def example1():       # Define a coroutine that would be interrup
    print("Start example1 coroutin.")
    await asyncio.sleep(1)      # inturrup the coroutine for 1 second
    print("Finish example1 coroutin.")

async def example2():   # Define a coroutine
    print("Start example2 coroutin.")
    # do some process...
    print("Finish example2 coroutin.")

tasks = [       # create a list of task
    asyncio.ensure_future(example1()),
    asyncio.ensure_future(example2()),
]

# register the two corotinue to EventLoop
# loop start, exec example1, pause example, exec example2, resume example1
loop.run_until_complete(asyncio.wait(tasks))

# output:
# Start example1 coroutin.
# Start example2 coroutin.
# Finish example2 coroutin.
# Finish example1 coroutin.
```

### Coroutine
A **coroutine** is a function that can be paused, returned, and resumed in the halfway.
<br><br>
For Python Package `asycnio`, a corotinue can be declare by adding `async` in front of the function, like ```async def example():```

### Task
To put it simply, a **coroutine** must be encapencapsulated to a **task** to communicate with **EventLoop**.
For example, the line `loop.run_until_complete(example())` would convert the coroutine `example()` into a task, then register to EventLoop.

### Await
If there were no `await`, the coroutine would have executed the counter directly, instead of pausing. One can think `await` as a declaration of **callback** function. One can relate the concept to the picture(2)(3) above.

### Reference
* [python的asyncio模組(二)：異步程式設計基本概念 - iT 邦幫忙::一起幫忙解決難題，拯救 IT 人的一天](https://ithelp.ithome.com.tw/articles/10199403)
* [async await 學習筆記. 何謂非同步 | by 髒桶子 | 喜歡解決問題的髒桶子 | Medium](https://medium.com/%E9%AB%92%E6%A1%B6%E5%AD%90/aysnc-await-%E6%95%99%E5%AD%B8%E7%AD%86%E8%A8%98-debabdb9db0e)

