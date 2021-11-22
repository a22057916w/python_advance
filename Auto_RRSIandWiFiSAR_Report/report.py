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



if __name__ == "__main__":

    global strUser
    global logPath
    global bLocalDebug
    bLocalDebug = True


    """
    if bResult:
        shutil.copy2(strFileName, ResultPath)
        updateWebpageInfo(100, "[I] F I N I S H.")

    else:
        updateWebpageInfo(1, "[E] Process Fail.")
    """

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
