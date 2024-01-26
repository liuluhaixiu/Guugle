# Guugle
Guugle is a link spider which is used to search information in tons of languages via google.
## 使用方法
### 1.在keys.csv中保存谷歌的api和搜索引擎cx
(获取方法详阅https://zhuanlan.zhihu.com/p/174666017)
每行一个
### 2.在trans_secret中保存有道翻译API的key和密码
### 3.在source.txt中输入需要处理的关键字

### python3 guugle.py

## 过程：
脚本1会先将source.txt中的词语翻译为21种谷歌搜索支持的语言，然后脚本2会用这些语言在谷歌翻译上进行搜索。
每种语言搜索20条结果。也就是说一个关键字会进行40次搜索，理论上获取800条网页

## 注意事项：
谷歌翻译每天每个账户有100条翻译次数的限制。因此尽量提供更多key和cx为宜
翻译api是付费的，但是注册送60块，够用很久

# 参数:
-d/--direct:如果之前已经完成了第一阶段(翻译)
-x/--xslx 使用googlehacking来搜索存在表格文件的网站
-p/--pdf 使用googlehacking搜索存在pdf的网站


# 持续更新中...
