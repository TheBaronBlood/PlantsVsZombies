""""""
__author__ = "Miro K."
__copyright__ = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

import random

# IMPORTS
# Arcade Packages
import arcade
import arcade.gui
from arcade import BasicSprite

# Math
from pyglet.math import Vec2

from components.projectile import ProjectileManager
# Game Imports
import constants as c

class Zombie(arcade.Sprite):
    def __init__(
        self,
        name,
        health,
        speed,
        texture,
    ) -> None:
        super().__init__(scale=c.SCALE_FACTOR)

        self.name = name
        self.health = health
        self.speed = speed
        self.state = c.IDLE
        self.damage = 10
        self.attack_time = 1
        self.rest_time = 0

        self.sprite_texture = None
        self.bullet_texture = None
        self._split_texture(texture)


        self.velocity = Vec2(-self.speed,0)
        self.lane = None


    def _split_texture(self, path):
        sprite_sheet = arcade.load_spritesheet(path)
        texture = sprite_sheet.get_texture_grid((32, 32), 2, 2)
        self.sprite_texture = texture[0]
        self.bullet_texture = texture[1]

        self.texture = texture[0]
    def take_damage(self, damage: int) -> None:
        self.health -= damage


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



class ZombieNormal(Zombie):
    def __init__(self, projectile_sprite_list: arcade.SpriteList):
        Zombie.__init__(self, "Normal", 100, 1,":sprites:zombie_normal/zombie_normal.png")

class ZombiePylone(Zombie):
    def __init__(self, projectile_sprite_list: arcade.SpriteList):
        Zombie.__init__(self, "Normal", 200, 1,":sprites:zombie_pylons/zombie_pylon.png")

class ZombieBucket(Zombie):
    def __init__(self, projectile_sprite_list: arcade.SpriteList):
        Zombie.__init__(self, "Normal", 350, 1,":sprites:zombie_bucket/zombie_bucket.png")


# TODO Zombie VERTIGSTELLEN
class ZombieManager:
    def __init__(
            self,
            zombie_sprite_list: arcade.SpriteList,
            projectileManager: ProjectileManager,
            scene: arcade.scene.Scene,
    ) -> None:
        super().__init__()

        self.zombie_sprite_list = zombie_sprite_list
        self.projectileManager = projectileManager
        self.scene = scene

    def spawn_zombie(self, name: str, lane:int = None):
        new_zombie = None
        if "Normal" == name:
            new_zombie = ZombieNormal(self.projectileManager.projectile_sprite_list)
        if "Pylone" == name:
            new_zombie = ZombiePylone(self.projectileManager.projectile_sprite_list)
        if "Bucket" == name:
            new_zombie = ZombieBucket(self.projectileManager.projectile_sprite_list)


        if lane is None:
            r_lane = random.choice(self.scene["Zombie_Grid"])
            print(r_lane)
            new_zombie.center_y = r_lane.center_y
            new_zombie.center_x = r_lane.center_x
        else:
            new_zombie.center_y = self.scene["Zombie_Grid"][lane-1].center_y
            new_zombie.center_x = self.scene["Zombie_Grid"][lane-1].center_x


        self.zombie_sprite_list.append(new_zombie)


