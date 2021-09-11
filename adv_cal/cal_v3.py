import tkinter as tk
from tkinter import messagebox
import re
import math
import os
from time import strftime, localtime
import codecs    # log output for windows `

# ------------------ log function ---------------------
def printLog(strLogMsg):
    print(strLogMsg)
    fileLog = codecs.open("./cal_v3.log", 'a', "utf-8")
    fileLog.write("[%s]%s\n" % (getDateTimeFormat(), strLogMsg))
    fileLog.close()

def getDateTimeFormat():
    strDateTime = "%s" % (strftime("%Y/%m/%d %H:%M:%S", localtime()))
    return strDateTime

class Calculator():
    def __init__(self):
        printLog("[I][__init__] Iniiating the Calculator")

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

        self.btnMod = tk.Button(self.window, width=20, text="%", font=12, command=lambda:self.pressArithm(
        "%"))
        self.btnMod.grid(row=1, column=3, sticky=tk.NW+tk.SE)

        # ------- setup special operation buttons ---------

        self.btnRoot = tk.Button(self.window, width=20, text="\u221A", font=12, command=lambda:self.pressRoot())
        self.btnRoot.grid(row=1, column=4, sticky=tk.NW+tk.SE)

        self.btnSquare = tk.Button(self.window, width=20, text="x\u00B2", font=12, command=lambda:self.pressSquare())
        self.btnSquare.grid(row=2, column=4, sticky=tk.NW+tk.SE)

        self.btnCube = tk.Button(self.window, width=20, text="x\u00B3", font=12, command=lambda:self.pressCube())
        self.btnCube.grid(row=3, column=4, sticky=tk.NW+tk.SE)

        self.btnFact = tk.Button(self.window, width=20, text="n!", font=12, command=lambda:self.pressFact())
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
        printLog("[I][pressNum] The button %s has been pressed" % strNum)
        # if the expression is single digit
        if len(self.strExpr) < 2:
            # if the expression is 0, simply change it to strNum
            if self.strExpr == "0":
                self.strExpr = strNum
            # else, concatenation the expression and strNum
            else:
                self.strExpr += strNum
        # if the length of expression >= 2
        else:
            # make sure there can not be equation like 3+02, should be 3+2
            if self.hasOp(self.strExpr[-2]) and self.strExpr[-1] == "0":
                self.strExpr = self.strExpr[:-1] + strNum
            # concatenation the expression and pressed button var
            else:
                self.strExpr += strNum
        self.strEqua.set(self.strExpr)

    # handling the alrithmatic buttons
    def pressArithm(self, strOp):
        printLog("[I][pressArithm] The button %s has been pressed" % strOp)

        # if the last char is op or ".", repalace with strOp
        if self.hasOp(self.strExpr[-1]) or self.strExpr[-1] == ".":
            self.strExpr = self.strExpr[:-1] + strOp
        # if the op is in the expression and not in the last pos, do calculation
        elif self.hasOp(self.strExpr):
            self.pressEqu()
            self.strExpr += strOp
        # concatenation the expression and alrithmatic button
        else:
            self.strExpr += strOp
        self.strEqua.set(self.strExpr)


    def pressRoot(self):
        printLog("[I][pressRoot] The button \u221A has been pressed")

        try:
            # if the last char is op, remove it
            if self.hasOp(self.strExpr[-1]):
                self.strExpr = self.strExpr[:-1]

            # split expression by ops for examle, 123+4 goes to [123, 4].  Then
            # get the number last number(4) and calculate
            strLast = re.split(r'\+|-|\*|\/|%', self.strExpr)[-1]
            strVal = str(math.sqrt(eval(strLast)))

            self.strExpr = self.strExpr[:-len(strLast)] + strVal
            self.strEqua.set(self.strExpr)

        except OverflowError as e:
            printLog("[W][pressRoot] The \u221A operation will go overflow")
            messagebox.showinfo("Error", e)
            self.strExpr = "0"
            self.strEqua.set(self.strExpr)

        except Exception as e:
            printLog("[E][pressRoot] Unexpected Error: " + e)


    def pressSquare(self):
        printLog("[I][pressSquare] The button x\u00B2 has been pressed")

        # if the last char is op, remove it
        if self.hasOp(self.strExpr[-1]):
            self.strExpr = self.strExpr[:-1]

        strLast = re.split(r'\+|-|\*|\/|%', self.strExpr)[-1]
        strVal = str(eval(strLast)**2)

        self.strExpr = self.strExpr[:-len(strLast)] + strVal
        self.strEqua.set(self.strExpr)

    def pressCube(self):
        printLog("[I][pressCube] The button x\u00B3 has been pressed")

        # if the last char is op, remove it
        if self.hasOp(self.strExpr[-1]):
            self.strExpr = self.strExpr[:-1]

        strLast = re.split(r'\+|-|\*|\/|%', self.strExpr)[-1]
        strVal = str(eval(strLast)**3)

        self.strExpr = self.strExpr[:-len(strLast)] + strVal
        self.strEqua.set(self.strExpr)

    def pressFact(self):
        printLog("[I][pressFact] The button n! has been pressed")

        try:
            # if the last char is op, remove it
            if self.hasOp(self.strExpr[-1]):
                self.strExpr = self.strExpr[:-1]

            strLast = re.split(r'\+|-|\*|\/|%', self.strExpr)[-1]

            # if the value > 100,000, return to default value
            if eval(strLast) > 1E5:
                printLog("[W][pressFact] The factorial number is out of limit")
                messagebox.showinfo("Error", "The factorial number is out of limit")
                self.strExpr = "0"
                self.strEqua.set(self.strExpr)
            else:
                strVal = str(math.factorial(eval(strLast)))

                self.strExpr = self.strExpr[:-len(strLast)] + strVal
                self.strEqua.set(self.strExpr)

        except ValueError as e:
            printLog("[W][pressFact] The factorial number is out of limit")
            messagebox.showinfo("Error", e)
            self.strExpr = "0"
            self.strEqua.set(self.strExpr)

        except Exception as e:
            printLog("[E][pressFact] Unexpected Error: " + e)
            #print(e)

    def pressEqu(self):
        printLog("[I][pressEqu] The button = has been pressed")

        try:
            # evaluate the expression
            self.strExpr = str(eval(self.strExpr))
            self.strEqua.set(self.strExpr)

        except ZeroDivisionError:
            printLog("[W][pressEqu] Action involves zero division")
            messagebox.showinfo("Error", "Can not divide by zero")     # tkinter.messagebox
            self.strExpr = "0"
            self.strEqua.set(self.strExpr)

        # deal with invalid expression such as 8*(*(*(, then return default value
        except SyntaxError:
            printLog("[W][pressEqu] The expression is incomplete")
            self.strExpr = "0"
            self.strEqua.set(self.strExpr)

        except Exception as e:
            printLog("[E][pressEqu] Unexpected Error: " + e)
            #print("Unexpected Error: " + e)

    def pressDec(self):
        printLog("[I][pressDec] The button . has been pressed")

        # if the last char is operator
        if self.hasOp(self.strExpr[-1]):
            # if there is already "." in expression, replace op with nothing
            if "." in self.strExpr:
                self.strExpr = self.strExpr[:-1]
            # otherwise, replace op wiht "."
            else:
                self.strExpr = self.strExpr[:-1] + "."
        # make sure there can be two floating numbers in the expression. e.g. 3.2 + 6.4
        # if three is "." in the expression after spliting by ops, do noting
        elif "." in re.split(r'\+|-|\*|\/|%', self.strExpr)[-1]:
            return
        # otherewise, add decimal point to the expression
        else:
            self.strExpr = self.strExpr + "."
        self.strEqua.set(self.strExpr)


    def pressClear(self):
        printLog("[I][pressClaer] The button AC has been pressed")

        self.strExpr = "0"
        self.strEqua.set(self.strExpr)


    def pressMinus(self):
        printLog("[I][pressMinus] The button +/- has been pressed")

        if self.strExpr[0] == "-":
            self.strExpr = self.strExpr[1:]
        else:
            self.strExpr = "-" + self.strExpr[0:]
        self.strEqua.set(self.strExpr)


    def pressErase(self):
        printLog("[I][pressErase] The button \u232B has been pressed")

        # if the expression is single digit or something else, set to 0(default)
        if len(self.strExpr) < 2:
            self.strExpr = "0"
        else:
            self.strExpr = self.strExpr[:-1]
        self.strEqua.set(self.strExpr)

# ------------------ end of method of button events -----------------------

    def hasOp(self, strOp):
        listOps = ["+", "-", "*", "/", "%"]
        return 1 in [op in strOp for op in listOps]

    def mainloop(self):
        printLog("[I][mainloop] Start the Calculator")
        self.window.mainloop()

if __name__ == '__main__':

    # new an instance of a Calculator then start it
    cal = Calculator()
    cal.mainloop()

    printLog("[I][__main__] End of process")
