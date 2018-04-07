from ursar.plugin import UrsarPlugin
from ursar.decorators import respond_to

import requests

class UrbanDictionaryPlugin(UrsarPlugin):

    @respond_to('^urban dictionary (?P<word>.*?)(?: (?P<limit>\d+))?$')
    def definition(self, message, word=None, limit=5):
        response = requests.get('http://api.urbandictionary.com/v0/define?term=%s' % word)
        json = response.json()
        if json['result_type'] == 'exact':
            all_definitions = [definition['definition'] for definition in json['list'][:int(limit)]]
            return '\n'.join(all_definitions)
        else:
            return 'No results.'
