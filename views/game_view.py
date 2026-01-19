import arcade
import arcade.gui as gui
from pyglet.math import Vec2
import json

from components.plant import Plant
from components.zombie import Zombie
from components.projectile import Projectile
from constants import *


#from views.menu_view import MenuView

class GameView(arcade.View):
    def __init__(self,):
        super().__init__()
        self.manager = gui.UIManager()
        self._setup_ui()
        self._load_tilemap(":level:level.tmx")

    # Erstellt die Buttons und die UI
    def _setup_ui(self):
        back_button = arcade.gui.UIFlatButton(text="Back", width=250, x=30, y=30)

        # Initialise the button with an on_click event.
        @back_button.event("on_click")
        def on_click_switch_button(event):
            from views.menu_view import MenuView
            # Passing the main view into menu view as an argument.
            menu_view = MenuView()
            self.window.show_view(menu_view)

        # Use the anchor to position the button on the screen.
        self.manager.add(back_button)

    # Lädt die Tilemap
    def _load_tilemap(self, map_file: str):
        try:
            self.tilemap = arcade.load_tilemap(map_file, scaling=SCALE_FACTOR, offset=Vec2(0, 0))
            self.scene = arcade.Scene.from_tilemap(self.tilemap)
        except Exception as e:
            # Falls Map nicht gefunden / Fehler beim Laden: Fehler protokollieren
            print(f"Fehler beim Laden der Tilemap '{map_file}': {e}")
            self.tilemap = None
            self.scene = None

    def _load_plants(self):
        with open(str(ROOT_PATH / "assets" / "data" / "plants_data.json")) as f:
            data = json.load(f)

        for plant_data in data:
            new_plant = Plant(plant_data["name"])



    #
    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.scene.draw(pixelated=True)
        self.manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass