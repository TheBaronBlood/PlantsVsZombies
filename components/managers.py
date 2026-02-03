"""Managers handle creation and placement of entities."""
__author__ = "Miro K."
__copyright__ = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

import random

import arcade

from components.context import GameContext
from components.entities import (
    IcePeaShooter,
    PeaShooter,
    Projectile,
    Repeater,
    Sunflower,
    ZombieBucket,
    ZombieNormal,
    ZombiePylone,
)


class ProjectileManager:
    def __init__(self, context: GameContext) -> None:
        self.context = context

    def spawn_projectile(self, projectile: Projectile) -> None:
        self.context.projectiles.append(projectile)


class PlantManager:
    def __init__(self, context: GameContext, projectile_manager: ProjectileManager) -> None:
        self.context = context
        self.projectile_manager = projectile_manager

    def spawn(self, name: str, tile: arcade.Sprite) -> None:
        if arcade.get_sprites_at_point((tile.center_x, tile.center_y), self.context.plants):
            return

        plant = None
        if name == "peashooter":
            plant = PeaShooter()
        elif name == "sunflower":
            plant = Sunflower()
        elif name == "icepeashooter":
            plant = IcePeaShooter()
        elif name == "repeater":
            plant = Repeater()

        if plant:
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

        if lane is None:
            lane_sprite = random.choice(self.context.scene["Zombie_Grid"])
        else:
            lane_sprite = self.context.scene["Zombie_Grid"][lane - 1]

        zombie.center_x = lane_sprite.center_x
        zombie.center_y = lane_sprite.center_y
        self.context.zombies.append(zombie)
