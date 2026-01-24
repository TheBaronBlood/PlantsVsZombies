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
from components.projectile import Projectile, ProjectileManager
# Game Imports
import constants as c


class Plant(arcade.Sprite):
    def __init__(
        self,
        name,
        health,
        sprite_texture,
        bullet_texture
    ) -> None:
        super().__init__(path_or_texture=sprite_texture, scale=c.SCALE_FACTOR)

        self.name = name
        self.health = health
        self.state = c.IDLE
        self.shoot_timer = 0

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
    def __init__(self):
        Plant.__init__(self,
                       "sunf",
                       100,
                       ":sprites:sunflower/sunflower.png",
                       ":sprites:bullets/sunflower_bullet.png") # TODO - IDLE klasse definieren

class Sunflower(Plant):
    def __init__(self):
        Plant.__init__(self,
                       "sunflower",
                       100,
                       ":sprites:sunflower/sunflower.png",
                       ":sprites:bullets/sunflower_bullet.png")

class PeaShooter(Plant):
    def __init__(self, projectile_manager: ProjectileManager):
        Plant.__init__(self,
                       "peashooter",
                       100,
                       ":sprites:peashooter/peashooter.png",
                       ":sprites:bullets/peashooter_bullet.png")

        self.projectile_manager = projectile_manager


        # TODO erstellen das man einfach durch Namenkonventioinen die richtige sprites geladen werden

    def attacking(self):
        bullet = Projectile(10, self.bullet_texture)

        bullet.center_x = self.center_x
        bullet.center_y = self.center_y

        self.projectile_manager.spawn_projectile(bullet)


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
        scene: arcade.scene.Scene,

    ) -> None:
        super().__init__()

        self.plant_sprite_list = plant_sprite_list
        self.projectileManager = projectileManager
        self.scene = scene

        self.selected_plant= None


    def _create_plant(self, plant):
        return self.plant_sprite_list.append(plant)

    def spawn_plant(self, name: str, tile: arcade.Sprite) -> PeaShooter | None:
        if "peashooter" == name:
            new_plant = PeaShooter(self.projectileManager)
            new_plant .center_x = tile.center_x
            new_plant .center_y = tile.center_y

            self._create_plant(new_plant)




    def on_update(self, delta_time: float) -> None:
        pass