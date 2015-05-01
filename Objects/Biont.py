__author__ = 'beniamin'

import pygame, random

from Utils.helpers import *
from Objects.Life import *


class Biont(Life):

    type = 'biont'
    can_eat = ['food']

    def override_initial_const_params(self):
        self.defence = 20
        self.attack = 12
        self.speed = 6.0
        self.params['receptors'] = {
            'chemo': 40,
            'termo': 0,
            'elektro': 0,
            'magneto': 0,
            'sight': 0,
            'smell': 0,
            'hear': 0
        }
        self.nutritional_value = 800
        self.reproducing_interval = 100
        self.reproducing_probability = 0.2
        self.max_energy = 4000
        self.min_healthy_energy = 1000  # int
        self.energy_needed_to_reproduce = 1000
        self.energy_needed_to_move = 20
        self.energy_live_cost = 1
        self.energy_move_cost = 2
        self.energy_reproduce_cost = 200
        self.mutation_rate = 1.0  # float: > 0.0 - 1.0
        self.mutation_factor = 0.3  # float: 0.0 - 1.0

    def override_initial_changeable_params(self):
        self.energy = random.randint(500, 1000)
        self.life_expectancy = random.randint(2000, 3000)  # int

    def move(self):
        if self._check_moving_ability():
            if self.last_move_interval > 1:
                self.last_move_interval -= 1
                prey = None
                if self.energy < self.max_energy:
                    x, y, prey = self._search_for_prey()
                if prey is None:
                    x, y = self._random_move()
                else:
                    self._try_to_eat(prey)
                if any((x, y)):
                    self._change_xy(x, y)
                    self.energy -= self.energy_move_cost
            else:
                self.last_move_interval += self.speed * self.environment.calculate_speed_factor(
                    self.humidity_likeness, self.temperature_likeness)

    def _search_for_prey(self):
        prey = None
        if any(self.params['receptors']):
            x = self.rect.centerx / 25
            y = self.rect.centery / 25
            min_x = x - 1 if x > 0 else x
            min_y = y - 1 if y > 0 else y
            max_x = x + 2 if x + 1 < self.surfaceMap.width / 25 else x + 1 if x < self.surfaceMap.width / 25 else x
            max_y = y + 2 if y + 1 < self.surfaceMap.height / 25 else y + 1 if y < self.surfaceMap.height / 25 else y
            for _x in xrange(min_x, max_x):
                for _y in xrange(min_y, max_y):
                    for obj in self.surfaceMap.regions[_x][_y]:
                        if obj != self and obj.get_defence_factor() < self.get_attack_factor() and obj.type in self.can_eat:
                            dist = distance(obj.rect.centerx, obj.rect.centery, self.rect.centerx, self.rect.centery)
                            if dist <= self.params['receptors']['chemo'] + self.size / 2.0:
                                if prey is None or dist < prey[1]:
                                    prey = (obj, dist)
        min_x, max_x, min_y, max_y = self._get_move_bounds()
        if prey:
            return min_x if prey[0].rect.x < self.rect.x else max_x if prey[0].rect.x > self.rect.x else 0, \
                   min_y if prey[0].rect.y < self.rect.y else max_y if prey[0].rect.y > self.rect.y else 0, \
                   prey[0]
        else:
            return 0, 0, None

    def _try_to_eat(self, prey):
        rect = self.rect.copy()
        rect.inflate_ip(2, 2)
        if rect.colliderect(prey.rect):
            self._eat(prey)

    def _eat(self, prey):
        prey.die()
        self.energy += prey.nutritional_value


