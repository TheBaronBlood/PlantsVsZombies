""""""
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

from constants import *




class GameEngine:
    def __init__(self):
        pass

    def _find_tile_at(self, x: float, y: float, sprite_layer: str)-> arcade.Sprite:
        tiles = arcade.get_sprites_at_point((x,y), self.scene[sprite_layer])
        return tiles[0] if tiles else None


class UIEngine:
    pass