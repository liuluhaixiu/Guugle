from trans_api import api
import pandas as pd
import thread
# from tqdm import tqdm
from time import sleep
# from loguru import logger
import argparse
import file
import sys
def progress_bar(total, progress):
    # 初始化进度条
    progress += 1
    bar_length = 20
    percent = progress * 100.0 / total
    arrow = '-' * int(percent/100 * bar_length - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write('\rProgress: [%s%s] %d %%' % (arrow, spaces, percent))
    sys.stdout.flush()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--direct', action='store_true', help='set direct to True,pass translating progress')
    parser.add_argument('-x', '--xlsx', action='store_true', help='set xlsx to True,focus on search organized infomation')
    return parser.parse_args()
#接收参数
args = parse_args()
print("处理翻译中...")
languages = ['中文', '英语', '日语', '韩语', '俄语', '阿拉伯语', '西班牙语', '法语',
             '德语', '意大利语', '葡萄牙语', '荷兰语', '波兰语', '芬兰语', '捷克语',
             '瑞典语', '丹麦语', '挪威语', '希腊语', '匈牙利语', '土耳其语', '印度尼西亚语']
if not args.direct:

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
        print("翻译 " + words[i] + " {}\{}".format(i,len(words)))
        for k,lang in enumerate(languages):
            progress_bar(len(languages),k)
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
    print("\n翻译处理结束...初始化metasearch...")
else:
    words = file.openwordsfile()
    print("\n翻译跳过...直接处理words.xlsx...")
df = thread.creatdf()
langs = languages[1:]
sum = 0
keynum = 1
keys = file.getkeylist()
import random
for i in range(len(words)):
    try:
        print("搜索词语:"+words.iloc[i,0]+"进度{}/{}".format(i,len(words)))

        for k,lang in enumerate(langs): #21种语言
            progress_bar(len(langs),k)
            for offset in range(2):#前20条内容=> 每个词42次请求
                try:
                    key, cx, keys = file.getkey(keys)
                    s = words.loc[i,lang]
                    if args.xlsx:
                        s += " filetype:xlsx OR filetype:xls OR filetype:csv"
                    data = thread.getsingle(s,lang,10,1+offset*10,key,cx,words.iloc[i,0])
                    df = df.append(pd.DataFrame(data, columns=df.columns), ignore_index=True)
                    sleep(random.uniform(1, 3))
                    sum += 1
                except:
                    file.savekey(keys)
                    print("!!!处理词语"+words.iloc[i,0]+"时出现错误,请求量{},密钥池{}\n".format(sum,keynum))
    except:
        pass

file.savekey(keys)
file.saveresult(df)
print('\n=====运行完毕！=====\n成功查询{}次\n失败{}次'.format(sum,len(df)*2*21-sum))

