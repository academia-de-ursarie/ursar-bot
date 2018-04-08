from ursar.plugin import PluginManager
from ursar.settings import settings

import re
from os import environ
from inspect import getmembers, ismethod, isfunction
from skpy import SkypeEventLoop, SkypeNewMessageEvent

class UrsarBot(SkypeEventLoop):

    message_listeners = []

    def __init__(self):
        super(UrsarBot, self).__init__(settings['SKYPE_USERNAME'], settings['SKYPE_PASSWORD'])
        self.bootstrap_plugins()

    def bootstrap_plugins(self):
        '''
        Bootstrap plugins to their appropriate uses
        '''
        for plugin in PluginManager().load_plugins():
            try:
                plugin_instances = {}
                for function_name, fn in getmembers(plugin['class'], predicate=lambda x: ismethod(x) or isfunction(x)):
                    try:
                        if hasattr(fn, 'ursar_fn_metadata'):
                            meta = fn.ursar_fn_metadata
                            if ('listens_to_messages' in meta and meta['listens_to_messages'] and 'listener_regex' in meta):
                                if plugin['class'] in plugin_instances:
                                    instance = plugin_instances[plugin['class']]
                                else:
                                    instance = plugin['class']()
                                    plugin_instances[plugin['class']] = instance

                                self.message_listeners.append({
                                    'full_method_name': '%s.%s' % (plugin['name'], function_name),
                                    'function_name': function_name,
                                    'class_name': plugin['name'],
                                    'regex_pattern': meta['listener_regex'],
                                    'regex': re.compile(meta['listener_regex']),
                                    'fn': getattr(instance, function_name),
                                    'args': meta['listener_args'],
                                    'direct_mentions_only': meta['listens_only_to_direct_mentions']
                                })
                    except Exception as e :
                        print ('Error bootstrapping %s.%s: %s' % (plugin['class'], function_name, e))
            except Exception as e:
                print ('Error bootstrapping %s: %s' % (plugin['class'], e))

    def onEvent(self, event):
        '''
        Handle Skype events
        '''
        if isinstance(event, SkypeNewMessageEvent) and not event.msg.userId == self.userId:
            inGroupChat = self.inGroupChat(event)
            isMentioned = self.isMentioned(event)

            if isMentioned:
                event.msg.content = re.sub(r'\s*<at id="8:%s">.+?</at>\s*' % self.userId, '', event.msg.content)

            for listener in self.message_listeners:
                search_matches = listener['regex'].search(event.msg.content)
                if ((listener['direct_mentions_only'] and (isMentioned or not inGroupChat)) or not listener['direct_mentions_only']) and search_matches:
                    try:
                        args = {'message' : event.msg.content}
                        args.update({key:val for key, val in search_matches.groupdict().items() if val is not None})
                        messageToSend = listener['fn'](**args)
                    except Exception as e:
                        print ("Error while trying to execute %s: %s" % (listener['full_method_name'], e))
                        messageToSend = 'An exception occured while trying to process your request.'

                    if messageToSend:
                        event.msg.chat.sendMsg(messageToSend, rich=True)

    def isMentioned(self, event):
        '''
        Determine if current user is mentioned in message
        '''
        return re.search(r'\s*<at id="8:%s">.+?</at>\s*' % self.userId, event.msg.content) != None

    def inGroupChat(self, event):
        '''
        Determine if current chat is a group chat
        '''
        return 'thread' in event.msg.chatId