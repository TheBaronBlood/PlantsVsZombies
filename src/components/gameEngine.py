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

    def load_tilemap(self, map_file: str) -> None:
        try:
            self.context.tilemap = arcade.load_tilemap(
                map_file,
                scaling=c.WORLD_SCALE,
                offset=Vec2(0, 0),
            )
            self.context.scene = arcade.Scene.from_tilemap(self.context.tilemap)
        except Exception as exc:
            print(f"Fehler beim Laden der Tilemap '{map_file}': {exc}")

    def find_tile_at(self, x: float, y: float, layer: str) -> arcade.Sprite | None:
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
