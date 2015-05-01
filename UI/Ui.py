import sys
import pygame
from pygame.locals import *


class Ui(object):

    def __init__(self, mouse, keyboard, gameSpeed, stats_dumper):
        self.mouse = mouse
        self.keyboard = keyboard
        self.gameSpeed = gameSpeed
        self.surfaces = []
        self.stats_dumper = stats_dumper

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.constants.QUIT:
                return self.terminate()
            if event.type == pygame.constants.KEYDOWN:
                if event.key == pygame.constants.K_ESCAPE: # pressing escape quits
                    return self.terminate()
                self.keyboard.keys_down.append(event.key)
            if event.type == pygame.constants.KEYUP:
                if event.key in self.keyboard.keys_down:
                    self.keyboard.keys_down.remove(event.key)
                    self.keyboard.key_pressed = event.key
            if self.keyboard.key_pressed == K_s:
                self.stats_dumper.write_to_file()
            if event.type == MOUSEMOTION:
                self.mouse.x, self.mouse.y = event.pos
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse.pressed = True
                elif event.button == 3:
                    self.mouse.right_pressed = True
                elif event.button in (4, 5):
                    self.mouse.scrolling = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1 and self.mouse.pressed is True:
                    self.mouse.pressed = False
                    self.mouse.clicked = True
                elif event.button == 3 and self.mouse.right_pressed is True:
                    self.mouse.right_pressed = False
                    self.mouse.right_clicked = True
                elif event.button == 5 and self.mouse.scrolling is True:
                    self.mouse.scrolling = False
                    self.mouse.scroll_down = True
                elif event.button == 4 and self.mouse.scrolling is True:
                    self.mouse.scrolling = False
                    self.mouse.scroll_up = True

    def terminate(self):
        self.stats_dumper.write_to_file()
        pygame.quit()
        sys.exit()
