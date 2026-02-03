"""Simple game over view placeholder."""
__author__ = "Miro K."
__copyright__ = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

import arcade


class GameOverView(arcade.View):
    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Game Over",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.RED,
            32,
            anchor_x="center",
        )
