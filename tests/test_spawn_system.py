import pytest

from src.components.systems import SpawnSystem


class DummyZombieManager:
    def __init__(self) -> None:
        self.spawn_calls: list[tuple[str, int | None]] = []

    def spawn(self, name: str, lane: int | None = None) -> None:
        self.spawn_calls.append((name, lane))


def test_set_waves_parses_and_sorts() -> None:
    manager = DummyZombieManager()
    system = SpawnSystem(manager)

    system.set_waves(
        [
            {"time": "2.0", "zombie": "normal", "lane": "2"},
            {"time": 1, "zombie": "bucket"},
            {"time": "bad", "zombie": "normal"},
            {"zombie": "normal"},
            "invalid",
        ],
    )

    assert system.waves == [
        {"time": 1.0, "zombie": "bucket", "lane": None},
        {"time": 2.0, "zombie": "normal", "lane": 2},
    ]
    assert system.elapsed == 0.0
    assert system.next_index == 0


def test_update_spawns_in_time_order() -> None:
    manager = DummyZombieManager()
    system = SpawnSystem(manager)
    system.set_waves(
        [
            {"time": 0.5, "zombie": "normal", "lane": 1},
            {"time": 1.0, "zombie": "bucket"},
        ],
    )

    system.update(0.25)
    assert manager.spawn_calls == []

    system.update(0.25)
    assert manager.spawn_calls == [("normal", 1)]
    assert not system.is_finished()

    system.update(0.5)
    assert manager.spawn_calls == [("normal", 1), ("bucket", None)]
    assert system.is_finished()
