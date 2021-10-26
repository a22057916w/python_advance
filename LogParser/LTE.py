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
import sys
import pandas as pd
import codecs
import time

# [Main]
g_strVersion = "3.0.0.1"

#[ParseLogPath]
g_strLogDir = "./TryingLog"


# ----------- read and parse target log ----------
def parseLog(strSNDLog):
    printLog("[I][parseLog] ------- Start Parsing Log -------")

    listLTE, listZigbee = [], []
    try:
        for strSNDir in listSNLogs:
            strSNLog = os.path.join(g_strLogDir, strSNDir)

            # iterate through log files in a SN folder (second layer)
            for strLog in os.listdir(strSNLog):
                strLog = os.path.join(strSNLog, strLog)

                # parse GFI20_RF_LTE.log files
                reMatch = re.fullmatch("^.*RF_LTE\.log", strLog)
                if(reMatch != None):
                    dictLTE = parseLTE(strLog)
                    dictLTE.update({"SN" : strSNDir})   # update() for concat two dicts
                    listLTE.append(dictLTE)

                # parse GFI20_RF_Zigbee.log files
                reMatch = re.fullmatch("^.*RF_Zigbee\.log", strLog)
                if(reMatch != None):
                    dictZigbee = parseZigbee(strLog)
                    dictZigbee.update({"SN" : strSNDir})
                    listZigbee.append(dictZigbee)
        printLog("[I][parseLog] ------- Finish Parsing Log -------")
    except Exception as e:
        printLog("[E][parseLog] Unexpected Error: " + str(e))
    return listLTE, listZigbee

def parseLTE(strLTEPath):
    printLog("[I][parseLTE] Parse LTE log: %s" % strLTEPath)

    dictLTE = {
        "dBm_CH9750" : None,
        "dBm_CH2787" : None,
        "dBm_2G_CH124" : None,
        "Current_mA_3G_CH9750" : None,
        "Current_mA_3G_CH2787" : None,
        "Current_mA_2G_CH124" : None,
        "dBm_CH124" : None }
    try:
        nPowerCase, nCurrentCase = 1, 1
        with open(strLTEPath, encoding='big5') as log:  # big5 for windows
            content = log.readlines()
            for line in content:
                #strPower = "-1e9"
                #strCurrent = "-1e9"

                if re.search("Power: [+-]?[0-9]*\.?[0-9]*", line) != None:
                    # get the figure of the line "Power: 31.718\n"
                    strPower = line.split(": ")[1].strip(" \n")
                    #print(strPower)
                    if nPowerCase == 1:
                        dictLTE["dBm_CH2787"] = strPower
                    elif nPowerCase == 2:
                        dictLTE["dBm_CH9750"] = strPower
                    elif nPowerCase == 3:
                        dictLTE["dBm_2G_CH124"] = strPower
                    nPowerCase += 1

                if re.search("Current: [+-]?[0-9]*\.?[0-9]* A", line) != None:
                    # get the figure of the line "Current: 0.246 A\n"
                    strCurrent = line.split(": ")[1].strip(" A\n")
                    #print(strCurrent)
                    if nCurrentCase == 1:
                        dictLTE["Current_mA_3G_CH2787"] = str(eval(strCurrent) * 1000)
                    elif nCurrentCase == 2:
                        dictLTE["Current_mA_3G_CH9750"] = str(eval(strCurrent) * 1000)
                    elif nCurrentCase == 3:
                        dictLTE["Current_mA_2G_CH124"] = str(eval(strCurrent) * 1000)
                    nCurrentCase += 1

                if re.search("Rx RSSI: [+-]?[0-9]*\.?[0-9]* dBm", line) != None:
                    # get the figure of the line "Rx RSSI: -15 dBm\n"
                    print(line)
                    strRSSI = line.split(": ")[1].strip(" dBm\n")
                    dictLTE["dBm_CH124"] = strRSSI
                    break
    except Exception as e:
        printLog("[E][parseLTE] Unexpected Error: " + str(e))
    return(dictLTE)

