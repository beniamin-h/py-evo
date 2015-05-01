__author__ = 'benek'


class Label(object):

    def __init__(self, ui, surface, text, x, y, font, color, align='left', on_hover=None, on_hover_args=None,
                 on_click=None, on_click_args=None, on_right_click=None, on_right_click_args=None):
        self.ui = ui
        self.surface = surface
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.color = color
        self.align = align
        self.text_obj = None
        self.text_rect = None
        self.on_hover = on_hover
        self.on_hover_args = on_hover_args
        self.on_click = on_click
        self.on_click_args = on_click_args
        self.on_right_click = on_right_click
        self.on_right_click_args = on_right_click_args
        self.generate_label()

    def generate_label(self):
        self.text_obj = self.font.render('%s' % self.text, 1, self.color)
        self.text_rect = self.text_obj.get_rect()
        x = self.x
        if self.align == 'right':
            x -= self.text_rect.width
        elif self.align == 'center':
            x -= self.text_rect.width / 2
        elif self.align != 'left':
            raise ValueError('Invalid value for param align: %s' % self.align)
        self.text_rect.topleft = (x, self.y)

    def draw(self, y=0):
        if y:
            self.y = y
            self.text_rect.top = y
        self.surface.blit(self.text_obj, self.text_rect)
        if self.on_hover is not None and self.ui.mouse.is_over_rect(self.text_rect):
            self.on_hover(*self.on_hover_args)
        if self.on_click is not None and self.ui.mouse.is_over_rect(self.text_rect) and self.ui.mouse.clicked:
            self.on_click(*self.on_click_args)
        if self.on_right_click is not None and self.ui.mouse.is_over_rect(self.text_rect) and self.ui.mouse.right_clicked:
            self.on_right_click(*self.on_right_click_args)


