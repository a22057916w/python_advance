from configparser import ConfigParser
import tkinter as tk
import os

# global var for .ini file info
nInitValue = 0
nFirstOperand = 0
nSecondOperand = 0
nThirdOperand = 0
nFourthOperand = 0
pass

# global var for cal_UI
expression = ""

# read section "Setting" in .ini file
def read_ini_section(section):
    try:
        global nInitValue, nFirstOperand, nSecondOperand, nThirdOperand, nFourthOperand

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
    except Exception as e:
        print(e)


def operation(strOperator, nOperand):
    nTmp = eval(strResult.get())
    print(nTmp)
    if strOperator == "+":
        nTmp += nOperand
    elif strOperator == "-":
        nTmp -= nOperand
    elif strOperator == "*":
        nTmp *= nOperand

    # need to deal overflow

    strResult.set(str(nTmp))

# create calculator GUI
def cal_UI(nInitValue, nFirstOperand, nSecondOperand, nThirdOperand, nFourthOperand):
    global strResult

    window = tk.Tk()
    window.title("Simple Calculator")
    window.geometry("600x800")

    strResult = tk.StringVar()
    strResult.set(str(nInitValue))
    print(type(strResult))

    lbResult = tk.Label(window, textvariable=strResult)
    lbResult.pack()

    # -------- button setup ---------
    btnFirst = tk.Button(window, width=20, text=str(nFirstOperand), command=operation("+", nFirstOperand))
    btnFirst.pack(side="left")

    btnSecond = tk.Button(window, width=20, text=str(nSecondOperand), command=operation("-", nSecondOperand))
    btnSecond.pack(side="right")

    btnThird = tk.Button(window, width=20, text=str(nThirdOperand), command=operation("+", nThirdOperand))
    btnThird.pack(side="left")

    btnFourth = tk.Button(window, width=20, text=str(nFourthOperand), command=operation("*", nFourthOperand))
    btnFourth.pack(side="right")

    window.mainloop()

if __name__ == '__main__':
    strAbsPath = os.path.abspath(__file__)
    strFileDir = os.path.dirname(strAbsPath)

    strSettingPath = os.path.join(strFileDir, 'Setting.ini')    # Setting.ini

    # open Setting.ini then assign values to global vars
    with open(strSettingPath) as iniFile:
        config = ConfigParser()
        config.read_file(iniFile)
        read_ini_section(config["Setting"])

    print(nInitValue, nFirstOperand, nSecondOperand, nThirdOperand, nFourthOperand)

    # 將 StringVar 變數與 Tkinter 控制元件關聯後，修改 StringVar 變數後，Tkinter 將自動更新此控制元件


    cal_UI(nInitValue, nFirstOperand, nSecondOperand, nThirdOperand, nFourthOperand)
