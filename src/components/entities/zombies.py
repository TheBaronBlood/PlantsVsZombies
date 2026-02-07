import src.constants as c
import arcade

from pyglet.math import Vec2
########################################################################################################################

class Zombie(arcade.Sprite):
    def __init__(self, name: str, health: int, speed: int = c.ZOMBIE_SPEED, texture_path: str | None = None) -> None:
        super().__init__(scale=c.ZOMBIE_SCALE)
        self.name = name
        self.health = health
        self.speed = speed
        self.damage = 10
        self.attack_time = 1.0
        self.rest_time = 0.0
        self._set_textures(texture_path)
        self.velocity = Vec2(-self.speed, 0)

    def _set_textures(self, path: str | None) -> None:
        if path is None:
            path = f":sprites:zombies/zombie_{self.name}.png"

        sprite_sheet = arcade.load_spritesheet(path)
        texture = sprite_sheet.get_texture_grid((32, 32), 2, 2)
        self.texture = texture[0]

    def take_damage(self, damage: int) -> None:
        self.health -= damage

########################################################################################################################

class ZombieNormal(Zombie):
    def __init__(self) -> None:
        super().__init__("normal", c.ZOMBIE_NORMAL.get("health"))

class ZombiePylone(Zombie):
    def __init__(self) -> None:
        super().__init__("pylone", c.ZOMBIE_PYLONE.get("health") )

class ZombieBucket(Zombie):
    def __init__(self) -> None:
        super().__init__("bucket", c.ZOMBIE_BUCKET.get("health"))