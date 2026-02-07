import json
from pathlib import Path

import arcade
import arcade.gui

import src.constants as c
from src.components.gameEngine import GameEngine
from src.views.endView import EndView


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()

        self.levels = self._load_levels()
        if not self.levels:
            raise RuntimeError("No levels found.")

        self.level_index = 0
        self.engine = GameEngine()
        self.selected_plant = "peashooter"
        self.sun_score = 0
        self._load_level_index(self.level_index)

    def on_show(self):
        self.ui_manager.enable()

    def on_hide(self):
        self.ui_manager.disable()

    def on_draw(self):
        self.clear()
        self.engine.draw()

    def on_update(self, delta_time: float):
        self.engine.update(delta_time)
        if (
            self.engine.spawn_system.has_waves()
            and self.engine.spawn_system.is_finished()
            and not self.engine.context.zombies
        ):
            self._advance_level()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.KEY_1:
            self.selected_plant = "sunflower"
        if symbol == arcade.key.KEY_2:
            self.selected_plant = "peashooter"
        if symbol == arcade.key.KEY_3:
            self.selected_plant = "icepeashooter"
        if symbol == arcade.key.KEY_4:
            self.selected_plant = "repeater"

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        tile = self.engine.find_tile_at(x, y, "Plants_Grid")
        if tile:
            self.engine.plant_manager.spawn(self.selected_plant, tile)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        collected = self.engine.collect_sun_at(x, y)
        if collected:
            self.sun_score += collected
            print(self.sun_score)

    def _advance_level(self) -> None:
        next_index = self.level_index + 1
        if next_index >= len(self.levels):
            self.window.show_view(EndView())
            return
        self._load_level_index(next_index)

    def _load_levels(self) -> list[Path]:
        data_dir = c.ROOT_PATH / "assets" / "data"
        levels_file = data_dir / "levels.json"
        if levels_file.exists():
            with levels_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
            levels = []
            for entry in data.get("levels", []):
                if isinstance(entry, str):
                    filename = entry
                elif isinstance(entry, dict) and "file" in entry:
                    filename = entry["file"]
                else:
                    continue
                levels.append(data_dir / filename)
            if levels:
                return levels

        return sorted(p for p in data_dir.glob("*.json") if p.name != "levels.json")

    def _load_level_index(self, index: int) -> None:
        self.level_index = index
        self.engine = GameEngine()
        level_data = self.engine.load_level(self.levels[index])
        self.sun_score = int(level_data.get("sun", 0))
