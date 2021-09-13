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
        for i in range(4):
            self.window.columnconfigure(i, weight=1)
        for i in range(6):
            self.window.rowconfigure(i, weight=1)

        # 將 StringVar 變數與 Tkinter 控制元件關聯後，修改 StringVar 變數後，Tkinter 將自動更新此控制元件
        self.strEqua = tk.StringVar()

        # 儲存算式然後 set 到 strEqua
        self.strExpr = "0"
        self.strEqua.set(self.strExpr)

        self.bEvaluated = False

        # 使用Entry顯示計算值
        self.entResult = tk.Entry(self.window, textvariable=self.strEqua, state=tk.DISABLED, justify="right")     # "state=tk.DISABLED" will not allow user to input, "justify="right"" aligns the text to the right
        self.entResult.config(disabledbackground=self.window["bg"], font=12)     # set disabledbackground colour
        self.entResult.grid(row = 0, column = 0, columnspan=4, ipadx=70, sticky=tk.NW+tk.SE)

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
        self.btnAdd.grid(row=4, column=3, sticky=tk.NW+tk.SE)

        self.btnSub = tk.Button(self.window, width=20, text="-", font=12, command=lambda:self.pressArithm("-"))
        self.btnSub.grid(row=3, column=3, sticky=tk.NW+tk.SE)

        self.btnMult = tk.Button(self.window, width=20, text="*", font=12, command=lambda:self.pressArithm("*"))
        self.btnMult.grid(row=2, column=3, sticky=tk.NW+tk.SE)

        self.btnDiv = tk.Button(self.window, width=20, text="/", font=12, command=lambda:self.pressArithm("/"))
        self.btnDiv.grid(row=1, column=3, sticky=tk.NW+tk.SE)

        # ------- setup parenthsis buttons ---------
        self.btnLeftParen = tk.Button(self.window, width=20, text="(", font=12, command=lambda:self.pressLeftParen())
        self.btnLeftParen.grid(row=1, column=1, sticky=tk.NW+tk.SE)

        self.btnRightParen = tk.Button(self.window, width=20, text=")", font=12, command=lambda:self.pressRightParen())
        self.btnRightParen.grid(row=1, column=2, sticky=tk.NW+tk.SE)


        # -------- setup buttons of other operations  ---------
        self.btnEqu = tk.Button(self.window, width=20, text="=", font=12, command=lambda:self.pressEqu())
        self.btnEqu.grid(row=5, column=3, sticky=tk.NW+tk.SE)

        self.btnDec = tk.Button(self.window, width=20, text=".", font=12, command=lambda:self.pressDec())
        self.btnDec.grid(row=5, column=2, sticky=tk.NW+tk.SE)

        self.btnClear = tk.Button(self.window, width=20, text="AC", font=12, command=lambda:self.pressClear())
        self.btnClear.grid(row=1, column=0, sticky=tk.NW+tk.SE)


