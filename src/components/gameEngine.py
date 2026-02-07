import json
from pathlib import Path

import src.constants as c
import arcade

from pyglet.math import Vec2

from src.components.world import GameContext
from src.components.managers import PlantManager, ZombieManager, ProjectileManager
from src.components.systems import CombatSystem, ShootingSystem, SpawnSystem, SunSystem

class GameEngine:
    def __init__(self) -> None:
        self.context = GameContext()

        self.projectile_manager = ProjectileManager(self.context)
        self.plant_manager = PlantManager(self.context, self.projectile_manager)
        self.zombie_manager = ZombieManager(self.context)

        self.combat_system = CombatSystem(self.context)
        self.spawn_system = SpawnSystem(self.zombie_manager)
        self.sun_system = SunSystem(self.context)
        self.shooting_system = ShootingSystem(self.context, self.projectile_manager)

    def load_tilemap(self, map_file: str) -> bool:
        try:
            self.context.tilemap = arcade.load_tilemap(
                map_file,
                scaling=c.WORLD_SCALE,
                offset=Vec2(0, 0),
            )
            self.context.scene = arcade.Scene.from_tilemap(self.context.tilemap)
            return True
        except Exception as exc:
            self.context.scene = None
            print(f"Fehler beim Laden der Tilemap '{map_file}': {exc}")
            return False

    def load_level(self, level_path: str | Path) -> dict:
        level_path = Path(level_path)
        with level_path.open("r", encoding="utf-8") as f:
            level_data = json.load(f)

        map_name = level_data.get("map")
        if not map_name:
            raise ValueError("Level map missing.")

        map_resource = map_name if str(map_name).startswith(":") else f":maps:{map_name}"
        if not self.load_tilemap(map_resource):
            raise RuntimeError(f"Tilemap load failed: {map_resource}")

        self.spawn_system.set_waves(level_data.get("waves", []))
        return level_data

    def find_tile_at(self, x: float, y: float, layer: str) -> arcade.Sprite | None:
        if not self.context.scene or layer not in self.context.scene:
            return None
        tiles = arcade.get_sprites_at_point((x, y), self.context.scene[layer])
        return tiles[0] if tiles else None

    def update(self, delta_time: float) -> None:
        self.context.plants.update(delta_time)
        self.context.zombies.update(delta_time)
        self.context.projectiles.update(delta_time)
        self.context.suns.update(delta_time)

        self.combat_system.update(delta_time)
        self.shooting_system.update(delta_time)
        self.sun_system.update(delta_time)
        self.spawn_system.update(delta_time)

    def draw(self) -> None:
        if self.context.scene:
            self.context.scene.draw(pixelated=True)
        self.context.plants.draw(pixelated=True)
        self.context.zombies.draw(pixelated=True)
        self.context.projectiles.draw(pixelated=True)
        self.context.suns.draw(pixelated=True)

    def collect_sun_at(self, x: float, y: float) -> int:
        return self.sun_system.collect_at(x, y)
