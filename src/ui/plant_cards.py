import arcade

import src.constants as c


class PlantCardBar:
    def __init__(
        self,
        loadout_plants: list[str],
        *,
        max_slots: int,
        card_scale: float,
    ) -> None:
        self.loadout_plants = list(loadout_plants)
        self.max_slots = max_slots
        self.base_scale = card_scale

        self._time_elapsed = 0.0
        self._plant_ready_at: dict[str, float] = {}
        self._selected_plant = self.loadout_plants[0] if self.loadout_plants else ""

        self._card_textures: dict[str, arcade.Texture] = {}
        self._card_sprite_by_plant: dict[str, arcade.Sprite] = {}
        self._ui_sprites = arcade.SpriteList()

        self._sun_sprite: arcade.Sprite | None = None
        self._sun_text: arcade.Text | None = None
        self._sun_text_pos: tuple[float, float] | None = None
        self._sun_font_size = 14
        self._last_sun_score: int | None = None

    def build(self, width: int, height: int) -> None:
        self._ui_sprites = arcade.SpriteList()
        self._card_sprite_by_plant = {}

        if width <= 0 or height <= 0:
            return

        x_padding = 16
        y_padding = 16
        spacing = 8

        scale_adjust = min(width / c.SCREEN_WIDTH, height / c.SCREEN_HEIGHT)
        card_scale = self.base_scale * scale_adjust
        self._sun_font_size = max(10, int(14 * card_scale))

        sun_texture = arcade.load_texture(":sprites:buttons/sun_scoreboard.png")
        self._sun_sprite = arcade.Sprite(sun_texture, scale=card_scale)
        sun_width = self._sun_sprite.width
        sun_height = self._sun_sprite.height
        self._sun_sprite.center_x = x_padding + sun_width / 2
        self._sun_sprite.center_y = height - y_padding - sun_height / 2
        self._sun_text_pos = (
            self._sun_sprite.center_x - sun_width * 0.16,
            self._sun_sprite.center_y - sun_height * 0.12,
        )
        self._ui_sprites.append(self._sun_sprite)

        if not self.loadout_plants:
            return

        textures = [self._get_card_texture(name) for name in self.loadout_plants]
        card_width = max(texture.width for texture in textures) * card_scale
        card_height = max(texture.height for texture in textures) * card_scale

        missing = max(0, self.max_slots - len(self.loadout_plants))
        start_x = (
            x_padding
            + sun_width
            + spacing
            + (card_width + spacing) * missing
            + card_width / 2
        )
        top_y = height - y_padding - max(card_height, sun_height) / 2

        for index, name in enumerate(self.loadout_plants):
            texture = self._get_card_texture(name)
            sprite = arcade.Sprite(texture, scale=card_scale)
            sprite.center_x = start_x + index * (card_width + spacing)
            sprite.center_y = top_y
            self._card_sprite_by_plant[name] = sprite
            self._ui_sprites.append(sprite)

    def update(self, delta_time: float, sun_score: int) -> None:
        self._time_elapsed += delta_time
        self._update_card_states(sun_score)
        self._update_sun_text(sun_score)

    def draw(self) -> None:
        self._ui_sprites.draw(pixelated=True)
        if self._sun_text:
            self._sun_text.draw()

    def handle_click(self, x: int, y: int, sun_score: int) -> bool:
        if not self._card_sprite_by_plant:
            return False
        hit = arcade.get_sprites_at_point((x, y), self._ui_sprites)
        if not hit:
            return False
        sprite = hit[-1]
        for name, card_sprite in self._card_sprite_by_plant.items():
            if card_sprite is sprite:
                if self.can_place(name, sun_score):
                    self._selected_plant = name
                return True
        return False

    def get_selected(self) -> str:
        return self._selected_plant

    def set_selected(self, plant_name: str) -> None:
        if plant_name:
            self._selected_plant = plant_name

    def set_loadout(self, plants: list[str]) -> None:
        self.loadout_plants = list(plants)[: self.max_slots]
        if self.loadout_plants:
            self._selected_plant = self.loadout_plants[0]

    def can_place(self, plant_name: str, sun_score: int) -> bool:
        return self._is_ready(plant_name) and self._can_afford(plant_name, sun_score)

    def mark_used(self, plant_name: str) -> None:
        config = c.get_plant_config(plant_name)
        cooldown = float(config.get("plant_place_cooldown", 1.0))
        self._plant_ready_at[plant_name] = self._time_elapsed + cooldown

    def _update_card_states(self, sun_score: int) -> None:
        for name, sprite in self._card_sprite_by_plant.items():
            ready = self._is_ready(name)
            affordable = self._can_afford(name, sun_score)
            enabled = ready and affordable
            sprite.alpha = 255 if enabled else 120
            sprite.color = (255, 255, 255) if enabled else (140, 140, 140)

    def _update_sun_text(self, sun_score: int) -> None:
        if self._sun_text_pos is None:
            return
        if self._sun_text is None:
            self._sun_text = arcade.Text(
                str(sun_score),
                self._sun_text_pos[0],
                self._sun_text_pos[1],
                color=arcade.color.BLACK,
                font_size=self._sun_font_size,
            )
            self._last_sun_score = sun_score
            return
        if self._last_sun_score != sun_score:
            self._sun_text.text = str(sun_score)
            self._last_sun_score = sun_score

    def _is_ready(self, plant_name: str) -> bool:
        ready_at = self._plant_ready_at.get(plant_name, 0.0)
        return self._time_elapsed >= ready_at

    def _can_afford(self, plant_name: str, sun_score: int) -> bool:
        cost = int(c.get_plant_config(plant_name).get("cost", 0))
        return sun_score >= cost

    def _get_card_texture(self, plant_name: str) -> arcade.Texture:
        texture = self._card_textures.get(plant_name)
        if texture:
            return texture
        path = f":sprites:buttons/card_{plant_name}.png"
        texture = arcade.load_texture(path)
        self._card_textures[plant_name] = texture
        return texture
