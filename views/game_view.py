import arcade
import arcade.gui as gui
from pyglet.math import Vec2

from constants import SCALE_FACTOR


#from views.menu_view import MenuView

class GameView(arcade.View):
    def __init__(self,):
        super().__init__()
        self.manager = gui.UIManager()
        

        back_button = arcade.gui.UIFlatButton(text="Back", width=250, x=30, y=30)
        # Initialise the button with an on_click event.
        @back_button.event("on_click")
        def on_click_switch_button(event):
            from views.menu_view import MenuView
            # Passing the main view into menu view as an argument.
            menu_view = MenuView()
            self.window.show_view(menu_view)
        # Use the anchor to position the button on the screen.
        self.manager.add(back_button)

        map_name = ":level:level.tmx"
        
        self.tilemap = arcade.load_tilemap(map_name, scaling=SCALE_FACTOR, offset=Vec2(0,0))
        self.scene = arcade.Scene.from_tilemap(self.tilemap)

        

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.scene.draw(pixelated=True)
        self.manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        tile = arcade.get_sprites_at_point((x, y), self.scene["Feld"])
        tile[0].alpha = 90

    def on_mouse_release(self, x, y, button, modifiers):
        tile = arcade.get_sprites_at_point((x, y), self.scene["Feld"])
        tile[0].alpha = 1000