from UI.Label import Label
import pygame.constants


class EnvironmentUI(object):

    def __init__(self, ui, surface, panel_layout_config, font, environment):
        self.ui = ui
        self.surface = surface
        self.panel_layout_config = panel_layout_config
        self.font = font
        self.environment = environment
        self.x = self.panel_layout_config.left + self.panel_layout_config.margin.left
        self.y = self.panel_layout_config.top + 310
        self.line_height = 21
        self.font_color = (255, 255, 255)
        self._generate_labels()

    def _generate_labels(self):
        y = self.y
        y_ref = [y]
        self.labels = []
        self.labels.append(self._generate_label(
            'Humidity - %i%%' % round(self.environment.humidity * 100), y_ref, 'humidity'))
        self.labels.append(self._generate_label(
            'Insolation - %i%%' % round(self.environment.insolation * 100), y_ref, 'insolation'))
        self.labels.append(self._generate_label(
            'Temperature - %i%%' % round(self.environment.temperature * 100), y_ref, None))
        self.labels.append(self._generate_label(
            'UV radiation - %i%%' % round(self.environment.uv_radiation * 100), y_ref, 'uv_radiation'))
        self.labels.append(self._generate_label(
            'X radiation - %i%%' % round(self.environment.x_radiation * 100), y_ref, 'x_radiation'))
        self.labels.append(self._generate_label(
            'Chemical mutagens - %i%%' % round(self.environment.chemical_mutagens * 100), y_ref,
            'chemical_mutagens'))

    def _generate_label(self, text, y_ref, property_name):
        y_ref[0] += self.line_height
        return Label(self.ui, self.surface, text, self.x, y_ref[0], self.font, self.font_color,
                     on_click=self.change_param, on_click_args=[property_name, 1],
                     on_right_click=self.change_param, on_right_click_args=[property_name, -1])

    def change_param(self, property_name, change):
        if property_name is None:
            return
        if pygame.constants.K_LSHIFT in self.ui.keyboard.keys_down or \
                pygame.constants.K_RSHIFT in self.ui.keyboard.keys_down :
            change *= 5
        property_value = getattr(self.environment, property_name)
        setattr(self.environment, property_name, property_value + change / 100.0)
        self._generate_labels()

    def draw(self):
        for label in self.labels:
            label.draw()
