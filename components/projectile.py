""""""
__author__ = "Miro K."
__copyright__ = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

# IMPORTS
# Arcade Packages
import arcade
import arcade.gui
from arcade import SpriteList, SpriteType, BasicSprite

# Math
from pyglet.math import Vec2

# Game Imports
import constants as c







class Projectile(arcade.Sprite):
    def __init__(
        self,
        speed,
        bullet_texture,
    ) -> None:
        super().__init__(path_or_texture=bullet_texture, scale=c.SCALE_FACTOR)

        self.speed = speed
        self.velocity = Vec2(self.speed, 0) # Bewegt es nach Rechts


    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        try:
            super().update(delta_time)
        except TypeError:
            # Manche Arcade-Versionen rufen update() ohne Parameter; sicherheitshalber aufrufen
            super().update()

        # Bildschirmränder prüfen
        try:
            max_x = c.SCREEN_WIDTH
            max_y = c.SCREEN_HEIGHT
        except NameError:
            max_x = 2000
            max_y = 2000

        margin = 64
        if (
            self.center_x < -margin
            or self.center_x > max_x + margin
            or self.center_y < -margin
            or self.center_y > max_y + margin
        ):
            self.remove_from_sprite_lists()




# TODO Projectile VERTIGSTELLEN
class ProjectileManager:
    def __init__(
            self,
            projectile_sprite_list: arcade.SpriteList,
            scene: arcade.scene.Scene,
    ) -> None:
        super().__init__()

        self.projectile_sprite_list = projectile_sprite_list
        self.scene = scene

    def spawn_projectile(self, projectile: Projectile):
        self.projectile_sprite_list.append(projectile)

