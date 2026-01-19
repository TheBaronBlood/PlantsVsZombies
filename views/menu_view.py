import arcade
import arcade.gui as gui

from views.game_view import GameView

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = gui.UIManager()
        self._setup_ui()

    def _setup_ui(self):
        # Use the anchor to position the button on the screen.
        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        play_button = arcade.gui.UIFlatButton(text="Play", width=250, y=0)
        # Initialise the button with an on_click event.
        @play_button.event("on_click")
        def _on_click(event):
            # Passing the main view into menu view as an argument.
            game_view = GameView()
            self.window.show_view(game_view)

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=play_button,
            align_y=100
        )

        load_button = arcade.gui.UIFlatButton(text="Load", width=250)
        # Initialise the button with an on_click event.
        @load_button.event("on_click")
        def _on_click(event):
            # Passing the main view into menu view as an argument.
            game_view = GameView()
            self.window.show_view(game_view)

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=load_button,
            align_y=0
        )

        exit_button = arcade.gui.UIFlatButton(text="exit", width=250)

        # Initialise the button with an on_click event.
        @exit_button.event("on_click")
        def _on_click(event):
            # Passing the main view into menu view as an argument.
            game_view = GameView()
            self.window.close()

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=exit_button,
            align_y=-100
        )

    def on_show_view(self):
        arcade.set_background_color([rgb - 50 for rgb in arcade.color.DARK_BLUE_GRAY])
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()

        self.manager.draw()
        