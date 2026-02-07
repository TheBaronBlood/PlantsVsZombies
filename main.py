#!/usr/bin/env python
"""View, dass das Game an sich rendert und Handled"""
__author__      = "Miro K."
__copyright__   = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

import arcade

from constants import *
from views.game_view import GameView

from views.menu_view import MenuView

class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        # Verbindet den Ordnerpfad sicher mit den Unterordnern
        arcade.resources.add_resource_handle("sprites", str(ROOT_PATH / "assets" / "sprites"))
        arcade.resources.add_resource_handle("maps", str(ROOT_PATH / "assets" / "maps"))
        arcade.resources.add_resource_handle("sounds", str(ROOT_PATH / "assets" / "sounds"))
        arcade.resources.add_resource_handle("data", str(ROOT_PATH / "assets" / "data"))
#-----------------------------------------------------------#
# main funktion with Window
#-----------------------------------------------------------#
def GameStart():
    window = MyWindow()
    main_view = GameView()
    window.show_view(main_view)
    arcade.run()

if __name__ == "__main__":
    GameStart()