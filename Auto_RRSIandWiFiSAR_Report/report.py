##! python3
##==============================================================================
##    Copyright (c) 2021 COMPAL Electronic Inc. All rights reserved.
##    This program contains proprietary and confidential information.
##    All rights reserved except as may be permitted by prior written consent.
##
##    Compal STiD NPSD Test Program Release Notification.
##
##    ModuleName:
##            report.py
##
##    Abstract:
##
##
##    Author:
##            22-Nov-2021 Willy Chen
##
##    Revision History:
##            Rev 1.0.0.1 22-Nov-2021 Willy
##                    First create.
##==============================================================================
import os, sys
import traceback
import shutil
import socket
import requests
import pandas as pd
import openpyxl as opxl
from openpyxl.styles import PatternFill, Alignment, Font
from openpyxl.styles.borders import Border, Side
import re
import time, logging

# [Main]
g_strVersion = "1.0.0.1"

#[ParseLogPath]
g_strLogDir = "./ALL_SN/"

#[Webside progress bar]
g_nProgressC = 0

g_ShareFolder_ip = ""


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


# Update UI Process (%)
def updateWebpageInfo(nProgress=g_nProgressC, strWebpageInfo=None):
    global g_nProgressC
    strWebComPath = os.path.join(logPath, "WebComunicate_%s.txt" % strUser)
    if nProgress != g_nProgressC:
        g_nProgressC = nProgress

    if nProgress == 0:
        ## Renew WebComunicate.txt
        with open(strWebComPath, 'w') as f:
            f.write('')
    else:
        strToWrite = "%s;%s" % (nProgress, strWebpageInfo)
        with open(strWebComPath, 'w') as f:
            f.write(strToWrite)


def getDateTimeFormat():
    strDateTime = "%s" % (time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
    return strDateTime

#/====================================================================\#
#|               Functions of parsing target logs                     |#
#\====================================================================/#

def parseLog(list_SNs):

    listRSSI, listWIFI = [], []

    try:
        for strSN in list_SNs:
            strRSSI_Intel, strRSSI_MTK = "ITPM_RSSITest_A32.LOG", "MTKlog_" + strSN + ".LOG"  # e.g. MTKlog_7228979800008.LOG
            strWIFI = "SarLog_DynAnt.txt"

            # for RSSI excel columns and WIFI's
            dictRSSI = {
                "UNIT PN" : strSN,
                "Test Result" : None,
                "Main" : None,
                "Aux" : None,
                "Spec" : None }
            dictWIFI = {
                "UNIT PN" : strSN,
                "Result" : "no log" }

            b_hasRSSI, b_hasWIFI = False, False             # flag for checking if the target log exists
            strSNPath = os.path.join(g_strLogDir, strSN)    # set abspath for SN logs

            # iterate through log files in a SN folder
            for strFileName in os.listdir(strSNPath):
                strLogPath = os.path.join(strSNPath, strFileName)
                """
                # check if ITPM_RSSITest_A32.log exists. If not, flag = False and parse only SN.
                if strFileName == strRSSI_Intel:
                    parseRSSI_Intel(dictRSSI, strLogPath)
                    b_hasRSSI = True

                # if MTKlog_7228979800008.LOG exists, parse the log
                if strFileName == strRSSI_MTK:
                    parseRSSI_MTK(dictRSSI, strLogPath)
                    b_hasRSSI = True
                """
                if strFileName == strWIFI:
                    parseWIFI(dictWIFI, strLogPath)
                    b_hasWIFI = True

            # if log not exists, append initial dict
            listRSSI.append(dictRSSI)
            listWIFI.append(dictWIFI)



    except Exception as e:
        print("[E][parseLog] Unexpected Error: " + str(e))


def parseRSSI_Intel(dictRSSI, strRSSIPath):
    print("[I][parseRSSI_Intel] Parse RSSI-MTK log: %s" % strRSSIPath.replace(g_strLogDir, ""))
    try:
        with open(strRSSIPath, encoding="big5") as RSSILog:    # big5 for windows
            content = RSSILog.readlines()
            for line in content:

                # if the first line is PASS or FAIL, save to dict
                if content.index(line) == 0 and ("PASS" in line or "FAIL" in line):
                    dictRSSI["Test Result"] = line.strip("\n")

                if 'CODE NO="010001A0"' in line:
                    # line return <CODE NO="010001A0" KEYNAME="RSSI" VALUE1="-65" VALUE2="-63" ...
                    list_Info = line.split(" ")

                    # get VALUE1 figure
                    strSpec = list_Info[3].split("=")[1].strip('"')
                    dictRSSI["Spec"] = strSpec

                    # get VALUE2 figure
                    strMain = list_Info[4].split("=")[1].strip('"')
                    dictRSSI["Main"] = strMain

                if 'CODE NO="01000120"' in line:
                    # line return <CODE NO="01000120" KEYNAME="RSSI" VALUE1="-65" VALUE2="-62" ...
                    list_Info = line.split(" ")

                    strAux = list_Info = list_Info[4].split("=")[1].strip('"')
                    dictRSSI["Aux"] = strAux
    except Exception as e:
        print("[E][parseRSSI_Intel] Unexpected Error: " + str(e))


def parseRSSI_MTK(dictRSSI, strRSSIPath):
    print("[I][parseRSSI_MTK] Parse RSSI-MTK log: %s" % strRSSIPath.replace(g_strLogDir, ""))
    try:
        with open(strRSSIPath, encoding="big5") as RSSILog:    # big5 for windows
            content = RSSILog.readlines()
            for line in content:

                if "== ANT1 (sub) ==" in line:
                    idx = content.index(line)       # get the line index of keyword
                    for line in content[idx:]:
                        if "Threshold" in line:
                            dictRSSI["Spec"] = line.split(": ")[1].strip("\n")
                        if "Average" in line:
                            dictRSSI["Main"] = line.split(": ")[1].strip("\n")
                if "== ANT2 (main) ==" in line:
                    dx = content.index(line)       # get the line index of keyword
                    for line in content[idx:]:
                        if "Average" in line:
                            dictRSSI["Aux"] = line.split(": ")[1].strip("\n")
                        if "PASS" in line or "FAIL" in line:
                            dictRSSI["Test Result"] = line.strip("\n")

    except Exception as e:
        print("[E][parseRSSI] Unexpected Error: " + str(e))

def parseWIFI(dictWIFI, strWIFIPath):
    print("[I][parseWIFI] Parse RSSI-MTK log: %s" % strWIFIPath.replace(g_strLogDir, ""))
    try:
        with open(strWIFIPath, encoding="big5") as WIFILog:    # big5 for windows
            content = WIFILog.readlines()
            print(content[-1])
            

    except Exception as e:
        print("[E][parseWIFI] Unexpected Error: " + str(e))


if __name__ == "__main__":

    # ------------ find the target file --------------
    try:
        # get directory names of TryingLog (first layer)
        listSNLogs = os.listdir(g_strLogDir)
        # iterate through log files in a SN folder (second layer)
        parseLog(listSNLogs)


    except Exception as e:
        print("[E][main] Unexpected Error: " + str(e))
