""""""
__author__ = "Miro K."
__copyright__ = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

import math
import random
import time

# IMPORTS
# Arcade Packages
import arcade
import arcade.gui
from arcade.math import lerp_2d

# Math
from pyglet.math import Vec2
from components.projectile import Projectile, ProjectileManager
# Game Imports
import constants as c


class Plant(arcade.Sprite):
    def __init__(
        self,
        name,
        health,
        texture,
    ) -> None:
        super().__init__(scale=c.SCALE_FACTOR)

        self.name = name
        self.health = health
        self.state = c.IDLE
        self.shoot_timer = 0

        self.sprite_texture = None
        self.bullet_texture = None
        self._split_texture(texture)


    def _split_texture(self, path):
        sprite_sheet = arcade.load_spritesheet(path)
        texture = sprite_sheet.get_texture_grid((32, 32), 2, 2)
        self.sprite_texture = texture[0]
        self.bullet_texture = texture[1]

        self.texture = texture[0]
    def take_damage(self, damage: int) -> None:
        self.health-= damage

    def get_pos_vec_2d(self):
        return Vec2(self.center_x,self.center_y)

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
    def __init__(self, start: Vec2, target: Vec2):
        Plant.__init__(self,
                       "sun",
                       0,
                       ":sprites:sunflower/sunflower.png")

        self.texture = self.bullet_texture



        self.value = 25

        self.p0 = start
        self.p2 = target

        mid = (start + target) / 2
        self.p1 = mid + Vec2(0, random.uniform(40, 80))

        self.t = 0.0
        self.speed = 0.8
        self.finished = False

        self.center_x = start.x
        self.center_y = start.y

        # TODO - IDLE klasse definieren

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        super().update(delta_time)
        def bezier_quad(p0: Vec2, p1: Vec2, p2: Vec2, t: float) -> Vec2:
            return (
                    (1 - t) ** 2 * p0 +
                    2 * (1 - t) * t * p1 +
                    t ** 2 * p2
            )

        if self.finished:
            return

        self.t += delta_time * self.speed

        if self.t >= 1.0:
            self.t = 1.0
            self.finished = True

        pos = bezier_quad(self.p0, self.p1, self.p2, self.t)
        self.center_x = pos.x
        self.center_y = pos.y


class Sunflower(Plant):
    def __init__(self, sun_sprite_list):
        Plant.__init__(self,
                       "sunflower",
                       100,
                       ":sprites:sunflower/sunflower.png")#

        self.sun_sprite_list = sun_sprite_list

    def random_point_in_radius(self, center: Vec2, radius: float) -> Vec2:
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(radius * 0.4, radius)
        return Vec2(
            center.x + math.cos(angle) * r,
            center.y + math.sin(angle) * r
        )

    def idling(self) -> None:
        start = self.get_pos_vec_2d()
        target = self.random_point_in_radius(start, radius=120)

        sun = Sun(start, target)
        self.sun_sprite_list.append(sun)

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.shoot_timer += delta_time
        SHOOT_COOLDOWN = random.randint(5, 20)
        if self.shoot_timer >= SHOOT_COOLDOWN:
            self.idling()
            self.shoot_timer = 0.0

class PeaShooter(Plant):
    def __init__(self, projectile_manager: ProjectileManager):
        Plant.__init__(self,
                       "peashooter",
                       100,
                       ":sprites:peashooter/peashooter.png")

        self.projectile_manager = projectile_manager


        # TODO erstellen das man einfach durch Namenkonventioinen die richtige sprites geladen werden

    def attacking(self):
        self.projectile_manager.spawn_projectile(Projectile(self.center_x, self.center_y, 5, 10, self.bullet_texture))


    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.shoot_timer += delta_time
        SHOOT_COOLDOWN = 1
        if self.shoot_timer >= SHOOT_COOLDOWN:
            self.attacking()
            self.shoot_timer = 0.0

class Repeater(Plant):
    def __init__(self, projectile_manager: ProjectileManager):
        Plant.__init__(self,
                       "repeater",
                       100,
                       ":sprites:peashooter/repeater.png")

        self.projectile_manager = projectile_manager


        # TODO erstellen das man einfach durch Namenkonventioinen die richtige sprites geladen werden

    def attacking(self):
        self.projectile_manager.spawn_projectile(Projectile(self.center_x, self.center_y, 5, 15, self.bullet_texture))
        self.projectile_manager.spawn_projectile(Projectile(self.center_x + 40, self.center_y, 5, 15, self.bullet_texture))


    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.shoot_timer += delta_time
        SHOOT_COOLDOWN = 1
        if self.shoot_timer >= SHOOT_COOLDOWN:
            self.attacking()
            self.shoot_timer = 0.0

class IcePeaShooter(Plant):
    def __init__(self, projectile_manager: ProjectileManager):
        Plant.__init__(self,
                       "icepeashooter",
                       100,
                       ":sprites:peashooter/icepeashooter.png")

        self.projectile_manager = projectile_manager


        # TODO erstellen das man einfach durch Namenkonventioinen die richtige sprites geladen werden

    def attacking(self):
        self.projectile_manager.spawn_projectile(Projectile(self.center_x, self.center_y, 5, 20, self.bullet_texture))


    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.shoot_timer += delta_time
        SHOOT_COOLDOWN = 1
        if self.shoot_timer >= SHOOT_COOLDOWN:
            self.attacking()
            self.shoot_timer = 0.0




class Walnut(Plant):
    pass # TODO - Attack Klasse Festlegen


class PlantManager:
    def __init__(
        self,
        plant_sprite_list: arcade.SpriteList,
        projectileManager,
        sun_sprite_list,
        scene: arcade.scene.Scene,

    ) -> None:
        super().__init__()

        self.plant_sprite_list = plant_sprite_list
        self.projectileManager = projectileManager
        self.sun_sprite_list = sun_sprite_list
        self.scene = scene

        self.selected_plant= None


    def _create_plant(self, plant):
        return self.plant_sprite_list.append(plant)

    def spawn_plant(self, name: str, tile: arcade.Sprite) -> PeaShooter | None:
        if not arcade.get_sprites_at_point((tile.center_x,tile.center_y) , self.plant_sprite_list):
            new_plant = None
            if "peashooter" == name:
                new_plant = PeaShooter(self.projectileManager)
            if "sunflower" == name:
                new_plant = Sunflower(self.sun_sprite_list)
            if "icepeashooter" == name:
                new_plant = IcePeaShooter(self.projectileManager)
            if "repeater" == name:
                new_plant = Repeater(self.projectileManager)

            new_plant .center_x = tile.center_x
            new_plant .center_y = tile.center_y

            self._create_plant(new_plant)




    def on_update(self, delta_time: float) -> None:
        pass