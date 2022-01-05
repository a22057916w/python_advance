import os, sys
import shutil
import re

from pathlib import Path
import win32wnet        # for windows only (local side)

strDestDirPath = Path("\\\\10.110.140.222\File\Willy\Data\IPA72")
strProjectTitle = "IPA72"

# making connection to remote ip (only windows cappble for local side )
def wnet_connect(strHost, strUserName, strPassword):
    print("[I][wnet_connect] Connecting share disk, IP: %s" % strHost)
    unc = ''.join(['\\\\', strHost])

    try:
        win32wnet.WNetAddConnection2(0, None, unc, None, strUserName, strPassword)
        print("[I][wnet_connect] Connect share disk success.")
        return True
    except Exception as e:
        print("[E][wnet_connect] Connection Error: %s" % str(e))
        return False

def rename_folder():
    # scr for server side; dest for local side
    try:
        rePattern = re.escape(strProjectTitle) + r'-\d{13}'

        for folder_name in os.listdir(strDestDirPath):
            if re.fullmatch(rePattern, folder_name):
                strOldDirPath = os.path.join(strDestDirPath, folder_name)
                strNewDirPath = os.path.join(strDestDirPath, folder_name.split("-")[1])

                if os.path.exists(strNewDirPath):
                    print("[I][rename_folder] remove existing folder %s" % strNewDirPath)   
                    shutil.rmtree(strNewDirPath)

                os.rename(strOldDirPath, strNewDirPath)
                print("[I][rename_folder] Reanme folder %s to %s" % (folder_name, folder_name.split("-")[1]))

    except Exception as e:
        print("[E][rename_folder] Unexpect Error:" + str(e))
        return

if __name__ == "__main__":
    if wnet_connect("10.110.140.222", "WillyWJ_Chen", "40205gup!"):
        rename_folder()
