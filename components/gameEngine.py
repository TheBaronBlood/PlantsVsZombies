""""""
__author__ = "Miro K."
__copyright__ = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

# IMPORTS
# Arcade Packages
import arcade
import arcade.gui
# Math
from pyglet.math import Vec2

# Game Imports
from components.plant import PlantManager, Plant
from components.projectile import ProjectileManager, Projectile
from components.zombie import ZombieManager, Zombie
import constants as c


class GameEngine:
    def __init__(self):
        self.tilemap: arcade.TileMap | None = None
        self.scene: arcade.Scene | None = None

        # Erstellt Sprite Listen
        self.plant_sprite_list = arcade.SpriteList()
        self.zombie_sprite_list = arcade.SpriteList()
        self.projectile_sprite_list = arcade.SpriteList()

        # Erstellung der Manager für die Game Logic
        self.plant_manager = None
        self.zombie_manager = None
        self.projectile_manager = None

        self.load_manager()

    def load_manager(self):
        """Erstellung der Manager für die Game Logic"""
        self.projectile_manager = ProjectileManager(self.projectile_sprite_list, self.scene)
        self.plant_manager = PlantManager(self.plant_sprite_list,
                                          self.projectile_manager,
                                          self.scene)

        self.zombie_manager = ZombieManager(self.zombie_sprite_list,
                                            self.projectile_manager,
                                            self.scene)



    def _find_tile_at(self, x: float, y: float, sprite_layer: str)-> arcade.Sprite:
        tiles = arcade.get_sprites_at_point((x,y), self.scene[sprite_layer])
        return tiles[0] if tiles else None

    def load_tilemap(self, map_file: str):
        try:
            self.tilemap = arcade.load_tilemap(map_file, scaling=c.SCALE_FACTOR, offset=Vec2(0, 0))
            self.scene = arcade.Scene.from_tilemap(self.tilemap)

        except Exception as e:
            # Falls Map nicht gefunden / Fehler beim Laden: Fehler protokollieren
            print(f"Fehler beim Laden der Tilemap '{map_file}': {e}")

    def sprite_list_draw(self, pixelated: bool = False):
        """Zeichnet die Sprite Listen \n
            ``self.plant_sprite_list.draw()`` \n
            ``self.zombie_sprite_list.draw()`` \n
            ``self.projectile_sprite_list.draw()``
        """
        self.plant_sprite_list.draw(pixelated=pixelated)
        self.zombie_sprite_list.draw(pixelated=pixelated)
        self.projectile_sprite_list.draw(pixelated=pixelated)


    def update(self, delta_time: float):
        self.plant_sprite_list.update(delta_time)
        self.zombie_sprite_list.update(delta_time)
        self.projectile_sprite_list.update(delta_time)


    # TODO Ideen ausarbeiten was mit der GameEngine noch alles übernommen werdne kann

class UIEngine:
    pass