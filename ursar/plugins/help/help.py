from ursar.plugin import UrsarPlugin
from ursar.decorators import respond_to

class HelpPlugin(UrsarPlugin):

    @respond_to("^help(?: (?P<plugin>.*))?$")
    def help(self, message, plugin=None):
        return "Here's what I know how to do:"