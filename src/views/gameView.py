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
        self.virtual_width = c.SCREEN_WIDTH
        self.virtual_height = c.SCREEN_HEIGHT
        self.camera: arcade.Camera2D | None = None

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
        if self.window:
            self._apply_viewport(self.window.width, self.window.height)

    def on_hide(self):
        self.ui_manager.disable()

    def on_draw(self):
        self.clear()
        if self.camera:
            self.camera.use()
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
        if symbol == arcade.key.F11:
            window = self.window
            if not window:
                return
            window.set_fullscreen(not window.fullscreen)
            if not window.fullscreen:
                window.set_size(c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
            return
        if symbol == arcade.key.KEY_1:
            self.selected_plant = "sunflower"
        if symbol == arcade.key.KEY_2:
            self.selected_plant = "peashooter"
        if symbol == arcade.key.KEY_3:
            self.selected_plant = "blumerrang"
        if symbol == arcade.key.KEY_4:
            self.selected_plant = "walnut"

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        world_x, world_y = self._screen_to_world(x, y)
        tile = self.engine.find_tile_at(world_x, world_y, "Plants_Grid")
        if tile:
            self.engine.plant_manager.spawn(self.selected_plant, tile)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        world_x, world_y = self._screen_to_world(x, y)
        collected = self.engine.collect_sun_at(world_x, world_y)
        if collected:
            self.sun_score += collected
            print(self.sun_score)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self._apply_viewport(width, height)

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
        if self.window:
            self._apply_viewport(self.window.width, self.window.height)

    def _apply_viewport(self, width: int, height: int) -> None:
        if width <= 0 or height <= 0:
            return
        if not self.camera:
            if not self.window:
                return
            self.camera = arcade.Camera2D(window=self.window)
        self.camera.match_window()
        map_size = self._get_map_pixel_size()
        x_offset = 0.96
        y_offset = 1
        zoom_offset = 1.1
        if map_size:
            map_width, map_height = map_size
            scale_x = width / map_width
            scale_y = height / map_height
            self.camera.zoom = min(scale_x, scale_y) * (zoom_offset)
            self.camera.position = (map_width / 2 * x_offset, map_height / 2 * y_offset)

    def _get_map_pixel_size(self) -> tuple[float, float] | None:
        tilemap = self.engine.context.tilemap
        if not tilemap:
            return None
        map_width = tilemap.width * tilemap.tile_width
        map_height = tilemap.height * tilemap.tile_height
        if map_width <= 0 or map_height <= 0:
            return None
        return float(map_width), float(map_height)

    def _screen_to_world(self, x: float, y: float) -> tuple[float, float]:
        if not self.camera:
            return x, y
        world = self.camera.unproject((x, y))
        return world[0], world[1]
