from ursar.plugin import UrsarPlugin
from ursar.decorators import respond_to

class PingPlugin(UrsarPlugin):

    @respond_to('^ping$')
    def ping(self, message):
        return 'pong'

    @respond_to('^pong$')
    def pong(self, message):
        return 'ping'