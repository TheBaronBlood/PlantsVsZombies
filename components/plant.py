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
from components.gameEngine import GameEngine, UIEngine
import constants as c



class PlantManager:
    def __init__(
        self,
        plant_sprite_list: arcade.SpriteList,
        scene: arcade.scene.Scene,
    ) -> None:
        super().__init__()


    def create_plant(self):
        pass

    def spawn_plant(self) -> None:
        pass

    def on_update(self, delta_time: float) -> None:
        pass

class Plant(arcade.Sprite):
    def __init__(
        self,
        name,
        health,
        sprite_texture,
        bullet_texture,
    ) -> None:
        super().__init__()

        self.name = name
        self.health = health
        self.state = c.IDLE

        self.sprite_texture = sprite_texture
        self.bullet_texture = bullet_texture


    def take_damage(self, damage: int) -> None:
        pass

    def get_pos(self):
        pass

    def idling(self):
        pass
    def attacking(self):
        pass
    def setIdle(self):
        self.state = c.IDLE
    def setAttack(self):
        self.state = c.ATTACK

    def handleState(self):
        if self.state == c.IDLE:
            self.idling()
        elif self.state == c.ATTACK:
            self.attacking()





class Sun(Plant):
    pass

class Sunflower(Plant):
    pass

class PeaShooter(Plant):
    pass

class Walnut(Plant):
    pass