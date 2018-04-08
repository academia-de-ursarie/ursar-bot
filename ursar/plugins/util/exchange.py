from ursar.plugin import UrsarPlugin
from ursar.decorators import respond_to

import requests

class ExchangePlugin(UrsarPlugin):

    @respond_to('^(exchange|curs) (?P<coin>\w{3})$')
    def exchange_coin_to_ron(self, message, coin=None):
        return self.exchange(1, coin)

    @respond_to('^(exchange|curs) (?P<amount>\d+\.?\d*) (?P<fromCoin>\w{3}) in (?P<toCoin>\w{3})$')
    def exchange_from_to(self, message, amount=0, fromCoin=None, toCoin=None):
        return self.exchange(amount, fromCoin, toCoin)

    def exchange(self, amount=1, fromCoin='EUR', toCoin='RON'):
        response = requests.get('http://openexchangerates.appspot.com/currency?from=%s&to=%s&q=%s' % (fromCoin, toCoin, amount))
        if response and response.status_code == 200:
            json = response.json()
            if 'rate' in json:
                return "%.2f %s = %.2f %s" % (float(amount), fromCoin.upper(), float(amount) * float(json['rate']), toCoin.upper())
        
        return 'Something went wrong. Try again.'