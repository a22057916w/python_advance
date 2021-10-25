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
import os
import re
import sys
import time
import threading
import win32service
import win32serviceutil
import win32event
import win32wnet
import win32api
import win32con
import win32gui
import win32ui
import win32console
import win32process
import configparser
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from enum import IntEnum
from pyadb import ADB
import subprocess
import psutil
import random
import codecs
import traceback
import shutil       # for delete dir, standard lib

# [Main]
g_strVersion = "3.0.0.1"

# Process Event
class CONNECTTYPE(IntEnum):
    NONE = 0
    USBADB = 1              # adb shell via cable line (USB)
    WIRELESSADB = 2         # adb shell via wirelsee tool (Wifi)
    COM = 3                 # USB
    SSH = 4
    PERL = 5

#/====================================================================\#
#|                               Class                                |#
#\====================================================================/#

class cTestScriptUI(QDialog):       # QDialog is inheretented from QtWidgets
    signal_parent = pyqtSignal(str)

    def signal_from_parent(self, string):
        print("[TestScriptUI] get msg from parent : %s" % string)
        if string == 'END':
            self.closeUI.emit()

    def __init__(self, dictTestStatus, parent=None):
        super(cTestScriptUI, self).__init__(parent)
        self.dictTestStatus = dictTestStatus
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.centralLayout = QtWidgets.QGridLayout()
        self.centralLayout.setSpacing(3)
        self.centralLayoutButton = QtWidgets.QGridLayout()
        self.centralLayoutButton.setSpacing(3)
        self.centralLayoutChooseButton = QtWidgets.QGridLayout()
        self.centralLayoutChooseButton.setSpacing(3)
        self.labelTitle = QtWidgets.QLabel("")
        self.labelTitle.setFont(font)
        self.labelTitle.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.labelTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.btnStart = QtWidgets.QPushButton()
        self.btnStart.setText("Start")
        self.btnStart.setFont(font)
        self.btnStart.hide()
        self.btnPass = QtWidgets.QPushButton()
        self.btnPass.setStyleSheet('QPushButton {color: green}')
        self.btnPass.setText("Pass")
        self.btnPass.setFont(font)
        self.btnRetry = QtWidgets.QPushButton()
        self.btnRetry.setText("Retry")
        self.btnRetry.setFont(font)
        self.btnRetry.hide()
        self.btnOK = QtWidgets.QPushButton()
        self.btnOK.setText("OK")
        self.btnOK.setFont(font)
        self.btnOK.hide()
        self.btnFail = QtWidgets.QPushButton()
        self.btnFail.setStyleSheet('QPushButton {color: red}')
        self.btnFail.setText("Fail")
        self.btnFail.setFont(font)

        self.VoicePlayer = QtMultimedia.QMediaPlayer()      # for playing wav

        self.btnOK.clicked.connect(self.finishTest)
        self.centralLayout.addWidget(self.labelTitle, 0, 0)
        self.centralLayoutButton.addWidget(self.btnPass, 0, 0)
        self.centralLayoutButton.addWidget(self.btnStart, 0, 1)
        self.centralLayoutButton.addWidget(self.btnOK, 0, 1)
        self.centralLayoutButton.addWidget(self.btnRetry, 0, 1)
        self.centralLayoutButton.addWidget(self.btnFail, 0, 2)
        self.centralLayout.addLayout(self.centralLayoutChooseButton, 1, 0)
        self.centralLayout.addLayout(self.centralLayoutButton, 2, 0)
        self.setLayout(self.centralLayout)

        self.nShelfCount = dictTestStatus['ShelfCount']
        self.nMDUTNum = dictTestStatus['MDUTNum']
        if dictTestStatus['SN'] == "No_SN":
            self.strSN = "%s%d" %(dictTestStatus['SN'], self.nMDUTNum)
        else:
            self.strSN = dictTestStatus['SN']
        self.nMethodIndex = dictTestStatus['MethodIndex']

        self.tTestScriptThread = TestScriptThread(self, self.dictTestStatus)
        self.tTestScriptThread.showMsg.connect(self.showMsg)        # connect signal slot showMsg to method self.showMsg
        self.tTestScriptThread.controlUI.connect(self.controlUI)
        self.tTestScriptThread.closeUI.connect(self.closeUI)
        self.tTestScriptThread.playSound.connect(self.playSound)
        self.tTestScriptThread.stopSound.connect(self.stopSound)
        self.tTestScriptThread.start()

    # remove bShowChooseBth and its implementation
    def controlUI(self, strLabelTitle, bShowStartBtn, bShowChooseBtn, bShowPassBtn, bShowOKBtn, bShowRetryBtn, bShowFailBtn):
        self.emptyUI()
        # Text Title
        if (strLabelTitle is not None):
            font = QtGui.QFont()
            font.setFamily("Arial")
            if (strLabelTitle == "PASS"):
                font.setPointSize(40)
                self.labelTitle.setFont(font)
                self.labelTitle.setStyleSheet('QLabel {color: green}')
            elif ("FAIL" in strLabelTitle):
                font.setPointSize(30)
                self.labelTitle.setFont(font)
                self.labelTitle.setStyleSheet('QLabel {color: red}')
            else:
                font.setPointSize(18)
                self.labelTitle.setFont(font)
                self.labelTitle.setStyleSheet('QLabel {color: black}')
            self.labelTitle.setText(strLabelTitle)
            self.labelTitle.show()
        # Button Start
        if (bShowStartBtn):
            self.btnStart.show()
        # Button Pass
        if (bShowPassBtn):
            self.btnPass.show()
        # Button OK
        if (bShowOKBtn):
            self.btnOK.show()
        # Button Retry
        if (bShowRetryBtn):
            self.btnRetry.show()
        # Button Fail
        if (bShowFailBtn):
            self.btnFail.show()
        QApplication.processEvents()

    def emptyUI(self):
        try:
            self.labelTitle.hide()
        except:
            pass
        try:
            self.btnStart.hide()
        except:
            pass
        try:
            self.btnPass.hide()
        except:
            pass
        try:
            self.btnOK.hide()
        except:
            pass
        try:
            self.btnRetry.hide()
        except:
            pass
        try:
            self.btnFail.hide()
        except:
            pass

    def playSound(self, strVoiceName):

        # ^.* 代表開頭是任何字元的字串, 匹配任何路徑下的.mp3, .mp4, .wav檔, re.I(ignore case) 會忽略大小寫
        reMatch = re.fullmatch("^.*\.(MP3|MP4|WAV)", strVoiceName, re.I)

        if (reMatch != None):
            if os.path.exists(strVoiceName):
                printLog("[I][playSound] Start to play Voice (%s)" % strVoiceName)
                self.VoicePlayer.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(strVoiceName)))
                self.VoicePlayer.setVolume(100)
                self.VoicePlayer.play()
            else:
                win32ui.MessageBox("%s not found!" % os.path.abspath(os.getcwd() + strVoiceName), "Load Voice Error")
        else:
            printLog("[W][playSound] Vocie file name format error!")

    def stopSound(self):
        if self.VoicePlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            printLog("[I][stopSound] Stop to play Voice")
            self.VoicePlayer.stop()
        self.VoicePlayer.setMedia(QtMultimedia.QMediaContent())

    # invoked while reading INI fail
    def showMsg(self, strMsg):
        message = QMessageBox() # QMessageBox is inheretented from QtWidgets
        message.setIcon(QMessageBox.Critical)
        message.setWindowTitle("Error")
        message.setText(strMsg)
        message.exec_()         # show the message, locing event loop. Also, return click result(int)
        self.finishTest()

    def finishTest(self):
        printLog("========== End MDUT ==========\n\n")
        self.signal_parent.emit('End')
        self.closeUI()

    def closeUI(self):
        self.close()        # close the window

    def closeEvent(self, event):
        self.signal_parent.emit('End')

