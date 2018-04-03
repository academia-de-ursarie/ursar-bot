import requests
from xml.etree import ElementTree

from .messagechain import MessageChain

messageChain = MessageChain()

@messageChain.on_message('ping')
def ping(matches):
    return 'pong'

@messageChain.on_message('ursar')
def ursar_hello():
    return 'qui est le plus ursar?'

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

@messageChain.on_message("dex (.*)")
def dex(matches):
    word = matches.group(1)
    response = requests.get("https://dexonline.ro/definitie/%s?format=json" % word)
    if response and response.status_code == 200:
        json = response.json()
        if json['definitions'] and len(json['definitions']) > 0:
            all_definitions = [d['htmlRep'] for d in json['definitions']]
            return '\n'.join(all_definitions)
        else:
            return 'Nici un rezultat'
    return 'Ceva merge prost. Mai incearca.'

@messageChain.on_message("^curs (\w{3})$")
def currency(matches):
    coin = matches.group(1)
    response = requests.get("http://openexchangerates.appspot.com/currency?from=%s&to=RON&q=1" % coin)
    if response and response.status_code == 200:
        json = response.json()
        if 'rate' in json:
            return "%s valoreaza %.2f RON" % (coin.upper(), float(json['rate']))
    return 'Ceva merge prost. Mai incearca'