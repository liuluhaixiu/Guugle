import pandas as pd
import requests
from loguru import logger
import file
KEY = "AIzaSyC1DlWA5nf-qAj39sxHO4OwMJ8iCQ31ncg"
CX = "31cada641ddb84fc4"
langdict_reverse = {
"lang_ar":"阿拉伯语",

"lang_bg":"保加利亚语",

"lang_ca":"加泰罗尼亚语",

"lang_cs":"捷克语",

"lang_da":"丹麦语",

"lang_de":"德语",

"lang_el":"希腊语",

"lang_en":"英语",

"lang_es":"西班牙语",

"lang_et":"爱沙尼亚语",

"lang_fi":"芬兰语",

"lang_fr":"法语",

"lang_hr":"克罗地亚语",

"lang_hu":"匈牙利语",

"lang_id":"印度尼西亚语",

"lang_is":"冰岛语",

"lang_it":"意大利语",

"lang_iw":"希伯来语",

"lang_ja":"日语",

"lang_ko":"韩语",

"lang_lt":"立陶宛语",

"lang_lv":"拉脱维亚语",

"lang_nl":"荷兰语",

"lang_no":"挪威语",

"lang_pl":"波兰语",

"lang_pt":"葡萄牙语",

"lang_ro":"罗马尼亚语",

"lang_ru":"俄语",

"lang_sk":"斯洛伐克语",

"lang_sl":"斯洛文尼亚语",

"lang_sr":"塞尔维亚语",

"lang_sv":"瑞典语",

"lang_tr":"土耳其语",

"lang_zh-TW":"中文"
}

def creatdf():
    list = ['中文原词','国家','网址','语种','站点内容','命中url']
    return pd.DataFrame(columns=list)

#api调用每次10条，每天调用100次 num最大值为10 start最大值为90
url = "https://customsearch.googleapis.com/customsearch/v1?" \
      "key={}" \
      "&cx={}" \
      "&q={}" \
      "&lr={}" \
      "&num={}" \
      "&start={}" \

def api(q,lr,num,start,key,cx):
    response = eval(requests.get(url.format(key,cx,q,lr,num,start)).text)
    if "items" in dict(response).keys():

        return response["items"]
    else:
        logger.error("api wrong")
        print(response)
        print("\n===================uri===================\n")
        print(url.format(key,cx,q,lr,num,start))
        exit()

def find_keys_by_value(dic,value):
    keys = [key for key,val in dic.items() if val == value]
    if keys:
        return keys[0]
    return None

def getsingle(q:str,lang:str,num:int,start:int,key:str,cx:str,word:str):
    result = []
    if find_keys_by_value(langdict_reverse,lang) == None:
        logger.debug("{} 语种不存在".format(lang))
        return None
    response = api(q,find_keys_by_value(langdict_reverse,lang),num,start,key,cx)
    if response:
        file.savejson(response)
        for item in response:
            result.append([word,lang.replace("语",""),item["displayLink"],lang,item["snippet"],item["link"]])
        return result
    logger.debug("{} 请求失败".format(q))
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

