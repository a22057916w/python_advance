import tkinter as tk
from tkinter import messagebox
import re

class Calculator():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Calculator")
        self.window.geometry("800x400")          # set window size
        self.window.resizable(0, 0)              # set window fixed

        # 讓grid column and row可隨視窗放大, grid size: 4x6
        for i in range(5):
            self.window.columnconfigure(i, weight=1)
        for i in range(6):
            self.window.rowconfigure(i, weight=1)

        # 將 StringVar 變數與 Tkinter 控制元件關聯後，修改 StringVar 變數後，Tkinter 將自動更新此控制元件
        self.strEqua = tk.StringVar()

        # 儲存算式然後 set 到 strEqua
        self.strExpr = "0"
        self.strEqua.set(self.strExpr)

        self.listStack = [self.strExpr]

        # 使用Entry顯示計算值
        self.entResult = tk.Entry(self.window, textvariable=self.strEqua, state=tk.DISABLED, justify="right")     # "state=tk.DISABLED" will not allow user to input, "justify="right"" aligns the text to the right
        self.entResult.config(disabledbackground=self.window["bg"], font=12)     # set disabledbackground colour
        self.entResult.grid(row = 0, column = 0, columnspan=5, ipadx=70, sticky=tk.NW+tk.SE)

        # -------- setup buttons of number  ---------
        self.btnZero = tk.Button(self.window, width=20, text="0", font=12, command=lambda:self.pressNum("0"))
        self.btnZero.grid(row=5, column=0, columnspan=2, sticky=tk.NW+tk.SE)

        self.btnOne = tk.Button(self.window, width=20, text="1", font=12, command=lambda:self.pressNum("1"))
        self.btnOne.grid(row=4, column=0, sticky=tk.NW+tk.SE)

        self.btnTwo = tk.Button(self.window, width=20, text="2", font=12, command=lambda:self.pressNum("2"))
        self.btnTwo.grid(row=4, column=1, sticky=tk.NW+tk.SE)

        self.btnThree = tk.Button(self.window, width=20, text="3", font=12, command=lambda:self.pressNum("3"))
        self.btnThree.grid(row=4, column=2, sticky=tk.NW+tk.SE)

        self.btnFour = tk.Button(self.window, width=20, text="4", font=12, command=lambda:self.pressNum("4"))
        self.btnFour.grid(row=3, column=0, sticky=tk.NW+tk.SE)

        self.btnFive = tk.Button(self.window, width=20, text="5", font=12, command=lambda:self.pressNum("5"))
        self.btnFive.grid(row=3, column=1, sticky=tk.NW+tk.SE)

        self.btnSix = tk.Button(self.window, width=20, text="6", font=12, command=lambda:self.pressNum("6"))
        self.btnSix.grid(row=3, column=2, sticky=tk.NW+tk.SE)

        self.btnSeven = tk.Button(self.window, width=20, text="7", font=12, command=lambda:self.pressNum("7"))
        self.btnSeven.grid(row=2, column=0, sticky=tk.NW+tk.SE)

        self.btnEight = tk.Button(self.window, width=20, text="8", font=12, command=lambda:self.pressNum("8"))
        self.btnEight.grid(row=2, column=1, sticky=tk.NW+tk.SE)

        self.btnNine = tk.Button(self.window, width=20, text="9", font=12, command=lambda:self.pressNum("9"))
        self.btnNine.grid(row=2, column=2, sticky=tk.NW+tk.SE)

        # -------- setup buttons of alrithmatic  ---------
        self.btnAdd = tk.Button(self.window, width=20, text="+", font=12, command=lambda:self.pressArithm("+"))
        self.btnAdd.grid(row=5, column=3, sticky=tk.NW+tk.SE)

        self.btnSub = tk.Button(self.window, width=20, text="-", font=12, command=lambda:self.pressArithm("-"))
        self.btnSub.grid(row=4, column=3, sticky=tk.NW+tk.SE)

        self.btnMult = tk.Button(self.window, width=20, text="*", font=12, command=lambda:self.pressArithm("*"))
        self.btnMult.grid(row=3, column=3, sticky=tk.NW+tk.SE)

        self.btnDiv = tk.Button(self.window, width=20, text="/", font=12, command=lambda:self.pressArithm("/"))
        self.btnDiv.grid(row=2, column=3, sticky=tk.NW+tk.SE)

        self.btnMod = tk.Button(self.window, width=20, text="%", command=lambda:self.pressArithm("%"))
        self.btnMod.grid(row=1, column=3, sticky=tk.NW+tk.SE)

        # ------- setup special operation buttons ---------

        self.btnRoot = tk.Button(self.window, width=20, text="\u221A", font=12)
        self.btnRoot.grid(row=1, column=4, sticky=tk.NW+tk.SE)

        self.btnSquare = tk.Button(self.window, width=20, text="x\u00B2", font=12)
        self.btnSquare.grid(row=2, column=4, sticky=tk.NW+tk.SE)

        self.btnCube = tk.Button(self.window, width=20, text="x\u00B3", font=12)
        self.btnCube.grid(row=3, column=4, sticky=tk.NW+tk.SE)

        self.btnFact = tk.Button(self.window, width=20, text="n!", font=12)
        self.btnFact.grid(row=4, column=4, sticky=tk.NW+tk.SE)

        # -------- setup buttons of other operations  ---------
        self.btnEqu = tk.Button(self.window, width=20, text="=", font=12, command=lambda:self.pressEqu())
        self.btnEqu.grid(row=5, column=4, sticky=tk.NW+tk.SE)

        self.btnDec = tk.Button(self.window, width=20, text=".", font=12, command=lambda:self.pressDec())
        self.btnDec.grid(row=5, column=2, sticky=tk.NW+tk.SE)

        self.btnClear = tk.Button(self.window, width=20, text="AC", font=12, command=lambda:self.pressClear())
        self.btnClear.grid(row=1, column=0, sticky=tk.NW+tk.SE)

        self.btnMinus = tk.Button(self.window, width=20, text="+/-", font=12, command=lambda:self.pressMinus())
        self.btnMinus.grid(row=1, column=2, sticky=tk.NW+tk.SE)

        self.btnErase = tk.Button(self.window, width=20, text="\u232B", font=12, command=lambda:self.pressErase())
        self.btnErase.grid(row=1, column=1, sticky=tk.NW+tk.SE)

