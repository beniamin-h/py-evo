__author__ = 'beniamin'


class Namespace(dict):

    def __init__(self, name, file_path, obj={}):
        super(Namespace, self).__init__(obj)
        self.__file_path = file_path
        self.__name = name

    def __dir__(self):
        return tuple(self)

    def __repr__(self):
        return "%s(%s)" % (self.__name, super(Namespace, self).__repr__())

    def __getattribute__(self, name):
        try:
            return self[name]
        except KeyError:
            msg = "'%s' object has no attribute '%s'. Config file path: %s"
            raise AttributeError(msg % (self.__name, name, self.__file_path))

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]
