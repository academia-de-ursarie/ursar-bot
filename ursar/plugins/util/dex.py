from ursar.plugin import UrsarPlugin
from ursar.decorators import respond_to

import requests

class DexPlugin(UrsarPlugin):

    @respond_to("^dex (?P<word>.*)$")
    def definition(self, message, word=None):
        response = requests.get("https://dexonline.ro/definitie/%s?format=json" % word)
        if response and response.status_code == 200:
            json = response.json()
            if json['definitions'] and len(json['definitions']) > 0:
                all_definitions = [definition['htmlRep'] for definition in json['definitions']]
                return '\n'.join(all_definitions)
            else:
                return 'Nici un rezultat'
        return 'Ceva merge prost. Mai incearca.'