class TestScriptThread(QThread):
    showMsg = pyqtSignal(str)       # Set handlers for asynchronous events as a signal
    controlUI = pyqtSignal(str, bool, bool, bool, bool, bool, bool)
    closeUI = pyqtSignal()
    playSound = pyqtSignal(str)
    stopSound = pyqtSignal()

    def __init__(self, UIWindow, dictTestStatus):
        QThread.__init__(self)
        self.uiWindow = UIWindow
        self.nMDUTNum = dictTestStatus['MDUTNum']
        if dictTestStatus['SN'] == "No_SN":
            self.strSN = "%s%d" % (dictTestStatus['SN'], self.nMDUTNum)
        else:
            self.strSN = dictTestStatus['SN']
        self.nMethodIndex = dictTestStatus['MethodIndex']
        self.nConnectType = dictTestStatus['ConnectType']
        self.strCountryCode = dictTestStatus['CountryCode']
        if 'ConnectType1_DeviceName' in dictTestStatus:
            self.nConnectType1_DeviceName = dictTestStatus['ConnectType1_DeviceName']
        else:
            self.nConnectType1_DeviceName = None
        self.strDeviceName = None

        self.strTestingStatus = None
        self.bSave = False          # True while file is paresed


        self.uiWindow.btnStart.clicked.connect(self.startTest)
        self.uiWindow.btnPass.clicked.connect(self.pressPassBtn)
        self.uiWindow.btnRetry.clicked.connect(self.pressRetryBtn)
        self.uiWindow.btnFail.clicked.connect(self.pressFailBtn)

        self._stop_event = threading.Event()
        self.strTestingStatus = "First Test"

    def __del__(self):
        self.wait()     # wait until the Qthread finish, then delete the thread

    def run(self):      # Qtherad will run the function after Qtheread.start() had been called
        global g_strResultPath, g_strLogPath, g_strLogDir, g_strFileName    # common global vars
        global g_strSoxDir, g_strCliToolDir, g_strADBPath                   # vars for the script

        g_strFileName = os.path.basename(__file__).split('.')[0]
        strWorkingDir = os.getcwd()
        g_strLogDir = os.path.join(strWorkingDir, "Log/Temp/%s/" % (self.strSN))
        g_strResultPath = strWorkingDir + "/Log/Temp/%s/TestResult.txt" % (self.strSN)
        g_strLogPath = "./Log/Temp/%s" % (self.strSN)
        if not os.path.exists(g_strLogPath):
            os.makedirs(g_strLogPath)
        g_strLogPath = "/Log/Temp/%s/%s.log" % (self.strSN, g_strFileName)
        g_strLogPath = strWorkingDir + g_strLogPath
        strINIPath = "./INI/%s.ini" % (g_strFileName)

        # vars for the script
        g_strADBPath = os.path.join(os.getcwd(), "PortFile/%s/EXE/ADB" % self.nMDUTNum)
        g_strSoxDir = os.path.join(os.getcwd(), "PortFile/%s/EXE/Cyclops_MIC_Test" % self.nMDUTNum)
        g_strCliToolDir = os.path.join(os.getcwd(), "PortFile/%s/EXE/Mic_Tool" % self.nMDUTNum)

        printLog("========== Start ==========")
        printLog("[I][main] Python " + sys.version)
        printLog("[I][main] %s.py %s" % (g_strFileName, g_strVersion))

        if(self.readINI(strINIPath, self.nMethodIndex) == False):
            self.showMsg.emit(self.strFailReasonTemp)
            self.finishTest()
        else:
            if self.bStartButton:   # default 1 from readINI
                self.controlUI.emit("Press start button", True, False, False, False, False, False)
            else:
                self.startTest()

    def readINI(self, strINIPath, nMethodIndex):
        try:
            config = configparser.ConfigParser()
            config.read(strINIPath)
            strMethod = 'Method%s' % nMethodIndex
            printLog("[I][readINI] ---------- INI ----------")

            self.bStartButton = bool(int(config.get(strMethod, 'StartButton_ON')))
            printLog("[I][readINI] StartButton_ON = %s" % self.bStartButton)

            self.nLowerLimmit = int(config.get(strMethod, 'LowerLimmit_Value'))
            printLog("[I][readINI] LowerLimmit_Value = %d" % self.nLowerLimmit)

            self.nTestSecond = int(config.get(strMethod, 'TestSecond'))
            printLog("[I][readINI] TestSecond = %d" % self.nTestSecond)
            self.strErrorCode = config.get(strMethod, 'EC')
            printLog("[I][readINI] EC = %s" % self.strErrorCode)

            printLog("[I][readINI] ---------- INI ----------")
            return True
        except Exception as e:
            printLog("[E][readINI] Error: %s" % str(e))
            self.strFailReasonTemp = "Read INI error: %s" % str(e)
            return False

    def getDeviceName(self):
        try:
            printLog("[I][getDeviceName] Reading %s from BOM." % (self.nConnectType))
            configDUTInfo = configparser.ConfigParser()
            configDUTInfo.optionxform = str
            configDUTInfo.read("./Log/Temp/%s/DUTInfo.txt" % self.strSN)
            strDeviceName = configDUTInfo.get("DUT", self.nConnectType1_DeviceName)
            printLog("[I][getDeviceName] %s : %s" % (self.nConnectType, strDeviceName))
            return strDeviceName

        except:
            printLog("[W][getDeviceName] Reading DUTInfo.txt fail.")
            self.strFailReasonTemp = "Reading DUTInfo.txt fail."
            return None

    # run in adb shell
    def sendADBCommand(self, strCommand):      # called by startTest
