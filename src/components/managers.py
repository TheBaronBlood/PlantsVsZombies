import src.constants as c
import arcade

import random

from src.components.entities import *
from src.components.world import GameContext


class ProjectileManager:
    def __init__(self, context: GameContext) -> None:
        self.context = context

    def spawn_projectile(self, projectile: Projectile) -> None:
        self.context.projectiles.append(projectile)


class PlantManager:
    def __init__(self, context: GameContext, projectile_manager: ProjectileManager) -> None:
        self.context = context
        self.projectile_manager = projectile_manager

        self.PLANT_FACTORY = {
            "sunflower": Sunflower,
            "peashooter": PeaShooter,
            "icepeashooter": IcePeaShooter,
            "repeater": Repeater,
        }

    def spawn(self, name: str, tile: arcade.Sprite) -> None:
        if arcade.get_sprites_at_point((tile.center_x, tile.center_y), self.context.plants):
            return
        plant_cls = self.PLANT_FACTORY.get(name)
        if not plant_cls:
            return
        plant = plant_cls()
        plant.center_x = tile.center_x
        plant.center_y = tile.center_y
        self.context.plants.append(plant)


class ZombieManager:
    def __init__(self, context: GameContext) -> None:
        self.context = context

    def spawn(self, name: str, lane: int | None = None) -> None:
        zombie = None
        if name == "Normal":
            zombie = ZombieNormal()
        elif name == "Pylone":
            zombie = ZombiePylone()
        elif name == "Bucket":
            zombie = ZombieBucket()

        if not zombie:
            return

        lane_sprites = self.context.scene[
            "Zombie_Grid"] if self.context.scene and "Zombie_Grid" in self.context.scene else None
        if not lane_sprites:
            return

        if lane is None:
            lane_sprite = random.choice(lane_sprites)
        else:
            if lane < 1 or lane > len(lane_sprites):
                return
            lane_sprite = lane_sprites[lane - 1]

        zombie.center_x = lane_sprite.center_x
        zombie.center_y = lane_sprite.center_y
        self.context.zombies.append(zombie)
