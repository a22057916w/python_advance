import os, time
import datetime as df
import json
import zipfile

def zip_all_files():
    with zipfile.ZipFile(os.path.join("D:\code\python_advance\Auto_RRSIandWiFiSAR_Report\output\WillyWJ_Chen", "fuckyou_%s.zip" % "bitch"), "w") as zf:
        for dirPath, dirNames, fileNames in os.walk("D:\code\python_advance\Auto_RRSIandWiFiSAR_Report\output\WillyWJ_Chen"):
            for f in fileNames:
                if "zip" not in f:
                    #print(88888,os.path.join(dirPath, f))
                    zf.write(os.path.join(dirPath, f), os.path.basename(f))
                    print(os.path.basename(f))
                    print(f)

zip_all_files()
