"""Main gameplay view."""
__author__ = "Miro K."
__copyright__ = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

import arcade
import arcade.gui

import constants as c
from components.gameEngine import GameEngine


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()
        self.camera: arcade.Camera | None = None

        self.engine = GameEngine()
        self.engine.load_tilemap(":maps:map_1.tmx")

        self.selected_plant = "peashooter"
        self.sun_score = 50

    def on_show(self):
        self.ui_manager.enable()
        self._configure_camera()

    def on_hide(self):
        self.ui_manager.disable()

    def on_draw(self):
        self.clear()
        if self.camera:
            self.camera.use()
        self.engine.draw()

    def on_update(self, delta_time: float):
        self.engine.update(delta_time)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self._configure_camera()

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

    def _configure_camera(self) -> None:
        if not self.window:
            return
        if self.camera is None:
            self.camera = arcade.Camera(self.window.width, self.window.height)
        else:
            self.camera.resize(self.window.width, self.window.height)
        zoom_x = self.window.width / c.SCREEN_WIDTH
        zoom_y = self.window.height / c.SCREEN_HEIGHT
        self.camera.zoom = min(zoom_x, zoom_y)
