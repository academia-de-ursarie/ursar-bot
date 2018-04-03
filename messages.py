from messagechain import MessageChain
import requests

messageChain = MessageChain()

@messageChain.on_message("ursar")
def ursar_hello():
    return "qui est le plus ursar?"

@messageChain.on_message("giphy (.*)")
def giphy(matches):
    search = matches.group(1)
    r = requests.get('http://api.giphy.com/v1/gifs/search?api_key=dc6zaTOxFJmzC&q=test&q=%s' % search)
    json = r.json()
    return json['data'][0]['images']['preview_gif']['url']

@messageChain.on_message("vremea in (.*)")
def weather(matches):
    location = matches.group(1)
    r = requests.get('https://query.yahooapis.com/v1/public/yql?q=select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="%s")&format=json&env=store://datatables.org/alltableswithkeys&u=c' % location)
    json = r.json()
    print(json)
    if json['query']['results']:
        currentTemp = int(json['query']['results']['channel']['item']['condition']['temp'])
        clouds = json['query']['results']['channel']['item']['condition']['text']
        ttl = (currentTemp - 32) / 1.8
        return "In %s sunt %.2f grade, %s" % (matches.group(1).title(), ttl, clouds)
    return None
