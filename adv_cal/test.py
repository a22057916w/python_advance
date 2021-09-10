import os
from time import strftime, localtime

def printLog(strLogMsg):
    print(strLogMsg)
    fileLog = open("./log.log", 'a')
    fileLog.write("[%s]%s\n" % (getDateTimeFormat(), strLogMsg))
    fileLog.close()

def getDateTimeFormat():
    strDateTime = "%s" % (strftime("%Y/%m/%d %H:%M:%S", localtime()))
    return strDateTime


printLog("[E][readINI] Read INI fail!!!")
