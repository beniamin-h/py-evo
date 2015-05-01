

class Mouse(object):

    def __init__(self):
        self.x, self.y = 0, 0
        self.pressed = False
        self.right_pressed = False
        self.clicked = False
        self.right_clicked = False
        self.scrolling = False
        self.scroll_down = False
        self.scroll_up = False

    def is_over_rect(self, rect):
        return rect.collidepoint(self.x, self.y)

    def clear_events(self):
        self.clicked = False
        self.right_clicked = False
        self.scroll_down, self.scroll_up = False, False

