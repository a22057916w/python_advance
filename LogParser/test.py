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
import codecs
import time

# [Main]
g_strVersion = "3.0.0.1"

#[ParseLogPath]
g_strLogDir = "./TryingLog"

def getDateTimeFormat():
    strDateTime = "[%s]" % (time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))
    return strDateTime

def printLog(strPrintLine):
    strFileName = os.path.basename(__file__).split('.')[0]
    strLogPath = strFileName + ".log"
    fileLog = codecs.open(strLogPath, 'a', "utf-8")
    print(strPrintLine)
    fileLog.write("%s%s\r\n" % (getDateTimeFormat(), strPrintLine))
    fileLog.close()


# ----------- read and parse target log ----------
def parseLog(strSNDLog):
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
    except Exception as e:
        printLog("[E][parseLog] Unexpected Error: " + str(e))
    return listLTE, listZigbee

def parseLTE(strLTEPath):
    dictLTE = {
        "dBm_CH9750" : None,
        "dBm_CH2787" : None,
        "dBm_2G_CH124" : None,
        "Current_mA_3G_CH9750" : None,
        "Current_mA_3G_CH2787" : None,
        "Current_mA_2G_CH124" : None,
        "dBm_CH124" : None }

    nPowerCase = 1
    nCurrentCase = 1
    with open(strLTEPath, encoding='big5') as log:  # big5 for windows
        content = log.readlines()
        for line in content:
            #strPower = "-1e9"
            #strCurrent = "-1e9"

            if "Power: " in line:
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

            if "Current: " in line:
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

            if "Rx RSSI: " in line:
                # get the figure of the line "Rx RSSI: -15 dBm\n"
                strRSSI = line.split(": ")[1].strip(" dbm\n")
                dictLTE["dBm_CH124"] = strRSSI
                break
    return(dictLTE)

def parseZigbee(strZigBeePath):
    dictZigbee ={
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

                if re.search("Power: [0-9]*\.[0-9]* dBm", line) != None:
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

                if "Current: " in line:
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

                if "Rx RSSI: " in line:
                    # get the figure of the line "Rx RSSI: -15 dBm\n"
                    strRSSI = line.split(": ")[1].strip(" dBm\n")
                    if nLNACase == 1:
                        dictZigbee["dBm_LNA_ON"] = strRSSI
                    elif nLNACase == 2:
                        dictZigbee["dBm_LNA_Off"] = strRSSI
                        break
                    nLNACase += 1

    except Exception as e:
        print(str(e))

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

    print(dfLogInfo)

def readINI(strKey):
        try:
            config = configparser.ConfigParser()
            config.read(g_strINIPath)
            strMethod = 'Method%s' % g_nMethodIndex

            printLog("[I][readINI] ---------- INI ----------")
            Power_dBm_CH15 = 100,0
            Power_dBm_CH21 = 100,0
            Power_dBm_CH24 = 100,0
            dBm_LNA_ON = 100,-100
            dBm_LNA_Off = 100,-100
            Current_mA_CH15 = 1000,0
            Current_mA_CH21 = 1000,0
            Current_mA_CH24 = 1000,0
            dBm_CH9750 = 100,0
            dBm_CH2787 = 100,0
            dBm_2G_CH124 = 100,0
            Current_mA_3G_CH9750 = 1000,0
            Current_mA_3G_CH2787 = 1000,0
            Current_mA_2G_CH124 = 1000,0
            dBm_CH124 = 100,-100


            strValue = config.get(strMethod, strKey)
            printLog("[I][readINI] %s = %s" % (strKey, strValue))

            dict["Power_dBm_CH21"] = config.get(strMethod, 'Power_dBm_CH21')
            printLog("[I][readINI] Power_dBm_CH21 = %s" % dict["Power_dBm_CH21"])

            dict["Power_dBm_CH24"] = config.get(strMethod, 'Power_dBm_CH24')
            printLog("[I][readINI] Power_dBm_CH24 = %s" % dict["Power_dBm_CH24"])

            dict["dBm_LNA_ON"] = config.get(strMethod, 'dBm_LNA_ON')
            printLog("[I][readINI] dBm_LNA_ON = %s" % dict["dBm_LNA_ON"])

            dict["dBm_LNA_Off"] = config.get(strMethod, 'dBm_LNA_Off')
            printLog("[I][readINI] dBm_LNA_Off = %s" % dict["dBm_LNA_Off"])

            dict["Current_mA_CH15"] = config.get(strMethod, 'Current_mA_CH15')
            printLog("[I][readINI] Current_mA_CH15 = %s" % dict["Current_mA_CH15"])

            dict["Current_mA_CH21"] = config.get(strMethod, 'Current_mA_CH21')
            printLog("[I][readINI] Current_mA_CH21 = %s" % dict["Current_mA_CH21"])

            dict["Current_mA_CH24"] = config.get(strMethod, 'Current_mA_CH24')
            printLog("[I][readINI] Current_mA_CH24 = %s" % dict["Current_mA_CH24"])

            dict["dBm_CH9750"] = config.get(strMethod, 'dBm_CH9750')
            printLog("[I][readINI] dBm_CH9750 = %s" % dict["dBm_CH9750"])

            dict["dBm_CH2787"] = config.get(strMethod, 'dBm_CH2787')
            printLog("[I][readINI] dBm_CH2787 = %s" % dict["dBm_CH2787"])

            dict["dBm_2G_CH124"] = config.get(strMethod, 'dBm_2G_CH124')
            printLog("[I][readINI] dBm_2G_CH124 = %s" % dict["dBm_2G_CH124"])

            dict["Current_mA_3G_CH9750"] = config.get(strMethod, 'Current_mA_3G_CH9750')
            printLog("[I][readINI] Current_mA_3G_CH9750 = %s" % dict["Current_mA_3G_CH9750"])

            dict["Current_mA_3G_CH2787"] = config.get(strMethod, 'Current_mA_3G_CH2787')
            printLog("[I][readINI] Current_mA_3G_CH2787 = %s" % dict["Current_mA_3G_CH2787"])

            dict["Current_mA_2G_CH124"] = config.get(strMethod, 'Current_mA_2G_CH124')
            printLog("[I][readINI] Current_mA_2G_CH124 = %s" % dict["Current_mA_2G_CH124"])

            dict["dBm_CH124"] = config.get(strMethod, 'dBm_CH124')
            printLog("[I][readINI] dBm_CH124 = %s" % dict["dBm_CH124"])

            printLog("[I][readINI] ---------- INI ----------")
            return True
        except Exception as e:
            printLog("[E][readINI] Error: %s" % str(e))
            self.strFailReasonTemp = "Read INI error: %s" % str(e)
            return False

if __name__ == "__main__":
    printLog("----------- Start Parsing Log ----------")
    listLTE, listZigbee = [], []
    # ------------ find the target file --------------
    try:
        # get file names of TryingLog (first layer)
        listSNLogs = os.listdir(g_strLogDir)
        listLTE, listZigbee = parseLog(listSNLogs)


        print(listLTE)

        save(listLTE, listZigbee)
    except Exception as e:
        print(e)
