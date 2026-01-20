import arcade

from components.projectile import Projectile
from constants import *




class Plant(arcade.Sprite):
    def __init__(
            self,
            name: str,
            sun_cost: str,
            hp: float,
            damage: float,
            recharge: float,
            scale: float,
            texture: str,
            projectile_texture: str,
            scene: arcade.scene.Scene,
            plants_spritelist: arcade.SpriteList,
            projectiles_spritelist: arcade.SpriteList
    ) -> None:

        super().__init__(path_or_texture=texture,
                         scale=scale)
        self.name = name
        self.sun_cost = sun_cost
        self.hp = hp
        self.damage = damage
        self.recharge = recharge

        self.projectile_texture = projectile_texture
        self.scene = scene
        self.plants_list = plants_spritelist
        self.projectiles_list = projectiles_spritelist

        self._planting_sound = arcade.load_sound(":sounds:/einplfanzen.wav")



    def _find_tile_at(self, x: float, y: float)-> arcade.Sprite:
        tiles = arcade.get_sprites_at_point((x,y), self.scene["Plants"])
        return tiles[0] if tiles else None



    def plant_at(self, x: float, y: float) -> str:
        """
        Versucht, eine Pflanze auf dem Tile bei `(x,y)` zu setzen. \n
        - Wenn kein Plant-Tile unter `(x,y)` ist -> "no_tile"
        - Wenn bereits eine Pflanze vorhanden ist -> entfernt sie und return "removed"
        - Sonst: neue Instanz erzeugen, in plants_list einfügen -> "planted"
        :param x:
        :param y:
        :return None:
        """
        target_tile = self._find_tile_at(x,y)
        if not target_tile:
            return "No Tile"

        existing_plant = arcade.get_sprites_at_point((target_tile.center_x, target_tile.center_y), self.plants_list)
        if existing_plant:
            return "is existing plant"

        else:
            arcade.play_sound(self._planting_sound)
            new_plant = Plant(
                self.name,
                self.sun_cost,
                self.hp,
                self.damage,
                self.recharge,
                self.scale,
                self.texture,
                self.projectile_texture,
                self.scene["Plants"],
                self.plants_list,
                self.projectiles_list,
            )


            new_plant.center_x = target_tile.center_x
            new_plant.center_y = target_tile.center_y



            self.plants_list.append(new_plant)
            if self._planting_sound:
                arcade.play_sound(self._planting_sound)
            return "planted"

    def remove_plant_from(self, x: float, y: float) -> str:
        """
        Versucht, eine Plfanze auf dem Tile bei `(x,y)` zu Enterfen. \n
        :param x:
        :param y:
        :return:
        """
        target_tile = self._find_tile_at(x, y)

        if not target_tile:
            return "No Tile"

        existing_plant = arcade.get_sprites_at_point((target_tile.center_x, target_tile.center_y), self.plants_list)
        if existing_plant:
            existing_plant[0].remove_from_sprite_lists()
            return "removed existing plant"
        else:
            return "no existing plant"

    def shoot(self):
        pass

    def update(self, delta_time: float):
        pass