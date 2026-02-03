"""Game systems that encapsulate specific gameplay logic."""
__author__ = "Miro K."
__copyright__ = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

import random

import arcade
from pyglet.math import Vec2

from components.plant import Sun
from components.zombie import ZombieManager


class CombatSystem:
    def __init__(
        self,
        zombie_sprite_list: arcade.SpriteList,
        plant_sprite_list: arcade.SpriteList,
        projectile_sprite_list: arcade.SpriteList,
        scene: arcade.Scene,
    ) -> None:
        self.zombie_sprite_list = zombie_sprite_list
        self.plant_sprite_list = plant_sprite_list
        self.projectile_sprite_list = projectile_sprite_list
        self.scene = scene

    def handle_projectile_hits(self) -> None:
        for zombie in self.zombie_sprite_list:
            collisions = arcade.check_for_collision_with_list(
                zombie,
                self.projectile_sprite_list,
            )
            rasenmeaher_list = arcade.check_for_collision_with_list(
                zombie,
                self.scene["Rasenmäher"],
            )
            for projectile in collisions:
                zombie.take_damage(projectile.damage)
                projectile.remove_from_sprite_lists()

            if zombie.health <= 0:
                zombie.remove_from_sprite_lists()

            for rasenmeaher in rasenmeaher_list:
                zombie.kill()

    def handle_plant_hits(self, delta_time: float) -> None:
        for zombie in self.zombie_sprite_list:
            collisions = arcade.check_for_collision_with_list(
                zombie,
                self.plant_sprite_list,
            )
            if collisions:
                for plant in collisions:
                    zombie.velocity = Vec2(0, 0)
                    zombie.rest_time += delta_time
                    if zombie.rest_time >= zombie.attack_time:
                        plant.take_damage(zombie.damage)
                    if plant.health <= 0:
                        zombie.velocity = Vec2(-zombie.speed, 0)
                        plant.remove_from_sprite_lists()
            else:
                if zombie.change_x == 0:
                    zombie.change_x = -zombie.speed
                    zombie.velocity = (-zombie.speed, 0)
                    zombie.rest_time = 0


class SpawnSystem:
    def __init__(
        self,
        zombie_manager: ZombieManager,
        zombie_names: list[str],
        spawn_interval: float = 1.0,
    ) -> None:
        self.zombie_manager = zombie_manager
        self.zombie_names = zombie_names
        self.spawn_interval = spawn_interval
        self.timer = 0.0

    def update(self, delta_time: float) -> None:
        self.timer += delta_time
        if self.timer >= self.spawn_interval:
            self.zombie_manager.spawn_zombie(random.choice(self.zombie_names))
            self.timer = 0.0


class SunSystem:
    def __init__(self, sun_sprite_list: arcade.SpriteList):
        self.sun_sprite_list = sun_sprite_list

    def despawn(self, delta_time: float) -> None:
        for sun in self.sun_sprite_list:
            sun.shoot_timer += delta_time
            despawn_cooldown = 5
            if sun.shoot_timer >= despawn_cooldown:
                sun.remove_from_sprite_lists()

    def collect_at(self, x: float, y: float) -> int:
        sun_list = arcade.get_sprites_at_point((x, y), self.sun_sprite_list)
        if not sun_list:
            return 0
        sun = sun_list[-1]
        if isinstance(sun, Sun):
            sun.remove_from_sprite_lists()
            return sun.value
        return 0
