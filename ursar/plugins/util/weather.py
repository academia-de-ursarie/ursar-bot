from ursar.plugin import UrsarPlugin
from ursar.decorators import respond_to

import requests

class WeatherPlugin(UrsarPlugin):

    @respond_to("^(weather|vremea) in (?P<location>.*)$")
    def weather(self, message, location=None):
        response = requests.get('https://query.yahooapis.com/v1/public/yql?q=select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="%s")&format=json&env=store://datatables.org/alltableswithkeys&u=c' % location)
        json = response.json()

        if json['query']['results']:
            currentTemp = int(json['query']['results']['channel']['item']['condition']['temp'])
            clouds = json['query']['results']['channel']['item']['condition']['text']
            ttl = (currentTemp - 32) / 1.8
            return 'In %s sunt %.2f grade, %s' % (location.title(), ttl, clouds)
        
        return None