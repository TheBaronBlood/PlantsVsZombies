import json
from pathlib import Path

import arcade

import src.constants as c
from src.components.gameEngine import GameEngine
from src.ui import PlantCardBar
from src.views.endView import EndView


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.virtual_width = c.SCREEN_WIDTH
        self.virtual_height = c.SCREEN_HEIGHT
        self.camera: arcade.Camera2D | None = None

        self.levels = self._load_levels()
        if not self.levels:
            raise RuntimeError("No levels found.")

        self.level_index = 0
        self.engine = GameEngine()
        self.available_plants = c.PLANT_CARD_ORDER or ["sunflower", "peashooter", "icepeashooter"]
        self.loadout_plants = list(self.available_plants)[: c.PLANT_CARD_SLOTS]
        self.card_bar = PlantCardBar(
            self.loadout_plants,
            max_slots=c.PLANT_CARD_SLOTS,
            card_scale=c.PLANT_CARD_SCALE,
        )
        self.sun_score = 0
        self._load_level_index(self.level_index)
        self._build_card_bar()

    def on_show(self):
        if self.window:
            self._apply_viewport(self.window.width, self.window.height)
        self._build_card_bar()

    def on_hide(self):
        return

    def on_draw(self):
        self.clear()
        if self.camera:
            self.camera.use()
        self.engine.draw()
        if self.window:
            self.window.default_camera.use()
        self.card_bar.draw()

    def on_update(self, delta_time: float):
        self.engine.update(delta_time)
        self.card_bar.update(delta_time, self.sun_score)
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
            self._build_card_bar()
            return
        return

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        if self.card_bar.handle_click(x, y, self.sun_score):
            return
        world_x, world_y = self._screen_to_world(x, y)
        tile = self.engine.find_tile_at(world_x, world_y, "Plants_Grid")
        selected_plant = self.card_bar.get_selected()
        if tile and self.card_bar.can_place(selected_plant, self.sun_score):
            self.engine.plant_manager.spawn(selected_plant, tile)
            self._apply_plant_cost(selected_plant)
            self.card_bar.mark_used(selected_plant)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        world_x, world_y = self._screen_to_world(x, y)
        collected = self.engine.collect_sun_at(world_x, world_y)
        if collected:
            self.sun_score += collected
            print(self.sun_score)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self._apply_viewport(width, height)
        self._build_card_bar()

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

    def _build_card_bar(self) -> None:
        width = self.window.width if self.window else c.SCREEN_WIDTH
        height = self.window.height if self.window else c.SCREEN_HEIGHT
        self.card_bar.build(width, height)

    def _apply_plant_cost(self, plant_name: str) -> None:
        cost = int(c.get_plant_config(plant_name).get("cost", 0))
        self.sun_score = max(0, self.sun_score - cost)

    def set_loadout(self, plants: list[str]) -> None:
        self.loadout_plants = list(plants)[: c.PLANT_CARD_SLOTS]
        self.card_bar.set_loadout(self.loadout_plants)
        self._build_card_bar()

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