# ------------------ method of button events -------------------------

    # handling the button events of numbers
    def pressNum(self, strNum):
        # if the expression is single digit
        if len(self.strExpr) < 2:
            # if the expression is 0, simply change it to strNum
            if self.strExpr == "0":
                self.strExpr = strNum
            # else, concatenation the expression and strNum
            else:
                self.strExpr = self.strExpr + strNum
        # if the length of expression >= 2
        else:
            # make sure there can be equation like 3+02, should be 3+2
            if self.isOperator(self.strExpr[-2]) and self.strExpr[-1] == "0":
                self.strExpr = self.strExpr[:-1] + strNum
            else:
                # concatenation the expression and pressed button var
                self.strExpr = self.strExpr + strNum
        self.strEqua.set(self.strExpr)

    # handling the alrithmatic buttons
    def pressArithm(self, strOp):
        # checking if the expression contains decimal point
        if strOp == "." and "." in self.strExpr:
            pass
        # checking if the last char of string is op or "."
        elif self.isOperator(self.strExpr[-1]) or self.strExpr[-1] == ".":
            self.strExpr = self.strExpr[:-1] + strOp
        else:
            # concatenation the expression and alrithmatic button
            self.strExpr = self.strExpr + strOp
        self.strEqua.set(self.strExpr)


    def pressRoot(self):
        pass

    def pressSquare(self):
        pass

    def pressFact(self):
        pass

    def pressEqu(self):
        try:
            # checking zeor division
            if self.strExpr[-2:] == "/0":
                messagebox.showinfo("Error", "Don't be silly.")     # tkinter.messagebox
                self.strExpr = "0"
            else:
                # evaluate the expression
                self.strExpr = str(eval(self.strExpr))
            self.strEqua.set(self.strExpr)
        except Exception as e:
            print("Unexpected Error: " + e)


    def pressDec(self):
        # if the last char is operator
        if self.isOperator(self.strExpr[-1]):
            # if there is already "." in expression, replace op with nothing
            if "." in self.strExpr:
                self.strExpr = self.strExpr[:-1]
            # otherwise, replace op wiht "."
            else:
                self.strExpr = self.strExpr[:-1] + "."
        # make sure there can be two floating numbers in the expression. e.g. 3.2 + 6.4
        # if three is "." in the expression after spliting by ops, do noting
        elif "." in re.split(r'\+|-|\*|\/|%', self.strExpr)[-1]:
            pass
        # otherewise, add decimal point to the expression
        else:
            self.strExpr = self.strExpr + "."
        self.strEqua.set(self.strExpr)


    def pressClear(self):
        self.strExpr = "0"
        self.strEqua.set(self.strExpr)


    def pressMinus(self):
        if self.strExpr[0] == "-":
            self.strExpr = self.strExpr[1:]
        else:
            self.strExpr = "-" + self.strExpr[0:]
        self.strEqua.set(self.strExpr)


    def pressErase(self):
        # if the expression is single digit or something else, set to 0(default)
        if len(self.strExpr) < 2:
            self.strExpr = "0"
        else:
            self.strExpr = self.strExpr[:-1]
        self.strEqua.set(self.strExpr)



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
