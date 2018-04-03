from skpy import SkypeEventLoop, SkypeNewMessageEvent, SkypeMsg
from getpass import getpass
from messages import messageChain

class UrsarBot(SkypeEventLoop):
    def __init__(self, chain):
        super(UrsarBot, self).__init__(user="user", pwd="password")
        self._chain = chain

    def onEvent(self, event):
        if isinstance(event, SkypeNewMessageEvent) and not event.msg.userId == self.userId:
            messageToSend = self._chain.run(event.msg.content.lower())
            if messageToSend:
                event.msg.chat.sendMsg(messageToSend)

if __name__ == "__main__":
    UrsarBot(messageChain).loop()
