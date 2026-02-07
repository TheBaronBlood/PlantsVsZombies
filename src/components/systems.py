import src.constants as c
import arcade

import random
from pyglet.math import Vec2

from src.components.world import GameContext
from src.components.entities import Sun, Projectile, Sunflower
from src.components.managers import ZombieManager, ProjectileManager


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

            plant_config = c.get_plant_config(plant.name)
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
        self._initial_delay = float(c.PLANTS_SUNFLOWER.get("sun_initial_delay", 2.0))
        self._cooldown_min = float(c.PLANTS_SUNFLOWER.get("sun_cooldown_min", 5.0))
        self._cooldown_max = float(c.PLANTS_SUNFLOWER.get("sun_cooldown_max", 20.0))
        self._fall_enabled = bool(c.PLANTS.get("sun", {}).get("fall_enabled", True))
        self._fall_initial_delay = float(c.PLANTS.get("sun", {}).get("fall_initial_delay", 8.0))
        self._fall_interval_min = float(c.PLANTS.get("sun", {}).get("fall_interval_min", 10.0))
        self._fall_interval_max = float(c.PLANTS.get("sun", {}).get("fall_interval_max", 18.0))
        self._fall_target_min_y = float(c.PLANTS.get("sun", {}).get("fall_target_min_y", 260.0))
        self._fall_target_max_y = float(c.PLANTS.get("sun", {}).get("fall_target_max_y", 520.0))
        self._fall_speed = float(c.PLANTS.get("sun", {}).get("fall_speed", 0.8))
        self._fall_timer = 0.0
        self._next_fall = self._fall_initial_delay

    def update(self, delta_time: float) -> None:
        self._spawn_sun(delta_time)
        self._spawn_falling_sun(delta_time)
        self._despawn_suns(delta_time)

    def _spawn_sun(self, delta_time: float) -> None:
        for plant in self.context.plants:
            if not isinstance(plant, Sunflower):
                continue

            plant.shoot_timer += delta_time
            if not hasattr(plant, "sun_ready"):
                plant.sun_ready = False
            if not hasattr(plant, "sun_cooldown"):
                plant.sun_cooldown = random.uniform(self._cooldown_min, self._cooldown_max)

            if not plant.sun_ready:
                if plant.shoot_timer >= self._initial_delay:
                    self.context.suns.append(plant.create_sun())
                    plant.shoot_timer = 0.0
                    plant.sun_ready = True
                    plant.sun_cooldown = random.uniform(self._cooldown_min, self._cooldown_max)
                continue

            if plant.shoot_timer >= plant.sun_cooldown:
                self.context.suns.append(plant.create_sun())
                plant.shoot_timer = 0.0
                plant.sun_cooldown = random.uniform(self._cooldown_min, self._cooldown_max)

    def _despawn_suns(self, delta_time: float) -> None:
        for sun in self.context.suns:
            sun.shoot_timer = getattr(sun, "shoot_timer", 0.0) + delta_time
            if sun.shoot_timer >= 5:
                sun.remove_from_sprite_lists()

    def _spawn_falling_sun(self, delta_time: float) -> None:
        if not self._fall_enabled:
            return
        self._fall_timer += delta_time
        if self._fall_timer < self._next_fall:
            return

        map_width = c.SCREEN_WIDTH
        map_height = c.SCREEN_HEIGHT
        if self.context.tilemap:
            map_width = self.context.tilemap.width * self.context.tilemap.tile_width
            map_height = self.context.tilemap.height * self.context.tilemap.tile_height

        start_x = random.uniform(0, map_width)
        start = Vec2(start_x, map_height + 32)

        def _to_world(value: float) -> float:
            if 0.0 < value <= 1.0:
                return value * map_height
            return value

        min_y = min(self._fall_target_min_y, self._fall_target_max_y)
        max_y = max(self._fall_target_min_y, self._fall_target_max_y)
        min_y = _to_world(min_y)
        max_y = _to_world(max_y)
        min_y = max(0.0, min(min_y, map_height))
        max_y = max(0.0, min(max_y, map_height))
        if max_y < min_y:
            min_y, max_y = max_y, min_y
        if max_y - min_y < 1.0:
            min_y = map_height * 0.4
            max_y = map_height * 0.75
        target_y = random.uniform(min_y, max_y)
        target = Vec2(start_x, target_y)
        sun = Sun(start, target)
        sun.speed = self._fall_speed
        self.context.suns.append(sun)

        self._fall_timer = 0.0
        self._next_fall = random.uniform(self._fall_interval_min, self._fall_interval_max)

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
            plant_config = c.get_plant_config(getattr(plant, "name", ""))
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
