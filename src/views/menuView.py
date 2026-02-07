import arcade
import arcade.gui

import src.constants as c
from src.views.gameView import GameView


class TestMenuView(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()
        self._layout = None

    def on_show(self):
        self.ui_manager.enable()
        self._build_ui()

    def on_hide(self):
        self.ui_manager.disable()

    def on_draw(self):
        self.clear()
        if self.window:
            self.window.default_camera.use()
        self.ui_manager.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.F11:
            window = self.window
            if not window:
                return
            window.set_fullscreen(not window.fullscreen)
            if not window.fullscreen:
                window.set_size(c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
            self._build_ui()

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self._build_ui()

    def _build_ui(self) -> None:
        self.ui_manager.clear()
        width = self.window.width if self.window else c.SCREEN_WIDTH
        height = self.window.height if self.window else c.SCREEN_HEIGHT
        self._layout = arcade.gui.UIAnchorLayout(width=width, height=height)
        self.ui_manager.add(self._layout)

        box = arcade.gui.UIBoxLayout(vertical=True, space_between=12)
        self._layout.add(box, anchor_x="center", anchor_y="center")

        play_button = arcade.gui.UIFlatButton(text="Play", width=200, height=48)
        play_button.on_click = lambda event: self._start_game()
        box.add(play_button)

        load_button = arcade.gui.UIFlatButton(text="Load", width=200, height=48)
        load_button.on_click = lambda event: self._load_game()
        box.add(load_button)

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=200, height=48)
        exit_button.on_click = lambda event: self._exit_game()
        box.add(exit_button)

        box.fit_content()

    def _start_game(self) -> None:
        if self.window:
            self.window.show_view(GameView())

    def _load_game(self) -> None:
        print("Load not implemented.")

    def _exit_game(self) -> None:
        if self.window:
            self.window.close()


class MenuView(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()
        self._setup_ui()

    def _setup_ui(self):
        # Use the anchor to position the button on the screen.
        self.anchor = self.ui_manager.add(arcade.gui.UIAnchorLayout())

        play_button = arcade.gui.UIFlatButton(text="Play", width=250, y=0)
        # Initialise the button with an on_click event.
        @play_button.event("on_click")
        def _on_click(event):
            arcade.schedule(lambda dt: self.window.show_view(GameView()), 0)
            arcade.unschedule(lambda dt: self.window.show_view(GameView()))

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
            arcade.exit()

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=exit_button,
            align_y=-100
        )

    def on_show_view(self):
        self.ui_manager.enable()
        arcade.set_background_color(arcade.color.BLACK)


    def on_hide_view(self):
        self.ui_manager.disable()

    def on_draw(self):
        self.clear()

        self.ui_manager.draw()

