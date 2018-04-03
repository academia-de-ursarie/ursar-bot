from os import environ
from skpy import SkypeEventLoop, SkypeNewMessageEvent, SkypeMsg

from .messages import messageChain

class UrsarBot(SkypeEventLoop):

    def __init__(self):
        super(UrsarBot, self).__init__(environ.get('SKYPE_USERNAME'), environ.get('SKYPE_PASSWORD'))

    def onEvent(self, event):
        if isinstance(event, SkypeNewMessageEvent) and not event.msg.userId == self.userId:
            messageToSend = messageChain.run(event.msg.content.lower())
            if messageToSend:
                event.msg.chat.sendMsg(messageToSend, rich=True)