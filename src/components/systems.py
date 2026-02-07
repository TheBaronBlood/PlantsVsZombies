import src.constants as c
import arcade

import random
from pyglet.math import Vec2

from src.components.world import GameContext
from src.components.entities import Sun, Projectile, Sunflower
from src.components.managers import ZombieManager, ProjectileManager


def _get_plant_config(name: str) -> dict:
    return {
        "sunflower": c.PLANTS_SUNFLOWER,
        "peashooter": c.PLANTS_PEASHOOTER,
        "icepeashooter": c.PLANTS_ICEPEASHOOTER,
        "repeater": c.PLANTS_REPEATER,
        "walnut": c.PLANTS_WALNUT,
        "blumerrang": c.PLANTS_BLUMERRANG,
        "potatomine": c.PLANTS_POTATOMINE,
    }.get(name, c.PLANTS_DEFAULTS)


class CombatSystem:
    def __init__(self, context: GameContext) -> None:
        self.context = context

    def update(self, delta_time: float) -> None:
        self._handle_potatomines()
        self._handle_projectile_hits()
        self._handle_plant_hits(delta_time)

    def _handle_projectile_hits(self) -> None:
        for zombie in self.context.zombies:
            mower_layer = None
            if self.context.scene and "Rasenmäher" in self.context.scene:
                mower_layer = self.context.scene["Rasenmäher"]

            collisions = arcade.check_for_collision_with_list(zombie, self.context.projectiles)
            mower_hits = arcade.check_for_collision_with_list(zombie, mower_layer) if mower_layer else []
            for projectile in collisions:
                hit_targets = getattr(projectile, "_hit_targets", None)
                if hit_targets is not None:
                    target_id = id(zombie)
                    if target_id in hit_targets:
                        continue
                    hit_targets.add(target_id)
                zombie.take_damage(projectile.damage)
                if not getattr(projectile, "pierce", False):
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
                        zombie.rest_time = 0.0

                    if plant.health <= 0:
                        zombie.velocity = Vec2(-zombie.speed, 0)
                        plant.remove_from_sprite_lists()
            else:
                if zombie.change_x == 0:
                    zombie.change_x = -zombie.speed
                    zombie.velocity = (-zombie.speed, 0)
                    zombie.rest_time = 0

    def _handle_potatomines(self) -> None:
        if not self.context.plants or not self.context.zombies:
            return

        tile_width = 32
        tile_height = 32
        if self.context.tilemap:
            tile_width = self.context.tilemap.tile_width or tile_width
            tile_height = self.context.tilemap.tile_height or tile_height

        for plant in list(self.context.plants):
            if getattr(plant, "name", "") != "potatomine":
                continue
            stage_times = getattr(plant, "_plant_stage_times", [])
            if not stage_times:
                continue
            ready_time = sum(stage_times)
            if getattr(plant, "_plant_anim_time", 0.0) < ready_time:
                continue

            plant_config = _get_plant_config(plant.name)
            trigger_x_tiles = float(plant_config.get("explosion_trigger_x_tiles", 0.5))
            trigger_y_tiles = float(plant_config.get("explosion_trigger_y_tiles", 0.4))
            explosion_x_tiles = float(plant_config.get("explosion_radius_x_tiles", 0.75))
            explosion_y_tiles = float(plant_config.get("explosion_radius_y_tiles", 0.6))

            trigger_x_offset = tile_width * trigger_x_tiles
            trigger_y_offset = tile_height * trigger_y_tiles
            explosion_x = tile_width * explosion_x_tiles
            explosion_y = tile_height * explosion_y_tiles

            triggered = False
            for zombie in self.context.zombies:
                if abs(zombie.center_y - plant.center_y) > trigger_y_offset:
                    continue
                dx = zombie.center_x - plant.center_x
                if 0 <= dx <= trigger_x_offset:
                    triggered = True
                    break

            if not triggered:
                continue

            damage = int(plant_config.get("explosion_damage", 999))

            for zombie in list(self.context.zombies):
                if abs(zombie.center_x - plant.center_x) <= explosion_x and abs(
                    zombie.center_y - plant.center_y
                ) <= explosion_y:
                    zombie.take_damage(damage)
                    if zombie.health <= 0:
                        zombie.remove_from_sprite_lists()

            plant.remove_from_sprite_lists()

