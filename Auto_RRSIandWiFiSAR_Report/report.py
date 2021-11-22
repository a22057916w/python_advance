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


def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)-5s][%(lineno)-4d][%(funcName)s] %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
    fh.setFormatter(formatter)

    # define a Handler which writes INFO messages or higher to the sys.stderr
    ch = logging.StreamHandler(sys.stdout)
    # ch = logging.StreamHandler()
    ch.setLevel(logging.CRITICAL)

    # set a format which is simpler for console use
    formatter = logging.Formatter('%(levelname)-5s - %(lineno)-4d - %(funcName)s : %(message)s')
    # tell the handler to use this format
    ch.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
