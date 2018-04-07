from ursar.plugin import UrsarPlugin
from ursar.decorators import respond_to, hear

class BirthdayPlugin(UrsarPlugin):

    @hear('(happy birthday|la multi ani|lma)')
    def hear_happy_birthday(self, message):
        return 'Hei, happy birthday!'