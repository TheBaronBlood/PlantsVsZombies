"""Simple menu view placeholder."""
__author__ = "Miro K."
__copyright__ = "Electronic Arts (EA) and PopCap Games"
__license__ = "Attribution-ShareAlike 4.0 International"

import arcade


class MenuView(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        self._scheduled_start = False

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
            self._schedule_game_start()

    def _schedule_game_start(self) -> None:
        if self._scheduled_start:
            return
        self._scheduled_start = True

        def _show_game_view(_delta_time: float) -> None:
            arcade.unschedule(_show_game_view)
            from views.game_view import GameView

            self.window.show_view(GameView())

        arcade.schedule(lambda delta_time: _show_game_view(delta_time), 0)
