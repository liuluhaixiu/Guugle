from trans_api import api
import pandas as pd
import google_api
import colorama
from rich.console import Console
from rich.table import Table
from time import sleep
import argparse
import file
import os
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
    parser = argparse.ArgumentParser(description="Guugle is an osint web scanner based on google hacking phrase.")
    parser.add_argument('-i', '--info', action='store_true', help='enter setting mod')
    parser.add_argument('-s', '--syntax', help='set googlehacking syntax')
    parser.add_argument('-a', action='store_true', help='query the available time of google apis')
    parser.add_argument('-L', '--lang', action='store_true', help='set to multi-languag mod')
    parser.add_argument('-C', '--country', action='store_true', help='set to multi-country mod')
    parser.add_argument('-Ld', '--direct', action='store_true', help='set to multi-language mod and pass the translating process'
                                                                     '(Only used when program stopped during the last use and the translation was finished,to cut down expenditures,for tokens and time.)')
    return parser.parse_args()
#接收参数
def logo():

    print(colorama.Fore.MAGENTA )
    logo = r"""
    ===================================================================
              ____                                    __            
           /  __   \   __   __   __   __    ___      /  /    ___
          /  /   /_/  /    / /  /    / /  /  _  \   /  /   /  _  \
         /  /__----  /  __/ /  /  __/ /  /  __/ /  /  /   /  \_  /
         \_____ /    \____ /   \____ /   \___  /   \___/  \____/
                                         __   /
                                       /  _  /
                                       \___ /            VER.2.0
    ===================================================================
                                    """
    print(logo)
    print(colorama.Style.RESET_ALL)
logo()
# 还原默认颜色
print(colorama.Style.RESET_ALL)
args = parse_args()
syntax = ""
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
if args.info:
    console = Console()
    table = Table(show_header=True, header_style="dim")
    table.add_column("API NAME", style="dim")
    table.add_column("API VALUE", style="dim", justify="left")
    length = len(file.getkeylist())
    table.add_row("Google API", str(length)+"(num)")
    file_path = "trans_secret.txt"
    with open(file_path, 'r') as f:
        key, secret = f.read().splitlines()
    table.add_row("YouDao Translate API", "key : "+key+'\n'+"secret : "+secret)
    table.add_row("ChatGLM API", "abcdefghijklmn")
    console.print(table)
    print(colorama.Fore.MAGENTA+"Please make sure google api is avaliable before using this script.")
    print(colorama.Style.RESET_ALL+"use:python guugle.py -a")
    exit()
if args.a:
    console = Console()
    table = Table(show_header=True, header_style="dim")
    table.add_column("api", style="dim")
    table.add_column("cx", style="dim", justify="right")
    table.add_column("last update", style="dim", justify="right")
    table.add_column("available times", style="dim", justify="right")
    keys = file.getkeylist()
    import datetime
    for i in range(len(keys)):
        dt = datetime.datetime.fromtimestamp(keys.iloc[i,3])
        date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
        table.add_row(str(keys.iloc[i,0]), str(keys.iloc[i,1]),date_str,str(keys.iloc[i,2]))
    console.print(table)
    print(colorama.Fore.MAGENTA + "The google api flush betwen 24h.")
    print(colorama.Style.RESET_ALL)
    exit()
if args.syntax:
    syntax += args.syntax