# [11-Nov-2020 Sanchez] =>
        adb = ADB('.\\PortFile\\%s\\EXE\\ADB\\adb.exe' % self.nMDUTNum)
# <= [11-Nov-2020 Sanchez]
        # 1 to multi
        if self.nConnectType1_DeviceName is not None:
            if (self.strDeviceName == None):
                self.strDeviceName = self.getDeviceName()

            if self.strDeviceName != None:
                printLog("[I][sendADBCommand] Send DUT command: -s %s shell %s" % (self.strDeviceName, strCommand))
                adb.run_cmd("-s %s shell %s" % (self.strDeviceName, strCommand))
                strDUTReturn = adb.get_output()
                if strDUTReturn == None:
                    return None
                elif type(strDUTReturn) == list:
                    strForReturn = ""
                    for i in strDUTReturn:
                        printLog(i)
                        if strForReturn == "":
                            strForReturn = strForReturn + str(i)
                        else:
                            strForReturn = strForReturn + "\r\n" + str(i)
                    return strForReturn
                else:
                    return strDUTReturn

            elif self.strDeviceName == None:
                printLog("[E][sendADBCommand] No Device Name to connect adb device.")
                return False

        # 1 to 1
        else:
            adb.run_cmd('devices')  # equals command `adb devices` in cmd

            deviceslist = []
            print(adb.get_output())
            for i in adb.get_output()[0].split('\r\n'):     # \r\n == \n
                if i is not '':
                    deviceslist.append(i)

            nDevicesNum = len(deviceslist) - 1
            if nDevicesNum > 1:
                printLog("[E][sendADBCommand] More than one device detect!")
                return False
            printLog("[I][sendADBCommand] Send DUT command: %s" % strCommand)
            strDUTReturn = adb.shell_command(strCommand)
            strADBError = adb.get_error()
            if (strADBError is not None):
                printLog("[E][sendADBCommand] ADB error: %s" % strADBError)
                self.strFailReasonTemp = "ADB %s" % strADBError
                return False
            else:
                if (strDUTReturn is None) or (strDUTReturn == []):
                    printLog("[E][sendADBCommand] DUT return None with no error message.")
                    return False
                else:
                    printLog("[I][sendADBCommand] DUT return : %s" % strDUTReturn)
                    return strDUTReturn

