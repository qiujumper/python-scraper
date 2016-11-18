#获取页面对象
from urllib.request import urlopen
from urllib.request import urlretrieve
#修改请求头模块,模拟真人访问
import requests
#选择器
from bs4 import BeautifulSoup
#正则对象
import re
#获取随机数
import random
#获取日期
import datetime

#你自己的配置文件，请将config-sample.py重命名为config.py,然后填写对应的值即可
import config

#定义链接集合，以免链接重复
pages = set()
session = requests.Session()


#获取所有列表页连接
def getAllPages():
    pageList = []
    i = 1
    while(i < 5):
        newLink = 'http://nn.focus.cn/search/index_p' + str(i) +'.html'
        pageList.append(newLink)
        i = i + 1
    return pageList

#获取当前页面的所有连接
def getItemLinks(url):
    global pages;
    #先判断是否能获取页面
    try:
        req = session.get(url, headers = config.value['headers'])
    #这个判断只能判定是不是404或者500的错误，如果DNS没法解析，是无法判定的
    except IOError as e:
        print('can not reach the page. ')
        print(e)
    
    else: 
        bsObj = BeautifulSoup(req.text)
        #获取第一页的所有房子模块
        houseItems = bsObj.select('.s-lp-list .lp-list-li')

        #从模块中提取我们需要的信息，比如详情页的URL,价格，略缩图等
        #我倾向只获取详情页的URL，然后在详情页中获取更多的信息
        for houseItem in houseItems:
            houseUrl = houseItem.find('a', {'class','_click'})['href']
            pages.add(houseUrl)
        

def getItemDetails(url):
    #先判断是否能获取页面
    try:
        html = urlopen(url);
    #这个判断只能判定是不是404或者500的错误，如果DNS没法解析，是无法判定的
    except IOError as e:
        print('can not reach the page. ')
        print(e)


#start to run the code
allPages = getAllPages()

for i in allPages:
    getItemLinks(i)
#此时pages 应该充满了很多url的内容

