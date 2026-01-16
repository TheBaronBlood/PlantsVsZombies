import arcade
import arcade.gui as gui

from views.game_view import GameView

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = gui.UIManager()


        play_button = arcade.gui.UIFlatButton(text="Play", width=250,y=0)
        # Initialise the button with an on_click event.
        @play_button.event("on_click")
        def on_click_switch_button(event):
            # Passing the main view into menu view as an argument.
            game_view = GameView()
            self.window.show_view(game_view)
        # Use the anchor to position the button on the screen.
        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout(y=100))
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=play_button,
        )

        load_button = arcade.gui.UIFlatButton(text="Load", width=250)
        # Initialise the button with an on_click event.
        @load_button.event("on_click")
        def on_click_switch_button(event):
            # Passing the main view into menu view as an argument.
            game_view = GameView()
            self.window.show_view(game_view)
        # Use the anchor to position the button on the screen.
        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout(y=0))
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=load_button
        )

        exit_button = arcade.gui.UIFlatButton(text="exit", width=250)
        # Initialise the button with an on_click event.
        @exit_button.event("on_click")
        def on_click_switch_button(event):
            # Passing the main view into menu view as an argument.
            game_view = GameView()
            self.window.close()
        # Use the anchor to position the button on the screen.
        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout(y=-100))
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=exit_button
        )

    def on_show_view(self):
        arcade.set_background_color([rgb - 50 for rgb in arcade.color.DARK_BLUE_GRAY])
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()

        self.manager.draw()
        