# vim: set fileencoding=utf-8 :

class UnknownService(Exception):
    pass

class UnknownParameter(Exception):
    pass

class RecursiveParameterResolutionError(Exception):
    pass

class CyclicReference(Exception):
    pass
    
class LoadingError(Exception):
    pass

class DuplicateServiceDefinition(Exception):
    pass

class ParameterHolderIsFrozen(Exception):
    pass

class AbstractDefinitionInitialization(Exception):
    pass