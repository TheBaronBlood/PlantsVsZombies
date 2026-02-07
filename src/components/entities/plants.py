import src.constants as c
import arcade

import math, random
from pyglet.math import Vec2
from arcade.sprite.animated import TextureAnimation, TextureAnimationSprite, TextureKeyframe
########################################################################################################################

def _build_animation(frames: list[arcade.Texture], fps: int) -> TextureAnimation | None:
    if len(frames) < 2:
        return None
    frame_ms = max(1, int(1000 / fps))
    keyframes = [TextureKeyframe(texture=frame, duration=frame_ms) for frame in frames]
    return TextureAnimation(keyframes)


class Plant(TextureAnimationSprite):
    def __init__(self, name: str, health: int, texture_path: str | None = None) -> None:
        super().__init__(scale=c.PLANTS_SCALE)
        self.name = name
        self.health = health
        self.shoot_timer = 0.0
        self.bullet_texture = None
        self.bullet_animation = None
        self._plant_frames: list[arcade.Texture] = []
        self._plant_anim_time = 0.0
        self._plant_stage_times: list[float] = []
        self._plant_health_stages: list[int] = []
        self._set_textures(texture_path)


    # Läd die Texture und teilt sie in Sprite und Projectile
    def _set_textures(self, path: str | None) -> None:
        if path is None:
            path = f":sprites:plants/{self.name}.png"

        sprite_sheet = arcade.load_spritesheet(path)
        width, height = sprite_sheet.image.size
        columns = max(1, width // 32)
        rows = max(1, height // 32)
        total = columns * rows
        textures = sprite_sheet.get_texture_grid((32, 32), columns, total)

        plant_config = self._get_config()
        plant_frames_count = int(plant_config.get("plant_frames", 1) or 1)
        bullet_frames_count = int(plant_config.get("bullet_frames", 1) or 0)

        if rows >= 2:
            plant_frames = textures[:columns][:plant_frames_count]
            bullet_row = textures[columns: columns * 2]
            bullet_frames = bullet_row[:bullet_frames_count]
        else:
            plant_frames = textures[:plant_frames_count]
            bullet_frames = textures[plant_frames_count: plant_frames_count + bullet_frames_count]

        self._plant_frames = plant_frames
        stage_times = plant_config.get("plant_stage_times")
        health_stages = plant_config.get("plant_health_stages")
        if isinstance(health_stages, list) and health_stages:
            self._plant_health_stages = [int(h) for h in health_stages]
            if plant_frames:
                self.texture = plant_frames[0]
        elif isinstance(stage_times, list) and stage_times:
            self._plant_stage_times = [float(t) for t in stage_times]
            if plant_frames:
                self.texture = plant_frames[0]
        else:
            plant_fps = int(plant_config.get("plant_fps", 8) or 8)
            plant_animation = _build_animation(plant_frames, fps=plant_fps)
            if plant_animation:
                self.animation = plant_animation
            elif plant_frames:
                self.texture = plant_frames[0]

        if bullet_frames:
            self.bullet_texture = bullet_frames[0]
            bullet_fps = int(plant_config.get("bullet_fps", 12) or 12)
            self.bullet_animation = _build_animation(bullet_frames, fps=bullet_fps)

    def _get_config(self) -> dict:
        return {
            "sunflower": c.PLANTS_SUNFLOWER,
            "peashooter": c.PLANTS_PEASHOOTER,
            "icepeashooter": c.PLANTS_ICEPEASHOOTER,
            "repeater": c.PLANTS_REPEATER,
            "walnut": c.PLANTS_WALNUT,
            "blumerrang": c.PLANTS_BLUMERRANG,
            "potatomine": c.PLANTS_POTATOMINE,
        }.get(self.name, c.PLANTS_DEFAULTS)
    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        super().update(delta_time)
        if self._plant_health_stages and self._plant_frames:
            frame_index = 0
            for threshold in self._plant_health_stages:
                if self.health <= threshold:
                    frame_index += 1
            frame_index = min(frame_index, len(self._plant_frames) - 1)
            self.texture = self._plant_frames[frame_index]
        elif self._plant_stage_times and self._plant_frames:
            self._plant_anim_time += delta_time
            elapsed = self._plant_anim_time
            frame_index = 0
            for duration in self._plant_stage_times:
                if elapsed < duration:
                    break
                elapsed -= duration
                frame_index += 1
            frame_index = min(frame_index, len(self._plant_frames) - 1)
            self.texture = self._plant_frames[frame_index]
        elif getattr(self, "_animation", None) is not None:
            self.update_animation(delta_time)

    # Fügt Schaden Hinzu
    def take_damage(self, damage: int) -> None:
        self.health -= damage


class Projectile(TextureAnimationSprite):
    def __init__(
        self,
        x: float,
        y: float,
        speed: int,
        damage: int,
        texture: arcade.Texture | TextureAnimation,
    ) -> None:
        if isinstance(texture, TextureAnimation):
            super().__init__(center_x=x, center_y=y, scale=c.PLANTS_SCALE, animation=texture)
        else:
            super().__init__(center_x=x, center_y=y, scale=c.PLANTS_SCALE)
            self.texture = texture
        self.speed = speed * 0.013
        self.damage = damage
        self.pierce = False
        self._hit_targets: set[int] = set()
        self.velocity = Vec2(self.speed, 0)

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        super().update(delta_time)
        if getattr(self, "_animation", None) is not None:
            self.update_animation(delta_time)
        margin = 64
        if (
            self.center_x < -margin
            or self.center_x > c.SCREEN_WIDTH + margin
            or self.center_y < -margin
            or self.center_y > c.SCREEN_HEIGHT + margin
        ):
            self.remove_from_sprite_lists()

########################################################################################################################

class Sun(arcade.Sprite):
    def __init__(self, start: Vec2, target: Vec2, value: int = 25) -> None:
        super().__init__(scale=c.SUN_SCALE)
        sprite_sheet = arcade.load_spritesheet(":sprites:plants/sunflower.png")
        texture = sprite_sheet.get_texture_grid((32, 32), 2, 2)
        self.texture = texture[1]

        self.value = value
        self.p0 = start
        self.p2 = target
        self.t = 0.0
        self.speed = 0.8
        self.finished = False

        mid = (start + target) / 2
        self.p1 = mid + Vec2(0, random.uniform(40, 80))

        self.center_x = start.x
        self.center_y = start.y

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        super().update(delta_time)

        if self.finished:
            return

        self.t += delta_time * self.speed
        if self.t >= 1.0:
            self.t = 1.0
            self.finished = True

        pos = (1 - self.t) ** 2 * self.p0 + 2 * (1 - self.t) * self.t * self.p1 + self.t ** 2 * self.p2
        self.center_x = pos.x
        self.center_y = pos.y

class Sunflower(Plant):
    def __init__(self) -> None:
        super().__init__("sunflower", c.PLANTS_SUNFLOWER.get("health"))

    def create_sun(self) -> Sun:
        start = Vec2(self.center_x, self.center_y)
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(20, 60)
        target = Vec2(start.x + math.cos(angle) * radius, start.y + math.sin(angle) * radius)
        return Sun(start, target)

class PeaShooter(Plant):
    def __init__(self) -> None:
        super().__init__("peashooter", c.PLANTS_PEASHOOTER.get("health"))

class Repeater(Plant):
    def __init__(self) -> None:
        super().__init__("repeater", c.PLANTS_REPEATER.get("health"))

class IcePeaShooter(Plant):
    def __init__(self) -> None:
        super().__init__("icepeashooter", c.PLANTS_ICEPEASHOOTER.get("health"))

class Walnut(Plant):
    def __init__(self) -> None:
        super().__init__("walnut", c.PLANTS_WALNUT.get("health"))

class Blumerrang(Plant):
    def __init__(self) -> None:
        super().__init__("blumerrang", c.PLANTS_BLUMERRANG.get("health"))

class Potatomine(Plant):
    def __init__(self) -> None:
        super().__init__("potatomine", c.PLANTS_POTATOMINE.get("health"))

