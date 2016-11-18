from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError

#你自己的配置文件，请将config-sample.py重命名为config.py,然后填写对应的值即可
import config
def scraper():
    #定义链接集合，以免链接重复
    pages = set()

    #先判断是否能获取页面
    try:
        html = urlopen(config.value['url']);
    #这个判断只能判定是不是404或者500的错误，如果DNS没法解析，是无法判定的
    except IOError as e:
        print('can not reach the page【/(ㄒoㄒ)/~~】')
        print(e)
    
    else: 
        bsObj = BeautifulSoup(html.read())
        #获取第一页的所有房子模块
        houseItems = bsObj.select('.s-lp-list .lp-list-li')

        #从模块中提取我们需要的信息，比如详情页的URL,价格，略缩图等
        #我倾向只获取详情页的URL，然后在详情页中获取更多的信息
        for houseItem in houseItems:
            houseUrl = houseItem.find('a', {'class','_click'})['href']
            pages.add(houseUrl)
        print(pages)

if __name__ == '__main__': scraper()
