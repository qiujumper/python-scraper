#获取页面对象
from urllib.request import urlopen
from urllib.request import urlretrieve
from pyquery import PyQuery as pq
#修改请求头模块,模拟真人访问
import requests
import time
#引入系统对象
import os

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
    while(i < 2):
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

#这个函数内部的路径按照自己的真实情况来写，方便之后的数据导入
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
        h = pq(req.text)
        #获取第一页的所有房子模块
        houseItems = h('.item-mod')
        #从模块中提取我们需要的信息，比如详情页的URL,价格，略缩图等
        #我倾向只获取详情页的URL，然后在详情页中获取更多的信息
        for houseItem in houseItems.items():
            houseUrl = houseItem.find('.items-name').attr('href')
            #print(houseUrl)
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
        h = pq(req.text)

        #get title
        housePrice = h('h1').text() if h('h1') != None else 'none'

        #get price
        housePrice = h('.sp-price').text() if h('.sp-price') != None else 'none'

        #get image url
        houseImage = h('.con a:first-child img').attr('src')
        houseImageUrl = getAbsoluteURL(baseUrl, houseImage)
        if houseImageUrl != None:
            urlretrieve(houseImageUrl, getDownloadPath(baseUrl, houseImageUrl, downLoadDir))     
       

        


#start to run the code
allPages = getAllPages()

for i in allPages:
    getItemLinks(i)
#此时pages 应该充满了很多url的内容
for i in pages:
    getItemDetails(i)
#print(pages)

