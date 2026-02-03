"""Simple menu view placeholder."""
__author__ = "Miro K."
__copyright__ = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

import arcade


class MenuView(arcade.View):
    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Press Enter to Start",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.WHITE,
            24,
            anchor_x="center",
        )

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            from views.game_view import GameView

            self.window.show_view(GameView())
