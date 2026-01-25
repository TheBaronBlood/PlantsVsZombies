"""View, Zeigt das Spiel und handled den Spiel Verlauf"""
__author__      = "Miro K."
__copyright__   = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

# IMPORTS
# Arcade Packages
import arcade
import arcade.gui

# Math
from pyglet.math import Vec2


from components.gameEngine import GameEngine, UIEngine
import constants as c

# TODO GameView zum Laufen Kriegen
class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.UImanager = arcade.gui.UIManager()

        self.game_engine = GameEngine()
        self.game_engine.load_tilemap(":maps:map_1.tmx")

        self.selected_plant = "peashooter"


    def _setup(self):
        pass

    def on_show(self):
        self.UImanager.enable()

    def on_hide(self):
        self.UImanager.disable()

    def on_draw(self):
        self.clear()
        self.game_engine.scene.draw(pixelated=True)
        self.game_engine.sprite_list_draw(pixelated=True)

    def on_update(self, delta_time: float) -> bool | None:
        self.game_engine.update(delta_time)

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.KEY_1:
            self.selected_plant = "sunflower"
        if symbol == arcade.key.KEY_2:
            self.selected_plant = "peashooter"
        if symbol == arcade.key.KEY_3:
            self.selected_plant = "icepeashooter"
        if symbol == arcade.key.KEY_4:
            self.selected_plant = "repeater"

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        target = self.game_engine._find_tile_at(x, y, "Plants_Grid")
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.game_engine.plant_manager.spawn_plant(self.selected_plant, target)

    def get_game_engine(self):
        return self.game_engine