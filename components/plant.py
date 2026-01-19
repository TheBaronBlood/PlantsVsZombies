import arcade

from constants import *

class Plant(arcade.Sprite):
    def __init__(
            self,
            texture: str,
            scale: float,
            scene: arcade.scene.Scene,
            plants_spritelist: arcade.SpriteList,
            projectiles_spritelist: arcade.SpriteList
    ) -> None:
        super().__init__(path_or_texture=texture,
                         scale=scale)

        self.scene = scene
        self.plants_list = plants_spritelist

    def _find_tile_at(self, x: float, y: float):
        tiles = arcade.get_sprites_at_point((x,y), self.scene["Plants"])