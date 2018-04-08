from ursar.plugin import UrsarPlugin
from ursar.decorators import respond_to, hear

import datetime
import random

class BirthdayPlugin(UrsarPlugin):

    @hear('(happy (bday|birthday)')
    def hear_happy_birthday(self, message):
        if self.is_own_birthday():
            return random.choice([
                'Thank you!',
                'Aww, thanks!',
                ':)',
            ])

        return 'Hei, happy birthday fellow ursar!'

    @hear('(la multi ani|lma)')
    def hear_happy_birthday(self, message):
        if self.is_own_birthday():
            return random.choice([
                'Multumesc!',
                'Heh, mersi!',
                ':)',
            ])

        return 'Hei, la multi ani ursar!'

    def is_own_birthday(self):
        today = datetime.datetime.today()
        return today.month == 6 and (today.day == 7 or today.day == 8)