def parseZigbee(strZigBeePath):
    printLog("[I][parseZigbee] Parse Zigbee log: %s" % strZigBeePath)

    dictZigbee = {
        "Power_dBm_CH15" : None,
        "Power_dBm_CH21" : None,
        "Power_dBm_CH24" : None,
        "dBm_LNA_ON" : None,
        "dBm_LNA_Off" : None,
        "Current_mA_CH15" : None,
        "Current_mA_CH21" : None,
        "Current_mA_CH24" : None }
    try:
        nPowerCase , nCurrentCase, nLNACase = 1, 1, 1
        with open(strZigBeePath, encoding="big5") as Zigbee:    # big5 for windows
            content = Zigbee.readlines()
            for line in content:
                #strPower = "-1e9"
                #strCurrent = "-1e9"

                if re.search("Power: [+-]?[0-9]*\.?[0-9]* dBm", line) != None:
                    # get the figure of the line "Power: 8.817 dBm\n"
                    strPower = line.split(": ")[1].strip(" dBm\n")
                    #print(strPower)
                    if nPowerCase == 1:
                        dictZigbee["Power_dBm_CH15"] = strPower
                    elif nPowerCase == 2:
                        dictZigbee["Power_dBm_CH21"] = strPower
                    elif nPowerCase == 3:
                        dictZigbee["Power_dBm_CH24"] = strPower
                    nPowerCase += 1

                if re.search("Current: [+-]?[0-9]*\.?[0-9]* A", line) != None:
                    # get the figure of the line "Current: 0.081 A\n"
                    strCurrent = line.split(": ")[1].strip(" A\n")
                    #print(strCurrent)
                    if nCurrentCase == 1:
                        dictZigbee["Current_mA_CH15"] = str(eval(strCurrent) * 1000)
                    elif nCurrentCase == 2:
                        dictZigbee["Current_mA_CH21"] = str(eval(strCurrent) * 1000)
                    elif nCurrentCase == 3:
                        dictZigbee["Current_mA_CH24"] = str(eval(strCurrent) * 1000)
                    nCurrentCase += 1

                if re.search("Rx RSSI: [+-]?[0-9]*\.?[0-9]* dBm", line) != None:
                    # get the figure of the line "Rx RSSI: -15 dBm\n"
                    strRSSI = line.split(": ")[1].strip(" dBm\n")
                    if nLNACase == 1:
                        dictZigbee["dBm_LNA_ON"] = strRSSI
                    elif nLNACase == 2:
                        dictZigbee["dBm_LNA_Off"] = strRSSI
                        break
                    nLNACase += 1

    except Exception as e:
        printLog("[E][parseZigbee] Unexpected Error: " + str(e))
    return(dictZigbee)

def save(listLTE, listZigbee):
    # listLTE and listZigbee both has same length
    listInfo = [None] * len(listLTE)
    #print(listLTE)
    for i in range (0, len(listLTE)):
        listLTE[i].update(listZigbee[i])
        listInfo[i] = listLTE[i]
    dfLogInfo = pd.DataFrame(listInfo)

    writer = pd.ExcelWriter("test.xlsx", engine='xlsxwriter')
    dfLogInfo.to_excel(writer)
    writer.save()

    #print(dfLogInfo)

def mergeLogs(listLTE, listZigbee):
    try:
        printLog("[I][mergeLogs] ------- Merging two Log data -------")
        # listLTE and listZigbee both has same length
        listInfo = [None] * len(listLTE)
        for i in range (0, len(listLTE)):
            listLTE[i].update(listZigbee[i])
            listInfo[i] = listLTE[i]
        printLog("[I][mergeLogs] ------- Merged two Log data -------")
        return listInfo
    except Exception as e:
        printLog("[E][mergeLogs] Unexpected Error: " + str(e))
        return None

# ------------------ print log functions ----------------------

def getDateTimeFormat():
    strDateTime = "[%s]" % (time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))
    return strDateTime

def printLog(strPrintLine):
    strFileName = os.path.basename(__file__).split('.')[0]
    fileLog = codecs.open(g_strFileName + ".log", 'a', "utf-8")
    print(strPrintLine)
    fileLog.write("%s%s\r\n" % (getDateTimeFormat(), strPrintLine))
    fileLog.close()


if __name__ == "__main__":
    global g_strFileName    # log file of the program
    g_strFileName = os.path.basename(__file__).split('.')[0]

    printLog("========== Start ==========")
    printLog("[I][main] Python " + sys.version)
    printLog("[I][main] %s.py %s" % (g_strFileName, g_strVersion))

    listLTE, listZigbee = [], []
    # ------------ find the target file --------------
    try:
        # get directory names of TryingLog (first layer)
        listSNLogs = os.listdir(g_strLogDir)
        # iterate through log files in a SN folder (second layer)
        listLTE, listZigbee = parseLog(listSNLogs)
        # merge data from two different log files
        listInfo = mergeLogs(listLTE, listZigbee)



        save(listLTE, listZigbee)

    except Exception as e:
        printLog("[E][main] Unexpected Error: " + str(e))
    printLog("========== End ==========")
