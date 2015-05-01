__author__ = 'benek'

from Utils.latin_names import latin_names
from random import sample


class Species(object):

    latin_names_used = []

    def __init__(self, life_obj, speciesList):
        self.life_obj = life_obj
        self.speciesList = speciesList
        self.population = 0
        self.name = None
        self.on_change_func = None
        self.on_change_func_args = None
        self.life_objs_list = []
        self.species_label = None
        self.generate_name()

    def generate_name(self):
        name = None
        counter = 0
        while (name is None or name in self.latin_names_used) and counter < 1000:
            name = ' '.join(sample(latin_names, 3))
        if name is None:
            raise ValueError('Too many species - not enough latin names')
        self.name = name

    def increase_population(self, life_obj):
        self.population += 1
        self.life_objs_list.append(life_obj)
        if self.on_change_func is not None:
            self.on_change_func(self, *self.on_change_func_args)

    def decrease_population(self, life_obj):
        """ Return true if species vanishes (population is 0) """
        self.population -= 1
        self.life_objs_list.remove(life_obj)
        if self.on_change_func is not None:
            self.on_change_func(self, *self.on_change_func_args)
        if self.population == 0:
            self.speciesList.species_list.remove(self)
            return True
        else:
            return False

    def set_on_change_func(self, on_change_func, *args):
        self.on_change_func = on_change_func
        self.on_change_func_args = args

