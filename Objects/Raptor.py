__author__ = 'beniamin'

import pygame, random

from Utils.helpers import *
from Objects.Biont import *


class Raptor(Biont):

    type = 'raptor'
    can_eat = ['biont']

    def override_initial_const_params(self):
        super(Raptor, self).override_initial_const_params()
        self.defence = 30
        self.attack = 29
        self.reproducing_interval = 2000
        self.max_energy = 6000  # int
        self.min_healthy_energy = 1500  # int
        self.energy_needed_to_reproduce = 1000
        self.speed = 4.5
        self.uv_radiation_sensitivity = 0.01
        self.chemical_mutagens_sensitivity = 0.3
        self.x_radiation_sensitivity = 0.3
        self.mutation_rate = 1.0

    def override_initial_changeable_params(self):
        super(Raptor, self).override_initial_changeable_params()
        self.energy = random.randint(1500, 2000)  # int
        self.life_expectancy = random.randint(3000, 6000)  # int