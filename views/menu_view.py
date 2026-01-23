"""Zeigt das Start-Menü"""
__author__ = "Miro K."
__copyright__ = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

# IMPORTS
# Arcade Packages
import arcade
import arcade.gui

# Math
from pyglet.math import Vec2

# Game Imports
from components.plant import Plant, PlantManager
from components.zombie import Zombie, ZombieManager
from components.projectile import Projectile, ProjectileManager

from components.gameEngine import GameEngine, UIEngine
from constants import *


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

    def _setup(self):
        pass

    def on_show(self):
        pass

    def on_hide(self):
        pass

    def on_draw(self):
        pass

    def on_update(self, delta_time):
        pass



