__author__ = 'beniamin'

import Configs.layout
import Configs.life
from Objects.Life import Life
from Objects.Biont import Biont
from Objects.Raptor import Raptor
from Utils.Exceptions import NoEmptyXYFound


class LifeCollection(object):
    def __init__(self, surfaceMap, windowSurface, random2, speciesListDict, environment):
        self.surfaceMap = surfaceMap
        self.windowSurface = windowSurface
        self.random2 = random2
        self.food = []
        self.bionts = []
        self.raptors = []
        self.speciesListDict = speciesListDict
        self.environment = environment
        self.initialSpeciesDict = {}

    @staticmethod
    def _get_min_max_xy(margin):
        return Configs.layout.main_panel.left + margin, \
               Configs.layout.main_panel.left + Configs.layout.main_panel.width - margin, \
               Configs.layout.main_panel.top + margin, \
               Configs.layout.main_panel.top + Configs.layout.main_panel.height - margin

    def generateInitialFood(self, size, amount):
        min_x, max_x, min_y, max_y = self._get_min_max_xy(10)
        self.food = []
        species = None
        for i in xrange(amount):
            try:
                life_obj = Life(self.surfaceMap.find_empty_xy_randomly(min_x, max_x, min_y, max_y, size),
                                size,
                                Configs.life.food.color,
                                self.surfaceMap,
                                self.windowSurface,
                                self,
                                self.food,
                                self.random2,
                                self.environment)
                if i == 0:
                    species = self.speciesListDict['food'].add_species(life_obj)
                life_obj.set_species(species)
                self.food.append(life_obj)
            except NoEmptyXYFound:
                pass
        self.initialSpeciesDict['food'] = species

    def generateInitialBionts(self, size, amount):
        min_x, max_x, min_y, max_y = self._get_min_max_xy(20)
        self.bionts = []
        species = None
        for i in xrange(amount):
            try:
                life_obj = Biont(self.surfaceMap.find_empty_xy_randomly(min_x, max_x, min_y, max_y, size),
                                 size,
                                 Configs.life.biont.color,
                                 self.surfaceMap,
                                 self.windowSurface,
                                 self,
                                 self.bionts,
                                 self.random2,
                                 self.environment)
                if i == 0:
                    species = self.speciesListDict['bionts'].add_species(life_obj)
                life_obj.set_species(species)
                self.bionts.append(life_obj)
            except NoEmptyXYFound:
                pass
        self.initialSpeciesDict['bionts'] = species

    def generateInitialRaptors(self, size, amount):
        min_x, max_x, min_y, max_y = self._get_min_max_xy(30)
        self.raptors = []
        species = None
        for i in xrange(amount):
            try:
                life_obj = Raptor(self.surfaceMap.find_empty_xy_randomly(min_x, max_x, min_y, max_y, size),
                                  size,
                                  Configs.life.raptor.color,
                                  self.surfaceMap,
                                  self.windowSurface,
                                  self,
                                  self.raptors,
                                  self.random2,
                                  self.environment)
                if i == 0:
                    species = self.speciesListDict['raptors'].add_species(life_obj)
                life_obj.set_species(species)
                self.raptors.append(life_obj)
                life_obj.energy += 1000
            except NoEmptyXYFound:
                pass
        self.initialSpeciesDict['raptors'] = species

    def addSingleFood(self, size):
        min_x, max_x, min_y, max_y = self._get_min_max_xy(10)
        life_obj = Life(self.surfaceMap.find_empty_xy_randomly(min_x, max_x, min_y, max_y, size),
                        size,
                        Configs.life.food.color,
                        self.surfaceMap,
                        self.windowSurface,
                        self,
                        self.food,
                        self.random2,
                        self.environment)
        self.food.append(life_obj)
        if self.initialSpeciesDict['food'] is not None:
            if self.initialSpeciesDict['food'] not in self.speciesListDict['food'].species_list:
                self.speciesListDict['bionts'].species_list.append(self.initialSpeciesDict['food'])
            species = self.initialSpeciesDict['food']
        else:
            species = self.speciesListDict['bionts'].add_species(life_obj)
            self.initialSpeciesDict['food'] = species
        life_obj.set_species(species)


