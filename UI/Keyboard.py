

class Keyboard(object):

    def __init__(self):
        self.key_pressed = None
        self.keys_down = []

    def clear_events(self):
        self.key_pressed = None

