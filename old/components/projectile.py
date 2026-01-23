import arcade

from constants import *

class Projectile(arcade.Sprite):
    def __init__(
            self,
            path_or_texture: str,
            damage: float,
            speed: float,
            scale: float,
    ) -> None:
        # Initialisiere das Sprite
        super().__init__(path_or_texture=path_or_texture, scale=scale)
        
        self.damage = damage
        self.speed = speed
        self.center_x = center_x
        self.center_y = center_y

    def update(self):
        """
        Wird automatisch von Arcade aufgerufen, wenn projectiles_list.update() 
        im Hauptspiel aufgerufen wird.
        """
        # Das Projektil bewegt sich nach rechts (typisch für PvZ-Klone)
        self.center_x += self.speed

        # Wenn das Projektil den rechten Bildschirmrand verlässt, lösche es
        # (Angenommen, die Breite ist in deinen constants hinterlegt oder wir nutzen 2000 als Puffer)
        if self.left > SCREEN_WIDTH: # Hier kannst du SCREEN_WIDTH aus deinen constants nutzen
            self.remove_from_sprite_lists()