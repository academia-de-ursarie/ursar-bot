from ursar.plugin import UrsarPlugin
from ursar.decorators import respond_to

import requests

class UrbanDictionaryPlugin(UrsarPlugin):

    @respond_to("^urban dictionary (?P<word>.*)$")
    def definition(self, message, word):
        response = requests.get("http://api.urbandictionary.com/v0/define?term=%s" % word)
        json = response.json()
        if json['result_type'] == 'exact':
            all_definitions = [definition['definition'] for definition in json['list']]
            return '\n'.join(all_definitions)
        else:
            return 'Nici un rezultat'
