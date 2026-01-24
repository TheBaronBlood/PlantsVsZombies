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
from constants import *


# TODO Zombie VERTIGSTELLEN
class ZombieManager:
    def __init__(
            self,
            zombie_sprite_list: arcade.SpriteList,
            scene: arcade.scene.Scene,
    ) -> None:
        super().__init__()

        self.zombie_sprite_list = zombie_sprite_list
        self.scene = scene



class Zombie(arcade.Sprite):
    pass