if args.lang or args.direct:
    if not args.direct:
        console = Console()
        print("language supported:")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("language", style="dim")
        table.add_column("explain", style="dim", justify="right")
        for x in langdict_reverse.items():
            table.add_row(x[0], x[1])
        console.print(table)
        print(colorama.Fore.MAGENTA+"Step1:Please input the language list(file name or languages separated with ',' :")
        print(colorama.Style.RESET_ALL)
        language_str = input()
        languages = [""]
        if "." in language_str:
            try:
                f = open(language_str, encoding="utf-8")
                languages = f.readlines()
            except:
                print(colorama.Fore.RED + "[Error]Failed to open the file. Please check whether the file is entered correctly")
                print(colorama.Style.RESET_ALL)
                exit()
        else:
            languages = language_str.split(",")
        if languages == ['']:
            print(colorama.Fore.RED + "[Error]No search language, program ends")
            print(colorama.Style.RESET_ALL)
            exit()
        print(colorama.Fore.MAGENTA+"Step2:Please input the original words(file name or words separated with ',' :")
        print(colorama.Style.RESET_ALL)
        source_str = input()
        words = ['']
        if "." in source_str:
            try:
                f = open(source_str, encoding="utf-8")
                words = f.readlines()
            except:
                print(colorama.Fore.RED+"[Error]Failed to open the file. Please check whether the file is entered correctly")
                print(colorama.Style.RESET_ALL)
                exit()
        else:
            words = source_str.split(",")
        if words ==['']:
            print(colorama.Fore.RED + "[Error]No search term, program ends")
            print(colorama.Style.RESET_ALL)
            exit()
        print(colorama.Fore.MAGENTA + "Step3:Please input the page to scrape for every words(max=100) ',' :")
        pagenum = int(input())
        if pagenum < 1:
            print(colorama.Fore.RED + "[Error]Need value >= 1")
            print(colorama.Style.RESET_ALL)
            exit()
        os.system('cls' if os.name == 'nt' else 'clear')
        logo()
        print("================Program started!================")
        print(colorama.Fore.RED+"[Info] translation processing...")
        print(colorama.Style.RESET_ALL)
        df = pd.DataFrame(columns=languages, index=None)
        print(languages)
        print(words)
        for i in range(len(words)):
            os.system('cls' if os.name == 'nt' else 'clear')
            logo()
            print(colorama.Fore.RED+"[info] Translating " + words[i] + " [{}\{}]".format(i, len(words)))
            print(colorama.Style.RESET_ALL)
            for k, lang in enumerate(languages):
                progress_bar(len(languages), k)
                try:
                    translation = api(words[i], lang)[0]
                    df.loc[i, lang] = translation
                    sleep(1)
                    df.loc[i, '中文原词'] = words[i]
                except:
                    print(colorama.Fore.RED + "[Error] occured when translating {}...".format(words[i]))
                    print(colorama.Style.RESET_ALL)
        df.to_excel("words.xlsx", sheet_name='Sheet1', index=False)
        words = df
        print(colorama.Fore.RED + "[Info] translation finished...")
        print(colorama.Style.RESET_ALL)
    else:
        print(colorama.Fore.MAGENTA + "Please input the page to scrape for every words(max=100) ',' :")
        pagenum = int(input())
        if pagenum < 1:
            print(colorama.Fore.RED + "[Error]Need value >= 1")
            print(colorama.Style.RESET_ALL)
            exit()
        words = file.openwordsfile()
        languages = words.columns
        print(colorama.Fore.RED + "[Info] translation skipped...")
        print(colorama.Style.RESET_ALL)
    df = google_api.creatdf()
    sucesssum = 0
    wrongsum = 0
    keys = file.getkeylist()
    for i in range(len(words)):
        os.system('cls' if os.name == 'nt' else 'clear')
        logo()
        print(colorama.Fore.RED)
        print("[Mode] Multi Language")
        print("[Info] Language processing:"+",".join(languages))
        print("[Info] Guugling word:" + words.loc[i, '中文原词'] + "  ==> process:[{}/{}]".format(i, len(words)))
        print(colorama.Style.RESET_ALL)
        for k, lang in enumerate(languages):
            progress_bar(len(languages), k)
            for offset in range(pagenum):
                try:
                    key, cx, keys = file.getkey(keys)
                    s = words.loc[i, lang]
                    s += syntax
                    data = google_api.lang_getsingle(s, lang, 10, 1 + offset * 10, key, cx, words.iloc[i, 0])
                    df = df.append(pd.DataFrame(data, columns=df.columns), ignore_index=True)
                    sleep(0.5)
                    sucesssum += 1
                except:
                    file.savekey(keys)
                    wrongsum += 1
                    print(colorama.Fore.RED+"[Error] occured when handling" + colorama.Fore.MAGENTA+words.loc[i, '中文原词'] + colorama.Fore.RED+",SUM success time:{},error time:{}".format(sucesssum,wrongsum))
                    print(colorama.Style.RESET_ALL)


    file.savekey(keys)
    savename = file.saveresult(df)
    print('\n=========Process Finished！=========\n[SUM] success time:{},error time:{}'.format(sucesssum,wrongsum))
    print(colorama.Fore.GREEN+"[info] result saved to '{}'".format(savename))
