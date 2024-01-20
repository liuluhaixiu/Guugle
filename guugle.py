from trans_api import api
import pandas as pd
import thread
from tqdm import tqdm
from time import sleep
from loguru import logger
import argparse
import file

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--direct', action='store_true', help='set direct to True,pass translating progress')
    return parser.parse_args()
#接收参数
args = parse_args()
if not args.direct:
    languages = ['中文','英语'	,'日语','韩语',	'俄语'	,'阿拉伯语',	'西班牙语',	'法语',
                 '德语'	,'意大利语'	,'葡萄牙语'	,'荷兰语'	,'波兰语'	,'芬兰语',	'捷克语'	,
                 '瑞典语','丹麦语'	,'挪威语','希腊语','匈牙利语',	'土耳其语'	,'印度尼西亚语']
    df = pd.DataFrame(columns=languages,index = None)
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
    def find_keys_by_value(value, dic=None):
        if dic is None:
            dic = langdict_reverse
        keys = [key for key,val in dic.items() if val == value]
        if keys:
            return keys[0]
        return None

    with open('source.txt','r',encoding='utf-8') as f:
        words = f.readlines()
    if words == []:
        print("此表为空")
        exit()

    for i in range(len(words)):
        logger.info("handling " + words[i] + " {}\{}".format(i,len(words)))
        for lang in tqdm(languages):
            try:
                fanyi = api(words[i],find_keys_by_value(lang))[0]
                df.loc[i,lang] = fanyi
                sleep(1)
                df.loc[i,'中文'] = words[i]
            except:
                print(words[i],'出错')
    # df.iloc[0,0] = None
    df.to_excel("words.xlsx",sheet_name='Sheet1',index=False)
    words = df
else:
    words = file.openwordsfile()

df = thread.creatdf()
langs = words.columns[1:]
sum = 0
keynum = 1
keys = file.getkeylist()
import random
for i in range(7,15):
    try:
        print("处理词语:"+words.iloc[i,0])

        for lang in tqdm(langs): #21种语言
            for offset in range(2):#前20条内容=> 每个词42次请求
                try:
                    key, cx, keys = file.getkey(keys)
                    data = thread.getsingle(words.loc[i,lang],lang,10,1+offset*10,key,cx,words.iloc[i,0])
                    df = df.append(pd.DataFrame(data, columns=df.columns), ignore_index=True)
                    sleep(random.uniform(1, 3))
                    sum += 1
                except:
                    file.savekey(keys)
                    logger.debug("处理词语"+words.iloc[i,0]+"时出现错误,请求量{},密钥池{}".format(sum,keynum))
    except:
        pass

file.savekey(keys)
file.saveresult(df)

