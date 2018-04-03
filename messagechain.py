import re
import inspect

class MessageChain():
    _chain = {}
    def on_message(self, message):
        def fun(original_function):
            self._chain[message] = original_function
        return fun

    def run(self, message):
        for key, fn in self._chain.items():
            matchers = re.match(key, message)
            if matchers:
                argsSpec = inspect.getfullargspec(fn)
                if len(argsSpec.args) is not 0:
                    return fn(matchers)
                else:
                    return fn()
        return None