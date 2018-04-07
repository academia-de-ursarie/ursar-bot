def hear(regex):
    '''
    Respond to messages not necessarily directed to the bot
    '''
    def wrap(f):
        passed_args = []
        def wrapped_f(*args, **kwargs):
            return f(*args, **kwargs)
        wrapped_f.ursar_fn_metadata = getattr(f, "ursar_fn_metadata", {})
        wrapped_f.ursar_fn_metadata["listens_to_messages"] = True
        wrapped_f.ursar_fn_metadata["listens_only_to_direct_mentions"] = False
        wrapped_f.ursar_fn_metadata["listener_regex"] = regex
        wrapped_f.ursar_fn_metadata["listener_args"] = passed_args
        wrapped_f.ursar_fn_metadata["__doc__"] = f.__doc__
        return wrapped_f
    return wrap

def respond_to(regex):
    '''
    Respond to direct messages, be them either mentions in group chats or messages in private chats
    '''
    def wrap(f):
        passed_args = []
        def wrapped_f(*args, **kwargs):
            return f(*args, **kwargs)
        wrapped_f.ursar_fn_metadata = getattr(f, "ursar_fn_metadata", {})
        wrapped_f.ursar_fn_metadata["listens_to_messages"] = True
        wrapped_f.ursar_fn_metadata["listens_only_to_direct_mentions"] = True
        wrapped_f.ursar_fn_metadata["listener_regex"] = regex
        wrapped_f.ursar_fn_metadata["listener_args"] = passed_args
        wrapped_f.ursar_fn_metadata["__doc__"] = f.__doc__
        return wrapped_f
    return wrap

