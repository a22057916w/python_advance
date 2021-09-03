## Problem
1. Button is executed automatically
```
btnFirst = tk.Button(window, width=20, text=str(nFirstOperand), command=operation("+", nFirstOperand))
```
It happens because you're calling the function. Pass it a function object instead, such as one created with `lambda`.
```
..., command=(lambda: operation("+", nFirstOperand)))
```
2. 更改initValue(顯示數字)的值


3. 讓widget隨視窗放大

## Reference
* [Why my python tkinter button is executed automatically - Stack Overflow](https://stackoverflow.com/questions/19285907/why-my-python-tkinter-button-is-executed-automatically)
* [[Python教學]Python Lambda Function應用技巧分享](https://www.learncodewithmike.com/2019/12/python-lambda-functions.html)
* [configparser — Configuration file parser — Python 3.9.7 documentation](https://docs.python.org/3/library/configparser.html)
