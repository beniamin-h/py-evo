__author__ = 'beniamin'

import pygame
import random

from Objects.LifeCollection import LifeCollection
from Utils.helpers import *
from Utils.SurfaceMap import SurfaceMap
from Utils.Random2 import Random2
from Utils.Exceptions import NoEmptyXYFound
from UI.SpeciesListUI import SpeciesListUI
from Objects.SpeciesList import SpeciesList
from UI.Ui import Ui
from UI.Mouse import Mouse
from UI.Keyboard import Keyboard
from UI.GameSpeed import GameSpeed
from Objects.Environment import Environment
from UI.EnvironmentUI import EnvironmentUI
from UI.StatsGridUI import StatsGridUI
from Utils.StatsDeque import StatsDeque
from Utils.StatsDumper import StatsDumper
from Objects.Life import Life

import Configs.layout

random2 = Random2()

pygame.init()
pygame.display.set_caption('Evo')

mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((Configs.layout.window.width, Configs.layout.window.height))
defFont = pygame.font.SysFont(Configs.layout.window.def_font.name, Configs.layout.window.def_font.size)
smallFont = pygame.font.SysFont(Configs.layout.window.small_font.name, Configs.layout.window.small_font.size)

speciesInfoBoxSurface = pygame.Surface((Configs.layout.window.width, Configs.layout.window.height),
                                       pygame.SRCALPHA, 32)
surfaceMap = SurfaceMap(Configs.layout.main_panel.width, Configs.layout.main_panel.height)
environment = Environment()
stats_dumper = StatsDumper(environment)
ui = Ui(Mouse(), Keyboard(), GameSpeed(), stats_dumper)

environmentUI = EnvironmentUI(ui, windowSurface, Configs.layout.info_panel, defFont, environment)

lifeCollection = LifeCollection(surfaceMap, windowSurface, random2, {
    'food': SpeciesList('Food'),
    'bionts': SpeciesList('Bionts'),
    'raptors': SpeciesList('Raptors')
}, environment)

lifeCollection.generateInitialFood(2, 100)
lifeCollection.generateInitialBionts(6, 5)
lifeCollection.generateInitialRaptors(10, 5)
groups = [lifeCollection.food, lifeCollection.bionts, lifeCollection.raptors]
speciesListUI = SpeciesListUI(ui, windowSurface, speciesInfoBoxSurface, Configs.layout.info_panel, smallFont,
                              lifeCollection.speciesListDict)

food_count = StatsDeque()
bionts_count = StatsDeque()
raptors_count = StatsDeque()


statsGridUI = StatsGridUI(ui, windowSurface, Configs.layout.stats_panel, smallFont,
                          [food_count, bionts_count, raptors_count])

#lifeCollection.bionts[0].picked_for_test = True

counter = 0

while True:

    ui.handle_events(pygame.event.get())
    ui.gameSpeed.handle_keyboard_events(ui.keyboard)

    windowSurface.fill(Configs.layout.window.bg_color)
    speciesInfoBoxSurface.fill(0)

    if not ui.gameSpeed.game_paused:
        if random.random() < environment.calculate_reproducing_factor(
                Life.initial_humidity_likeness, Life.initial_temperature_likeness):
            try:
                lifeCollection.addSingleFood(2)
            except NoEmptyXYFound:
                pass
        for group in groups:
            for obj in group:
                obj.live()
        if counter % 10 == 0:
            food_count.add(len(lifeCollection.food))
            bionts_count.add(len(lifeCollection.bionts))
            raptors_count.add(len(lifeCollection.raptors))
            if counter % 100 == 0:
                stats_dumper.dumps(lifeCollection, counter / 100)
        counter += 1

    for group in groups:
        for obj in group:
            obj.draw()

    environmentUI.draw()
    speciesListUI.draw()
    statsGridUI.draw()
    windowSurface.blit(speciesInfoBoxSurface, (0, 0))

    drawText('FPS: %s' % mainClock.get_fps(), defFont, windowSurface,
             Configs.layout.info_panel.left + Configs.layout.info_panel.margin.left,
             Configs.layout.info_panel.top + Configs.layout.info_panel.margin.top)

    if len(lifeCollection.speciesListDict['food'].species_list):
        drawText('Food: %i' % len(lifeCollection.food), defFont, windowSurface,
                 Configs.layout.info_panel.left + Configs.layout.info_panel.margin.left,
                 Configs.layout.info_panel.top + Configs.layout.info_panel.margin.top + 20)

    if len(lifeCollection.speciesListDict['bionts'].species_list):
        drawText('Bionts: %i' % len(lifeCollection.bionts), defFont, windowSurface,
                 Configs.layout.info_panel.left + Configs.layout.info_panel.margin.left,
                 Configs.layout.info_panel.top + Configs.layout.info_panel.margin.top + 40)

    if len(lifeCollection.speciesListDict['raptors'].species_list):
        drawText('Raptors: %i' % len(lifeCollection.raptors), defFont, windowSurface,
                 Configs.layout.info_panel.left + Configs.layout.info_panel.margin.left,
                 Configs.layout.info_panel.top + Configs.layout.info_panel.margin.top + 60)

    ui.mouse.clear_events()
    ui.keyboard.clear_events()
    pygame.display.update()
    mainClock.tick(Configs.layout.window.FPS)
