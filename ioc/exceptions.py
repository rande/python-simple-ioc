# vim: set fileencoding=utf-8 :

# import exceptions

class UnknownService(Exception):
    pass

class UnknownParameter(Exception):
    pass

class CyclicReference(Exception):
    pass
    
class LoadingError(Exception):
    pass