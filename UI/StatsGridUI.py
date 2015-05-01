from UI.Label import Label
import pygame


class StatsGridUI(object):

    def __init__(self, ui, surface, panel_layout_config, font, statsCollection):
        self.ui = ui
        self.surface = surface
        self.statsCollection = statsCollection
        self.font = font
        self.font_color = (255, 255, 255)
        self.x = panel_layout_config.left + panel_layout_config.margin.left
        self.y = panel_layout_config.top + panel_layout_config.margin.top
        self.stats_labels_width = 200
        self.stats_labels_left_padding = 5
        self.multiple_scales = False
        self.grid_width = panel_layout_config.width - self.stats_labels_width - panel_layout_config.margin.left - \
                          panel_layout_config.margin.right
        self.grid_height = panel_layout_config.height - panel_layout_config.margin.top - panel_layout_config.margin.bottom
        self.panel_width = panel_layout_config.width
        self.panel_height = panel_layout_config.height
        self.grid_border_color = (255, 255, 255)
        self.grid_border_width = 1
        self.line_height = 10
        self.border_rect = pygame.Rect(self.x, self.y, self.grid_width, self.grid_height)
        self.colors = [(255, 255, 255), (0, 255, 0), (255, 0, 0)]
        self.global_max = 0
        self.max_per_stats = [0] * len(self.statsCollection)
        self.labels = None
        self._generate_labels()

    def _generate_labels(self):
        self.labels = []
        max_value = '/'.join(map(str, self.max_per_stats)) if self.multiple_scales else self.global_max
        switch_to = 'click to switch to one scale' if self.multiple_scales else 'click to switch to multiple scales'
        self.labels.append(Label(self.ui, self.surface, '%s - %s' % (max_value, switch_to),
                                 self.x + self.grid_width + self.stats_labels_left_padding,
                                 self.y, self.font, self.font_color,
                                 on_click=self.switch_scale, on_click_args=[]))
        self.labels.append(Label(self.ui, self.surface, 0,
                                 self.x + self.grid_width + self.stats_labels_left_padding,
                                 self.y + self.grid_height - self.line_height, self.font, self.font_color))

    def switch_scale(self):
        self.multiple_scales = not self.multiple_scales
        self._generate_labels()

    def draw(self):
        pygame.draw.rect(self.surface, self.grid_border_color, self.border_rect, self.grid_border_width)
        max_value = 0
        for stats_i, stats in enumerate(self.statsCollection):
            stats_max = max(stats.list) / 10 * 10 + 10
            if self.multiple_scales:
                if stats_max != self.max_per_stats[stats_i]:
                    self.max_per_stats[stats_i] = stats_max
                    self._generate_labels()
                max_value = self.max_per_stats[stats_i]
            else:
                max_value = stats_max if stats_max > max_value else max_value
                if self.global_max != max_value:
                    self.global_max = max_value
                    self._generate_labels()
            min_value = 0
            if max_value > min_value:
                for i, value in enumerate(stats.list):
                    if i == 0:
                        continue
                    y = self.y + self.grid_height - int(float(value - min_value) / (max_value - min_value) * self.grid_height)
                    x = self.x + i + 1
                    prev_y = self.y + self.grid_height - int(float(stats.list[i - 1] - min_value) /
                                                             (max_value - min_value) * self.grid_height)
                    prev_x = self.x + i
                    pygame.draw.aaline(self.surface, self.colors[stats_i], (x, y), (prev_x, prev_y))
        for label in self.labels:
            label.draw()