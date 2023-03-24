""" Chess With Friends """

import arcade
# import pieces

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Chess"
SQUARE_SIZE = 100
BOARD_SIZE = 8
MARGIN = 50

class Board(arcade.View):
    """ Draws Board / Currently holds functionality of generating pieces"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer / initialize constants
        super().__init__()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.title = SCREEN_TITLE
        arcade.set_background_color(arcade.color.LIGHT_GRAY)
        self.dragging = False

        # Generate pieces
        self.king_b = arcade.Sprite("sprites/kingb.png", center_x= 350, center_y= 50)
        self.queen_b = arcade.Sprite("sprites/queenb.png", center_x= 450, center_y= 50)
        self.rook_b = arcade.Sprite("sprites/rookb.png", center_x= 50, center_y= 50)
        self.rook_b2 = arcade.Sprite("sprites/rookb.png", center_x= 750, center_y= 50)
        self.bishop_b = arcade.Sprite("sprites/bishopb.png", center_x= 250, center_y= 50)
        self.bishop_b2 = arcade.Sprite("sprites/bishopb.png", center_x= 550, center_y= 50)
        self.knight_b = arcade.Sprite("sprites/knightb.png", center_x= 150, center_y= 50)
        self.knight_b2 = arcade.Sprite("sprites/knightb.png", center_x= 650, center_y= 50)
        self.pawn_b1 = arcade.Sprite("sprites/pawnb.png", center_x = 50, center_y = 150)
        self.pawn_b2 = arcade.Sprite("sprites/pawnb.png", center_x = 150, center_y = 150)
        self.pawn_b3 = arcade.Sprite("sprites/pawnb.png", center_x = 250, center_y = 150)
        self.pawn_b4 = arcade.Sprite("sprites/pawnb.png", center_x = 350, center_y = 150)
        self.pawn_b5 = arcade.Sprite("sprites/pawnb.png", center_x = 450, center_y = 150)
        self.pawn_b6 = arcade.Sprite("sprites/pawnb.png", center_x = 550, center_y = 150)
        self.pawn_b7 = arcade.Sprite("sprites/pawnb.png", center_x = 650, center_y = 150)
        self.pawn_b8 = arcade.Sprite("sprites/pawnb.png", center_x = 750, center_y = 150)

        
        #white pieces
        self.king_w = arcade.Sprite("sprites/kingw.png", center_x= 350, center_y= 750)
        self.queen_w = arcade.Sprite("sprites/queenw.png", center_x= 450, center_y= 750)
        self.rook_w = arcade.Sprite("sprites/rookw.png", center_x= 750, center_y= 750)
        self.rook_w2 = arcade.Sprite("sprites/rookw.png", center_x= 50, center_y= 750)
        self.bishop_w = arcade.Sprite("sprites/bishopw.png", center_x= 250, center_y= 750)
        self.bishop_w2 = arcade.Sprite("sprites/bishopw.png", center_x= 550, center_y= 750)
        self.knight_w = arcade.Sprite("sprites/knightw.png", center_x= 150, center_y= 750)
        self.knight_w2 = arcade.Sprite("sprites/knightw.png", center_x= 650, center_y= 750)
        self.pawn_w1 = arcade.Sprite("sprites/pawnw.png", center_x = 50, center_y = 650)
        self.pawn_w2 = arcade.Sprite("sprites/pawnw.png", center_x = 150, center_y = 650)
        self.pawn_w3 = arcade.Sprite("sprites/pawnw.png", center_x = 250, center_y = 650)
        self.pawn_w4 = arcade.Sprite("sprites/pawnw.png", center_x = 350, center_y = 650)
        self.pawn_w5 = arcade.Sprite("sprites/pawnw.png", center_x = 450, center_y = 650)
        self.pawn_w6 = arcade.Sprite("sprites/pawnw.png", center_x = 550, center_y = 650)
        self.pawn_w7 = arcade.Sprite("sprites/pawnw.png", center_x = 650, center_y = 650)
        self.pawn_w8 = arcade.Sprite("sprites/pawnw.png", center_x = 750, center_y = 650)
        
        
        
        
        
        
        self.pieces_list = arcade.SpriteList()

    def setup(self):
        """ Setup game here. Function should restart game """

        # List of pieces we are dragging with the mouse
        self.held_pieces = []

        # Original location of piece we are dragging with the mouse in case
        # they have to go back.
        self.held_pieces_original_position = []

        # Sprite list with all the pieces
        self.pieces_list = arcade.SpriteList()

        # Add pieces to list of pieces
        self.pieces_list.append(self.king_b)
        self.pieces_list.append(self.queen_b)
        self.pieces_list.append(self.rook_b)
        self.pieces_list.append(self.rook_b2)
        self.pieces_list.append(self.bishop_b)
        self.pieces_list.append(self.bishop_b2)
        self.pieces_list.append(self.knight_b)
        self.pieces_list.append(self.knight_b2)
        self.pieces_list.append(self.pawn_b1)
        self.pieces_list.append(self.pawn_b2)
        self.pieces_list.append(self.pawn_b3)
        self.pieces_list.append(self.pawn_b4)
        self.pieces_list.append(self.pawn_b5)
        self.pieces_list.append(self.pawn_b6)
        self.pieces_list.append(self.pawn_b7)
        self.pieces_list.append(self.pawn_b8)
        
        #white pieces
        self.pieces_list.append(self.king_w)
        self.pieces_list.append(self.queen_w)
        self.pieces_list.append(self.rook_w)
        self.pieces_list.append(self.rook_w2)
        self.pieces_list.append(self.bishop_w)
        self.pieces_list.append(self.bishop_w2)
        self.pieces_list.append(self.knight_w)
        self.pieces_list.append(self.knight_w2)
        self.pieces_list.append(self.pawn_w1)
        self.pieces_list.append(self.pawn_w2)
        self.pieces_list.append(self.pawn_w3)
        self.pieces_list.append(self.pawn_w4)
        self.pieces_list.append(self.pawn_w5)
        self.pieces_list.append(self.pawn_w6)
        self.pieces_list.append(self.pawn_w7)
        self.pieces_list.append(self.pawn_w8)

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
        self.pawn_b1.draw()
        self.pawn_b2.draw()
        self.pawn_b3.draw()
        self.pawn_b4.draw()
        self.pawn_b5.draw()
        self.pawn_b6.draw()
        self.pawn_b7.draw()
        self.pawn_b8.draw()
        
        self.king_w.draw()
        self.queen_w.draw()
        self.rook_w.draw()
        self.rook_w2.draw()
        self.bishop_w.draw()
        self.bishop_w2.draw()
        self.knight_w.draw()
        self.knight_w2.draw()
        self.pawn_w1.draw()
        self.pawn_w2.draw()
        self.pawn_w3.draw()
        self.pawn_w4.draw()
        self.pawn_w5.draw()
        self.pawn_w6.draw()
        self.pawn_w7.draw()
        self.pawn_w8.draw()
        
    
    def on_mouse_press(self, x, y, button, modifiers):
        """ Called when the user presses a mouse button. """

        if button == arcade.MOUSE_BUTTON_LEFT:
             if self.king_b.collides_with_point((x, y)):
                self.dragging = True
                self.offset_x = self.king_b.center_x - x
                self.offset_y = self.king_b.center_y - y
            

    def on_mouse_release(self, x, y, button, modifiers):
            if button == arcade.MOUSE_BUTTON_LEFT: #TODO And if move is legal
                
                self.dragging = False

    
    def on_mouse_motion(self, x, y, dx, dy):
        if self.dragging:
            self.king_b.center_x = x 
            self.king_b.center_y = y 

    def on_key_press(self, key, key_modifiers):
        """ Called whenever a key on the keyboard is pressed. """
        # Exit 
        if key == arcade.key.ESCAPE:
            arcade.close_window()

        if key == arcade.key.BACKSPACE:
            game_view = StartMenu()
            self.window.show_view(game_view)
            arcade.run()

    
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

def main():
    """ Main method """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = StartMenu()
    window.show_view(game_view)
    arcade.run()
    


if __name__ == "__main__":
    main()
