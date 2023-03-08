""" Chess With Friends """

import arcade
import pieces

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Chess"
SQUARE_SIZE = 100
BOARD_SIZE = 8
MARGIN = 50


class StartMenu(arcade.View):
    """Create start menu """
    
    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.GRAY)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Welcome to Chess with Friends", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 100,
                        arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("Click an option below:", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                        arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("Singleplayer", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50,
                        arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Multiplayer", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100,
                        arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Help", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 150,
                        arcade.color.WHITE, font_size=20, anchor_x="center")
        

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        # Singleplayer
        if 200 < x < 600 and 350 < y < 400:
            game_view = Board()
            self.window.show_view(game_view)

        # Multiplayer 
        elif 200 < x < 600 and 300 < y < 350:
            game_view = Board()
            self.window.show_view(game_view)

        # Help
        elif 200 < x < 600 and 250 < y < 300:
            game_view = HelperMenu()
            self.window.show_view(game_view)

class HelperMenu(arcade.View):
    #TODO: Implement this quickly so we have full functionality of menu related stuff.
    """Helper menu explains game and controls """


class Board(arcade.View):
    """ Draws Board """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer / initialize constants
        super().__init__()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.title = SCREEN_TITLE
        arcade.set_background_color(arcade.color.LIGHT_GRAY)

        #TODO: Sprites

        self.king_b = arcade.Sprite("sprites/kingb.png", center_x= 350, center_y= 50)
        self.queen_b = arcade.Sprite("sprites/queenb.png", center_x= 450, center_y= 50)
        self.rook_b = arcade.Sprite("sprites/rookb.png", center_x= 750, center_y= 50)
        self.rook_b2 = arcade.Sprite("sprites/rookb.png", center_x= 50, center_y= 50)
        self.bishop_b = arcade.Sprite("sprites/bishopb.png", center_x= 250, center_y= 50)
        self.bishop_b2 = arcade.Sprite("sprites/bishopb.png", center_x= 550, center_y= 50)
        self.knight_b = arcade.Sprite("sprites/knightb.png", center_x= 150, center_y= 50)
        self.knight_b2 = arcade.Sprite("sprites/knightb.png", center_x= 650, center_y= 50)


    def on_draw(self):
        """
        Render the board.
        """
        self.clear()

        arcade.start_render()

        # Iterate over each row and column
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):

                # Formula to calculate the x, y position of the square
                x = column * SQUARE_SIZE + MARGIN
                y = row * SQUARE_SIZE + MARGIN

                # if square is even, draw a black rectangle
                if (row + column) % 2 == 0:
                    arcade.draw_rectangle_filled(x, y, SQUARE_SIZE, SQUARE_SIZE, arcade.color.ONYX)
                else:
                    arcade.draw_rectangle_filled(x, y, SQUARE_SIZE, SQUARE_SIZE, arcade.color.EGGSHELL)

        # Render drawing after board
        self.king_b.draw()
        self.queen_b.draw()
        self.rook_b.draw()
        self.rook_b2.draw()
        self.bishop_b.draw()
        self.bishop_b2.draw()
        self.knight_b.draw()
        self.knight_b2.draw()
        

    def on_key_press(self, key, key_modifiers):
        """ Called whenever a key on the keyboard is pressed. """
        # Exit 
        if key == arcade.key.ESCAPE:
            arcade.close_window()

        if key == arcade.key.BACKSPACE:
            game_view = StartMenu()
            self.window.show_view(game_view)
            arcade.run()

def main():
    """ Main method """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = StartMenu()
    window.show_view(game_view)
    arcade.run()
    


if __name__ == "__main__":
    main()