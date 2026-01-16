from pathlib import Path

import arcade
import arcade.gui as gui

from constants import *

from views.menu_view import MenuView


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        # Findet den Ordner, in dem diese .py Datei liegt
        ROOT_PATH = Path(__file__).parent

        # Verbindet den Ordnerpfad sicher mit den Unterordnern
        arcade.resources.add_resource_handle("sprites", str(ROOT_PATH / "assets" / "sprites"))
        arcade.resources.add_resource_handle("tiles", str(ROOT_PATH / "assets" / "tiles"))
        arcade.resources.add_resource_handle("level", str(ROOT_PATH / "assets" / "levels"))
#-----------------------------------------------------------#
# main funktion with Window
#-----------------------------------------------------------#
def main():
    window = MyWindow()
    main_view = MenuView()
    window.show_view(main_view)
    arcade.run()

if __name__ == "__main__":
    main()