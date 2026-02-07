import arcade


class GameContext:
    def __init__(self) -> None:
        self.tilemap: arcade.TileMap | None = None
        self.scene: arcade.Scene | None = None

        self.plants: arcade.SpriteList = arcade.SpriteList()
        self.zombies: arcade.SpriteList = arcade.SpriteList()
        self.projectiles: arcade.SpriteList = arcade.SpriteList()
        self.suns: arcade.SpriteList = arcade.SpriteList()