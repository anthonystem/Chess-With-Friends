""" Chess With Friends """

import arcade
import math
# import pieces

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Chess"
SQUARE_SIZE = 100
BOARD_SIZE = 8
MARGIN = 50

grid = [] #2D array of squares. Indexed [y][x]

class Square():
    def __init__(self, xCoord, yCoord, x, y):
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.x = x
        self.y = y
        self.pieceOn = None
    
    def update(self):
        pass

    def __str__(self):
        return "Square: x = " + str(self.x) + ", y = " + str(self.y)

class Piece():
    def __init__(self, sprite, color, type, square):
        self.sprite = sprite
        self.color = color
        self.type = type
        self.hasMoved = False
        self.location = square
    
    def movePiece(self, square):
        self.location = square


def make_grid():
    for j in range(8):
        yCoord = j * 100 + 50
        y = j
        singleRow = []
        for i in range(8):
            xCoord = i * 100 + 50
            x = i
            singleRow.append(Square(xCoord,yCoord, x, y))
        grid.append(singleRow)

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
        self.movingPiece = None
        self.window.set_mouse_visible(False)
        self.cursor = arcade.Sprite("cursor/cursor.png", scale=2)
        self.cursor_grab = arcade.Sprite("cursor/cursor-grab.png", scale=2)

        #load black piece sprites
        self.king_b = arcade.Sprite("sprites/kingb.png", center_x= 350, center_y= 50, scale= 2)
        self.queen_b = arcade.Sprite("sprites/queenb.png", center_x= 450, center_y= 50, scale= 2)
        self.rook_b = arcade.Sprite("sprites/rookb.png", center_x= 50, center_y= 50, scale= 2)
        self.rook_b2 = arcade.Sprite("sprites/rookb.png", center_x= 750, center_y= 50, scale= 2)
        self.bishop_b = arcade.Sprite("sprites/bishopb.png", center_x= 250, center_y= 50, scale= 2)
        self.bishop_b2 = arcade.Sprite("sprites/bishopb.png", center_x= 550, center_y= 50, scale= 2)
        self.knight_b = arcade.Sprite("sprites/knightb.png", center_x= 150, center_y= 50, scale= 2)
        self.knight_b2 = arcade.Sprite("sprites/knightb.png", center_x= 650, center_y= 50, scale= 2)
        self.pawn_b1 = arcade.Sprite("sprites/pawnb.png", center_x = 50, center_y = 150, scale= 2)
        self.pawn_b2 = arcade.Sprite("sprites/pawnb.png", center_x = 150, center_y = 150, scale= 2)
        self.pawn_b3 = arcade.Sprite("sprites/pawnb.png", center_x = 250, center_y = 150, scale= 2)
        self.pawn_b4 = arcade.Sprite("sprites/pawnb.png", center_x = 350, center_y = 150, scale= 2)
        self.pawn_b5 = arcade.Sprite("sprites/pawnb.png", center_x = 450, center_y = 150, scale= 2)
        self.pawn_b6 = arcade.Sprite("sprites/pawnb.png", center_x = 550, center_y = 150, scale= 2)
        self.pawn_b7 = arcade.Sprite("sprites/pawnb.png", center_x = 650, center_y = 150, scale= 2)
        self.pawn_b8 = arcade.Sprite("sprites/pawnb.png", center_x = 750, center_y = 150, scale= 2)


        #load white piece sprites
        self.king_w = arcade.Sprite("sprites/kingw.png", center_x= 350, center_y= 750, scale= 2)
        self.queen_w = arcade.Sprite("sprites/queenw.png", center_x= 450, center_y= 750, scale= 2)
        self.rook_w = arcade.Sprite("sprites/rookw.png", center_x= 50, center_y= 750, scale= 2)
        self.rook_w2 = arcade.Sprite("sprites/rookw.png", center_x= 750, center_y= 750, scale= 2)
        self.bishop_w = arcade.Sprite("sprites/bishopw.png", center_x= 250, center_y= 750, scale= 2)
        self.bishop_w2 = arcade.Sprite("sprites/bishopw.png", center_x= 550, center_y= 750, scale= 2)
        self.knight_w = arcade.Sprite("sprites/knightw.png", center_x= 150, center_y= 750, scale= 2)
        self.knight_w2 = arcade.Sprite("sprites/knightw.png", center_x= 650, center_y= 750, scale= 2)
        self.pawn_w1 = arcade.Sprite("sprites/pawnw.png", center_x = 50, center_y = 650, scale= 2)
        self.pawn_w2 = arcade.Sprite("sprites/pawnw.png", center_x = 150, center_y = 650, scale= 2)
        self.pawn_w3 = arcade.Sprite("sprites/pawnw.png", center_x = 250, center_y = 650, scale= 2)
        self.pawn_w4 = arcade.Sprite("sprites/pawnw.png", center_x = 350, center_y = 650, scale= 2)
        self.pawn_w5 = arcade.Sprite("sprites/pawnw.png", center_x = 450, center_y = 650, scale= 2)
        self.pawn_w6 = arcade.Sprite("sprites/pawnw.png", center_x = 550, center_y = 650, scale= 2)
        self.pawn_w7 = arcade.Sprite("sprites/pawnw.png", center_x = 650, center_y = 650, scale= 2)
        self.pawn_w8 = arcade.Sprite("sprites/pawnw.png", center_x = 750, center_y = 650, scale= 2)
        
        self.setup()


    def setup(self):
        """ Setup game here. Function should restart game """

        #list of pieces
        self.pieces_list = []

        #generate grid of squares
        make_grid()

        #Add pieces to list of pieces
        #white pieces
        self.pieces_list.append(Piece(self.king_w, "white", "king", grid[7][3]))
        self.pieces_list.append(Piece(self.queen_w, "white", "queen", grid[7][4]))
        self.pieces_list.append(Piece(self.rook_w, "white", "rook", grid[7][0]))
        self.pieces_list.append(Piece(self.rook_w2, "white", "rook", grid[7][7]))
        self.pieces_list.append(Piece(self.bishop_w, "white", "bishop", grid[7][2]))
        self.pieces_list.append(Piece(self.bishop_w2, "white", "bishop", grid[7][5]))
        self.pieces_list.append(Piece(self.knight_w, "white", "knight", grid[7][1]))
        self.pieces_list.append(Piece(self.knight_w2, "white", "knight", grid[7][6]))
        self.pieces_list.append(Piece(self.pawn_w1, "white", "pawn", grid[6][0]))
        self.pieces_list.append(Piece(self.pawn_w2, "white", "pawn", grid[6][1]))
        self.pieces_list.append(Piece(self.pawn_w3, "white", "pawn", grid[6][2]))
        self.pieces_list.append(Piece(self.pawn_w4, "white", "pawn", grid[6][3]))
        self.pieces_list.append(Piece(self.pawn_w5, "white", "pawn", grid[6][4]))
        self.pieces_list.append(Piece(self.pawn_w6, "white", "pawn", grid[6][5]))
        self.pieces_list.append(Piece(self.pawn_w7, "white", "pawn", grid[6][6]))
        self.pieces_list.append(Piece(self.pawn_w8, "white", "pawn", grid[6][7]))
        #black pieces
        self.pieces_list.append(Piece(self.king_b, "black", "king", grid[0][3]))
        self.pieces_list.append(Piece(self.queen_b, "black", "queen", grid[0][4]))
        self.pieces_list.append(Piece(self.rook_b, "black", "rook", grid[0][0]))
        self.pieces_list.append(Piece(self.rook_b2, "black", "rook", grid[0][7]))
        self.pieces_list.append(Piece(self.bishop_b, "black", "bishop", grid[0][2]))
        self.pieces_list.append(Piece(self.bishop_b2, "black", "bishop", grid[0][5]))
        self.pieces_list.append(Piece(self.knight_b, "black", "knight", grid[0][1]))
        self.pieces_list.append(Piece(self.knight_b2, "black", "knight", grid[0][6]))
        self.pieces_list.append(Piece(self.pawn_b1, "black", "pawn", grid[1][0]))
        self.pieces_list.append(Piece(self.pawn_b2, "black", "pawn", grid[1][1]))
        self.pieces_list.append(Piece(self.pawn_b3, "black", "pawn", grid[1][2]))
        self.pieces_list.append(Piece(self.pawn_b4, "black", "pawn", grid[1][3]))
        self.pieces_list.append(Piece(self.pawn_b5, "black", "pawn", grid[1][4]))
        self.pieces_list.append(Piece(self.pawn_b6, "black", "pawn", grid[1][5]))
        self.pieces_list.append(Piece(self.pawn_b7, "black", "pawn", grid[1][6]))
        self.pieces_list.append(Piece(self.pawn_b8, "black", "pawn", grid[1][7]))

        #Update piece for each square
        for piece in self.pieces_list:
            piece.location.pieceOn = piece


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
        
        # Draw pieces
        for piece in self.pieces_list:
            piece.sprite.draw()

        # Draw cursor
        if not self.dragging:
            # Default cursor when not dragging a piece.
            self.cursor.draw()
        else:
            # Change cursor to grab on drag.
            self.cursor_grab.draw()

        
    def snapPiece(self, piece, x, y):
        min = 1000
        for row in grid:
            for square in row:
                xdist = pow((square.xCoord - x),2)
                ydist = pow((square.yCoord - y),2)
                dist = math.sqrt(xdist + ydist)
                if(dist < min):
                    min = dist
                    squareToMove = square
        return squareToMove

    def checkValidMove(self, piece, fromSquare, toSquare):

        def checkBishopLane():
            y = smallerXSquare.y + increment
            for x in range(smallerXSquare.x + 1, biggerXSquare.x):
                #print(grid[y][x])
                if grid[y][x].pieceOn:
                    #print("Piece on square")
                    return False
                y += increment
            return True

        def checkRookLaneX():
            for y in range(smallerYSquare.y + 1, biggerYSquare.y):
                    if grid[y][fromSquare.x].pieceOn:
                        return False
            return True
        
        def checkRookLaneY():
            for x in range(smallerXSquare.x + 1, biggerXSquare.x):
                    if grid[fromSquare.y][x].pieceOn:
                        return False
            return True

        def checkDoublePawnLane():
            if abs(fromSquare.y - toSquare.y) == 1:
                return True
            else:
                if piece.color == "white":
                    if grid[fromSquare.y - 1][fromSquare.x].pieceOn:
                        return False
                    else:
                        return True
                elif piece.color == "black":
                    if grid[fromSquare.y + 1][fromSquare.x].pieceOn:
                        return False
                    else:
                        return True

        #print("Checking Validitiy")

        #check same square
        if fromSquare is toSquare:
            #print("No move, same square")
            return False

        #get bigger x square
        if fromSquare.x > toSquare.x:
            biggerXSquare = fromSquare
            smallerXSquare = toSquare
        else:
            biggerXSquare = toSquare
            smallerXSquare = fromSquare
        #get bigger y square
        if fromSquare.y > toSquare.y:
            biggerYSquare = fromSquare
            smallerYSquare = toSquare
        else:
            biggerYSquare = toSquare
            smallerYSquare = fromSquare
        #check if variables refer to same square
        if smallerXSquare is smallerYSquare:
            increment = 1
        else:
            increment = -1
        #check that piece is not occupied by another piece of same color
        if toSquare.pieceOn: #if pieceOn is not None
            if toSquare.pieceOn.color == piece.color:
                return False
            
        #check that movement is appropriate for piece
        if piece.type == "pawn":
            if piece.hasMoved: #allow 1 step forward
                if piece.color == "white":
                    if toSquare.y + 1 == fromSquare.y and toSquare.x == fromSquare.x:
                        return True
                    else:
                        return False
                elif piece.color == "black":
                    if toSquare.y - 1 == fromSquare.y and toSquare.x == fromSquare.x:
                        return True
                    else:
                        return False
            else: #piece has not moved, allow double jump
                if piece.color == "white":
                    if fromSquare.y - toSquare.y <= 2 and toSquare.x == fromSquare.x:
                        return checkDoublePawnLane()
                    else:
                        return False
                elif piece.color == "black":
                    if toSquare.y - fromSquare.y <= 2 and toSquare.x == fromSquare.x:
                        return checkDoublePawnLane()
                    else:
                        return False


        if piece.type == "bishop":
            if abs(toSquare.x - fromSquare.x) == abs(toSquare.y - fromSquare.y):
                return checkBishopLane()
            else:
                return False
        if piece.type == "rook":
            if toSquare.x == fromSquare.x:
                return checkRookLaneX()
            elif toSquare.y == fromSquare.y:
                return checkRookLaneY()
            else:
                return False
        if piece.type == "knight":
            xChange = abs(toSquare.x - fromSquare.x)
            yChange = abs(toSquare.y - fromSquare.y)
            if (xChange == 2 and yChange == 1) or (xChange == 1 and yChange == 2):
                return True
            else:
                return False
        if piece.type == "king":
            if abs(toSquare.x - fromSquare.x) <= 1 and abs(toSquare.y - fromSquare.y) <= 1:
                return True
            else:
                return False
        if piece.type == "queen":
            if abs(toSquare.x - fromSquare.x) == abs(toSquare.y - fromSquare.y):
                return checkBishopLane()
            if toSquare.x == fromSquare.x:
                return checkRookLaneX()
            if toSquare.y == fromSquare.y:
                return checkRookLaneY()
            else:
                return False

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called when the user presses a mouse button. """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.movingPiece = None
            for piece in self.pieces_list:
                if piece.sprite.collides_with_point((x, y)):
                    self.dragging = True
                    self.movingPiece = piece
                    self.offset_x = piece.sprite.center_x - x
                    self.offset_y = piece.sprite.center_y - y
            
            self.cursor.stop()

    def on_mouse_release(self, x, y, button, modifiers):
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.dragging = False
                if self.movingPiece:
                    squareToMove = self.snapPiece(self.movingPiece, x, y)
                    #check valid move
                    if self.checkValidMove(self.movingPiece, self.movingPiece.location, squareToMove):
                        #set previous square to empty
                        self.movingPiece.location.pieceOn = None
                        #move piece, snap to new square
                        self.movingPiece.location = squareToMove
                        #update new square.pieceOn
                        squareToMove.pieceOn = self.movingPiece
                        #move sprite
                        self.movingPiece.sprite.center_x = squareToMove.xCoord 
                        self.movingPiece.sprite.center_y = squareToMove.yCoord
                        self.movingPiece.hasMoved = True
                    else:
                        #snap piece back to previous square
                        self.movingPiece.sprite.center_x = self.movingPiece.location.xCoord
                        self.movingPiece.sprite.center_y = self.movingPiece.location.yCoord

    
    def on_mouse_motion(self, x, y, dx, dy):

        self.cursor.center_x = x + 3
        self.cursor.center_y = y - 14
        self.cursor_grab.center_x = x + 3
        self.cursor_grab.center_y = y - 14

        if self.dragging:
            self.movingPiece.sprite.center_x = x 
            self.movingPiece.sprite.center_y = y 
            
        

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
