__author__ = 'beniamin'

import pygame, random

from Utils.helpers import *
from Utils.Exceptions import NoEmptyXYFound


class Life(object):

    mutating_params = [
        'size',
        'nutritional_value',
        'defence',
        'attack',
        'speed',
        'reproducing_interval',
        'reproducing_probability',
        'energy_needed_to_reproduce',
        #'energy_live_cost',
        #'energy_move_cost',
        #'energy_reproduce_cost',
        #'mutation_rate',
        #'mutation_factor',
        #'mutation_inheritance_factor',
    ]
    type = 'food'
    can_eat = []
    marker_rect_color = (0, 0, 0)
    initial_humidity_likeness = 0.9
    initial_temperature_likeness = 0.9

    def __init__(self, xy, size, color, surfaceMap, windowSurface, lifeCollection, _list, random2,
                 environment, parent=None):
        self.setup_initial_const_params(size)
        self.setup_initial_changeable_params()
        self.override_initial_const_params()
        self.override_initial_changeable_params()
        self.recalculate_changeable_params()
        self.setup_private_objs(xy, self.size, color, surfaceMap, windowSurface, lifeCollection, _list, random2,
                                environment)
        if parent is not None:
            self.inherit_params_from_parent(parent)
            self.set_inheritable_params(parent)
            if self.try_to_mutate(parent):
                species = parent.species.speciesList.add_species(self)
                self.set_species(species)
                parent.species.speciesList.speciesListUI.add_new_species(species)
            else:
                self.set_species(parent.species)
        else:
            self.set_initial_inheritable_params()
        self.generate_marker_rect((self.rect.x, self.rect.y), self.size)

    def setup_private_objs(self, xy, size, color, surfaceMap, windowSurface, lifeCollection, _list, random2,
                           environment):
        self.surfaceMap = surfaceMap
        self.windowSurface = windowSurface
        self.rect = pygame.Rect(xy[0], xy[1], size, size)
        self.map_region = self.surfaceMap.set_rect(self.rect, self)
        self.color = color
        self.list = _list
        self.random2 = random2
        self.lifeCollection = lifeCollection
        self.environment = environment

    def generate_marker_rect(self, xy, size):
        self.marker_rect = pygame.Rect(xy[0], xy[1], size, size)
        self.marker_rect_color = list(self.color)
        self.inflate_marker_rect_counter = 0

    def inflate_marker_rect(self):
        self.inflate_marker_rect_counter += 1
        if self.inflate_marker_rect_counter < 10:
            self.marker_rect.inflate_ip(2, 2)
            self.marker_rect_color = [(color - 20 if color > 20 else 0) for color in self.marker_rect_color]
        elif self.inflate_marker_rect_counter < 30:
            self.marker_rect_color = (0, 0, 0)
        else:
            self.generate_marker_rect((self.rect.x, self.rect.y), self.size)

    def setup_initial_const_params(self, size):
        self.size = int(size)  # int
        self.size_float = float(size)  # float
        self.defence = 2  # float
        self.attack = 2  # float
        self.params = {}
        self.speed = 1.0  # float
        self.reproducing_interval = 1000  # int
        self.reproducing_probability = 0.2  # float: 0.0 - 1.0
        self.max_energy = 2000  # int
        self.min_healthy_energy = 1000  # int
        self.energy_needed_to_reproduce = 500  # int
        self.energy_needed_to_move = 10  # int
        self.energy_live_cost = -1  # int
        self.energy_move_cost = 1  # int
        self.energy_reproduce_cost = 100  # int
        self.mutation_rate = 0.0  # float: 0.0 - 1.0  #FIXME: lower by 1  -- NOT
        self.mutation_factor = 0.0  # float: 0.0 - 1.0  #FIXME: lower by 1  -- NOT
        self.mutation_inheritance_factor = 0.3  # float: 0.0 - 1.0  #FIXME: lower by 1  -- NOT
        self.max_nutritional_value_per_size = 200
        self.min_nutritional_value_per_size = 50
        self.nutritional_value = 300
        self.humidity_likeness = self.initial_humidity_likeness
        self.temperature_likeness = self.initial_temperature_likeness
        self.uv_radiation_sensitivity = 1
        self.x_radiation_sensitivity = 1
        self.chemical_mutagens_sensitivity = 1

    def override_initial_const_params(self):
        #Implemented in Biont and Raptor classes
        pass

    def setup_initial_changeable_params(self):
        self.picked_for_test = False
        self.random_move_direction = [0, 0]  # [int:-1,0,1, int:-1,0,1]
        self.last_move_interval = 0  # int
        self.last_reproduce_interval = random.randint(0, self.reproducing_interval)  # int
        self.life_expectancy = random.randint(1000, 2000)  # int
        self.energy = random.randint(500, 1000)  # int
        self.mutated_params = []
        self.health = 1.0
        self.health_checking_interval = random.randint(20, 50)

    def override_initial_changeable_params(self):
        #Implemented in Biont and Raptor classes
        pass

    def inherit_params_from_parent(self, parent):
        self.size = int(parent.inheritable_size)  # float
        self.size_float = float(parent.inheritable_size)  # float
        self.nutritional_value = parent.inheritable_nutritional_value
        self.defence = parent.inheritable_defence
        self.attack = parent.inheritable_attack
        self.speed = parent.inheritable_speed
        self.reproducing_interval = parent.inheritable_reproducing_interval
        self.reproducing_probability = parent.inheritable_reproducing_probability
        self.energy_needed_to_reproduce = parent.inheritable_energy_needed_to_reproduce
        self.energy_needed_to_move = parent.inheritable_energy_needed_to_move
        self.energy_move_cost = parent.inheritable_energy_move_cost
        self.energy_live_cost = parent.inheritable_energy_live_cost

    def recalculate_changeable_params(self):
        self.mutating_params_len = len(self.mutating_params)  # int
        self._generate_defence_random_factor()
        self._generate_attack_random_factor()

    def set_initial_inheritable_params(self):
        self.inheritable_size = float(self.size)  # float
        self.inheritable_nutritional_value = self.nutritional_value
        self.inheritable_defence = self.defence
        self.inheritable_attack = self.attack
        self.inheritable_speed = self.speed
        self.inheritable_reproducing_interval = self.reproducing_interval
        self.inheritable_reproducing_probability = self.reproducing_probability
        self.inheritable_energy_needed_to_reproduce = self.energy_needed_to_reproduce
        self.inheritable_energy_needed_to_move = self.energy_needed_to_move
        self.inheritable_energy_move_cost = self.energy_move_cost
        self.inheritable_energy_live_cost = self.energy_live_cost

    def set_inheritable_params(self, parent):
        self.inheritable_size = float(parent.inheritable_size)  # float
        self.inheritable_nutritional_value = parent.inheritable_nutritional_value
        self.inheritable_defence = parent.inheritable_defence
        self.inheritable_attack = parent.inheritable_attack
        self.inheritable_speed = parent.inheritable_speed
        self.inheritable_reproducing_interval = parent.inheritable_reproducing_interval
        self.inheritable_reproducing_probability = parent.inheritable_reproducing_probability
        self.inheritable_energy_needed_to_reproduce = parent.inheritable_energy_needed_to_reproduce
        self.inheritable_energy_needed_to_move = parent.inheritable_energy_needed_to_move
        self.inheritable_energy_move_cost = parent.inheritable_energy_move_cost
        self.inheritable_energy_live_cost = parent.inheritable_energy_live_cost

    def set_species(self, species):
        self.species = species
        self.species.increase_population(self)

    def draw(self):
        self.windowSurface.fill(self.color, self.rect)

    def draw_marker(self):
        self.inflate_marker_rect()
        pygame.draw.rect(self.windowSurface, self.marker_rect_color, self.marker_rect, 1)

    def live(self):
        self._randomize_params()
        self.move()
        self.try_to_reproduce()
        if self.check_energy():
            if self.check_life_expectancy():
                self.check_health()
                pass

    def check_energy(self):
        self.energy -= self.energy_live_cost - self.environment.calculate_energy_drain_factor(
            self.humidity_likeness, self.temperature_likeness)
        if self.energy < 1:
            self.die()
            return False
        else:
            return True

    def check_life_expectancy(self):
        self.life_expectancy -= 1
        if self.life_expectancy < 0:
            self.die()
            return False
        else:
            return True

    def check_health(self):
        self.health_checking_interval -= 1
        if self.health_checking_interval == 0:
            self.health_checking_interval = random.randint(20, 50)
            factor = (self.energy / float(self.min_healthy_energy) - 1) / 5.0
            factor -= self.environment.calculate_health_harmfulness_factor(
                self.uv_radiation_sensitivity, self.x_radiation_sensitivity, self.chemical_mutagens_sensitivity) / 5.0
            self.health += factor
            if self.health < 0:
                self.die()
                return False
            else:
                return True

    def die(self):
        self.list.remove(self)
        self.surfaceMap.unset_rect(self.rect, self)
        self.species.decrease_population(self)

    def _randomize_params(self):
        """Generate radom factors if randomization_desc_counter is 1 for each param"""
        if self._defence_factor_randomization_desc_counter > 1:
            self._defence_factor_randomization_desc_counter -= 1
        else:
            self._generate_defence_random_factor()
        if self._attack_factor_randomization_desc_counter > 1:
            self._attack_factor_randomization_desc_counter -= 1
        else:
            self._generate_attack_random_factor()

    def _generate_defence_random_factor(self):
        self._defence_random_factor = random.uniform(0, self.defence / 5.0)
        self._defence_factor_randomization_desc_counter = random.randint(100, 1000)

    def _generate_attack_random_factor(self):
        self._attack_random_factor = random.uniform(0, self.attack / 5.0)
        self._attack_factor_randomization_desc_counter = random.randint(100, 1000)

    def move(self):
        if self._check_moving_ability():
            while self.last_move_interval > 1:
                self.last_move_interval -= 1
                x, y = self._random_move()
                if any((x, y)):
                    self._change_xy(x, y)
                    self.energy -= self.energy_move_cost
            else:
                self.last_move_interval += self.speed * self.environment.calculate_speed_factor(
                    self.humidity_likeness, self.temperature_likeness)

    def _change_xy(self, x, y):
        """@param x, y: {-1,0,1}"""
        if self.surfaceMap.is_empty_or_obj_rect_border(self.rect, self, x, y):
            if x == -1:
                self.surfaceMap.unset_col(self.rect.x + self.rect.width - 1, self.rect.y, self.rect.height)
                self.surfaceMap.set_col(self.rect.x - 1, self.rect.y, self.rect.height, self)
            elif x == 1:
                self.surfaceMap.unset_col(self.rect.x, self.rect.y, self.rect.height)
                self.surfaceMap.set_col(self.rect.x + self.rect.width, self.rect.y, self.rect.height, self)
            if x:
                self.rect.move_ip(x, 0)
                self.marker_rect.move_ip(x, 0)
            if y == -1:
                self.surfaceMap.unset_row(self.rect.x, self.rect.y + self.rect.height - 1, self.rect.width)
                self.surfaceMap.set_row(self.rect.x, self.rect.y - 1, self.rect.width, self)
            elif y == 1:
                self.surfaceMap.unset_row(self.rect.x, self.rect.y, self.rect.width)
                self.surfaceMap.set_row(self.rect.x, self.rect.y + self.rect.height, self.rect.width, self)
            if y:
                self.rect.move_ip(0, y)
                self.marker_rect.move_ip(0, y)
            self.surfaceMap.update_region(self.rect, self)

    def _check_moving_ability(self):
        return self.speed > 0 and self.energy >= self.energy_needed_to_move

    def _random_move(self):
        min_x, max_x, min_y, max_y = self._get_move_bounds()
        self._check_random_move_direction(min_x, max_x, min_y, max_y)
        # Horizontal move
        min_x = 0 if self.random_move_direction[0] > 0 else min_x
        max_x = 0 if self.random_move_direction[0] < 0 else max_x
        if max_x - min_x == 1:
            # max_x, min_x: 1, 0 or
            # max_x, min_x: 0, -1
            x = self.random2.rand01() + min_x
        else:  # max_x - min_x == 2
            # max_x, min_x: 1, -1
            x = random.randint(min_x, max_x)
            # Vertical move
        min_y = 0 if self.random_move_direction[1] > 0 else min_y
        max_y = 0 if self.random_move_direction[1] < 0 else max_y
        if max_y - min_y == 1:
            # max_y, min_y: 1, 0 or
            # max_y, min_y: 0, -1
            y = self.random2.rand01() + min_y
        else:  # max_y - min_y == 2
            # max_y, min_y: 1, -1
            y = random.randint(min_y, max_y)
        return x, y

    def _check_random_move_direction(self, min_x, max_x, min_y, max_y):
        """
        Update random_move_direction (2-elems list: x, y), if:
            value == 0: random value between -mapWidth and mapWidth divided by 2
            value > 0: decrease by 1
            value < 0: increase by 1
        """
        if not self.random_move_direction[0] and not self.random_move_direction[1]:
            if min_x and max_x:
                self.random_move_direction[0] = random.randint(0, self.surfaceMap.width / 4) - self.surfaceMap.width / 8
                self.random_move_direction[0] = int(self.random_move_direction[0] * self.speed)
            elif max_x:
                self.random_move_direction[0] = random.randint(0, self.surfaceMap.width) / 8
                self.random_move_direction[0] = int(self.random_move_direction[0] * self.speed)
            elif min_x:
                self.random_move_direction[0] = random.randint(-self.surfaceMap.width, 0) / 8
                self.random_move_direction[0] = int(self.random_move_direction[0] * self.speed)
            if min_y and max_y:
                self.random_move_direction[1] = random.randint(0,
                                                               self.surfaceMap.height / 4) - self.surfaceMap.height / 8
                self.random_move_direction[1] = int(self.random_move_direction[1] * self.speed)
            elif max_y:
                self.random_move_direction[1] = random.randint(0, self.surfaceMap.height) / 8
                self.random_move_direction[1] = int(self.random_move_direction[1] * self.speed)
            elif min_y:
                self.random_move_direction[1] = random.randint(-self.surfaceMap.height, 0) / 8
                self.random_move_direction[1] = int(self.random_move_direction[1] * self.speed)
        else:
            # Vertical move
            if self.random_move_direction[0] < 0:
                if min_x:
                    self.random_move_direction[0] += 1
                else:
                    self.random_move_direction[0] = random.randint(0, self.surfaceMap.width) / 8
                    self.random_move_direction[0] = int(self.random_move_direction[0] * self.speed)
            elif self.random_move_direction[0] > 0:
                if max_x:
                    self.random_move_direction[0] -= 1
                else:
                    self.random_move_direction[0] = random.randint(-self.surfaceMap.width, 0) / 8
                    self.random_move_direction[0] = int(self.random_move_direction[0] * self.speed)
                # Horizontal move
            if self.random_move_direction[1] < 0:
                if min_y:
                    self.random_move_direction[1] += 1
                else:
                    self.random_move_direction[1] = random.randint(0, self.surfaceMap.height) / 8
                    self.random_move_direction[1] = int(self.random_move_direction[1] * self.speed)
            elif self.random_move_direction[1] > 0:
                if max_y:
                    self.random_move_direction[1] -= 1
                else:
                    self.random_move_direction[1] = random.randint(-self.surfaceMap.height, 0) / 8
                    self.random_move_direction[1] = int(self.random_move_direction[1] * self.speed)

    def _get_move_bounds(self):
        return -1 if self.rect.x > 0 else 0, \
               1 if self.rect.x + self.rect.width < self.surfaceMap.width else 0, \
               -1 if self.rect.y > 0 else 0, \
               1 if self.rect.y + self.rect.height < self.surfaceMap.height else 0

    def get_defence_factor(self):
        return (self.defence + self._defence_random_factor) * (self.energy / self.max_energy / 3 + 0.66)

    def get_attack_factor(self):
        return (self.attack + self._attack_random_factor) * (self.energy / self.max_energy / 2 + 0.5)

    def try_to_reproduce(self):
        self.last_reproduce_interval += 1
        if self.energy >= self.energy_needed_to_reproduce and \
                self.last_reproduce_interval > self.reproducing_interval and \
                random.random() < self.reproducing_probability:
            if self.reproduce():
                self.last_reproduce_interval = 0
                self.energy -= self.energy_reproduce_cost

    def reproduce(self):
        sibling = self.surfaceMap.get_empty_sibling(self.rect)
        if sibling:
            #Generate new instance of self class
            child = self.__class__(
                (sibling[0], sibling[1]),
                self.inheritable_size,
                self.color,
                self.surfaceMap,
                self.windowSurface,
                self.lifeCollection,
                self.list,
                self.random2,
                self.environment,
                self
            )
            self.list.append(child)
            return True
        else:
            return False

    def try_to_mutate(self, parent):
        if random.random() <= self.mutation_rate * self.environment.calculate_mutable_factor(
                self.uv_radiation_sensitivity, self.x_radiation_sensitivity, self.chemical_mutagens_sensitivity):
            mutating_param = self.mutating_params[random.randint(0, self.mutating_params_len - 1)]
            if mutating_param == 'size':
                return self.mutate_size(parent)
            elif mutating_param == 'nutritional_value':
                return self.mutate_nutritional_value()
            elif mutating_param == 'defence':
                return self.mutate_defence()
            elif mutating_param == 'attack':
                return self.mutate_attack()
            elif mutating_param == 'speed':
                return self.mutate_speed()
            elif mutating_param == 'reproducing_interval':
                return self.mutate_reproducing_interval()
            elif mutating_param == 'reproducing_probability':
                return self.mutate_reproducing_probability()
            elif mutating_param == 'energy_needed_to_reproduce':
                return self.mutate_energy_needed_to_reproduce()
        else:
            return False

    def _calculate_mutation_factor(self, for_multiplication=True):
        return (1 if for_multiplication else 0) + random.uniform(-self.mutation_factor, self.mutation_factor)

    def _is_mutation_inheritable(self):
        return random.random() <= self.mutation_inheritance_factor

    def mutate_size(self, parent):
        mutation_factor = self._calculate_mutation_factor(False)
        new_size_float = self.size_float * (1 + mutation_factor)
        if new_size_float < 1:
            return False
        new_size_lvl = int(new_size_float)
        self.nutritional_value *= (1 + mutation_factor / 2.0)
        self.defence *= (1 + mutation_factor / 3.0)
        self.attack *= (1 + mutation_factor / 4.0)
        self.speed *= (1 - mutation_factor / 3.0)
        self.size_float = new_size_float
        self.energy_needed_to_move *= (1 + mutation_factor / 2.0)
        self.energy_move_cost *= 1 + mutation_factor
        self.energy_live_cost *= 1 + mutation_factor
        difference = new_size_lvl - self.size
        if difference != 0:
            #if child has new size level we create new rect
            new_rect = pygame.Rect(self.rect.x, self.rect.y, new_size_lvl, new_size_lvl)
            if difference > 0:
                #if child size is bigger than parents
                if self.rect.x < parent.rect.x:
                    #if child was born on the left side of parent we move it to left
                    new_rect = pygame.Rect(new_rect.x - difference, new_rect.y, new_size_lvl, new_size_lvl)
                if self.rect.y < parent.rect.y:
                    #if child was born above parent we move it up
                    new_rect = pygame.Rect(new_rect.x, new_rect.y - difference, new_size_lvl, new_size_lvl)
                if not self.surfaceMap.rect_is_in_map(new_rect) or \
                        not self.surfaceMap.is_empty_or_obj_rect_border(new_rect, self):
                    #if there is no free space we lower mutation to almost new size level
                    #and no need of reset surface Map points
                    self.size_float = self.size + 0.999
                else:
                    #otherwise we have to reset surface Map points
                    self._recalculate_size(new_rect)
            else:
                #also if new size level is lower we reset surface Map points
                self._recalculate_size(new_rect)
        if self._is_mutation_inheritable():
            self.inheritable_size = self.size_float
            self.inheritable_nutritional_value = self.nutritional_value
            self.inheritable_attack = self.attack
            self.inheritable_defence = self.defence
            self.inheritable_speed = self.speed
            self.inheritable_energy_needed_to_move *= self.energy_needed_to_move
            self.inheritable_energy_move_cost *= self.energy_move_cost
            self.inheritable_energy_live_cost *= self.energy_live_cost
            self.mutated_params.append('size')
            return True
        else:
            return False

    def _recalculate_size(self, new_rect):
        self.map_region = self.surfaceMap.set_rect(self.rect, self)
        self.surfaceMap.unset_rect(self.rect, self)
        self.size = int(self.size_float)
        self.rect = new_rect

    def mutate_nutritional_value(self):
        new_nutritional_value = int(self.nutritional_value * self._calculate_mutation_factor())
        if self.max_nutritional_value_per_size * self.size >= new_nutritional_value \
                >= self.min_nutritional_value_per_size * self.size:
            self.nutritional_value = new_nutritional_value
            if self._is_mutation_inheritable():
                self.inheritable_nutritional_value = self.nutritional_value
                self.mutated_params.append('nutritional_value')
                return True
            else:
                return False

    def mutate_defence(self):
        new_defence = self.defence * self._calculate_mutation_factor()
        if new_defence > 0 and self.defence:
            self.defence = new_defence
            if self._is_mutation_inheritable():
                self.inheritable_defence = self.defence
                self.mutated_params.append('defence')
                return True
            else:
                return False

    def mutate_attack(self):
        new_attack = self.attack * self._calculate_mutation_factor()
        if new_attack > 0:
            self.attack = new_attack
            if self._is_mutation_inheritable():
                self.inheritable_attack = self.attack
                self.mutated_params.append('attack')
                return True
            else:
                return False

    def mutate_speed(self):
        factor = self._calculate_mutation_factor(False)
        new_speed = self.speed * (1 + factor)
        if new_speed > 0:
            self.speed = new_speed
            self.energy_needed_to_move *= 1 + factor * 2
            if self._is_mutation_inheritable():
                self.inheritable_speed = self.speed
                self.mutated_params.append('speed')
                return True
            else:
                return False

    def mutate_reproducing_interval(self):
        new_value = self.reproducing_interval * self._calculate_mutation_factor()
        if new_value > 0:
            self.reproducing_interval = new_value
            if self._is_mutation_inheritable():
                self.inheritable_reproducing_interval = new_value
                self.mutated_params.append('reproducing_interval')
                return True
            else:
                return False

    def mutate_reproducing_probability(self):
        new_value = self.reproducing_probability * self._calculate_mutation_factor()
        if 1 > new_value > 0:
            self.reproducing_probability = new_value
            if self._is_mutation_inheritable():
                self.inheritable_reproducing_probability = new_value
                self.mutated_params.append('reproducing_probability')
                return True
            else:
                return False

    def mutate_energy_needed_to_reproduce(self):
        new_value = self.energy_needed_to_reproduce * self._calculate_mutation_factor()
        if 1 > new_value > 0:
            self.energy_needed_to_reproduce = new_value
            if self._is_mutation_inheritable():
                self.inheritable_energy_needed_to_reproduce = new_value
                self.mutated_params.append('energy_needed_to_reproduce')
                return True
            else:
                return False






