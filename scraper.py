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
import time

#你自己的配置文件，请将config-sample.py重命名为config.py,然后填写对应的值即可
import config

#定义链接集合，以免链接重复
pages = set()
session = requests.Session()
baseUrl = 'http://pic1.ajkimg.com'
downLoadDir = 'images'

#获取所有列表页连接
def getAllPages():
    pageList = []
    i = 1
    while(i < 3):
        newLink = 'http://sh.fang.anjuke.com/loupan/all/p' + str(i) + '/'
        pageList.append(newLink)
        i = i + 1
    return pageList

def getAbsoluteURL(baseUrl, source):
    if source.startswith("http://www."):
        url = "http://"+source[11:] 
    elif source.startswith("http://"):
        url = source
    elif source.startswith("www."):
        url = "http://"+source[4:] 
    else:
        url = baseUrl+"/"+source 
    if baseUrl not in url:
        return None 
    return url


def getDownloadPath(baseUrl, absoluteUrl, downloadDirectory): 
    path = absoluteUrl.replace("www.", "")
    path = path.replace(baseUrl, "")
    path = downloadDirectory+path
    directory = os.path.dirname(path)
    if not os.path.exists(directory): 
        os.makedirs(directory)
    return path

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
        houseItems = bsObj.select('.item-mod')

        #从模块中提取我们需要的信息，比如详情页的URL,价格，略缩图等
        #我倾向只获取详情页的URL，然后在详情页中获取更多的信息
        for houseItem in houseItems:
            if houseItem.find('a', {'class','items-name'}) == None:
                houseUrl = '';
            else:
                houseUrl = houseItem.find('a', {'class','items-name'})['href']
                pages.add(houseUrl)
        
#获取详情页的各种字段，这里可以让用户自己编辑
def getItemDetails(url):
    #先判断是否能获取页面
    try:
        req = session.get(url, headers = config.value['headers'])
    #这个判断只能判定是不是404或者500的错误，如果DNS没法解析，是无法判定的
    except IOError as e:
        print('can not reach the page. ')
        print(e)
    else:
        time.sleep(1)
        bsObj = BeautifulSoup(req.text)
        houseTitle = bsObj.find('h1').text
        if bsObj.find('em',{'class','sp-price'}) == None:
            housePrice = 'None'
        else:
            housePrice = bsObj.find('em',{'class','sp-price'}).text;
        # if bsObj.select('.con a:first-child .item img')== None:
        #     houseThumbnail = 'None'
        # else:
        #     houseThumbnail = bsObj.select('.con a:first-child .item img');

        print(houseTitle + '--' + housePrice )


#start to run the code
allPages = getAllPages()

for i in allPages:
    getItemLinks(i)
#此时pages 应该充满了很多url的内容
for i in pages:
    getItemDetails(i)
#print(pages)

