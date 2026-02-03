""""""
__author__ = "Miro K."
__copyright__ = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

# IMPORTS
# Arcade Packages
import arcade
from arcade import SpriteList
# Math
from pyglet.math import Vec2

# Game Imports
from components.plant import PlantManager, Plant, Sun
from components.projectile import ProjectileManager, Projectile
from components.zombie import ZombieManager, Zombie
from components.systems import CombatSystem, SpawnSystem, SunSystem
import constants as c


class GameEngine:
    def __init__(self):
        self.tilemap: arcade.TileMap | None = None
        self.scene: arcade.Scene | None = None

        # Erstellt Sprite Listen
        self.plant_sprite_list: SpriteList[Plant] = arcade.SpriteList()
        self.zombie_sprite_list: SpriteList[Zombie] = arcade.SpriteList()
        self.projectile_sprite_list: SpriteList[Projectile] = arcade.SpriteList()
        self.sun_sprite_list: SpriteList[Sun] = arcade.SpriteList()

        # Erstellung der Manager für die Game Logic
        self.plant_manager = None
        self.zombie_manager = None
        self.projectile_manager = None

        self.combat_system = None
        self.spawn_system = None
        self.sun_system = None

        # self.load_manager()

    def load_manager(self):
        """Erstellung der Manager für die Game Logic"""
        self.projectile_manager = ProjectileManager(self.projectile_sprite_list, self.scene)
        self.plant_manager = PlantManager(self.plant_sprite_list,
                                          self.projectile_manager,
                                          self.sun_sprite_list,
                                          self.scene)

        self.zombie_manager = ZombieManager(self.zombie_sprite_list,
                                            self.projectile_manager,
                                            self.scene)

        self.combat_system = CombatSystem(
            self.zombie_sprite_list,
            self.plant_sprite_list,
            self.projectile_sprite_list,
            self.scene,
        )
        self.spawn_system = SpawnSystem(
            self.zombie_manager,
            ["Normal", "Pylone", "Bucket"],
            spawn_interval=1.0,
        )
        self.sun_system = SunSystem(self.sun_sprite_list)


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
        self.sun_sprite_list.draw(pixelated=pixelated)


    def update(self, delta_time: float):
        self.plant_sprite_list.update(delta_time)
        self.zombie_sprite_list.update(delta_time)
        self.projectile_sprite_list.update(delta_time)
        self.sun_sprite_list.update(delta_time)
        self.combat_system.handle_projectile_hits()
        self.combat_system.handle_plant_hits(delta_time)
        self.sun_system.despawn(delta_time)
        self.spawn_system.update(delta_time)

    def collect_sun_at(self, x: float, y: float) -> int:
        return self.sun_system.collect_at(x, y)




    # TODO Ideen ausarbeiten was mit der GameEngine noch alles übernommen werdne kann

class UIEngine:
    pass
