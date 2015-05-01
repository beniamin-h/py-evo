__author__ = 'benek'

from Objects.Species import Species
import Configs

class SpeciesList(object):

    colors = {
        'Food': (255, 255, 255),
        'Bionts': (165, 255, 165),
        'Raptors': (255, 165, 165)
    }

    def __init__(self, _type):
        self._type = _type
        self.color = self.colors[_type]
        self.species_list = []
        self.speciesListUI = None

    def set_ui(self, speciesListUI):
        self.speciesListUI = speciesListUI

    def add_species(self, life_obj):
        """ Return new Species instance """
        species = Species(life_obj, self)
        self.species_list.append(species)
        return species