# -------- button handling mostly by function controlUI in class cTestScriptUI ------------
# ------------------------ main test function ------------------------------
    def startTest(self):        # handling btnStart called by __init__() in cTestScriptUI or run() in TestScriptUI
        # mode: Normal, UniTest
        strMode = "Normal"
        #strMode = "UniTest"

        if strMode == "Normal":
            try:
                printLog("[I][startTest] ---------- StartTest ----------")
                self.controlUI.emit("Mic Test", False, False, False, False, False, False)
                self.strFailReasonTemp = None
                self.bSave = False          # True while file is paresed
                self.strTestingStatus = "FirstTest"


                if (self.nConnectType == CONNECTTYPE.USBADB):
                    if (self.sendADBCommand('root') == False):
                        printLog("[I][StartTest] Unable to use ADB!!")

                        # self.strFailReasonTemp modified when invoking self.sendADBCommand('root')
                        self.TestResult(False, self.strFailReasonTemp)
                    else:
                        self.strTestingStatus = "ParsePass"

                        # purging old files and initiating new directory
                        self.controlUI.emit("Initiating...", False, False, False, False, False, False)
                        self.init()

                        # play and record sound
                        if self.strTestingStatus == "InitPass":
                            #self.controlUI.emit("Recoding Sound...", False, False, False, False, False, False)
                            self.playAndRecord()    # dispaly UI and play thread, record thread

                        elif self.strTestingStatus == "InitFail":
                            printLog("[I][startTest] Initiating Fail")
                            self.TestResult(False, self.strFailReasonTemp)

                        # pull wav file from DUT and copy to ./Portfile/%s/EXE/Cyclops_MIC_Test/out
                        if self.strTestingStatus == "RecordPass":
                            self.controlUI.emit("Pulling wav...", False, False, False, False, False, False)
                            self.pullWav()
                        elif self.strTestingStatus == "RecordFail":
                            printLog("[I][startTest] play and record wav Fail")
                            self.TestResult(False, self.strFailReasonTemp)

                        # split and convert wav
                        if self.strTestingStatus == "PullPass":
                            self.controlUI.emit("Spliting and Convrting...", False, False, False, False, False, False)
                            self.splitAndConvert()
                        elif self.strTestingStatus == "PullFail":
                            printLog("[I][startTest] Pull wav Fail")
                            self.TestResult(False, self.strFailReasonTemp)

                        # run client tool to start subprocesses, testing 2 wav file
                        if self.strTestingStatus == "ParsePass":
                            self.controlUI.emit("Testing Mic...", False, False, False, False, False, False)
                            self.bSave = True
                            self.testWav()
                        elif self.strTestingStatus == "ParseFail":
                            printLog("[I][startTest] Split and Convert Fail")
                            self.TestResult(False, self.strFailReasonTemp)

                        # save resulting wav to log whether test fail or pass
                        if self.bSave:
                            self.controlUI.emit("Saving Result...", False, False, False, False, False, False)
                            self.SaveWav()

                        # final check
                        if self.strTestingStatus == "SavePass":
                            printLog("[I][startTest] Test Pass")
                            self.TestResult(True)
                        elif self.strTestingStatus == "TestFail":
                            printLog("[I][startTest] Test Fail")
                            self.TestResult(False, self.strFailReasonTemp)

                else:
                    printLog("[I][StartTest] Do not support connect type:%d" % self.nConnectType)
                    self.strFailReasonTemp = "Do not support connect type:%d" % self.nConnectType
                    self.TestResult(False, self.strFailReasonTemp)

            except:
                printLog("[W][StartTest] Unexpected error: %s" % (str(traceback.format_exc())))
                printLog("[W][StartTest] Unexpected error: %s" % (str(sys.exc_info())))
                self.TestResult(False, "Unexpected error")

        if strMode == "UniTest":
            print("[I][startTest] UniTest")
            #self.controlUI.emit("Recording Sound", False, False, False, False, False, False)
            self.playAndRecord()


