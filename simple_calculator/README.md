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
Using `columnconfigure(index, weight)` and `rowcofigure(index, weight)`: <br>
  Every column and row has a "weight" grid option associated with it, which tells it how much it should grow if there is extra room in the master to fill. By       default, the weight of each column or row is 0, meaning don't expand to fill space. For example:
  ```
  window.columnconfigure(0, weight=1)
  window.rowconfigure(0, weight=1)
  
  lbResult = tk.Label(window, textvariable=strResult)
  lbResult.grid(row = 0, column = 0, columnspan=2, ipadx=70)
  
  btnFirst = tk.Button(window, width=20, text=strFirstOp + str(nFirstOperand), command=lambda: operation(strFirstOp, nFirstOperand))
  btnFirst.grid(row=1, column=0, sticky=tk.NW+tk.SE)
  ```
  
## Reference
* [Why my python tkinter button is executed automatically - Stack Overflow](https://stackoverflow.com/questions/19285907/why-my-python-tkinter-button-is-executed-automatically)
* [[Python教學]Python Lambda Function應用技巧分享](https://www.learncodewithmike.com/2019/12/python-lambda-functions.html)
* [configparser — Configuration file parser — Python 3.9.7 documentation](https://docs.python.org/3/library/configparser.html)
* [python - What does 'weight' do in tkinter? - Stack Overflow](https://stackoverflow.com/questions/45847313/what-does-weight-do-in-tkinter)
* [Tkinter Grid Geometry Manager](https://www.pythontutorial.net/tkinter/tkinter-grid/)
