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

        self._plant_sprite_list = arcade.SpriteList()
        self._projectile_sprite_list = arcade.SpriteList()

        self.plants = self._load_plants()
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

    def _load_plants(self, name=None) -> dict[str , Plant] :
        with open(str(ROOT_PATH / "assets" / "data" / "plants_data.json")) as f:
            data = json.load(f)

        print(data)
        if name is None:
            plant_objects = {}
            for plant in data:
                plant_data = data[plant]

                if plant_data["scale"] != "SCALE_FACTOR":
                    scale = float(plant_data["scale"])

                else:
                    scale = SCALE_FACTOR

                new_plant = Plant(plant_data["name"],
                                  plant_data["sun_cost"],
                                  plant_data["hp"],
                                  plant_data["damage"],
                                  plant_data["recharge"],
                                  scale,
                                  plant_data["plant_texture"],
                                  plant_data["projectil_texture"],
                                  self.scene,
                                  self._plant_sprite_list,
                                  self._projectile_sprite_list)
                plant_objects[plant_data["name"]] = new_plant
            return plant_objects
        else:
            plant_data = data[name]
            new_plant = Plant(plant_data["name"],
                              plant_data["sun_cost"],
                              plant_data["hp"],
                              plant_data["damage"],
                              plant_data["recharge"],
                              scale,
                              plant_data["plant_texture"],
                              plant_data["projectil_texture"],
                              self.scene,
                              self._plant_sprite_list,
                              self._projectile_sprite_list)
            return new_plant

    #
    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.scene.draw(pixelated=True)
        self._plant_sprite_list.draw(pixelated=True)
        self._projectile_sprite_list.draw(pixelated=True)
        self.manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if not arcade.get_sprites_at_point((x,y), self._plant_sprite_list):
            self.plants["sunflower"].plant_at(x, y)
        else:
            self.plants["sunflower"].remove_plant_from(x,y)

