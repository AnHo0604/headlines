# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 09:39:57 2021

@author: anho
"""

from flask import render_template
import feedparser
from flask import Flask
from flask import request

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}
###############################################################################

# HTTP GET dung de lay thong tin ko nhay cam tu nguoi dung gui den server , thuong nam trong header .
# Doi so cua no la phan nam sau dau ? cua URL , phan doi so nay co the duoc dien tu dong va thu cong neu can .
def get_info():
    @app.route("/")
    def get_news():
        # tro publication den bbc neu chua co gi duoc chon
        query = request.args.get("publication")
        if not query or query.lower() not in RSS_FEEDS:
            publication = "bbc"
        else:
            publication = query.lower()
        feed = feedparser.parse(RSS_FEEDS[publication])
        return render_template("home3.html",articles=feed['entries'])
    app.run(port=5000, debug=True)
###############################################################################
# chen them 1 form vao trong template home3.index nhu sau :
'''
<form>
  <input type="text" name="publication" placeholder="search" />
  <input type="submit" value="Submit" />
</form>
'''
# ==> Khi do chung ta nhap vao o search vai ky tu va submit ==> URL se xuat hien thanh phan ten la publication: 
    # http://localhost:5000/?publication=hello ; co the search cnn hoac bbc se cho ra cac ket qua ben duoi khac nhau
    # publication se duoc get va dua vao trong query de truy van .
###############################################################################
# HTTP POST dang nhung thong tin nhay cam hon , goi stream lon hon len server :
# De su dung phuong thuc GET hoac POST chung ta thay the @app.route("/") ==> @app.route("/", methods=['GET', 'POST'])
# Qua trinh sau co nghia la lay thong tin tu RSS Feed sau do dua len server bang phuong thuc POST . 
# Tat nhien la o tren co the dung GET de lam nhung POST an toan hon . Khi su dung kieu nay ko con thay parameter sau dau ? nua .
def get_info2():
    # GET tu RSS sau do POST len server
    @app.route("/", methods=['GET', 'POST'])
    def get_news():
        # tro publication den bbc neu chua co gi duoc chon
        query = request.args.get("publication")
        if not query or query.lower() not in RSS_FEEDS:
            publication = "bbc"
        else:
            publication = query.lower()
        feed = feedparser.parse(RSS_FEEDS[publication])
        return render_template("home3.html",articles=feed['entries'])
    app.run(port=5000, debug=True)

###############################################################################
# Add them Weather vao trong trang web : dang ky acc tren trang weather va lay key API tren do . 
import json
#import urllib2
# urllib2 la urllib cua python 2  trong python 3 phai import kieu nhu sau :
import urllib.request as urllib2
import urllib
def JSON_Weather_API():
    def get_weather(query):
        api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=128874fb776c3f67955c3bc859cf88e8'
        query = urllib.parse.quote(query)
        url = api_url.format(query)
        data = urllib2.urlopen(url).read()
        parsed = json.loads(data)
        weather = None
        if parsed.get("weather"):
            weather = {"description":parsed["weather"][0]["description"],"temperature":parsed["main"]["temp"],"city":parsed["name"]}
        return weather
    
    @app.route("/", methods=['GET', 'POST'])
    def get_news():
        query = request.args.get("publication")
        if not query or query.lower() not in RSS_FEEDS:
            publication = "bbc"
        else:
            publication = query.lower()
        feed = feedparser.parse(RSS_FEEDS[publication])
        weather = get_weather("London,UK")
        return render_template("home4.html",articles=feed["entries"],weather=weather)
    app.run(port=5000, debug=True)
###############################################################################
# weather Ho Chi Minh :
def Weather_API_HCM():
    def get_weather(query):
        api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=128874fb776c3f67955c3bc859cf88e8'
        query = urllib.parse.quote(query)
        url = api_url.format(query)
        data = urllib2.urlopen(url).read()
        parsed = json.loads(data)
        weather = None
        if parsed.get("weather"):
            weather = {"description":parsed["weather"][0]["description"],"temperature":parsed["main"]["temp"],"city":parsed["name"]}
        return weather

    @app.route("/", methods=['GET', 'POST'])
    def get_news():
        query = request.args.get("publication")
        if not query or query.lower() not in RSS_FEEDS:
            publication = "bbc"
        else:
            publication = query.lower()
        feed = feedparser.parse(RSS_FEEDS[publication])
        weather = get_weather("Ho Chi Minh,VN")
        return render_template("home4.html",articles=feed["entries"],weather=weather)
    app.run(port=5000, debug=True)
###############################################################################
# search weather form :
def Weather_search_form():
     WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=128874fb776c3f67955c3bc859cf88e8'
     DEFAULTS = {'publication':'bbc', 'city': 'Ho Chi Minh,VN'}
     
     @app.route("/", methods=['GET', 'POST'])
     def home():
         # get customized headlines, based on user input or 
         publication = request.args.get('publication')
         if not publication:
             publication = DEFAULTS['publication']
         articles = get_news(publication)
         
         # get bien city tu form html cua form , neu ko lay duoc thi lay default .
         city = request.args.get('city')
         if not city:
             city = DEFAULTS['city']
         weather = get_weather(city)
         return render_template("home4.html", articles=articles,weather=weather)
     
     def get_news(query):
         if not query or query.lower() not in RSS_FEEDS:
             publication = DEFAULTS["publication"]
         else:
             publication = query.lower()
         feed = feedparser.parse(RSS_FEEDS[publication])
         return feed['entries']
     
     def get_weather(query):
         query = urllib.parse.quote(query)
         url = WEATHER_URL.format(query)
         data = urllib2.urlopen(url).read()
         parsed = json.loads(data)
         weather = None
         if parsed.get('weather'):
             weather = {'description':parsed['weather'][0]['description'],'temperature':parsed['main']['temp'],'city':parsed['name']}
         return weather
     app.run(port=5000,debug=True)
###############################################################################
# 
###############################################################################
# Chay :
def main():
    Weather_search_form()
if __name__=='__main__':
    main()