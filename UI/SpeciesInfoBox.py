__author__ = 'benek'

from UI.Label import Label
from Configs.layout import info_panel as info_panel_config
from pygame import Rect
import pygame.draw


class SpeciesInfoBox(object):

    def __init__(self, ui, surface, font, x, y, species):
        self.ui = ui
        self.surface = surface
        self.species = species
        self.font = font
        self.x = x
        self.y = y
        self.padding = (10, 10, 10, 10)
        self.line_height = 20
        self.width = info_panel_config.width - 1
        self.height = 300
        self.color = (255, 255, 255)
        self.mutated_param_color = (100, 255, 100)
        self.labels = None
        self.border_rect = Rect(self.x, self.y, self.width, self.height)
        self.border_width = 1
        self.border_color = (255, 255, 255)
        self.bg_rect = Rect(self.x + self.border_width, self.y + self.border_width,
                            self.width - self.border_width * 2, self.height - self.border_width * 2)
        self.bg_color = (30, 30, 30)
        self.y_offset = 0
        self._generate_labels()

    def _generate_labels(self):
        self.labels = []
        self.y_offset = self.y + self.padding[0]
        self._add_label('Type: %s' % str(self.species.life_obj.type))
        self._add_label('Size: %.2f' % float(self.species.life_obj.inheritable_size),
                        'size' in self.species.life_obj.mutated_params)
        self._add_label('Nutritional value: %.2f' % float(self.species.life_obj.inheritable_nutritional_value),
                        'nutritional_value' in self.species.life_obj.mutated_params)
        self._add_label('Defence: %.2f' % float(self.species.life_obj.inheritable_defence),
                        'defence' in self.species.life_obj.mutated_params)
        self._add_label('Attack: %.2f' % float(self.species.life_obj.inheritable_attack),
                        'attack' in self.species.life_obj.mutated_params)
        self._add_label('Speed: %.2f' % float(self.species.life_obj.inheritable_speed *
                                              self.species.life_obj.environment.calculate_speed_factor(
                                                  self.species.life_obj.humidity_likeness,
                                                  self.species.life_obj.temperature_likeness)),
                        'speed' in self.species.life_obj.mutated_params)
        self._add_label('Reproducing interval: %.2f' % float(self.species.life_obj.reproducing_interval),
                        'reproducing_interval' in self.species.life_obj.mutated_params)
        self._add_label('Reproducing probability: %.2f' % float(self.species.life_obj.reproducing_probability),
                        'reproducing_probability' in self.species.life_obj.mutated_params)
        self._add_label('Energy needed to reproduce: %.2f' % float(self.species.life_obj.energy_needed_to_reproduce),
                        'energy_needed_to_reproduce' in self.species.life_obj.mutated_params)
        self._add_label('Energy move cost: %.2f' % float(self.species.life_obj.energy_move_cost),
                        'energy_move_cost' in self.species.life_obj.mutated_params)
        self._add_label('Energy live cost: %.2f' % float(self.species.life_obj.energy_live_cost),
                        'energy_live_cost' in self.species.life_obj.mutated_params)

    def _add_label(self, text, param_has_mutated=False):
        self.labels.append(Label(self.ui, self.surface, text,
                                 self.x + self.padding[3], self.y_offset, self.font,
                                 self.color if not param_has_mutated else self.mutated_param_color))
        self.y_offset += self.line_height

    def draw(self, y):
        if y is not None and y + self.line_height != self.y:
            y += self.line_height
            self.border_rect.move_ip(0, y - self.y)
            self.bg_rect.move_ip(0, y - self.y)
            self.y = y
            self._generate_labels()
        pygame.draw.rect(self.surface, self.border_color, self.border_rect, self.border_width)
        pygame.draw.rect(self.surface, self.bg_color, self.bg_rect, 0)
        for label in self.labels:
            label.draw()

