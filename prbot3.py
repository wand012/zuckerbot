import tweepy
from markovbot import MarkovBot
from urllib import request, parse
from pytrends.request import TrendReq
import json,time,random
def getBot(filePath):
    tweetbot = MarkovBot()
    tweetbot.read(filePath)
    return tweetbot
def getSentence(bot,words):
    text = bot.generate_text(30, seedword=words)
    print(text)
    return text

def getRandomSentence():
    x="serving, discussing, doing, protecting, maximizing, investing, making, testing, working on, celebrating, " \
      "helping, growing, including, building, pioneering, announcing, funding, talking about, using, checking, " \
      "organizing, seeking, launching, asking for, sending, following, showing, learning, starting, " \
      "threatening, running, measuring, winning, looking for, expanding, saying".split(", ")
    y="VR, this election, fake news, hate speech, News Feed, targeted ads".split(", ")
    pytrends = TrendReq(hl='en-US', tz=360)
    data = pytrends.trending_searches()
    for i in list(data['title']):
        y.append(i)
    xItem=random.sample(x,1)[0]
    yItem=random.sample(y,1)[0]
    sentence="We sincerely apologize for {xItem} {yItem}.".format(xItem=xItem,yItem=yItem)
    return sentence

def getKeyWords(tweet):
    showapi_appid = "49335"
    showapi_sign = "b5802dc943ab4b44a29f6c1b6a6f54f5"
    url = "http://route.showapi.com/941-1"
    send_data = parse.urlencode([
        ('showapi_appid', showapi_appid)
        , ('showapi_sign', showapi_sign)
        , ('text', tweet)
        , ('num', "10")
    ])
    req = request.Request(url)
    try:
        response = request.urlopen(req, data=send_data.encode('utf-8'), timeout=10)
    except Exception as e:
        print(e)

    result = response.read().decode('utf-8')
    result_json = json.loads(result)
    return result_json['showapi_res_body']['list']


def getApi():
    cons_key = 'WOPOTC9rUp2kvSw2sY0xvnBgj'
    cons_secret = 'HS3NzYFWZHGRyVMEHUyRbijMRQlGbdiOFGDBQNUEkdiuRHvjqR'
    access_token = '925571167565565952-cGYrTpKNsyfsCTfUG9qJUoA24GuS2kD'
    access_token_secret = 'azUDbJSorzhudEpTFWbIIi8O9qT5CYGh4njmbqi8AsyyA'
    auth = tweepy.OAuthHandler(cons_key, cons_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def datetime_timestamp(dt):
    time.strptime(dt,'%Y-%m-%d %H:%M:%S')
    s = time.mktime(time.strptime(dt,'%Y-%m-%d %H:%M:%S'))
    return int(s)
def sendMessage(startAt,bot,api):
    print("Loading Messages")
    message = api.direct_messages()
    for item in message:
        if datetime_timestamp(str(item.created_at)) > startAt:
            sentence = getSentence(bot, getKeyWords(item.text))
            #sentence = getRandomSentence()
            api.send_direct_message(item.sender.screen_name, item.sender.screen_name, item.sender.id,
                                         sentence)
        api.destroy_direct_message(item.id)
    time.sleep(5)
def retweet(startAt,bot,api,m_list):
    mentions = api.mentions_timeline()
    print("Loading mentions")
    for item in mentions:
        if item.id not in m_list:
            if datetime_timestamp(str(item.created_at)) > startAt:
                #sentence = getSentence(bot, getKeyWords(item.text))
                sentence = getRandomSentence()
                api.update_status("@{name} {content}".format(name=item.user.screen_name, content=sentence))
            m_list.append(item.id)
    time.sleep(5)
if __name__=='__main__':
    startAt = int(time.time())
    bot=getBot("Zuckerberg.txt")
    m_list=[]
    for i in range(60 * 60 * 24 * 7):
        api = getApi()
        sendMessage(startAt,bot,api)
        retweet(startAt,bot,api,m_list)
        time.sleep(5)