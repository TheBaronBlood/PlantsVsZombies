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
        projectile_sprite_list: arcade.SpriteList
    ) -> None:
        super().__init__(scale=c.SCALE_FACTOR)

        self.name = name
        self.health = health
        self.state = c.IDLE

        self.sprite_texture = None
        self.bullet_texture = None
        self._split_texture(texture)

        self.velocity = Vec2(-speed,0)
        self.lane = None
        self.projectile_sprite_list = projectile_sprite_list


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

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        super().update(delta_time)

        collisions = arcade.check_for_collision_with_list(self, self.projectile_sprite_list)
        if collisions:  # list mit allen getroffenen Projectiles
            for projectile in collisions:
                self.take_damage(projectile.damage)
                # optional: Projectile entfernen, wenn es treffen soll
                projectile.remove_from_sprite_lists()

        if self.health < 0:
            self.kill()



class ZombieNormal(Zombie):
    def __init__(self, projectile_sprite_list: arcade.SpriteList):
        Zombie.__init__(self, "Normal", 100, 1,":sprites:zombie_normal/zombie_normal.png", projectile_sprite_list)

class ZombiePylone(Zombie):
    def __init__(self, projectile_sprite_list: arcade.SpriteList):
        Zombie.__init__(self, "Normal", 200, 1,":sprites:zombie_pylons/zombie_pylon.png", projectile_sprite_list)

class ZombieBucket(Zombie):
    def __init__(self, projectile_sprite_list: arcade.SpriteList):
        Zombie.__init__(self, "Normal", 350, 1,":sprites:zombie_bucket/zombie_bucket.png", projectile_sprite_list)


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

        new_zombie.center_x = 1413.6
        if lane == 1:
            new_zombie.center_y = 501.6
        if lane == 2:
            new_zombie.center_y = 410.40000000000003
        if lane == 3:
            new_zombie.center_y = 319.20000000000005
        if lane == 4:
            new_zombie.center_y = 228.0
        if lane == 5:
            new_zombie.center_y = 136.8

        if lane is None:
            r_lane = random.choice([501.6,410.40000000000003,319.20000000000005,228.0,136.8])
            new_zombie.center_y = r_lane



        self.zombie_sprite_list.append(new_zombie)


