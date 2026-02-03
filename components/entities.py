"""Game entities: plants, zombies, projectiles, and suns."""
__author__ = "Miro K."
__copyright__ = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

import math
import random

import arcade
from pyglet.math import Vec2

import constants as c


class Plant(arcade.Sprite):
    def __init__(self, name: str, health: int, texture_path: str) -> None:
        super().__init__(scale=c.SCALE_FACTOR)
        self.name = name
        self.health = health
        self.shoot_timer = 0.0
        self._set_textures(texture_path)

    def _set_textures(self, path: str) -> None:
        sprite_sheet = arcade.load_spritesheet(path)
        texture = sprite_sheet.get_texture_grid((32, 32), 2, 2)
        self.texture = texture[0]
        self.bullet_texture = texture[1]

    def take_damage(self, damage: int) -> None:
        self.health -= damage


class Sun(arcade.Sprite):
    def __init__(self, start: Vec2, target: Vec2, value: int = 25) -> None:
        super().__init__(scale=c.SCALE_FACTOR)
        sprite_sheet = arcade.load_spritesheet(":sprites:sunflower/sunflower.png")
        texture = sprite_sheet.get_texture_grid((32, 32), 2, 2)
        self.texture = texture[1]

        self.value = value
        self.p0 = start
        self.p2 = target
        self.t = 0.0
        self.speed = 0.8
        self.finished = False

        mid = (start + target) / 2
        self.p1 = mid + Vec2(0, random.uniform(40, 80))

        self.center_x = start.x
        self.center_y = start.y

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        super().update(delta_time)

        if self.finished:
            return

        self.t += delta_time * self.speed
        if self.t >= 1.0:
            self.t = 1.0
            self.finished = True

        pos = (1 - self.t) ** 2 * self.p0 + 2 * (1 - self.t) * self.t * self.p1 + self.t ** 2 * self.p2
        self.center_x = pos.x
        self.center_y = pos.y


class Sunflower(Plant):
    def __init__(self) -> None:
        super().__init__("sunflower", 100, ":sprites:sunflower/sunflower.png")

    def create_sun(self) -> Sun:
        start = Vec2(self.center_x, self.center_y)
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(60, 120)
        target = Vec2(start.x + math.cos(angle) * radius, start.y + math.sin(angle) * radius)
        return Sun(start, target)


class PeaShooter(Plant):
    def __init__(self) -> None:
        super().__init__("peashooter", 100, ":sprites:peashooter/peashooter.png")


class Repeater(Plant):
    def __init__(self) -> None:
        super().__init__("repeater", 100, ":sprites:peashooter/repeater.png")


class IcePeaShooter(Plant):
    def __init__(self) -> None:
        super().__init__("icepeashooter", 100, ":sprites:peashooter/icepeashooter.png")


class Projectile(arcade.Sprite):
    def __init__(self, x: float, y: float, speed: int, damage: int, texture: arcade.Texture) -> None:
        super().__init__(path_or_texture=texture, scale=c.SCALE_FACTOR, center_x=x, center_y=y)
        self.speed = speed
        self.damage = damage
        self.velocity = Vec2(self.speed, 0)

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        super().update(delta_time)
        margin = 64
        if (
            self.center_x < -margin
            or self.center_x > c.SCREEN_WIDTH + margin
            or self.center_y < -margin
            or self.center_y > c.SCREEN_HEIGHT + margin
        ):
            self.remove_from_sprite_lists()


class Zombie(arcade.Sprite):
    def __init__(self, name: str, health: int, texture_path: str, speed: int = c.ZOMBIE_SPEED) -> None:
        super().__init__(scale=c.SCALE_FACTOR)
        self.name = name
        self.health = health
        self.speed = speed
        self.damage = 10
        self.attack_time = 1.0
        self.rest_time = 0.0
        self._set_textures(texture_path)
        self.velocity = Vec2(-self.speed, 0)

    def _set_textures(self, path: str) -> None:
        sprite_sheet = arcade.load_spritesheet(path)
        texture = sprite_sheet.get_texture_grid((32, 32), 2, 2)
        self.texture = texture[0]

    def take_damage(self, damage: int) -> None:
        self.health -= damage


class ZombieNormal(Zombie):
    def __init__(self) -> None:
        super().__init__("Normal", 100, ":sprites:zombie_normal/zombie_normal.png")


class ZombiePylone(Zombie):
    def __init__(self) -> None:
        super().__init__("Pylone", 200, ":sprites:zombie_pylons/zombie_pylone.png")


class ZombieBucket(Zombie):
    def __init__(self) -> None:
        super().__init__("Bucket", 350, ":sprites:zombie_bucket/zombie_bucket.png")
