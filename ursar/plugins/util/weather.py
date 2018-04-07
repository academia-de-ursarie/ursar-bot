from ursar.plugin import UrsarPlugin
from ursar.decorators import respond_to

import requests

class WeatherPlugin(UrsarPlugin):

    @respond_to('^weather( in)? (?P<location>.*)$')
    def weather(self, message, location=None):
        return self.yahoo_weather(location, 'In {location} there are {temperature}°C, {forecast}')

    @respond_to('^vreme(a in)? (?P<location>.*)$')
    def vremea(self, message, location=None):
        return self.yahoo_weather(location, 'In {location} sunt {temperature}°C, {forecast}')

    def yahoo_weather(self, location, formatString):
        query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="%s") and u="c"' % location
        response = requests.get('https://query.yahooapis.com/v1/public/yql?q=%s&format=json' % query)
        json = response.json()

        if json['query']['results']:
            args = {
                'location': location.title(),
                'temperature': int(json['query']['results']['channel']['item']['condition']['temp']),
                'forecast': json['query']['results']['channel']['item']['condition']['text']
            }
            
            return formatString.format(**args)

        return None