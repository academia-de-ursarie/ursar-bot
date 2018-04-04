import requests
import random
from xml.etree import ElementTree

from .messagechain import MessageChain

messageChain = MessageChain()

@messageChain.on_message('boot man')
@messageChain.man('boot man')
def man():
    return '\n'.join(messageChain.get_man())

@messageChain.on_message('ping')
@messageChain.man('ping')
def ping(matches):
    return 'pong'

@messageChain.on_message('ursar')
@messageChain.man('ursar')
def ursar_hello():
    return 'qui est le plus ursar?'

@messageChain.on_message('vremea in (.*)')
@messageChain.man('vremea in :locatie')
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
@messageChain.man('dex :cuvant')
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
@messageChain.man('curs :moneda(EUR/USD...)')
def currency(matches):
    coin = matches.group(1)
    response = requests.get("http://openexchangerates.appspot.com/currency?from=%s&to=RON&q=1" % coin)
    if response and response.status_code == 200:
        json = response.json()
        if 'rate' in json:
            return "%s valoreaza %.2f RON" % (coin.upper(), float(json['rate']))
    return 'Ceva merge prost. Mai incearca'

@messageChain.on_message("(.*)(applause|applauze|aplauze|clap)")
@messageChain.man("(insincere|nesincere|slow) (applause|applauze|aplauze|clap)")
def applause(matches):
    sentiment = matches.group(1).strip()
    gif_url = None

    if sentiment in ['insincere', 'nesincere', 'slow']:
        gif_url = random.choice([
                'http://i.imgur.com/2QXgcqP.gif',
                'http://i.imgur.com/Yih2Lcg.gif',
                'http://i.imgur.com/un3MuET.gif',
                'http://i.imgur.com/H2wPc1d.gif',
                'http://i.imgur.com/uOtALBE.gif',
                'http://i.imgur.com/nmqrdiF.gif',
                'http://i.imgur.com/GgxOUGt.gif',
                'http://i.imgur.com/wyTQMD6.gif',
                'http://i.imgur.com/GYRGOy6.gif',
                'http://i.imgur.com/ojIsLUA.gif',
                'http://i.imgur.com/bRetADl.gif',
                'http://i.imgur.com/814mkEC.gif',
                'http://i.imgur.com/uYryMyr.gif',
                'http://i.imgur.com/YfrikPR.gif',
                'http://i.imgur.com/sBEFqYR.gif',
                'http://i.imgur.com/Sx8iAS8.gif',
                'http://i.imgur.com/5zKXz.gif'
            ])
    else:
        gif_url = random.choice([
            'http://i.imgur.com/pfrtv6H.gif',
            'http://i.imgur.com/Bp4P8l3.gif',
            'http://i.imgur.com/v7mZ22P.gif',
            'http://i.imgur.com/S1v4KuY.gif',
            'http://i.imgur.com/YTaSAkq.gif',
            'http://i.imgur.com/JO6Wz3r.gif',
            'http://i.imgur.com/pWEd6cF.gif',
            'http://i.imgur.com/zumSlIA.gif',
            'http://i.imgur.com/RGczKmV.gif',
            'http://i.imgur.com/KAQhoCm.gif',
            'http://i.imgur.com/PASRKXo.gif',
            'http://i.imgur.com/ZOWQTO6.gif',
            'http://i.imgur.com/cY0eH5c.gif',
            'http://i.imgur.com/wf5qvOM.gif',
            'http://i.imgur.com/9Zv4V.gif',
            'http://i.imgur.com/t8zvc.gif'
        ])

    return '<a href="{url}">{url}</a>'.format(url=gif_url)