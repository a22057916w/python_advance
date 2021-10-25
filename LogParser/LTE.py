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

if __name__ == "__main__":
