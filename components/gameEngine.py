""""""
__author__ = "Miro K."
__copyright__ = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

# IMPORTS
# Arcade Packages
import arcade
import arcade.gui
from arcade import SpriteList
# Math
from pyglet.math import Vec2

# Game Imports
from components.plant import PlantManager, Plant, Sun
from components.projectile import ProjectileManager, Projectile
from components.zombie import ZombieManager, Zombie
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
        self.on_zombie_hit()
        self.on_plant_hit(delta_time)
        self.sun_despawn(delta_time)

    def on_zombie_hit(self):
        for zombie in self.zombie_sprite_list:
            collisions = arcade.check_for_collision_with_list(zombie, self.projectile_sprite_list)
            rasenmeaher_list = arcade.check_for_collision_with_list(zombie, self.scene["Rasenmäher"])
            for projectile in collisions:
                zombie.take_damage(projectile.damage)
                # optional: Projectile entfernen, wenn es treffen soll
                projectile.remove_from_sprite_lists()

            if zombie.health <= 0:
                zombie.remove_from_sprite_lists()

            for rasenmeaher in rasenmeaher_list:
                zombie.kill()
                





    def on_plant_hit(self, delta_time: float):
        for zombie in self.zombie_sprite_list:
            collisions = arcade.check_for_collision_with_list(zombie, self.plant_sprite_list)
            if collisions:
                for plant in collisions:
                    zombie.velocity = Vec2(0, 0)
                    zombie.rest_time += delta_time
                    if zombie.rest_time >= zombie.attack_time:

                        plant.take_damage(zombie.damage)

                        # optional: Projectile entfernen, wenn es treffen soll
                    if plant.health <= 0:
                        zombie.velocity = Vec2(-zombie.speed, 0)
                        plant.remove_from_sprite_lists()
            else:
                if zombie.change_x == 0:
                    zombie.change_x = -zombie.speed
                    zombie.velocity = (-zombie.speed, 0)
                    zombie.rest_time = 0

    def sun_despawn(self, delta_time: float):
        for sun in self.sun_sprite_list:
            sun.shoot_timer += delta_time
            DESPAWN_COOLDOWN = 5
            if sun.shoot_timer >= DESPAWN_COOLDOWN:
                sun.remove_from_sprite_lists()




    # TODO Ideen ausarbeiten was mit der GameEngine noch alles übernommen werdne kann

class UIEngine:
    pass