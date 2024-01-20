import file
import pandas as pd
from tqdm import tqdm
from loguru import logger
import thread

import time
df = thread.creatdf()
langs = words.columns[1:]
sum = 0
keynum = 1
keys = file.getkeylist()
for i in range(7,15):
    try:
        print("处理词语:"+words.iloc[i,0])

        for lang in tqdm(langs): #21种语言
            for offset in range(2):#前20条内容=> 每个词42次请求
                try:
                    key, cx, keys = file.getkey(keys)
                    data = thread.getsingle(words.loc[i,lang],lang,10,1+offset*10,key,cx,words.iloc[i,0])
                    df = df.append(pd.DataFrame(data, columns=df.columns), ignore_index=True)
                    time.sleep(3)
                    sum += 1
                except:
                    file.savekey(keys)
                    logger.debug("处理词语"+words.iloc[i,0]+"时出现错误,请求量{},密钥池{}".format(sum,keynum))
    except:
        pass

file.savekey(keys)
file.saveresult(df)
# print(df)
