import src.constants as c
import arcade

import math, random
from pyglet.math import Vec2


class Plant(arcade.Sprite):
    def __init__(self, name: str, health: int, texture_path: str) -> None:
        super().__init__(scale=c.PLANT_SCALE)
        self.name = name
        self.health = health
        self.texture = None
        self.bullet_texture = None
        self._set_textures(texture_path)


    # Läd die Texture und teilt sie in Sprite und Projectile
    def _set_textures(self, path: str) -> None:
        sprite_sheet = arcade.load_spritesheet(path)
        texture = sprite_sheet.get_texture_grid((32, 32), 2, 2)
        self.texture = texture[0]
        self.bullet_texture = texture[1]

    # Fügt Schaden Hinzu
    def take_damage(self, damage: int) -> None:
        self.health -= damage



class Sun(arcade.Sprite):
    def __init__(self, start: Vec2, target: Vec2, value: int = 25) -> None:
        super().__init__(scale=c.PLANT_SCALE)
        sprite_sheet = arcade.load_spritesheet(":sprites:plants/sunflower.png")
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