# ---------------------------------------------- ------------------------------
    def pressPassBtn(self):
        printLog("[I][pressPassBtn] User click Pass button")
        self.TestResult(True)

    def pressFailBtn(self):
        printLog("[I][pressFailBtn] User click fail button")
        self.strFailReasonTemp = "User click fail button!"
        self.TestResult(False, self.strFailReasonTemp)

    def pressRetryBtn(self):
        printLog("[I][pressRetryBtn] User click Retry button")
        self.startTest()
# ---------------------------------------------------------------------------------------------

    # purging old files and initiating new directory
    def init(self):
        printLog("[I][init] Initiating files and directory")

        self.strTestingStatus = "InitFail"
        try:
            self.strFailReasonTemp = "Initiating Fail"

            strPullWavPath = os.path.join(g_strADBPath, "record.wav")
            self.removeFiles(strPullWavPath)

            strParseWavDir = os.path.join(g_strSoxDir, "out")
            self.removeFiles(strParseWavDir)
            os.makedirs(strParseWavDir)

            strWavLogDir = os.path.join(g_strLogDir, "out")
            self.removeFiles(strWavLogDir)
            os.makedirs(strWavLogDir)

            printLog("[I][init] Initiating done")
            self.strTestingStatus = "InitPass"
        except Exception as e:
            printLog("[E][init] Unexpected Error: " + str(e))
            self.TestResult(False, "Unexpected Error")

    # play and record sound
    def playAndRecord(self):
        printLog("[I][playAndRecord] Playing and Recoding Sound")

        self.strTestingStatus = "RecordFail"
        try:
            self.strFailReasonTemp = "Record Fail"

            # check if DUT is connected
            if not self.DUTconnect("hidtest AT+Key?"):
                return

            strVoiceName = "./Script/dtmf.wav"

            # play and record simultaneously
            t_play = threading.Thread(target = self.playSound.emit(strVoiceName), args=[])
            t_record = threading.Thread(target = self.recordSound, args=[])
            t_play.start()
            t_record.start()

            # countdown
            nSecond = self.nTestSecond + 1
            self.controlUI.emit("Recording Sound\n" + ("00:%02d" % nSecond), False, False, False, False, False, False)
            while(nSecond >= 0):
                QApplication.processEvents()
                self.uiWindow.labelTitle.setText("Recording Sound\n" + ("00:%02d" % nSecond))
                nSecond -= 1
                time.sleep(1)

            t_record.join()         # t_record will decide TestFail or TestPass
            self.stopSound.emit()

            # check if DUT is connected again
            if not self.DUTconnect("hidtest AT+Key?"):
                self.strTestingStatus = "RecordFail"
                return

            printLog("[I][playAndRecord] Recoding Successed")
        except Exception as e:
            printLog("[E][recordSound] Unexpected error: " + str(e))
            self.TestResult(False, "Unexpected error")

    # DUT record for threading
    def recordSound(self):
        printLog("[I][recordSound] Recording sound")

        self.strTestingStatus = "RecordFail"
        try:
            strADBCommand = "factory 8 0 " + str(self.nTestSecond)  # record command for DUT e.g. factory 8 0 5, 5 for second
            printLog("[I][recordSound] Send ADB command %s" % strADBCommand)
            self.sendADBCommand(strADBCommand)

            self.strTestingStatus = "RecordPass"
        except Exception as e:
            printLog("[E][recordSound] Unexpected error: " + str(e))
            self.TestResult(False, "Unexpected error")

    # pull record.wav from designated path
    def pullWav(self):
        printLog("[I][pullWav] Pulling wav file from DUT")

        self.strTestingStatus = "PullFail"
        try:
            # check if DUT is connected
            if not self.DUTconnect("pwd"):
                return

            # pull wav file from DUT
            pullFromDUT = subprocess.Popen(["adb", "pull", "/sdcard/factoryRokid/record.wav"], shell=True, cwd=g_strADBPath, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pullFromDUT.wait()

            # check pull successed
            strWavPath = os.path.join(g_strADBPath, "record.wav")
            if not os.path.exists(strWavPath):
                printLog("[I][pullWav] pulling wav fail")
                self.strFailReasonTemp = "Pulling wav fail"
                return


            strDestPath = os.path.join(g_strSoxDir, "out")
            self.copyWav(strWavPath, strDestPath)

            printLog("[I][pullWav] pulling wav successed")
            self.strTestingStatus = "PullPass"
        except Exception as e:
            printLog("[W][pullWav] Unexpected error: " + str(e))
            self.TestResult(False, "Unexpected error")

    # split original wav into two then convrt from 48k to 8k for each
    def splitAndConvert(self):
        printLog("[I][splitAndConvert] Ready to split and convert")

        self.strTestingStatus = "ParseFail"
        try:
            # spilting original file to two wav file
            self.strFailReason = "Spilting Fail"
            printLog("[I][splitAndConvert] Spliting wav file")
            splitWav = subprocess.Popen("run_splitchannel.bat", shell=True, cwd=g_strSoxDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            splitWav.wait()

            # check if spliting successed
            if splitWav.stderr.read().decode("big5") != "":
                printLog("[I][splitAndConvert] Spliting failed")
                return
            printLog("[I][splitAndConvert] Spliting successed")

            # convrt two 48k wav into 8k wav
            self.strFailReasonTemp = "Converting Fail"
            printLog("[I][splitAndConvert] Convrting wav files")
            convertWav = subprocess.Popen("run_convert.bat", shell=True, cwd=g_strSoxDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            convertWav.wait()

            # check if convrting successed
            if splitWav.stderr.read().decode("big5") != "":
                printLog("[I][splitAndConvert] Convert failed")
                return
            printLog("[I][splitAndConvert] Convrting seccessed")

            self.strTestingStatus = "ParsePass"
        except Exception as e:
            printLog("[E][splitAndConvert] Unexpected error: " + str(e))
            self.TestResult(False, "Unexpected error")

    # run client tool to test the wav file
    def testWav(self):
        printLog("[I][testWav] ----- Testing Mic -----")

        self.strTestingStatus = "TestFail"
        try:
            # testing Mic 1
            self.strFailReasonTemp = "Mic 1 Fail"
            strWavPath = os.path.join(g_strSoxDir, "out/record_1_converted.wav")
            strCMD = 'dtmf_test.exe "%s"' % strWavPath

            testWav = subprocess.Popen(strCMD, shell=True, cwd=g_strCliToolDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            testWav.wait()

            strSigCnt = testWav.stdout.read().decode("big5").split("\n")[1]    # decode cp950 (big5)
            print(strSigCnt)
            if int(strSigCnt) < self.nLowerLimmit:
                printLog("[I][testWav] Mic 1 Test Fail")
                return
            else:
                printLog("[I][testWav] Mic 1 Test Pass")

            # testing Mic 2
            self.strFailReasonTemp = "Mic 2 Fail"
            strWavPath = os.path.join(g_strSoxDir, "out/record_2_converted.wav")
            strCMD = 'dtmf_test.exe "%s"' % strWavPath

            testWav = subprocess.Popen(strCMD, shell=True, cwd=g_strCliToolDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            testWav.wait()

            strSigCnt = testWav.stdout.read().decode("big5").split("\n")[1]    # decode cp950 (big5)
            print(strSigCnt)
            if int(strSigCnt) < self.nLowerLimmit:
                printLog("[I][testWav] Mic 2 Test Fail")
                return
            else:
                printLog("[I][testWav] Mic 2 Test Pass")
                self.strTestingStatus = "TestPass"
                return

        except Exception as e:
            printLog("[E][testWav] Unexpected error: " + str(e))
            self.TestResult(False, "Unexpected error")

    # saving record.wav to log
    def SaveWav(self):
        printLog("[I][SaveWav] Save resulting wav files to log")

        self.strTestingStatus = "SaveFail"
        try:
            strDirPath = os.path.join(g_strSoxDir, "out")
            strDest = os.path.join(g_strLogDir, "out")

            # check if the dir exists, which should be make while invoking init()
            if not os.path.exists(strDirPath):
                printLog("[E][SaveWav] Target directory not exist: %s" % strDirPath)
                self.strFailReasonTemp = "Save Fail"
                return

            # save wavs to log
            for strDirPath, listDirName, listFileNames in os.walk(strDirPath):
                for strFile in listFileNames:
                    strSrc = os.path.join(strDirPath, strFile)
                    self.copyWav(strSrc, strDest)

            self.strTestingStatus = "SavePass"
            printLog("[I][SaveWav] Saving Successed")
        except Exception as e:
            printLog("[E][SaveWav] Unexpected error: " + str(e))
            self.TestResult(False, "Unexpected error")

    # check DUT connection
    def DUTconnect(self, strCommand):
        printLog("[I][DUTconnect] Checking DUT connection...")
        try:
            ADBResult = self.sendADBCommand(strCommand)
            # check if sendADBCommand return None
            if type(ADBResult) is bool:
                printLog("[E][DUTconnect] DUT return None")
                self.strFailReason = "DUT return None"
                return False

            strReturn = "".join(ADBResult)
            if "device not found" in strReturn or "Unable" in strReturn:
                printLog("[E][DUTconnect] DUT not connected")
                self.strFailReasonTemp = "DUT not found"
                return False
            else:
                printLog("[I][DUTconnect] DUT is connected")
                return True
        except Exception as e:
            printLog("[E][DUTconnect] Unexpected Error: " + str(e))
            return False

    # remove file or directory
    def removeFiles(self, strPath):
        printLog("[I][removeFiles] Removing %s" % strPath)
        try:
            if os.path.isdir(strPath):
                shutil.rmtree(strPath)      # remove dir including the files inside
            elif os.path.isfile(strPath):
                os.remove(strPath)

        except Exception as e:
            printLog("[E][removeFiles] Unexpected error: " + str(e))
            self.TestResult(False, "Unexpected error")

    # copy wav file
    def copyWav(self, strSrc, strDest):
        printLog("[I][copyWav] copying wav to %s" % strDest)

        try:
            if os.path.exists(strSrc) and os.path.exists(strDest):
                strCMD = 'copy "%s" "%s"' % (strSrc, strDest)
                os.system(strCMD)
                printLog("[I][copyWav] wav copied")
            else:
                printLog("[E][copyWav] Copy Fail, File Not Found")
                self.strFailReasonTemp = "Copy Fail, File Not Found"
                self.TestResult(False, self.strFailReasonTemp)
        except Exception as e:
            printLog("[E][copyWav] Unexpected Error: " + str(e))
            self.TestResult(False, "Unexpected Error")

# ------------------------ terminating function ---------------------------

    # show test result UI, and call saveTestResult()
    def TestResult(self, bPass, strFailReason = 'None'):
        if bPass == True:
            printLog("[I][TestResult] Test Pass!")
            self.saveTestResult(True)
            self.controlUI.emit("PASS", False, False, False, False, False, False)
            time.sleep(1)
            self.finishTest()
        else:
            printLog("[I][TestResult] Test Fail! %s" % strFailReason)
            self.saveTestResult(False, strFailReason)
            self.controlUI.emit("FAIL\n%s" % strFailReason, False, False, False, True, False, False)

    # save test result as an ini file named g_strResultPath
    def saveTestResult(self, bPass, strFailReason='None'):
        config = configparser.ConfigParser()
        config.add_section('TestResult')
        config.set('TestResult', 'Version', g_strVersion)
        if bPass == True:
            config.set('TestResult', 'Result', 'Pass')
        else:
            config.set('TestResult', 'Result', 'Fail')
            config.set('TestResult', 'Reason', strFailReason)
            config.set('TestResult', 'EC', self.strErrorCode)

        with open(g_strResultPath, 'w+') as configfile:
            config.write(configfile)

    def finishTest(self):
        printLog("========== End MDUT ==========\n\n")
        self.closeUI.emit()

    def stop(self):
        self._stop_event.set()

#/====================================================================\#
#|                             Function                               |#
#\====================================================================/#

# called by MDUT_Plus.py
def returnVersion():
    return g_strVersion

def getDateTimeFormat():
    strDateTime = "[%s]" % (time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))
    return strDateTime

def printLog(strPrintLine):
    strFileName = os.path.basename(__file__).split('.')[0]
    fileLog = codecs.open(g_strLogPath, 'a', "utf-8")
    print(strPrintLine)
    fileLog.write("%s%s\r\n" % (getDateTimeFormat(), strPrintLine))
    fileLog.close()


# Usage: [FileName].py [ShelfCount] [MDUT Num] [Method Index] [SN] [ConnectType] [IP/ComNum] [Port/BaudRate] [UserName] [PassWord]
if __name__ == "__main__":
    strFileName = os.path.basename(__file__).split('.')[0]  # get filename withou .py
    if (len(sys.argv) < 3):
        print("Use default parameter to script.")
        dictParameter = {'ShelfCount': 1, 'MDUTNum': 1, 'MethodIndex': 1, 'SN': '1', 'ConnectType': 1, 'CountryCode': "EN"}
    else:
        nShelfCount = int(sys.argv[1])
        nMDUTNum = int(sys.argv[2])
        nMethodIndex = int(sys.argv[3])
        strSN = sys.argv[4]
        nInterfaceType = int(sys.argv[5])

# ------------------------------------------ read by MDUT_Plus.py ---------------------------------------------
        if (len(sys.argv) > 6):
            strCountryCode = sys.argv[6]
        else:
            strCountryCode = 'EN'
        dictParameter = {'ShelfCount': nShelfCount, 'MDUTNum': nMDUTNum, 'MethodIndex': nMethodIndex, 'SN': strSN, 'ConnectType': nInterfaceType, 'CountryCode': strCountryCode}
        if nInterfaceType == CONNECTTYPE.USBADB and len(sys.argv) > 7:
            dictParameter['ConnectType1_DeviceName'] = sys.argv[6]
            if (len(sys.argv) > 7):
                dictParameter['CountryCode'] = sys.argv[7]
        if nInterfaceType == CONNECTTYPE.WIRELESSADB:
            dictParameter['ADBIP'] = sys.argv[6]
            dictParameter['ADBPort'] = sys.argv[7]
            if (len(sys.argv) > 8):
                dictParameter['CountryCode'] = sys.argv[8]
        if nInterfaceType == CONNECTTYPE.COM:
            dictParameter['ConnectType3_COM'] = sys.argv[6]
            dictParameter['ConnectType3_BaudRate'] = sys.argv[7]
            if (len(sys.argv) > 8):
                dictParameter['CountryCode'] = sys.argv[8]
        if nInterfaceType == CONNECTTYPE.SSH:
            dictParameter['SSHIP'] = sys.argv[6]
            dictParameter['SSHPort'] = sys.argv[7]
            dictParameter['Username'] = sys.argv[8]
            dictParameter['Password'] = sys.argv[9]
            if (len(sys.argv) > 10):
                dictParameter['CountryCode'] = sys.argv[10]
# ------------------------------------------------------------------------------------------------------

    os.chdir("../")     # chagne cwd to dir MDUtT_PLUS_3_0_0_20_GFM60
    app = QApplication(sys.argv)
    uiTestUI = cTestScriptUI(dictParameter)
    uiTestUI.resize(600, 400)
    uiTestUI.setWindowTitle(strFileName)
    uiTestUI.show()
    os._exit(app.exec_())
