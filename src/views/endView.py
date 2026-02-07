import arcade


class EndView(arcade.View):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.window.set_mouse_visible(False)
        self.background_color = arcade.color.BLACK
        self.text_studio = arcade.Text(text, self.window.width // 2, self.window.height // 2,
                                       arcade.color.WHITE, 124, anchor_x="center", anchor_y="center", bold=True,
                                       font_name="Liberation Mono")
        self.background_color = arcade.color.BLACK


    def on_draw(self):
        self.clear()
        self.text_studio.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol:
            from views import MenuView
            self.window.show_view(MenuView())
            self.window.set_mouse_visible(True)