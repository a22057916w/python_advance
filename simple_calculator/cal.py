from configparser import ConfigParser
import os

# global var for .ini file info
nInitValue = 0
nFirstOperand = 0
nSecondOperand = 0
nThirdOperand = 0
nFourthOperand = 0
pass

# read section "Setting" in .ini file
def read_ini_setting(section):
    try:
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

if __name__ == '__main__':
    strAbsPath = os.path.abspath(__file__)
    strFileDir = os.path.dirname(strAbsPath)

    strSettingPath = os.path.join(strFileDir, 'Setting.ini')    # Setting.ini

    with open(strSettingPath) as iniFile:
        config = ConfigParser()
        config.read_file(iniFile)
        #print(config["Setting"].getint("firstOperator"))
        read_ini_setting(config["Setting"])
