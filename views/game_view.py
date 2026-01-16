import arcade
import arcade.gui as gui

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
        
        self.tilemap = arcade.load_tilemap(map_name, scaling=2.85, offset=(0,0))
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
        # Größe eines Tiles in Pixeln (inkl. Scaling)
        tile_width = self.tilemap.tile_width * self.tilemap.scaling
        tile_height = self.tilemap.tile_height * self.tilemap.scaling

        # Tile-Koordinaten berechnen
        tile_x = int(x // tile_width)
        tile_y = int(y // tile_height)

        print(f"Tile angeklickt: x={tile_x}, y={tile_y}")

        # Optional: Tile aus der 'Feld'-Layer holen
        feld_layer = self.tilemap.get_tilemap_layer("Feld")
        print(feld_layer)