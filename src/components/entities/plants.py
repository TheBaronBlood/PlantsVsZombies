import src.constants as c
import arcade

import math, random
from pyglet.math import Vec2
########################################################################################################################

class Plant(arcade.Sprite):
    def __init__(self, name: str, health: int, texture_path: str | None = None) -> None:
        super().__init__(scale=c.PLANTS_SCALE)
        self.name = name
        self.health = health
        self.shoot_timer = 0.0
        self.bullet_texture = None
        self._set_textures(texture_path)


    # Läd die Texture und teilt sie in Sprite und Projectile
    def _set_textures(self, path: str | None) -> None:
        if path is None:
            path = f":sprites:plants/{self.name}.png"

        sprite_sheet = arcade.load_spritesheet(path)
        texture = sprite_sheet.get_texture_grid((32, 32), 2, 2)
        self.texture = texture[0]
        self.bullet_texture = texture[1]

    # Fügt Schaden Hinzu
    def take_damage(self, damage: int) -> None:
        self.health -= damage


class Projectile(arcade.Sprite):
    def __init__(self, x: float, y: float, speed: int, damage: int, texture: arcade.Texture) -> None:
        super().__init__(path_or_texture=texture, scale=c.PLANTS_SCALE, center_x=x, center_y=y)
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

########################################################################################################################

class Sun(arcade.Sprite):
    def __init__(self, start: Vec2, target: Vec2, value: int = 25) -> None:
        super().__init__(scale=c.SUN_SCALE)
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

class Sunflower(Plant):
    def __init__(self) -> None:
        super().__init__("sunflower", c.PLANTS_SUNFLOWER.get("health"))

    def create_sun(self) -> Sun:
        start = Vec2(self.center_x, self.center_y)
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(60, 120)
        target = Vec2(start.x + math.cos(angle) * radius, start.y + math.sin(angle) * radius)
        return Sun(start, target)

class PeaShooter(Plant):
    def __init__(self) -> None:
        super().__init__("peashooter", c.PLANTS_PEASHOOTER.get("health"))

class Repeater(Plant):
    def __init__(self) -> None:
        super().__init__("repeater", c.PLANTS_REPEATER.get("health"))

class IcePeaShooter(Plant):
    def __init__(self) -> None:
        super().__init__("icepeashooter", c.PLANTS_ICEPEASHOOTER.get("health"))

class Walnut(Plant):
    def __init__(self) -> None:
        super().__init__("walnut", c.PLANTS_WALNUT.get("health"))

class Blumerang(Plant):
    def __init__(self) -> None:
        super().__init__("blumerang", c.PLANTS_BLUMERRANG.get("health"))

