__author__ = 'beniamin'

import pygame, sys
import pygame.locals


def handle_quit(event):
    if event.type == pygame.locals.QUIT or (event.type == pygame.locals.KEYUP and event.key == pygame.locals.K_ESCAPE):
        pygame.quit()
        sys.exit()

def drawText(text, font, surface, x, y):
    text_obj = font.render(text, 1, (255, 0, 0))
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)