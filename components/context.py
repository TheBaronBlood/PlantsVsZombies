"""Shared game state container."""
__author__ = "Miro K."
__copyright__ = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

import arcade


class GameContext:
    def __init__(self) -> None:
        self.tilemap: arcade.TileMap | None = None
        self.scene: arcade.Scene | None = None

        self.plants: arcade.SpriteList = arcade.SpriteList()
        self.zombies: arcade.SpriteList = arcade.SpriteList()
        self.projectiles: arcade.SpriteList = arcade.SpriteList()
        self.suns: arcade.SpriteList = arcade.SpriteList()
