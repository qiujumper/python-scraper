from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
#先判断是否能获取页面
def scraper():
    try:
        html = urlopen('http://nn.focus.cn/xxsearch/index.html');
    #这个判断只能判定是不是404或者500的错误，如果DNS没法解析，是无法判定的
    except HTTPError as e:
        print('can not find web page')
        print(e)
    
    #通用的错误检查
    except:
        print(e)
    else: 
        bsObj = BeautifulSoup(html.read())
        print(bsObj.h1)

if __name__ == '__main__': scraper()
