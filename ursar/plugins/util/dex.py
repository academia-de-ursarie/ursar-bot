from ursar.plugin import UrsarPlugin
from ursar.decorators import respond_to

import requests

class DexPlugin(UrsarPlugin):

    @respond_to('^dex (?P<word>.*?)(?: (?P<limit>\d+))?$')
    def definition(self, message, word=None, limit=5):
        response = requests.get('https://dexonline.ro/definitie/%s?format=json' % word)
        if response and response.status_code == 200:
            json = response.json()
            if json['definitions'] and len(json['definitions']) > 0:
                all_definitions = [definition['htmlRep'] for definition in json['definitions'][:int(limit)]]
                return '\n'.join(all_definitions)
            else:
                return 'No results'
        return 'Something went wrong. Try again.'