##! python3
##==============================================================================
##    Copyright (c) 2021 COMPAL Electronic Inc. All rights reserved.
##    This program contains proprietary and confidential information.
##    All rights reserved except as may be permitted by prior written consent.
##
##    Compal STiD NPSD Test Program Release Notification.
##
##    ModuleName:
##            FFA60Audio.py
##
##    Abstract:
##            Test audio(Mic) reacording with sox.exe and tool(dtmf_test)
##            provided by client
##
##    Author:
##            30-Sep-2021 Willy Chen
##
##    Revision History:
##            Rev 1.0.0.1 30-Sep-2021 Willy
##                    First create.
##==============================================================================
import re
import os
import pandas as pd

# [Main]
g_strVersion = "3.0.0.1"

#[LogPath]
g_LogDir = "./TryingLog"


def getDateTimeFormat():
    strDateTime = "[%s]" % (time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))
    return strDateTime

def printLog(strPrintLine):
    strFileName = os.path.basename(__file__).split('.')[0]
    fileLog = codecs.open(g_strLogPath, 'a', "utf-8")
    print(strPrintLine)
    fileLog.write("%s%s\r\n" % (getDateTimeFormat(), strPrintLine))
    fileLog.close()

def readLog():
    # ------------ find the target file --------------
    try:
        # first layer
        listSNLogs = os.listdir(g_LogDir)
        #print(listSNLogs)
        for strSNLogDir in listSNLogs:
            #dictLogInfo["SN"] = strSNLogDir.split("_")[0]
            strLogPath = os.path.join(g_LogDir, strSNLogDir)
            print(strLogPath)
            # second layer
            for strLog in os.listdir(strLogPath):
                #print(strLog)

                strLog = os.path.join(strLogPath, strLog)
                reMatch = re.fullmatch("^.*RF_LTE\.log", strLog, re.I)  #!
                #strLTELog = os.path.join(SNLogPath, strLog)
                if(reMatch != None):
                    print(strLog)
                    #parseLTE(strLTELog, dictLogInfo)
                    break
                else:
                    pass
                #print("____________")

            break
    except Exception as e:
        print(e)

# ----------- read and parse target log--------
def parseLTE(strLTELog, dictLogInfo):
    #print("SDfsdfsdf")
    dictLTELogInfo = {
        "dBm_CH9750" : None,
        "dBm_CH2787" : None,
        "dBm_2G_CH124" : None,
        "Current_mA_3G_CH9750" : None,
        "Current_mA_3G_CH2787" : None,
        "Current_mA_2G_CH124" : None,
        "dBm_CH124" : None }

    listLTElogs = []
    with open(strLTELog) as logFile:
        blocks = re.split('\-* LTE_[2|3]G Freq.*\-*' ,logFile.read())

        # idx 2-> CH2787, idx 3->CH9750, idx 4-> CH124, idx 5-> dBm_Ch124
        for i in range (0, 1):
            #print(blocks[i].split('\n'))
            str_dBm = None
            strCurrent = None
            #print(type(blocks[2]))
            lines = blocks[2].split("\n")
            """
            for line in blocks.split('\r\n'):
                #print(line)
                if "Power" in line:
                    #print(line)
                    str_dBm = line.split(": ")[-1]
                    #print(str_dBm)
                    break
            """

if __name__ == "__main__":
    readLog()
