from ursar.plugin import UrsarPlugin
from ursar.decorators import respond_to

from ursar import VERSION

class VersionPlugin(UrsarPlugin):

    @respond_to('^version$')
    def version(self, message):
        return 'Running on v%s' % VERSION