if args.country:
    console = Console()
    print("Avaliable domain supported:")
    suggestion_top = {'.com': '商业（通用顶级域名）',
 '.org': '组织（通用顶级域名）',
 '.net': '网络（通用顶级域名）',
 '.gov': '政府（通用顶级域名）',
 '.edu': '教育（通用顶级域名）',
 '.int': '国际组织（通用顶级域名）',
 '.mil': '军事（通用顶级域名）',
 '.aero': '航空（专用顶级域名）',
 '.coop': '合作组织（专用顶级域名）',
 '.info': '信息（通用顶级域名）',
 '.pro': '专业人员（通用顶级域名）',
 '.name': '个人（通用顶级域名）',
 '.biz': '商业（通用顶级域名）',
 '.tv': '图瓦卢（国家顶级域名）',
 '.travel': '旅游（专用顶级域名）',
 '.mobi': '移动设备（专用顶级域名）',
 '.tel': '电话（专用顶级域名）',
 '.xxx': '成人内容（专用顶级域名）',
 '.asia': '亚洲（专用顶级域名）',
 '.eu': '欧盟（专用顶级域名）',
 '.org.uk': '英国的组织（二级域名）',
 '.gov.uk': '英国的政府（二级域名）',
 '.co.uk': '英国的商业（二级域名）'}
    suggestion_country = {
    ".af": "阿富汗",
    ".pk": "巴基斯坦",
    ".ps": "巴勒斯坦",
    ".br": "巴西",
    ".fr": "法国",
    ".ph": "菲律宾",
    ".kz": "哈萨克斯坦",
    ".kr": "韩国",
    ".us": "美国",
    ".de": "德国",
    ".it": "意大利",
    ".ru": "俄罗斯",
    ".cn": "中国",
    ".uk": "英国",
    ".jp": "日本",
    ".in": "印度",
    ".es": "西班牙",
    ".ca": "加拿大",
    ".au": "澳大利亚",
    ".tr": "土耳其",
    ".mx": "墨西哥",
    ".za": "南非",
    ".pt": "葡萄牙"}
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("country", style="dim")
    table.add_column("explain", style="dim", justify="right")
    table.add_column("top", style="dim")
    table.add_column("explain", style="dim", justify="right")
    ##在这里添加country
    st = list(suggestion_top.items())
    sc = list(suggestion_country.items())
    for i in range(min(len(st),len(sc))):
        table.add_row(sc[i][0].replace("."," "),sc[i][1],st[i][0].replace("."," "),st[i][1])
    console.print(table)
    print(colorama.Fore.MAGENTA + "Step1:Please input the country list(file name or countries separated with ',' :")
    print(colorama.Style.RESET_ALL)
    language_str = input()
    languages = [""]
    if "." in language_str:
        try:
            f = open(language_str, encoding="utf-8")
            languages = f.readlines()
        except:
            print(
                colorama.Fore.RED + "[Error]Failed to open the file. Please check whether the file is entered correctly")
            print(colorama.Style.RESET_ALL)
            exit()
    else:
        languages = language_str.split(",")
    if languages == ['']:
        print(colorama.Fore.RED + "[Error]No search country, program ends")
        print(colorama.Style.RESET_ALL)
        exit()
    countries = languages
    print(colorama.Fore.MAGENTA + "Step2:Please input the original words(file name or words separated with ',' :")
    print(colorama.Style.RESET_ALL)
    source_str = input()
    words = ['']
    if "." in source_str:
        try:
            f = open(source_str, encoding="utf-8")
            words = f.readlines()
        except:
            print(
                colorama.Fore.RED + "[Error]Failed to open the file. Please check whether the file is entered correctly")
            print(colorama.Style.RESET_ALL)
            exit()
    else:
        words = source_str.split(",")
    if words == ['']:
        print(colorama.Fore.RED + "[Error]No search term, program ends")
        print(colorama.Style.RESET_ALL)
        exit()
    print(colorama.Fore.MAGENTA + "Step3:Please input the page to scrape for every words(max=100) ',' :")
    pagenum = int(input())
    if pagenum < 1:
        print(colorama.Fore.RED + "[Error]Need value >= 1")
        print(colorama.Style.RESET_ALL)
        exit()
    os.system('cls' if os.name == 'nt' else 'clear')
    logo()
    print("================Program started!================")
    df = google_api.creatdf_country()
    sucesssum = 0
    wrongsum = 0
    keys = file.getkeylist()
    for i in range(len(words)):
        os.system('cls' if os.name == 'nt' else 'clear')
        logo()
        print(colorama.Fore.RED)
        print("[Mode] Multi Country")
        print("[Info] Countries processing:" + ",".join(countries))
        print("[Info] Guugling word:" + words[i] + "  ==> process:[{}/{}]".format(i, len(words)))
        print(colorama.Style.RESET_ALL)
        for k, country in enumerate(countries):
            progress_bar(len(countries), k)
            for offset in range(pagenum):
                try:
                    key, cx, keys = file.getkey(keys)
                    s = words[i]
                    s+="site:.{}".format(country)
                    s += syntax
                    data = google_api.country_getsingle(s,country, 10, 1 + offset * 10, key, cx, words[i])
                    df = df.append(pd.DataFrame(data, columns=df.columns), ignore_index=True)
                    sleep(0.5)
                    sucesssum += 1
                except:
                    file.savekey(keys)
                    wrongsum += 1
                    print(colorama.Fore.RED + "[Error] occured when handling " + colorama.Fore.MAGENTA + words[
                        i] + colorama.Fore.RED + ",SUM success time:{},error time:{}".format(sucesssum,
                                                                                                     wrongsum))
                    print(colorama.Style.RESET_ALL)

    file.savekey(keys)
    savename = file.saveresult(df)
    print('\n=========Process Finished！=========\n[SUM] success time:{},error time:{}'.format(sucesssum, wrongsum))
    print(colorama.Fore.GREEN + "[info] result saved to '{}'".format(savename))

