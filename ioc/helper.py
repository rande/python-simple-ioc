# vim: set fileencoding=utf-8 :

def is_scalar(value):
    return isinstance(value, (str))

def is_iterable(value):
    return isinstance(value, (dict, list))

def get_keys(arguments):
    if isinstance(arguments, (list)):
        return range(len(arguments))

    if isinstance(arguments, (dict)):
        return arguments.iterkeys()

    return []