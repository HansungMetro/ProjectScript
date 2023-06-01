import requests as req
from fake_useragent import UserAgent
import time
import datetime as dt
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager as chromeD
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
class newsData: #기사class
    def __init__(self, type, date, text):
        self.type = type
        self.date = date
        self.text = text

def NC_CrawlingSiteIn(url): #홈페이지 게시판 내 공지사항 글 크롤링
    headers = {'User-Agent' : UserAgent().random}
    res = req.get(url, headers=headers)

    soup = bs(res.text, 'html.parser')

    newsText = soup.find('div', class_="textarea-area").find('div', class_="txc-textbox")

    return newsText.get_text()

def NC_CrawlingSite(): #홈페이지 크롤링
    headers = {'User-Agent' : UserAgent().random}
    res = req.get("http://www.seoulmetro.co.kr/kr/board.do?menuIdx=546", headers=headers)
    
    soup = bs(res.text, 'html.parser')

    newsSite = []

    urlList = soup.find('tbody').find_all('a')
    newsDate = soup.find('tbody').find_all('td', class_="t-disn bd5")

    for i in range(1,8):
        url = "http://www.seoulmetro.co.kr/kr/%s" %(urlList[i].get('href'))
        newsText = NC_CrawlingSiteIn(url)
        newsSite.append(newsData('홈페이지', dt.datetime.fromisoformat(newsDate[i].get_text()), newsText))

    return newsSite

def NC_CrawlingTwitter(): #트위터 크롤링
    driver = webdriver.Chrome(chromeD().install())
    driver.get("https://twitter.com/seoul_metro")
    time.sleep(5)
    html = driver.page_source
    driver.close()

    soup = bs(html, 'html.parser')

    newsTwitter = []

    newsDate = soup.find('div', class_="css-1dbjc4n").find_all('time')
    newsText = soup.find('div', class_="css-1dbjc4n").find_all('div', dir="auto")

    for i in range (8):
        dates = newsDate[i].get('datetime')
        dates = dates[0:10]
        newsTwitter.append(newsData('트위터', dt.datetime.fromisoformat(dates), newsText[i+3].get_text()))
    
    return newsTwitter

def NC_SortNews(newsT, newsS, numNews): #홈페이지, 트위터에서 크롤링한 기사 날짜순 정렬
    newsList = []
    j = 0
    k = 0

    for i in range(numNews):
        if newsT[j].date > newsS[k].date:
            newsList.append(newsT[j])
            j += 1
        elif newsT[j].date < newsS[k].date:
            newsList.append(newsS[k])
            k += 1
        else:
            newsList.append(newsT[j])
            newsList.append(newsS[k])
            i += 1
            j += 1
            k += 1

    return newsList

def NC_PrintNews(numNews): #기사 출력 numNews:출력 기사 갯수(최대8)
    if numNews >= 8:
        numNews = 8
    newsT = NC_CrawlingTwitter()
    newsS = NC_CrawlingSite()
    news = NC_SortNews(newsT, newsS, numNews)
    sys.stdout.reconfigure(encoding='utf-8')
    textR = ""
    for i in news:
      #  textR+="───────────────────────────────────────────\n"
        textR+=f"[{i.type}]\t{str(i.date)[0:10]}\\"
        textR+=f"{i.text};"
  #  textR+="───────────────────────────────────────────\n"
    return textR
    
if __name__ == '__main__':
    Result = NC_PrintNews(8)
    print(Result)
