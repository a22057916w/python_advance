from configparser import ConfigParser
import pandas as pd
import os


strAbsPath = os.path.abspath(__file__)
strFileDir = os.path.dirname(strAbsPath)

strSettingPath = os.path.join(strFileDir, 'setting.ini')    # Setting.ini
strInputPath = os.path.join(strFileDir, 'input.txt')        # input.txt

# store input.txt to listNums
listNums = []
with open(strInputPath) as textFile:
    # list of integers where converted from string
    listNums = [int(i) for i in textFile.read().splitlines()]


# store setting.ini section "Setting" info to dictSetting
dictSetting = {}
with open(strSettingPath) as iniFile:
    config = ConfigParser()
    config.read_file(iniFile)
    dictSetting = dict(config.items('Setting'))     # config.items('Setting') will return list

#print(dictSetting)

# calculate the different averages and stored as Dictionary of list
dictAvgs = {}
for strKey, strValue in dictSetting.items():
    #print(key, value)

    listAvg = []    # stored each average interval
    nDivisor = int(strValue)

    # check if the total number of numbers is greater than the divisor
    if nDivisor <= len(listNums):
        for i in range(len(listNums) - (nDivisor - 1)):
            listAvg.append(int(sum(listNums[i:i+nDivisor]) / nDivisor))
    else:
        raise ValueError("The divisor {0} is greater than the total length of numbers {1}".format(nDivisor, len(listNums)))

    dictAvgs[strKey + strValue] = listAvg     # e.g. {firstavg5 : list of averages, ...}


# Using "df = pd.DataFrame.from_dict()" gets error: column of different length. Therefore, we
# apply pd.Series() to fill the empty value as <NA> with dtype=pd.Int64Dtype() for intType "value"
df = pd.DataFrame(dict([(strKey, pd.Series(listValue, dtype=pd.Int64Dtype())) for strKey, listValue in dictAvgs.items()]))

#print(df)

df.to_csv(os.path.join(strFileDir, "out.txt"), header=True, index=False, sep="\t")
df.to_csv(os.path.join(strFileDir, "out.csv"), header=True, index=False)
