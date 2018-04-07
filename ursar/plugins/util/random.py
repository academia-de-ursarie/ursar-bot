from ursar.plugin import UrsarPlugin
from ursar.decorators import respond_to

import random

class RandomPlugin(UrsarPlugin):

    @respond_to('^random (?P<items>.*?)(?: (?P<limit>\d+))?$')
    def random(self, message, items=None, limit=1):
        items = [item.strip() for item in items.split(',')]
        random.shuffle(items)
        return 'Randomly chosen: %s' % ', '.join(items[:int(limit)])