# ------------------ method of button events -------------------------

    # handling the button events of numbers
    def pressNum(self, strNum):
        # if the expression has been evaluated, reset the experssion to strNum
        if self.bEvaluated:
            self.strExpr = strNum
            self.strEqua.set(self.strExpr)
            self.bEvaluated = False
            return

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
            if self.isOp(self.strExpr[-2]) and self.strExpr[-1] == "0":
                self.strExpr = self.strExpr[:-1] + strNum
            elif self.strExpr[-1] == ")":
                return
            else:
                # concatenation the expression and pressed button var
                self.strExpr = self.strExpr + strNum
        self.strEqua.set(self.strExpr)


    # handling the alrithmatic buttons
    def pressArithm(self, strOp):
        if self.bEvaluated:
            self.strExpr = "0"
            self.strEqua.set(self.strExpr)
            self.bEvaluated = False
            return

        # 額外判斷 +, - 外的運算元和（的互動
        if strOp != "+" and strOp != "-":
            if self.isOp(self.strExpr[-1]) and self.strExpr[-2] == "(":
                return
            elif self.strExpr[-1] == "(":
                return
            else:
                pass


        # checking if the last char of string is op or "."
        if self.isOp(self.strExpr[-1]) or self.strExpr[-1] == ".":
            self.strExpr = self.strExpr[:-1] + strOp
        else:
            # concatenation the expression and alrithmatic button
            self.strExpr = self.strExpr + strOp
        self.strEqua.set(self.strExpr)


    def pressLeftParen(self):
        # if the expression is at dafault state, replace 0 with (
        if self.strExpr == "0":
            self.strExpr = "("
            self.strEqua.set(self.strExpr)
            return

        # if the last char is op, add "(", else do nothing
        if self.isOp(self.strExpr[-1]) or self.strExpr[-1] == "(":
            self.strExpr = self.strExpr + "("
        else:
            return
        self.strEqua.set(self.strExpr)


    def pressRightParen(self):
        # if the expression is at dafault state, do nothing
        if self.strExpr == "0":
            return

        # if ")" 數量(大)等於 "("" 數量, do noting
        if self.strExpr.count(")") >= self.strExpr.count("("):
            return

        if self.isOp(self.strExpr[-1]) or self.strExpr[-1] == ".":
            return
        else:
            self.strExpr = self.strExpr + ")"
        self.strEqua.set(self.strExpr)


    def pressEqu(self):
        try:
            # count the difference of numbers of "(" and ")", then rewrite the expression
            nParen = self.strExpr.count("(") - self.strExpr.count(")")
            if nParen > 0:
                self.strExpr += ")"*nParen

            # 特例: () 取代為 0
            self.strExpr = self.strExpr.replace("()", "0")

            # evaluate the expression
            self.strExpr = str(eval(self.strExpr))
            self.strEqua.set(self.strExpr)
            self.bEvaluated = True

        except ZeroDivisionError:
            messagebox.showinfo("Error", "Can not divide by zero")     # tkinter.messagebox
            self.strExpr = "0"
            self.strEqua.set(self.strExpr)
            self.bEvaluated = True

        # deal with invalid expression such as 8*(*(*(, then return default value
        except SyntaxError:
            self.strExpr = "0"
            self.strEqua.set(self.strExpr)
            self.bEvaluated = True

        except Exception as e:
            print("Unexpected Error: " + e)


    def pressDec(self):
        # if the last char is ( or ), do nothing
        if self.strExpr[-1] == "(" or self.strExpr[-1] == ")":
            return

        # if the last char is operator
        if self.isOp(self.strExpr[-1]):

            # if the expression is like (+, ( with an op, do noting
            if self.strExpr[-2] == "(" or self.strExpr[-2] == ")":
                return

            # if there is already "." in expression, replace op with nothing
            if "." in self.strExpr:
                self.strExpr = self.strExpr[:-1]
            # otherwise, replace op wiht "."
            else:
                self.strExpr = self.strExpr[:-1] + "."
        # make sure there can be two floating numbers in the expression. e.g. 3.2 + 6.4
        # if three is "." in the expression after spliting by ops, do noting
        elif "." in re.split(r'\+|-|\*|\/', self.strExpr)[-1]:
            return
        # otherewise, add decimal point to the expression
        else:
            self.strExpr = self.strExpr + "."
        self.strEqua.set(self.strExpr)


    def pressClear(self):
        self.strExpr = "0"
        self.strEqua.set(self.strExpr)
        self.bEvaluated = True


# ------------------ end of method of button events -----------------------

    def isOp(self, strOp):
        listOps = ["+", "-", "*", "/"]
        return 1 in [op in strOp for op in listOps]

    def mainloop(self):
        self.window.mainloop()

if __name__ == '__main__':

    # new an instance of a Calculator then start it
    cal = Calculator()
    cal.mainloop()
