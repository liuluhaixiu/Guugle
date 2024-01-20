import requests
import uuid
# 您的应用ID
import hashlib
import time
from loguru import logger
file_path = "trans_secret.txt"

def read_key_secret_from_file(file_path: str) -> tuple:
    with open(file_path, 'r') as f:
        key, secret = f.read().splitlines()
        return key, secret
APP_KEY,APP_SECRET = read_key_secret_from_file(file_path)

def api(q,lr='en'):
    url = "https://openapi.youdao.com/api" \
                                        "?q={}" \
                                        "&from=auto" \
                                        "&to={}" \
                                        "&appKey={}" \
                                        "&salt={}" \
                                        "&sign={}" \
                                        "&signType=v3" \
                                        "&curtime={}"
    salt = str(uuid.uuid1())
    curtime = str(int(time.time()))
    sign = getsign(APP_KEY,APP_SECRET,q,salt,curtime)
    url = url.format(q,lr,APP_KEY,salt,sign,curtime)
    res = requests.get(url)
    data = res.json()
    if data['errorCode'] == '0':
        return data['translation']
    else:
        logger.debug("翻译API请求失败")
        print(data)
        return None

def getinput(input):
    if input is None:
        return input
    inputLen = len(input)
    return input if inputLen <= 20 else input[0:10] + str(inputLen) + input[inputLen - 10:inputLen]

def encrypt(strSrc):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(strSrc.encode('utf-8'))
    return hash_algorithm.hexdigest()

def getsign(appKey, appSecret, q, salt, curtime):
    strSrc = appKey + getinput(q) + salt + curtime + appSecret
    return encrypt(strSrc)

