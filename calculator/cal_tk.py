import tkinter as tk
from tkinter import messagebox
import os
import re       # stand for regular expression

class Calculator():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Simple Calculator")
        self.window.geometry("800x400")          # set window size
        self.window.resizable(0, 0)              # set window fixed

        # 讓grid column and row可隨視窗放大, grid size: 4x6
        for i in range(4):
            self.window.columnconfigure(i, weight=1)
        for i in range(6):
            self.window.rowconfigure(i, weight=1)

        # 將 StringVar 變數與 Tkinter 控制元件關聯後，修改 StringVar 變數後，Tkinter 將自動更新此控制元件
        self.strEquation = tk.StringVar()

        # 儲存算式然後 set 到 strEquation
        self.strExpression = "0"
        self.strEquation.set(self.strExpression)

        # 使用Entry顯示計算值
        self.entResult = tk.Entry(self.window, textvariable=self.strEquation, state=tk.DISABLED, justify="right")     # "state=tk.DISABLED" will not allow user to input, "justify="right"" aligns the text to the right
        self.entResult.config(disabledbackground=self.window["bg"])     # set disabledbackground colour
        self.entResult.grid(row = 0, column = 0, columnspan=4, ipadx=70, sticky=tk.NW+tk.SE)

        # -------- setup buttons of number  ---------
        self.btnZero = tk.Button(self.window, width=20, text="0", command=lambda:self.pressNum("0"))
        self.btnZero.grid(row=5, column=0, columnspan=2, sticky=tk.NW+tk.SE)

        self.btnOne = tk.Button(self.window, width=20, text="1", command=lambda:self.pressNum("1"))
        self.btnOne.grid(row=4, column=0, sticky=tk.NW+tk.SE)

        self.btnTwo = tk.Button(self.window, width=20, text="2", command=lambda:self.pressNum("2"))
        self.btnTwo.grid(row=4, column=1, sticky=tk.NW+tk.SE)

        self.btnThree = tk.Button(self.window, width=20, text="3", command=lambda:self.pressNum("3"))
        self.btnThree.grid(row=4, column=2, sticky=tk.NW+tk.SE)

        self.btnFour = tk.Button(self.window, width=20, text="4", command=lambda:self.pressNum("4"))
        self.btnFour.grid(row=3, column=0, sticky=tk.NW+tk.SE)

        self.btnFive = tk.Button(self.window, width=20, text="5", command=lambda:self.pressNum("5"))
        self.btnFive.grid(row=3, column=1, sticky=tk.NW+tk.SE)

        self.btnSix = tk.Button(self.window, width=20, text="6", command=lambda:self.pressNum("6"))
        self.btnSix.grid(row=3, column=2, sticky=tk.NW+tk.SE)

        self.btnSeven = tk.Button(self.window, width=20, text="7", command=lambda:self.pressNum("7"))
        self.btnSeven.grid(row=2, column=0, sticky=tk.NW+tk.SE)

        self.btnEight = tk.Button(self.window, width=20, text="8", command=lambda:self.pressNum("8"))
        self.btnEight.grid(row=2, column=1, sticky=tk.NW+tk.SE)

        self.btnNine = tk.Button(self.window, width=20, text="9", command=lambda:self.pressNum("9"))
        self.btnNine.grid(row=2, column=2, sticky=tk.NW+tk.SE)

        # -------- setup buttons of alrithmatic  ---------
        self.btnAdd = tk.Button(self.window, width=20, text="+", command=lambda:self.pressArithm("+"))
        self.btnAdd.grid(row=4, column=3, sticky=tk.NW+tk.SE)

        self.btnSub = tk.Button(self.window, width=20, text="-", command=lambda:self.pressArithm("-"))
        self.btnSub.grid(row=3, column=3, sticky=tk.NW+tk.SE)

        self.btnMult = tk.Button(self.window, width=20, text="*", command=lambda:self.pressArithm("*"))
        self.btnMult.grid(row=2, column=3, sticky=tk.NW+tk.SE)

        self.btnDiv = tk.Button(self.window, width=20, text="/", command=lambda:self.pressArithm("/"))
        self.btnDiv.grid(row=1, column=3, sticky=tk.NW+tk.SE)

        self.btnMod = tk.Button(self.window, width=20, text="%", command=lambda:self.pressArithm("%"))
        self.btnMod.grid(row=1, column=2, sticky=tk.NW+tk.SE)

        # -------- setup buttons of other operations  ---------
        self.btnEqu = tk.Button(self.window, width=20, text="=", command=lambda:self.pressEqu())
        self.btnEqu.grid(row=5, column=3, sticky=tk.NW+tk.SE)

        self.btnDec = tk.Button(self.window, width=20, text=".", command=lambda:self.pressDec())
        self.btnDec.grid(row=5, column=2, sticky=tk.NW+tk.SE)

        self.btnClear = tk.Button(self.window, width=20, text="AC", command=lambda:self.pressClear())
        self.btnClear.grid(row=1, column=0, sticky=tk.NW+tk.SE)

        self.btnMinus = tk.Button(self.window, width=20, text="+/-", command=lambda:self.pressMinus())
        self.btnMinus.grid(row=1, column=1, sticky=tk.NW+tk.SE)

