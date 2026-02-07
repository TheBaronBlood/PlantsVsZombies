import arcade

import src.constants as c
from src.views import MenuView


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.GAME_TITLE, fullscreen=True)
        arcade.resources.add_resource_handle("sprites", str(c.ROOT_PATH / "assets" / "sprites"))
        arcade.resources.add_resource_handle("maps", str(c.ROOT_PATH / "assets" / "maps"))
        arcade.resources.add_resource_handle("sounds", str(c.ROOT_PATH / "assets" / "sounds"))
        arcade.resources.add_resource_handle("data", str(c.ROOT_PATH / "assets" / "data"))



def game_start() -> None:
    window = MyWindow()
    window.show_view(MenuView())
    arcade.run()



if __name__ == "__main__":
    game_start()
