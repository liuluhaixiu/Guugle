import pandas as pd
from loguru import logger
import json
import os
def openwordsfile():
    file = None
    # try:
    file = pd.read_excel("words.xlsx",sheet_name="Sheet1")
    # except:
    #     logger.error("cant find words list")
    return file

def saveresult(pd:pd.DataFrame):
    results = os.listdir("result")
    if results :
        namelist = sorted([int(x[6:-4]) for x in results])
        savename = "./result/result"+str(namelist[-1]+1)+".csv"
    else:
        savename = "./result/result1.csv"
    pd.to_csv(savename)
    return savename

#备份json文件
def savejson(jsonfile):
    jsondata = json.dumps(jsonfile)
    results = os.listdir("json")
    if results:
        namelist = sorted([int(x[4:-5]) for x in results])
        with open("./json/json" + str(namelist[-1] + 1) + ".json", "w") as file:
            file.write(jsondata)
    else:
        with open("./json/json1.json","w") as file:
            file.write(jsondata)
    # logger.info("request saved")

#key和cx存储 读入数据时判断能不能使用
import time
def getkeylist():
    df = None
    # try:
    if 1==1:
        df = pd.read_csv("keys.csv")
        for i in range(len(df)):
            if time.time() - df.iloc[i, 3] > 60 * 60 * 24 and df.iloc[i, 2] < 100:
                df.iloc[i, 2] = 100
                df.iloc[i, 3] = time.time()
    # except:
    #     logger.error("cant keylist")
    return df

#在keylist中得到一个key,同时减次数
def getkey(df:pd.DataFrame):
    for i in range(len(df)):
        if df.iloc[i, 2] != 0 :
            df.iloc[i,2] -= 1
            df.iloc[i,3] = time.time()
            return df.iloc[i,0],df.iloc[i,1],df

def savekey(df:pd.DataFrame):
    df.to_csv("keys.csv",columns=["key","cx","choice","timestamp"],index=False)