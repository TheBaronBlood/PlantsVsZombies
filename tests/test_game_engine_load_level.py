import json

import pytest

from src.components.gameEngine import GameEngine


class DummySpawnSystem:
    def __init__(self) -> None:
        self.waves: list[dict] | None = None

    def set_waves(self, waves: list[dict]) -> None:
        self.waves = waves


def test_load_level_prefixes_map_resource(tmp_path) -> None:
    engine = GameEngine.__new__(GameEngine)
    engine.spawn_system = DummySpawnSystem()
    captured: dict[str, object] = {}

    def fake_load_tilemap(path: str) -> bool:
        captured["path"] = path
        return True

    def fake_set_waves(waves: list[dict]) -> None:
        captured["waves"] = waves

    engine.load_tilemap = fake_load_tilemap
    engine.spawn_system.set_waves = fake_set_waves

    level_data = {"map": "map_1.tmx", "waves": [{"time": 1, "zombie": "normal"}]}
    level_path = tmp_path / "level.json"
    level_path.write_text(json.dumps(level_data), encoding="utf-8")

    result = engine.load_level(level_path)

    assert result == level_data
    assert captured["path"] == ":maps:map_1.tmx"
    assert captured["waves"] == level_data["waves"]


def test_load_level_keeps_prefixed_map(tmp_path) -> None:
    engine = GameEngine.__new__(GameEngine)
    engine.spawn_system = DummySpawnSystem()
    captured: dict[str, object] = {}

    def fake_load_tilemap(path: str) -> bool:
        captured["path"] = path
        return True

    engine.load_tilemap = fake_load_tilemap
    engine.spawn_system.set_waves = lambda waves: None

    level_data = {"map": ":maps:custom.tmx", "waves": []}
    level_path = tmp_path / "level.json"
    level_path.write_text(json.dumps(level_data), encoding="utf-8")

    engine.load_level(level_path)

    assert captured["path"] == ":maps:custom.tmx"


def test_load_level_missing_map_raises(tmp_path) -> None:
    engine = GameEngine.__new__(GameEngine)
    engine.spawn_system = DummySpawnSystem()
    level_path = tmp_path / "level.json"
    level_path.write_text(json.dumps({}), encoding="utf-8")

    with pytest.raises(ValueError):
        engine.load_level(level_path)


def test_load_level_tilemap_failure_raises(tmp_path) -> None:
    engine = GameEngine.__new__(GameEngine)
    engine.spawn_system = DummySpawnSystem()
    engine.load_tilemap = lambda path: False
    level_data = {"map": "map_1.tmx", "waves": []}
    level_path = tmp_path / "level.json"
    level_path.write_text(json.dumps(level_data), encoding="utf-8")

    with pytest.raises(RuntimeError):
        engine.load_level(level_path)
