__author__ = 'beniamin'

from Utils.Namespace import *


class Config(Namespace):

    def __setattr__(self, name, value):
        if not name in self:
            self[name] = value
        else:
            raise UserWarning('Property %s of %s already exists. Config file path: %s'
                              % (name, self.__name, self.__file_path))

    def override(self, name, value):
        self[name] = value

