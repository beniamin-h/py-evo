__author__ = 'benek'

from UI.Label import Label
from UI.SpeciesInfoBox import SpeciesInfoBox
from pygame import Rect
import pygame.draw


class SpeciesListUI(object):

    def __init__(self, ui, surface, speciesInfoBoxSurface, panel_layout_config, font, speciesListDict):
        self.ui = ui
        self.surface = surface
        self.panel_layout_config = panel_layout_config
        self.font = font
        self.speciesListDict = speciesListDict
        self.speciesInfoBoxSurface = speciesInfoBoxSurface
        self.line_height = 20
        self.color = (255, 255, 255)
        self.page_ctrl_buttons_colors = (235, 235, 0)
        self.y_offset = self.panel_layout_config.top + self.panel_layout_config.margin.top + 100
        self.labels = []
        self.page = 0
        self.labels_per_page = 20 # divided by 2 = number of species
        self._generate_initial_species_labels()
        self._delegate_ui_to_species_list()
        self._generate_page_ctrl_buttons()

    def _generate_page_ctrl_buttons(self):
        self.page_ctrl_buttons = {'up': Rect(
            self.panel_layout_config.left + self.panel_layout_config.width - 25,
            self.panel_layout_config.top + self.panel_layout_config.margin.top + 82,
            20, 10
        ), 'down': Rect(
            self.panel_layout_config.left + self.panel_layout_config.width - 25,
            self.panel_layout_config.top + self.panel_layout_config.margin.top + 302,
            20, 10
        )}

    def _delegate_ui_to_species_list(self):
        for species_list_key in self.speciesListDict:
            self.speciesListDict[species_list_key].set_ui(self)

    def _generate_label(self, text, color, y, align='left', on_hover=None, on_hover_args=None):
        if align == 'left':
            x = self.panel_layout_config.left + self.panel_layout_config.margin.left
        elif align == 'right':
            x = self.panel_layout_config.left + self.panel_layout_config.width - self.panel_layout_config.margin.right
        elif align == 'center':
            x = self.panel_layout_config.left + self.panel_layout_config.width / 2
        else:
            raise ValueError('Invalid value for param align: %s' % align)
        return Label(self.ui, self.surface, text, x, y, self.font, color, align, on_hover, on_hover_args)

    def update_label_population(self, species, species_label, population_label):
        if species.population == 0:
            self.remove_species(species_label, population_label)
        else:
            population_label.text = species.population
            population_label.generate_label()
            self.sort_species_labels_by_population()

    def sort_species_labels_by_population(self):
        indexes = {}
        new_labels = []
        for index, label in enumerate(self.labels):
            if index % 2:  # population label
                if label.text in indexes.keys():
                    indexes[label.text] = indexes[label.text] + (self.labels[index - 1], self.labels[index])
                else:
                    indexes[label.text] = (self.labels[index - 1], self.labels[index])
        for species_groups in sorted(indexes.items())[::-1]:
            for species in species_groups[1]:
                new_labels.append(species)
        self.labels = new_labels

    def on_species_label_hover(self, species_info_box, species):
        self.show_species_info_box(species_info_box, species.species_label.y)
        for life_obj in species.life_objs_list:
            life_obj.draw_marker()

    def show_species_info_box(self, species_info_box, y):
        species_info_box.draw(y)

    def add_new_species(self, species):
        species_info_box = SpeciesInfoBox(self.ui, self.speciesInfoBoxSurface, self.font,
                                          self.panel_layout_config.left, 0, species)
        species_label = self._generate_label(species.name, species.speciesList.color, self.y_offset,
                                             on_hover=self.on_species_label_hover,
                                             on_hover_args=[species_info_box, species])
        species.species_label = species_label
        population_label = self._generate_label(species.population, species.speciesList.color, self.y_offset, 'right')
        self.labels.append(species_label)
        self.labels.append(population_label)
        species.set_on_change_func(self.update_label_population, species_label, population_label)

    def remove_species(self, species_label, population_label):
        self.labels.remove(species_label)
        self.labels.remove(population_label)

    def _generate_initial_species_labels(self):
        for species_list in self.speciesListDict:
            for species in self.speciesListDict[species_list].species_list:
                self.add_new_species(species)

    def draw(self):
        i = 0
        y = self.y_offset
        for label in self.labels[self.page * self.labels_per_page:(self.page + 1) * self.labels_per_page]:
            label.draw((i / 2) * self.line_height + y)
            i += 1
            if self.labels_per_page == i:
                break
        self.draw_page_ctrl_buttons()

    def draw_page_ctrl_buttons(self):
        pages = len(self.labels) / self.labels_per_page
        for btn_idx in self.page_ctrl_buttons:
            btn_rect = self.page_ctrl_buttons[btn_idx]
            if btn_idx == 'up':
                if not self.page:
                    continue
                x1, y1 = btn_rect.left, btn_rect.top + btn_rect.height
                x2, y2 = btn_rect.left + btn_rect.width, btn_rect.top + btn_rect.height
                x3, y3 = btn_rect.left + btn_rect.width / 2, btn_rect.top
                if self.ui.mouse.is_over_rect(btn_rect) and self.ui.mouse.clicked:
                    self.page -= 1
            else:  # btn down
                if self.page >= pages:
                    continue
                x1, y1 = btn_rect.left, btn_rect.top
                x2, y2 = btn_rect.left + btn_rect.width, btn_rect.top
                x3, y3 = btn_rect.left + btn_rect.width / 2, btn_rect.top + btn_rect.height
                if self.ui.mouse.is_over_rect(btn_rect) and self.ui.mouse.clicked:
                    self.page += 1
            pygame.draw.polygon(self.surface, self.page_ctrl_buttons_colors, [
                [x1, y1],
                [x2, y2],
                [x3, y3]], 0)


