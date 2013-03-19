def build_object(object, instance):
    if object.__getattribute__(instance, "_obj") == None:
        container = object.__getattribute__(instance, "_container")
        id = object.__getattribute__(instance, "_id")

        object.__setattr__(instance, "_obj", container.get(id))

class Proxy(object):
    __slots__ = ["_obj", "_container", "_id", "__weakref__"]

    def __init__(self, container, id):
        object.__setattr__(self, "_obj", None)
        object.__setattr__(self, "_container", container)
        object.__setattr__(self, "_id", id)
        
    #
    # proxying (special cases)
    #
    def __getattribute__(self, name):
        build_object(object, self)
        return getattr(object.__getattribute__(self, "_obj"), name)

    def __delattr__(self, name):
        build_object(object, self)
        delattr(object.__getattribute__(self, "_obj"), name)

    def __setattr__(self, name, value):
        build_object(object, self)
        setattr(object.__getattribute__(self, "_obj"), name, value)
    
    def __nonzero__(self):
        build_object(object, self)
        return bool(object.__getattribute__(self, "_obj"))

    def __str__(self):

        build_object(object, self)
        return  "<Proxy " + str(object.__getattribute__(self, "_obj"))  + ">"

    def __repr__(self):
        build_object(object, self)

        return repr(object.__getattribute__(self, "_obj"))
    