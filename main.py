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


class MyGame(arcade.Window):
    """ Main application class that opens window, creates menus and board """


    def __init__(self, width, height, title):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(width, height, title)

        # Sprites will be put in lists to optmize drawing
        self.white_pawns_list = None
        self.white_bishops_list = None
        self.white_knight_list = None
        self.white_rooks_list = None
        self.white_queen = None
        self.white_king = None

        self.black_pawns_list = None
        self.black_bishops_list = None
        self.black_knight_list = None
        self.black_rooks_list = None
        self.black_queen = None
        self.black_king = None

        arcade.set_background_color(arcade.color.LIGHT_GRAY)


    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create sprites and sprite lists here
        pass


    def on_draw(self):
        """
        Render the screen.
        """


        #TODO: main menu

        # TODO: help menu
        
        # TODO: singleplayer or multiplayer menu
     
        # This command clears the screen to the background color.
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
                    arcade.draw_rectangle_filled(x, y, SQUARE_SIZE, SQUARE_SIZE, arcade.color.BLACK)
                else:
                    arcade.draw_rectangle_filled(x, y, SQUARE_SIZE, SQUARE_SIZE, arcade.color.WHITE)


    def on_key_press(self, key, key_modifiers):
        """ Called whenever a key on the keyboard is pressed. """
        # Exit 
        if key == arcade.key.ESCAPE:
            arcade.close_window()


def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()