import pandas as pd
import requests
from loguru import logger
import file
KEY = "AIzaSyC1DlWA5nf-qAj39sxHO4OwMJ8iCQ31ncg"
CX = "31cada641ddb84fc4"
langdict_reverse = {
    "ar":"阿拉伯语",
    "bg":"保加利亚语",
    "ca":"加泰罗尼亚语",
    "cs":"捷克语",
    "da":"丹麦语",
    "de":"德语",
    "el":"希腊语",
    "en":"英语",
    "es":"西班牙语",
    "et":"爱沙尼亚语",
    "fi":"芬兰语",
    "fr":"法语",
    "hr":"克罗地亚语",
    "hu":"匈牙利语",
    "id":"印度尼西亚语",
    "is":"冰岛语",
    "it":"意大利语",
    "iw":"希伯来语",
    "ja":"日语",
    "ko":"韩语",
    "lt":"立陶宛语",
    "lv":"拉脱维亚语",
    "nl":"荷兰语",
    "no":"挪威语",
    "pl":"波兰语",
    "pt":"葡萄牙语",
    "ro":"罗马尼亚语",
    "ru":"俄语",
    "sk":"斯洛伐克语",
    "sl":"斯洛文尼亚语",
    "sr":"塞尔维亚语",
    "sv":"瑞典语",
    "tr":"土耳其语",
    }
def creatdf():
    list = ['中文原词','网址','语种','站点内容','命中url']
    return pd.DataFrame(columns=list)
def creatdf_country():
    list = ['中文原词','网址','国家','站点内容','命中url']
    return pd.DataFrame(columns=list)
def creatdf_normal():
    list = ['中文原词','网址','站点内容','命中url']
    return pd.DataFrame(columns=list)
#api调用每次10条，每天调用100次 num最大值为10 start最大值为90
url = "https://customsearch.googleapis.com/customsearch/v1?" \
      "key={}" \
      "&cx={}" \
      "&lr={}" \
      "&q={}" \
      "&num={}" \
      "&start={}"
import colorama
def api(q,lr,num,start,key,cx):
    response = eval(requests.get(url.format(key,cx,lr,q,num,start)).text)
    if "items" in dict(response).keys():
        return response["items"]
    # else:
    #     print(colorama.Fore.RED+"[Error] api wrong:"+ url.format(key,cx,q,num,start))
    #     print("If this shows permanently,check your agent settings or internet connection")
    #     print(colorama.Style.RESET_ALL)
def api_country(q,num,start,key,cx):
    url2 = "https://customsearch.googleapis.com/customsearch/v1?" \
          "key={}" \
          "&cx={}" \
          "&q={}" \
          "&num={}" \
          "&start={}"
    response = eval(requests.get(url2.format(key,cx,q,num,start)).text)
    if "items" in dict(response).keys():
        return response["items"]
def find_keys_by_value(dic,value):
    keys = [key for key,val in dic.items() if val == value]
    if value == None:
        return "未设置"
    if keys:
        return keys[0]
    return None

def lang_getsingle(q:str,lang,num:int,start:int,key:str,cx:str,word:str):
    result = []
    response = api(q, lang, num, start, key, cx)
    if response:
        for item in response:
            displayLink = ""
            snippet = ""
            link = ""
            try:
                displayLink = item["displayLink"]
            except:
                pass
            try:
                snippet = item["snippet"]
            except:
                pass
            try:
                link = item["link"]
            except:
                pass
            result.append([word,displayLink,langdict_reverse[lang],snippet,link])
        return result
    return None

def country_getsingle(q:str,country,num:int,start:int,key:str,cx:str,word:str):
    result = []
    response = api_country(q, num, start, key, cx)
    if response:
        for item in response:
            displayLink = ""
            snippet = ""
            link = ""
            try:
                displayLink = item["displayLink"]
            except:
                pass
            try:
                snippet = item["snippet"]
            except:
                pass
            try:
                link = item["link"]
            except:
                pass
            result.append([word,displayLink,country,snippet,link])
        return result
    return None

def normal_getsingle(q:str,num:int,start:int,key:str,cx:str,word:str):
    result = []
    response = api_country(q, num, start, key, cx)
    if response:
        for item in response:
            displayLink = ""
            snippet = ""
            link = ""
            try:
                displayLink = item["displayLink"]
            except:
                pass
            try:
                snippet = item["snippet"]
            except:
                pass
            try:
                link = item["link"]
            except:
                pass
            result.append([word,displayLink,snippet,link])
        return result
    return None
def handlejson():
    import os
    import json
    jsonlist = os.listdir("json")
    df = creatdf()
    for file in jsonlist:
        string = None
        with open("./json/"+file,"r") as f:
            string = f.read()
        if string:
            entry = eval(string)
            for item in entry:
                print(["", "", item["displayLink"], item["snippet"], item["link"]])

