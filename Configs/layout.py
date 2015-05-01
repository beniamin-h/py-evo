__author__ = 'beniamin'

from Utils.Config import *

window = Config('window', __file__)
window.width = 1200
window.height = 800
window.bg_color = (0, 0, 0)
window.FPS = 120
window.def_font = Config('window.def_font', __file__)
window.def_font.size = 15
window.def_font.color = (255, 255, 255)
window.def_font.name = "Sans"
window.small_font = Config('window.small_font', __file__)
window.small_font.size = 10
window.small_font.color = (255, 255, 255)
window.small_font.name = "Sans"

main_panel = Config('main_panel', __file__)
main_panel.width = 1000
main_panel.height = 600
main_panel.left = 0
main_panel.top = 0
main_panel.bg_color = (0, 0, 0)

info_panel = Config('info_panel', __file__)
info_panel.width = 200
info_panel.height = 600
info_panel.left = 1000
info_panel.top = 0
info_panel.bg_color = (0, 0, 0)
info_panel.margin = Config('info_panel.margin', __file__)
info_panel.margin.top = 10
info_panel.margin.right = 10
info_panel.margin.bottom = 10
info_panel.margin.left = 10

stats_panel = Config('stats_panel', __file__)
stats_panel.width = 1200
stats_panel.height = 200
stats_panel.left = 0
stats_panel.top = 600
stats_panel.bg_color = (0, 0, 0)
stats_panel.margin = Config('stats_panel.margin', __file__)
stats_panel.margin.top = 10
stats_panel.margin.right = 10
stats_panel.margin.bottom = 10
stats_panel.margin.left = 10
