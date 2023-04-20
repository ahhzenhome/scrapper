import requests
from pprint import pprint
from bs4 import BeautifulSoup
import newsletter

QUALIFIED_SCORE = 100
MAX_PAGE = 5
url = "https://news.ycombinator.com/news?p=pageno"

def get_news(url, maxpage = MAX_PAGE):
    pageno = 1
    allnews = []

    while True:
        url1 = url.replace("pageno",str(pageno))
        res = requests.get(url1)

        pagenews = get_news_data(BeautifulSoup(res.text, "html.parser"))
        if len(pagenews) <= 0 or pageno >= maxpage:
            break
        allnews.extend(pagenews)
        pageno += 1
    return allnews

def get_news_data(soup):
    stories = soup.select(".athing")#19042023
    votes = soup.select(".score")
    ages = soup.select(".age")

    news_list = []

    for story in stories:
        news = {}
        # link = story.select(".storylink")[0]
        link = story.select(".titleline")[0].find("a") #19042023 OK

        storyid = story.get("id")   #OK
        storyage = ""
        
        # storyage = [age.find("a").text for age in ages if storyid in age.find("a").get("href")][0]
        storyage = [age.text for age in ages if storyid in age.find("a").get("href").split("=")[1]][0]
        news.update({"storyid": storyid, "title": link.text,"url": link.get("href"), "age": storyage})
        try:
            storyid2 = 'score_' + storyid
            votetext = [item for item in votes if storyid2 in item["id"]][0]
        except IndexError:
            news.update({"score": 0})
        else:
            votetext = int(votetext.text.replace("points",""))
            news.update({"score": votetext})
        if news["score"] >= QUALIFIED_SCORE:
            news_list.append(news.copy())

    return news_list

def display_news():

    allnews = get_news(url)
    allnews = sorted(allnews, key=lambda key: key["score"],reverse=True)

    for i, news in enumerate(allnews):
        print(i, end=" ")
        pprint(news)
        print()

def generate_news_email():
    allnews = get_news(url)
    allnews = sorted(allnews, key=lambda key: key["score"], reverse=True)
    newsletter.send_email(allnews)

if __name__ == "__main__":
    generate_news_email()
    