# ------------------ method of button events -------------------------

    # handling the button events of numbers
    def pressNum(self, strNum):
        if len(self.strExpression) > 1:
            # make sure there can be equation like 3+02, should be 3+2
            if self.isOperator(self.strExpression[-2]) and self.strExpression[-1] == "0":
                self.strExpression = self.strExpression[:-1] + strNum
            else:
                # concatenation the expression and pressed button var
                self.strExpression = self.strExpression + strNum
        # cheking if the expression is 0
        else:
            if self.strExpression == "0":
                self.strExpression = strNum
            else:
                self.strExpression = self.strExpression + strNum
        self.strEquation.set(self.strExpression)

    # handling the alrithmatic buttons
    def pressArithm(self, strOp):
        # checking if the expression contains decimal point
        if strOp == "." and "." in self.strExpression:
            pass
        # checking if the last char of string is op or "."
        elif self.isOperator(self.strExpression[-1]) or self.strExpression[-1] == ".":
            self.strExpression = self.strExpression[:-1] + strOp
        else:
            # concatenation the expression and alrithmatic button
            self.strExpression = self.strExpression + strOp
        self.strEquation.set(self.strExpression)

    # handling the equal button and calculate the equation
    def pressEqu(self):
        try:
            # checking zeor division
            if re.match(r'\d\/0', self.strExpression):      # "\d" for [0-9]
                messagebox.showinfo("Error", "Don't be silly.")     # tkinter.messagebox
                self.strExpression = "0"
            else:
                # evaluate the expression
                self.strExpression = str(eval(self.strExpression))
            self.strEquation.set(self.strExpression)
        except Exception as e:
            print("Unexpected Error: " + e)

    # handling the decimal points buttons
    def pressDec(self):
        # if the last char is operator
        if self.isOperator(self.strExpression[-1]):
            # if there is already "." in expression, replace op with nothing
            if "." in self.strExpression:
                self.strExpression = self.strExpression[:-1]
            # otherwise, replace op wiht "."
            else:
                self.strExpression = self.strExpression[:-1] + "."
        # make sure there can be two floating numbers in the expression. e.g. 3.2 + 6.4
        # if three is "." in the expression after spliting by ops, do noting
        elif "." in re.split(r'\+|-|\*|\/|%', self.strExpression)[-1]:
            pass
        # otherewise, add decimal point to the expression
        else:
            self.strExpression = self.strExpression + "."
        self.strEquation.set(self.strExpression)

    # handling the clear button then set the equation to 0
    def pressClear(self):
        self.strExpression = "0"
        self.strEquation.set(self.strExpression)

    # handling the Minus buttons
    def pressMinus(self):
        if self.strExpression[0] == "-":
            self.strExpression = self.strExpression[1:]
        else:
            self.strExpression = "-" + self.strExpression[0:]
        self.strEquation.set(self.strExpression)

# ------------------ end of method of button events -----------------------

    def isOperator(self, strOp):
        listOps = ["+", "-", "*", "/", "%"]
        return 1 in [op in strOp for op in listOps]

    def mainloop(self):
        self.window.mainloop()

if __name__ == '__main__':

    # new an instance of a Calculator then start it
    cal = Calculator()
    cal.mainloop()
