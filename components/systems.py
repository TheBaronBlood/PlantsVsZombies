"""Game systems that operate on the shared context."""
__author__ = "Miro K."
__copyright__ = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

import random

import arcade
from pyglet.math import Vec2

from components.context import GameContext
from components.entities import Projectile, Sun, Sunflower
from components.managers import ProjectileManager, ZombieManager


class CombatSystem:
    def __init__(self, context: GameContext) -> None:
        self.context = context

    def update(self, delta_time: float) -> None:
        self._handle_projectile_hits()
        self._handle_plant_hits(delta_time)

    def _handle_projectile_hits(self) -> None:
        for zombie in self.context.zombies:
            collisions = arcade.check_for_collision_with_list(zombie, self.context.projectiles)
            mower_hits = arcade.check_for_collision_with_list(zombie, self.context.scene["Rasenmäher"])
            for projectile in collisions:
                zombie.take_damage(projectile.damage)
                projectile.remove_from_sprite_lists()

            if zombie.health <= 0:
                zombie.remove_from_sprite_lists()

            for mower in mower_hits:
                zombie.kill()

    def _handle_plant_hits(self, delta_time: float) -> None:
        for zombie in self.context.zombies:
            collisions = arcade.check_for_collision_with_list(zombie, self.context.plants)
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


class SunSystem:
    def __init__(self, context: GameContext) -> None:
        self.context = context

    def update(self, delta_time: float) -> None:
        self._spawn_sunflowers(delta_time)
        self._despawn_suns(delta_time)

    def _spawn_sunflowers(self, delta_time: float) -> None:
        for plant in self.context.plants:
            if not isinstance(plant, Sunflower):
                continue
            plant.shoot_timer += delta_time
            cooldown = random.randint(5, 20)
            if plant.shoot_timer >= cooldown:
                self.context.suns.append(plant.create_sun())
                plant.shoot_timer = 0.0

    def _despawn_suns(self, delta_time: float) -> None:
        for sun in self.context.suns:
            sun.shoot_timer = getattr(sun, "shoot_timer", 0.0) + delta_time
            if sun.shoot_timer >= 5:
                sun.remove_from_sprite_lists()

    def collect_at(self, x: float, y: float) -> int:
        sun_list = arcade.get_sprites_at_point((x, y), self.context.suns)
        if not sun_list:
            return 0
        sun = sun_list[-1]
        if isinstance(sun, Sun):
            sun.remove_from_sprite_lists()
            return sun.value
        return 0


class SpawnSystem:
    def __init__(self, zombie_manager: ZombieManager) -> None:
        self.zombie_manager = zombie_manager
        self.timer = 0.0
        self.interval = 1.0
        self.zombie_names = ["Normal", "Pylone", "Bucket"]

    def update(self, delta_time: float) -> None:
        self.timer += delta_time
        if self.timer >= self.interval:
            self.zombie_manager.spawn(random.choice(self.zombie_names))
            self.timer = 0.0


class ShootingSystem:
    def __init__(self, context: GameContext, projectile_manager: ProjectileManager) -> None:
        self.context = context
        self.projectile_manager = projectile_manager

    def update(self, delta_time: float) -> None:
        for plant in self.context.plants:
            if not hasattr(plant, "bullet_texture"):
                continue

            plant.shoot_timer += delta_time
            cooldown = 1.0
            if plant.name == "repeater":
                cooldown = 1.0
            if plant.name == "icepeashooter":
                cooldown = 1.0

            if plant.shoot_timer >= cooldown:
                self._fire_projectile(plant)
                plant.shoot_timer = 0.0

    def _fire_projectile(self, plant) -> None:
        damage = 10
        if plant.name == "repeater":
            damage = 15
            self.projectile_manager.spawn_projectile(
                Projectile(plant.center_x + 40, plant.center_y, 5, damage, plant.bullet_texture),
            )
        if plant.name == "icepeashooter":
            damage = 20

        self.projectile_manager.spawn_projectile(
            Projectile(plant.center_x, plant.center_y, 5, damage, plant.bullet_texture),
        )
