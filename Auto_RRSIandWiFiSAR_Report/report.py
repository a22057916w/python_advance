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
g_strVersion = "1.0.0.2"

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



if __name__ == "__main__":

    global strUser
    global logPath
    global bLocalDebug
    bLocalDebug = True

    timeStartTime = time.time()


    if not bLocalDebug:

        argv = sys.argv
        strUser = argv[1]
        logPath = "/home/sanchez/Desktop/RDTool/CTO_R1R3_Checking"

        R1R3 = R1R3()
        R1R3.module_logger.info("User = %s" % (strUser))

        # Server upload path
        SourcePath = "/home/sanchez/Desktop/webserver/ToolPage/server/php/files/ToolPage/CTO_R1R3_Checking/%s" % strUser

        # InputFolder
        InputFolder = "/home/sanchez/Desktop/RDTool/CTO_R1R3_Checking/input_%s" % strUser

        # Output file in download folder
        ResultPath = "/home/sanchez/Desktop/webserver/ToolPage/Download/CTO_R1R3_Checking_%s.xlsx" % strUser

        # Output Path
        strOutputPath = "/home/sanchez/Desktop/RDTool/CTO_R1R3_Checking/output_%s" % strUser
        strFileName = strOutputPath + "/CTO_R1R3_Checking_%s.xlsx" % strUser

    else:
        # Local Path
        strUser = "Blake_Ma"
        logPath = os.getcwd()
        R1R3 = R1R3()
        SourcePath = os.path.join(os.getcwd(), "ServerPath")
        InputFolder = os.path.join(os.getcwd(), "input_%s" % strUser)
        ResultPath = os.path.join(os.getcwd(), "ServerDownload", "CTO_R1R3_Checking_%s.xlsx" % strUser)
        strOutputPath = os.path.join(os.getcwd(), "output_%s" % strUser)
        strFileName = os.path.join(strOutputPath, "CTO_R1R3_Checking_%s.xlsx" % strUser)

    #check file exist !

    # Test Flow
    R1R3.module_logger.info("======= START Process =======")


    list_process = ["R1R3.set_input_path(SourcePath, InputFolder)",
                    "R1R3.set_output_path(strOutputPath)",
                    "R1R3.set_dataframes()",
                    "R1R3.filter_Items()",
                    "R1R3.compare_Category()",
                    "R1R3.get_Category_dict_result()",
                    "R1R3.compare_Others()",
                    "R1R3.write_pandas()",
                    "R1R3.write_opxl()"]


    for pc in list_process:
        bResult = eval(pc)
        if not bResult:
            R1R3.module_logger.info("Fail :%s"%pc)
            break
            # print(pc,"Fail")

    # print(bResult)
    R1R3.module_logger.info("======= END Process =======")

    if bResult:
        shutil.copy2(strFileName, ResultPath)
        updateWebpageInfo(100, "[I] F I N I S H.")

    else:
        updateWebpageInfo(1, "[E] Process Fail.")


    # LYUR Update Record
    try:
        nSpendTime = int(time.time() - timeStartTime)
        R1R3.module_logger.info("[I][main] Spend Time: %d s" % (nSpendTime))

        hostname = socket.gethostname()
        IPAddr = get_host_ip()
        strDate = "%s" % (time.strftime("%Y-%m-%d", time.localtime()))
        strTime = "%s" % (time.strftime("%H:%M:%S", time.localtime()))
        data = {'pcip': IPAddr, 'pcname': hostname, 'account': strUser, 'toolid': 'Prj2011_SPT_CTOBOM_R1R3',
                'rundate': strDate, 'runtime': strTime, 'executiontime': nSpendTime,
                'note': 'version: %s' % (strVersion), 'cycle': 1, 'sbtn': 'Send'}
        response = requests.post('http://10.110.140.43/LYUR/logYourUsageRecord.php', data)
        R1R3.module_logger.info("[I][RunProgress] Posting to LYUR success.")


    except:
        R1R3.module_logger.warning("[W][RunProgress] Posting to LYUR failed.")
        R1R3.module_logger.error("[E][main] Unexpected error: %s" % (str(traceback.format_exc())))
        R1R3.module_logger.error("[E][main] Unexpected error: %s" % (str(sys.exc_info())))
