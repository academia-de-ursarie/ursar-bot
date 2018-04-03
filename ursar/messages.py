import requests

from .messagechain import MessageChain

messageChain = MessageChain()

@messageChain.on_message('ping')
def ping(matches):
    return 'pong'

@messageChain.on_message('ursar')
def ursar_hello():
    return 'qui est le plus ursar?'

@messageChain.on_message('giphy (.*)')
def giphy(matches):
    search = matches.group(1)
    response = requests.get('http://api.giphy.com/v1/gifs/search?api_key=dc6zaTOxFJmzC&q=test&q=%s' % search)
    json = response.json()
    return json['data'][0]['images']['preview_gif']['url']

@messageChain.on_message('vremea in (.*)')
def weather(matches):
    location = matches.group(1)
    response = requests.get('https://query.yahooapis.com/v1/public/yql?q=select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="%s")&format=json&env=store://datatables.org/alltableswithkeys&u=c' % location)
    json = response.json()
    if json['query']['results']:
        currentTemp = int(json['query']['results']['channel']['item']['condition']['temp'])
        clouds = json['query']['results']['channel']['item']['condition']['text']
        ttl = (currentTemp - 32) / 1.8
        return 'In %s sunt %.2f grade, %s' % (matches.group(1).title(), ttl, clouds)
    return None
