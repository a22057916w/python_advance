# Python-Advance
## Argvs
### Reference
* [python - What does ** (double star/asterisk) and * (star/asterisk) do for parameters? - Stack Overflow](https://stackoverflow.com/questions/36901/what-does-double-star-asterisk-and-star-asterisk-do-for-parameters)
## Decorator
### Reference
* [Python進階技巧 (3) — 神奇又美好的 Decorator ，嗷嗚！ | by Jack Cheng | 整個程式都是我的咖啡館 | Medium](https://medium.com/citycoddee/python%E9%80%B2%E9%9A%8E%E6%8A%80%E5%B7%A7-3-%E7%A5%9E%E5%A5%87%E5%8F%88%E7%BE%8E%E5%A5%BD%E7%9A%84-decorator-%E5%97%B7%E5%97%9A-6559edc87bc0)
* [Python 的 staticmethod 與 classmethod | by 莊子弘 | Medium](https://ji3g4zo6qi6.medium.com/python-tips-5d36df9f6ad5)

## Async/Await
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

### Coroutine
A **coroutine** is a function that can be paused, returned, and resumed in the halfway.
<br><br>
For Python Package `asycnio`, a corotinue can be declare by adding `async` in front of the function, like ```async def example():```.

### Reference
* [python的asyncio模組(二)：異步程式設計基本概念 - iT 邦幫忙::一起幫忙解決難題，拯救 IT 人的一天](https://ithelp.ithome.com.tw/articles/10199403)
* [async await 學習筆記. 何謂非同步 | by 髒桶子 | 喜歡解決問題的髒桶子 | Medium](https://medium.com/%E9%AB%92%E6%A1%B6%E5%AD%90/aysnc-await-%E6%95%99%E5%AD%B8%E7%AD%86%E8%A8%98-debabdb9db0e)
