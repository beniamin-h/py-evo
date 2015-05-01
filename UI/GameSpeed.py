import pygame


class GameSpeed(object):

    def __init__(self):
        self.game_speed = 1
        self.game_paused = False
        self._last_game_speed = 1

    def change_speed(self, new_speed):
        self.game_speed = new_speed

    def pause_game(self):
        self._last_game_speed = self.game_speed \
            if self.game_speed != 0 else self._last_game_speed
        self.game_paused = True
        self.change_speed(0)

    def unpause_game(self):
        self.game_paused = False
        self.change_speed(self._last_game_speed)

    def handle_keyboard_events(self, keyboard):
        if keyboard.key_pressed == pygame.constants.K_SPACE:
            self.game_paused = not self.game_paused

