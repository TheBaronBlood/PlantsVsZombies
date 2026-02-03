#!/usr/bin/env python
"""Entry point for the game."""
__author__ = "Miro K."
__copyright__ = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

import arcade

import constants as c
from views.game_view import GameView


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.SCREEN_TITLE, resizable=True)
        arcade.resources.add_resource_handle("sprites", str(c.ROOT_PATH / "assets" / "sprites"))
        arcade.resources.add_resource_handle("maps", str(c.ROOT_PATH / "assets" / "maps"))
        arcade.resources.add_resource_handle("sounds", str(c.ROOT_PATH / "assets" / "sounds"))
        arcade.resources.add_resource_handle("data", str(c.ROOT_PATH / "assets" / "data"))


def game_start() -> None:
    window = MyWindow()
    window.show_view(GameView())
    arcade.run()


if __name__ == "__main__":
    game_start()
