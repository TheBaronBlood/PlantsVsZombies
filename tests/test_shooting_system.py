from types import SimpleNamespace

import src.components.systems as systems
from src.components.systems import ShootingSystem


class DummyProjectile:
    def __init__(self, x, y, speed, damage, texture) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.texture = texture


class DummyProjectileManager:
    def __init__(self) -> None:
        self.spawned: list[DummyProjectile] = []

    def spawn_projectile(self, projectile) -> None:
        self.spawned.append(projectile)


def test_repeater_spawns_extra_projectile(monkeypatch) -> None:
    monkeypatch.setattr(systems, "Projectile", DummyProjectile)
    context = SimpleNamespace(plants=[])
    projectile_manager = DummyProjectileManager()
    system = ShootingSystem(context, projectile_manager)

    plant = SimpleNamespace(
        name="repeater",
        shoot_timer=0.9,
        bullet_texture=object(),
        center_x=10,
        center_y=20,
    )
    context.plants = [plant]

    system.update(0.2)

    assert len(projectile_manager.spawned) == 2
    assert plant.shoot_timer == 0.0


def test_sunflower_does_not_shoot(monkeypatch) -> None:
    monkeypatch.setattr(systems, "Projectile", DummyProjectile)
    context = SimpleNamespace(plants=[])
    projectile_manager = DummyProjectileManager()
    system = ShootingSystem(context, projectile_manager)

    plant = SimpleNamespace(
        name="sunflower",
        shoot_timer=2.0,
        bullet_texture=object(),
        center_x=10,
        center_y=20,
    )
    context.plants = [plant]

    system.update(0.1)

    assert projectile_manager.spawned == []


def test_plant_without_bullet_texture_is_skipped(monkeypatch) -> None:
    monkeypatch.setattr(systems, "Projectile", DummyProjectile)
    context = SimpleNamespace(plants=[])
    projectile_manager = DummyProjectileManager()
    system = ShootingSystem(context, projectile_manager)

    plant = SimpleNamespace(
        name="peashooter",
        shoot_timer=2.0,
        center_x=10,
        center_y=20,
    )
    context.plants = [plant]

    system.update(0.1)

    assert projectile_manager.spawned == []