class SunSystem:
    def __init__(self, context: GameContext) -> None:
        self.context = context

    def update(self, delta_time: float) -> None:
        self._spawn_sun(delta_time)
        self._despawn_suns(delta_time)

    def _spawn_sun(self, delta_time: float) -> None:
        for plant in self.context.plants:
            if not isinstance(plant, Sunflower):
                continue

            plant.shoot_timer += delta_time
            if not hasattr(plant, "sun_cooldown"):
                plant.sun_cooldown = random.uniform(5.0, 20.0)

            if plant.shoot_timer >= plant.sun_cooldown:
                self.context.suns.append(plant.create_sun())
                plant.shoot_timer = 0.0
                plant.sun_cooldown = random.uniform(5.0, 20.0)

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
        self.elapsed = 0.0
        self.waves: list[dict] = []
        self.next_index = 0

    def update(self, delta_time: float) -> None:
        if not self.waves:
            return
        self.elapsed += delta_time
        while self.next_index < len(self.waves):
            wave = self.waves[self.next_index]
            if wave["time"] > self.elapsed:
                break
            self.zombie_manager.spawn(wave["zombie"], wave.get("lane"))
            self.next_index += 1

    def set_waves(self, waves: list[dict] | None) -> None:
        self.elapsed = 0.0
        self.next_index = 0
        normalized: list[dict] = []
        for wave in waves or []:
            parsed = self._parse_wave(wave)
            if parsed:
                normalized.append(parsed)
        self.waves = sorted(normalized, key=lambda w: w["time"])

    def has_waves(self) -> bool:
        return bool(self.waves)

    def is_finished(self) -> bool:
        return self.next_index >= len(self.waves)

    def _parse_wave(self, wave: dict) -> dict | None:
        if not isinstance(wave, dict):
            return None
        if "time" not in wave or "zombie" not in wave:
            return None
        try:
            time_value = float(wave["time"])
        except (TypeError, ValueError):
            return None
        zombie = str(wave["zombie"])
        lane = wave.get("lane")
        if lane is not None:
            try:
                lane = int(lane)
            except (TypeError, ValueError):
                lane = None
        return {"time": time_value, "zombie": zombie, "lane": lane}


class ShootingSystem:
    def __init__(self, context: GameContext, projectile_manager: ProjectileManager) -> None:
        self.context = context
        self.projectile_manager = projectile_manager

    def update(self, delta_time: float) -> None:
        for plant in self.context.plants:
            if not hasattr(plant, "bullet_texture"):
                continue
            if getattr(plant, "bullet_animation", None) is None and getattr(plant, "bullet_texture", None) is None:
                continue
            if plant.name == "sunflower":
                continue

            plant.shoot_timer += delta_time
            plant_config = _get_plant_config(getattr(plant, "name", ""))
            cooldown = float(plant_config.get("cooldown", 1.0))

            if plant.shoot_timer >= cooldown:
                self._fire_projectile(plant, plant_config)
                plant.shoot_timer = 0.0

    def _fire_projectile(self, plant, plant_config: dict) -> None:
        damage = plant_config.get("damage", 10)
        projectile_speed = plant_config.get("projectile_speed", 5)
        extra_projectiles = int(plant_config.get("extra_projectiles", 0) or 0)
        projectile_texture = getattr(plant, "bullet_animation", None) or plant.bullet_texture
        pierce = bool(plant_config.get("projectile_pierce", False))

        for extra in range(extra_projectiles):
            projectile = Projectile(
                plant.center_x,
                plant.center_y,
                projectile_speed,
                damage,
                projectile_texture,
            )
            projectile.pierce = pierce
            self.projectile_manager.spawn_projectile(projectile)

        projectile = Projectile(
            plant.center_x,
            plant.center_y,
            projectile_speed,
            damage,
            projectile_texture,
        )
        projectile.pierce = pierce
        self.projectile_manager.spawn_projectile(projectile)
