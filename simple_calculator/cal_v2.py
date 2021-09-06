from configparser import ConfigParser
import tkinter as tk
import os
import sys

# --------- global var for .ini file info ----------
# read operands
nInitValue = 0
nFirstOperand = 0
nSecondOperand = 0
nThirdOperand = 0
nFourthOperand = 0

# read Operators
strFirstOp = ""
strSecondOp = ""
strThirdOp = ""
strFourthOp = ""



# read section "Setting" in .ini file
def read_ini_section(section):
    try:
        global nInitValue, nFirstOperand, nSecondOperand, nThirdOperand, nFourthOperand
        global strFirstOp, strSecondOp, strThirdOp, strFourthOp

        # ---------- read operands ----------
        if "initValue" in section:
            nInitValue = section.getint("initValue")
            print("get initValue %d success" % nInitValue)
        else:
            print("get initValue fail")
        if "firstOperand" in section:
            nFirstOperand = section.getint("firstOperand")
            print("get firstOperand %d success" % nFirstOperand)
        else:
            print("get firstOperand fail")
        if "secondOperand" in section:
            nSecondOperand = section.getint("secondOperand")
            print("get secondOperand %d success" % nSecondOperand)
        else:
            print("get secondOperand fail")
        if "thirdOperand" in section:
            nThirdOperand = section.getint("thirdOperand")
            print("get thirdOperand %d success" % nThirdOperand)
        else:
            print("get thirdOperand fail")
        if "fourthOperand" in section:
            nFourthOperand = section.getint("fourthOperand")
            print("get fourthOperand %d success" % nFourthOperand)
        else:
            print("get fourthOperand fail")

        # ---------- read oprators -----------
        if "firstOperator" in section:
            strFirstOp = section.get("firstOperator")
            print("successfully get firstOperator %s" % strFirstOp)
        else:
            print("get firstOperator fail")
        if "secondOperator" in section:
            strSecondOp = section.get("secondOperator")
            print("successfully get secondOperator %s" % strSecondOp)
        else:
            print("get secondOperator fail")
        if "thirdOperator" in section:
            strThirdOp = section.get("thirdOperator")
            print("successfully get thirdOperator %s" % strThirdOp)
        else:
            print("get thirdOperator fail")
        if "fourthOperator" in section:
            strFourthOp = section.get("fourthOperator")
            print("successfully get fourthOperator %s" % strFourthOp)
        else:
            print("get fourthOperator fail")
        return True
    except Exception as e:
        print(e)

# simple Calculator GUI
class Calculator():
    def __init__(self, nInitValue, nFirstOperand, nSecondOperand, nThirdOperand, nFourthOperand, strFirstOp, strSecondOp, strThirdOp, strFourthOp):

        self.window = tk.Tk()
        self.window.title("Simple Calculator")
        self.window.geometry("600x400")          # set window size
        self.window.resizable(0, 0)              # set window fixed

        # 讓grid column and row可隨視窗放大
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        for i in range(3):
            self.window.rowconfigure(i, weight=1)

        # 將 StringVar 變數與 Tkinter 控制元件關聯後，修改 StringVar 變數後，Tkinter 將自動更新此控制元件
        self.strResult = tk.StringVar()
        self.strResult.set(str(nInitValue))
        #print(type(strResult))

        # 使用Label顯示計算值
        self.lbResult = tk.Label(self.window, textvariable=self.strResult)
        self.lbResult.grid(row = 0, column = 0, columnspan=2, ipadx=70, sticky=tk.W+tk.E)

        # -------- button setup ---------
        self.btnFirst = tk.Button(self.window, width=20, text=strFirstOp + str(nFirstOperand), command=lambda: self.operation(strFirstOp, nFirstOperand))
        self.btnFirst.grid(row=1, column=0, sticky=tk.NW+tk.SE)

        self.btnSecond = tk.Button(self.window, width=20, text=strSecondOp + str(nSecondOperand), command=lambda: self.operation(strSecondOp, nSecondOperand))
        self.btnSecond.grid(row=1, column=1, sticky=tk.NW+tk.SE)

        self.btnThird = tk.Button(self.window, width=20, text=strThirdOp + str(nThirdOperand), command=lambda: self.operation(strThirdOp, nThirdOperand))
        self.btnThird.grid(row=2, column=0, sticky=tk.NW+tk.SE)

        self.btnFourth = tk.Button(self.window, width=20, text=strFourthOp + str(nFourthOperand), command=lambda: self.operation(strFourthOp, nFourthOperand))
        self.btnFourth.grid(row=2, column=1, sticky=tk.NW+tk.SE)

    # method for button call, which does +, -, and *
    def operation(self, strOperator, nOperand):

        # python int type has no range limit
        nTmp = eval(self.strResult.get())

        if strOperator == "+":
            nTmp += nOperand
        elif strOperator == "-":
            nTmp -= nOperand
        elif strOperator == "*":
            nTmp *= nOperand
        self.strResult.set(str(nTmp))

    def mainloop(self):
        self.window.mainloop()


if __name__ == '__main__':
    strAbsPath = os.path.abspath(__file__)
    strFileDir = os.path.dirname(strAbsPath)

    strSettingPath = os.path.join(strFileDir, 'Setting.ini')    # Setting.ini

    # open Setting.ini then assign values to global vars
    with open(strSettingPath) as iniFile:
        config = ConfigParser()
        config.read_file(iniFile)
        if read_ini_section(config["Setting"]) != True:
            sys.exit("read ini secion fail")


    # cheking if read .ini velue properly
    print(nInitValue, nFirstOperand, nSecondOperand, nThirdOperand, nFourthOperand)
    print(strFirstOp, strSecondOp, strThirdOp, strFourthOp)

    # new an instance of a Calculator then start it
    cal = Calculator(nInitValue, nFirstOperand, nSecondOperand, nThirdOperand, nFourthOperand, strFirstOp, strSecondOp, strThirdOp, strFourthOp)
    cal.mainloop()
