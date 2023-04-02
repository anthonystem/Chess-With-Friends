""" Chess With Friends """

import arcade
import math
import copy
import time
# import pieces

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Chess"
SQUARE_SIZE = 100
BOARD_SIZE = 8
MARGIN = 50

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

    def __str__(self):
        return f"{self.color} {self.type}"

class Game():
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.board = Board()
        self.pieces = self.board.pieces_list
        self.grid = self.board.grid

def snapPiece(piece, x, y, grid):
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

def checkValidMove(piece, fromSquare, toSquare, grid, boardClassObject):
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
    #check same square
    if fromSquare is toSquare:
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
    #set variables for castle-ing
    if piece.color == "black":
        colorY = 0
    elif piece.color == "white":
        colorY = 7
    #check that movement is appropriate for piece
    if piece.type == "pawn":
        #check if taking diagonal
        if piece.color == "white":
            if toSquare.y + 1 == fromSquare.y and abs(toSquare.x - fromSquare.x) == 1 and toSquare.pieceOn:
                return True
        elif piece.color == "black":
            if toSquare.y - 1 == fromSquare.y and abs(toSquare.x - fromSquare.x) == 1 and toSquare.pieceOn:
                return True
        if toSquare.pieceOn: #cannot take otherwise
            return False
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
                if fromSquare.y - toSquare.y <= 2 and fromSquare.y - toSquare.y > 0 and toSquare.x == fromSquare.x:
                    return checkDoublePawnLane()
                else:
                    return False
            elif piece.color == "black":
                if toSquare.y - fromSquare.y <= 2 and toSquare.y - fromSquare.y > 0 and toSquare.x == fromSquare.x:
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
        else: #check castle
            if toSquare.y == fromSquare.y and abs(toSquare.x - fromSquare.x) == 2 and piece.hasMoved == False: 
                if toSquare.x == 1: #left rook castle
                    if (not grid[colorY][0].pieceOn.hasMoved) and (not grid[colorY][1].pieceOn) and (not grid[colorY][2].pieceOn):
                        #boardClassObject.movePiece(grid[colorY][0].pieceOn,grid[colorY][2], True) #MOVE ROOK
                        return True
                elif toSquare.x == 5: #right rook castle
                    if (not grid[colorY][7].pieceOn.hasMoved) and (not grid[colorY][4].pieceOn) and (not grid[colorY][5].pieceOn) and (not grid[colorY][6].pieceOn):
                        #boardClassObject.movePiece(grid[colorY][7].pieceOn,grid[colorY][4], True) #MOVE ROOK
                        return True
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
        
def checkTurnAndColor(piece, turn):
    if piece.color == turn:
        return True
    else:
        return False
    #ALSO: check that player is that color

def kingInCheck(king, grid, boardClassObject):
    #check if any piece in pieces_list puts king in check
    for p in boardClassObject.pieces_list:
        if checkValidMove(p, p.location, king.location, grid, boardClassObject): #piece, fromSquare, toSquare, grid, boardClassObject
            return True
    return False


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
        #explosions
        self.explode = 18
        self.explosions = True
        #Audio
        self.audio_move_piece = arcade.load_sound('audio/place_piece.wav', False)
        #self.audio_capture_piece = arcade.sound.load_sound("audio_file_name")
        self.audio_explosion = arcade.load_sound('audio/explosion.wav', False)
        self.audio_check = arcade.load_sound('audio/check.wav', False)
        self.audio_checkmate = arcade.load_sound('audio/checkmate.wav', False)
        #Cursor
        self.window.set_mouse_visible(False)
        self.cursor = arcade.Sprite("cursor/cursor.png", scale=2)
        self.cursor_grab = arcade.Sprite("cursor/cursor-grab.png", scale=2)

        self.grid = [] #2D array of squares. Indexed [y][x]
        #generate grid of squares
        self.make_grid()

        self.turn = "white"
        self.whiteInCheck = False
        self.blackInCheck = False

        #list of pieces
        self.pieces_list = []

        self.started = False

        #load black piece sprites
        self.king_b = arcade.Sprite("sprites/kingb.png", center_x= 350, center_y= 50, scale = 2)
        self.queen_b = arcade.Sprite("sprites/queenb.png", center_x= 450, center_y= 50, scale = 2)
        self.rook_b = arcade.Sprite("sprites/rookb.png", center_x= 50, center_y= 50, scale = 2)
        self.rook_b2 = arcade.Sprite("sprites/rookb.png", center_x= 750, center_y= 50, scale = 2)
        self.bishop_b = arcade.Sprite("sprites/bishopb.png", center_x= 250, center_y= 50, scale = 2)
        self.bishop_b2 = arcade.Sprite("sprites/bishopb.png", center_x= 550, center_y= 50, scale = 2)
        self.knight_b = arcade.Sprite("sprites/knightb.png", center_x= 150, center_y= 50, scale = 2)
        self.knight_b2 = arcade.Sprite("sprites/knightb.png", center_x= 650, center_y= 50, scale = 2)
        self.pawn_b1 = arcade.Sprite("sprites/pawnb.png", center_x = 50, center_y = 150, scale = 2)
        self.pawn_b2 = arcade.Sprite("sprites/pawnb.png", center_x = 150, center_y = 150, scale = 2)
        self.pawn_b3 = arcade.Sprite("sprites/pawnb.png", center_x = 250, center_y = 150, scale = 2)
        self.pawn_b4 = arcade.Sprite("sprites/pawnb.png", center_x = 350, center_y = 150, scale = 2)
        self.pawn_b5 = arcade.Sprite("sprites/pawnb.png", center_x = 450, center_y = 150, scale = 2)
        self.pawn_b6 = arcade.Sprite("sprites/pawnb.png", center_x = 550, center_y = 150, scale = 2)
        self.pawn_b7 = arcade.Sprite("sprites/pawnb.png", center_x = 650, center_y = 150, scale = 2)
        self.pawn_b8 = arcade.Sprite("sprites/pawnb.png", center_x = 750, center_y = 150, scale = 2)

        #load white piece sprites
        self.king_w = arcade.Sprite("sprites/kingw.png", center_x= 350, center_y= 750, scale = 2)
        self.queen_w = arcade.Sprite("sprites/queenw.png", center_x= 450, center_y= 750, scale = 2)
        self.rook_w = arcade.Sprite("sprites/rookw.png", center_x= 50, center_y= 750, scale = 2)
        self.rook_w2 = arcade.Sprite("sprites/rookw.png", center_x= 750, center_y= 750, scale = 2)
        self.bishop_w = arcade.Sprite("sprites/bishopw.png", center_x= 250, center_y= 750, scale = 2)
        self.bishop_w2 = arcade.Sprite("sprites/bishopw.png", center_x= 550, center_y= 750, scale = 2)
        self.knight_w = arcade.Sprite("sprites/knightw.png", center_x= 150, center_y= 750, scale = 2)
        self.knight_w2 = arcade.Sprite("sprites/knightw.png", center_x= 650, center_y= 750, scale = 2)
        self.pawn_w1 = arcade.Sprite("sprites/pawnw.png", center_x = 50, center_y = 650, scale = 2)
        self.pawn_w2 = arcade.Sprite("sprites/pawnw.png", center_x = 150, center_y = 650, scale = 2)
        self.pawn_w3 = arcade.Sprite("sprites/pawnw.png", center_x = 250, center_y = 650, scale = 2)
        self.pawn_w4 = arcade.Sprite("sprites/pawnw.png", center_x = 350, center_y = 650, scale = 2)
        self.pawn_w5 = arcade.Sprite("sprites/pawnw.png", center_x = 450, center_y = 650, scale = 2)
        self.pawn_w6 = arcade.Sprite("sprites/pawnw.png", center_x = 550, center_y = 650, scale = 2)
        self.pawn_w7 = arcade.Sprite("sprites/pawnw.png", center_x = 650, center_y = 650, scale = 2)
        self.pawn_w8 = arcade.Sprite("sprites/pawnw.png", center_x = 750, center_y = 650, scale = 2)
        
        #Add pieces to list of pieces
        #white pieces
        self.pieces_list.append(Piece(self.king_w, "white", "king", self.grid[7][3]))
        self.pieces_list.append(Piece(self.queen_w, "white", "queen", self.grid[7][4]))
        self.pieces_list.append(Piece(self.rook_w, "white", "rook", self.grid[7][0]))
        self.pieces_list.append(Piece(self.rook_w2, "white", "rook", self.grid[7][7]))
        self.pieces_list.append(Piece(self.bishop_w, "white", "bishop", self.grid[7][2]))
        self.pieces_list.append(Piece(self.bishop_w2, "white", "bishop", self.grid[7][5]))
        self.pieces_list.append(Piece(self.knight_w, "white", "knight", self.grid[7][1]))
        self.pieces_list.append(Piece(self.knight_w2, "white", "knight", self.grid[7][6]))
        self.pieces_list.append(Piece(self.pawn_w1, "white", "pawn", self.grid[6][0]))
        self.pieces_list.append(Piece(self.pawn_w2, "white", "pawn", self.grid[6][1]))
        self.pieces_list.append(Piece(self.pawn_w3, "white", "pawn", self.grid[6][2]))
        self.pieces_list.append(Piece(self.pawn_w4, "white", "pawn", self.grid[6][3]))
        self.pieces_list.append(Piece(self.pawn_w5, "white", "pawn", self.grid[6][4]))
        self.pieces_list.append(Piece(self.pawn_w6, "white", "pawn", self.grid[6][5]))
        self.pieces_list.append(Piece(self.pawn_w7, "white", "pawn", self.grid[6][6]))
        self.pieces_list.append(Piece(self.pawn_w8, "white", "pawn", self.grid[6][7]))
        #black pieces
        self.pieces_list.append(Piece(self.king_b, "black", "king", self.grid[0][3]))
        self.pieces_list.append(Piece(self.queen_b, "black", "queen", self.grid[0][4]))
        self.pieces_list.append(Piece(self.rook_b, "black", "rook", self.grid[0][0]))
        self.pieces_list.append(Piece(self.rook_b2, "black", "rook", self.grid[0][7]))
        self.pieces_list.append(Piece(self.bishop_b, "black", "bishop", self.grid[0][2]))
        self.pieces_list.append(Piece(self.bishop_b2, "black", "bishop", self.grid[0][5]))
        self.pieces_list.append(Piece(self.knight_b, "black", "knight", self.grid[0][1]))
        self.pieces_list.append(Piece(self.knight_b2, "black", "knight", self.grid[0][6]))
        self.pieces_list.append(Piece(self.pawn_b1, "black", "pawn", self.grid[1][0]))
        self.pieces_list.append(Piece(self.pawn_b2, "black", "pawn", self.grid[1][1]))
        self.pieces_list.append(Piece(self.pawn_b3, "black", "pawn", self.grid[1][2]))
        self.pieces_list.append(Piece(self.pawn_b4, "black", "pawn", self.grid[1][3]))
        self.pieces_list.append(Piece(self.pawn_b5, "black", "pawn", self.grid[1][4]))
        self.pieces_list.append(Piece(self.pawn_b6, "black", "pawn", self.grid[1][5]))
        self.pieces_list.append(Piece(self.pawn_b7, "black", "pawn", self.grid[1][6]))
        self.pieces_list.append(Piece(self.pawn_b8, "black", "pawn", self.grid[1][7]))

        #Update piece for each square
        for piece in self.pieces_list:
            piece.location.pieceOn = piece

        self.blackKing = self.grid[0][3].pieceOn
        self.whiteKing = self.grid[7][3].pieceOn

        #explosion
        if self.explosions:
            self.explosion = arcade.AnimatedTimeBasedSprite()
            for i in range(1,18):
                frame = arcade.load_texture(f"sprites/explode/f{i}.png")
                anim = arcade.AnimationKeyframe(i-1,30,frame)
                self.explosion.frames.append(anim)
            self.explosion.scale = 1.5

    def make_grid(self):
        for j in range(8):
            yCoord = j * 100 + 50
            y = j
            singleRow = []
            for i in range(8):
                xCoord = i * 100 + 50
                x = i
                singleRow.append(Square(xCoord,yCoord, x, y))
            self.grid.append(singleRow)

    def on_update(self, delta_time):
        if self.explosions:
            if self.explode < 18:
                self.explosion.update_animation()
                self.explode += 1

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
        
        #draw pieces
        for piece in self.pieces_list:
            piece.sprite.draw()

        #draw explosion
        if self.explosions:
            if self.explode < 18:
                self.explosion.draw()

        # Draw cursor
        if not self.dragging:
            # Default cursor when not dragging a piece.
            self.cursor.draw()
        else:
            # Change cursor to grab on drag.
            self.cursor_grab.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called when the user presses a mouse button. """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.movingPiece = None
            for piece in self.pieces_list:
                if piece.sprite.collides_with_point((x, y)):
                    #check that it is your turn, and that piece is your color
                    if checkTurnAndColor(piece, self.turn):
                        self.dragging = True
                        self.movingPiece = piece
                        self.offset_x = piece.sprite.center_x - x
                        self.offset_y = piece.sprite.center_y - y
            self.cursor.stop()

    def on_mouse_release(self, x, y, button, modifiers):
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.dragging = False
                if self.movingPiece:
                    squareToMove = snapPiece(self.movingPiece, x, y, self.grid)
                    #check valid move
                    if self.fullCheck(self.movingPiece, squareToMove):
                        self.movePiece(self.movingPiece, squareToMove, False)
                    else:
                        #snap piece back to previous square
                        self.movingPiece.sprite.center_x = self.movingPiece.location.xCoord
                        self.movingPiece.sprite.center_y = self.movingPiece.location.yCoord

    def fullCheck(self, piece, squareToMove):
        if checkValidMove(piece, piece.location, squareToMove, self.grid, self):
            if self.testMove(piece,squareToMove):
                return True
            else:
                return False

    def checkMate(self, turn):
        piecesOfColor = []
        if turn == "white":
            for p in self.pieces_list:
                if p.color == "black":
                    piecesOfColor.append(p)
        elif turn == "black":
            for p in self.pieces_list:
                if p.color == "white":
                    piecesOfColor.append(p)
        for piece in piecesOfColor:
            for row in self.grid:
                for square in row:
                    if self.fullCheck(piece, square):
                        print(f"safe: {piece} to {square}")
                        return False
        return True

    def movePiece(self, pieceToMove, squareToMove, castle = False):
        #check if taking piece
        if squareToMove.pieceOn: #there is a piece of opposite color on that square
            self.pieces_list.remove(squareToMove.pieceOn) #remove piece
            if self.explosions:
                self.explode = 0
                self.explosion.center_x = squareToMove.xCoord
                self.explosion.center_y = squareToMove.yCoord
                arcade.play_sound(self.audio_explosion)
        #store previous location for caste-ing
        prevLocation = pieceToMove.location
        #set previous square to empty
        pieceToMove.location.pieceOn = None
        #move piece, snap to new square
        pieceToMove.location = squareToMove
        #update new square.pieceOn
        squareToMove.pieceOn = pieceToMove
        #move sprite
        pieceToMove.sprite.center_x = squareToMove.xCoord
        pieceToMove.sprite.center_y = squareToMove.yCoord
        pieceToMove.hasMoved = True
        #Move rook if castle
        if pieceToMove.color == "black":
            colorY = 0
        elif pieceToMove.color == "white":
            colorY = 7
        if pieceToMove.type == "king" and abs(squareToMove.x - prevLocation.x) == 2:
            if squareToMove.x == 1: #left rook castle
                self.movePiece(self.grid[colorY][0].pieceOn,self.grid[colorY][2], True) #MOVE ROOK
            elif squareToMove.x == 5: #right rook castle
                self.movePiece(self.grid[colorY][7].pieceOn,self.grid[colorY][4], True) #MOVE ROOK
        #check for king in check
        if pieceToMove.color == "white":
            king = self.blackKing
        elif pieceToMove.color == "black":
            king = self.whiteKing
        if kingInCheck(king, self.grid, self):
            arcade.play_sound(self.audio_check) #play check sound
            if pieceToMove.color == "white":
                self.blackInCheck = True
            elif pieceToMove.color == "black":
                self.whiteInCheck = True
        else:
            arcade.play_sound(self.audio_move_piece) #play regular move sound
            if pieceToMove.color == "white":
                self.blackInCheck = False
            elif pieceToMove.color == "black":
                self.whiteInCheck = False
        #check if check-mate
        if self.checkMate(self.turn):
            time.sleep(.5)
            arcade.play_sound(self.audio_checkmate) #play checkmate sound
        #update turn
        if not castle:
            if self.turn == "white":
                self.turn = "black"
            elif self.turn == "black":
                self.turn = "white"      
        
    def testMove(self, pieceToMove, squareToMove):
        takenPiece = None
        if squareToMove.pieceOn: #there is a piece of opposite color on that square
            takenPiece = squareToMove.pieceOn #store taken piece
            self.pieces_list.remove(squareToMove.pieceOn) #remove piece
        #store previous square
        prevSquare = pieceToMove.location
        #set previous square to empty
        pieceToMove.location.pieceOn = None
        #move piece, snap to new square
        pieceToMove.location = squareToMove
        #update new square.pieceOn
        squareToMove.pieceOn = pieceToMove
        #check if in check
        valid = True
        if pieceToMove.color == "white":
            king = self.whiteKing
        elif pieceToMove.color == "black":
            king = self.blackKing
        if kingInCheck(king, self.grid, self):
            valid = False
        
        #move piece back

        #add taken piece back to list, if needed
        if takenPiece:
            self.pieces_list.append(takenPiece)
        #set previous square pieceOn back to pieceToMove
        prevSquare.pieceOn = pieceToMove
        #move piece back to previous Square
        pieceToMove.location = prevSquare
        #set squareToMove to empty
        if takenPiece:
            squareToMove.pieceOn = takenPiece
        else:
            squareToMove.pieceOn = None
        #return
        return valid

    def ownKingSafe(self): #NOT CURRENTLY IN USE
        if self.movingPiece.color == "white" and self.whiteInCheck:
            if kingInCheck(self.whiteKing, self.grid, self):
                return False
        elif self.movingPiece.color == "black" and self.blackInCheck:
            if kingInCheck(self.blackKing, self.grid, self):
                return False
        return True
    
    def on_mouse_motion(self, x, y, dx, dy):
        if self.dragging:
            self.movingPiece.sprite.center_x = x 
            self.movingPiece.sprite.center_y = y 
        self.cursor.center_x = x + 3
        self.cursor.center_y = y - 14
        self.cursor_grab.center_x = x + 3
        self.cursor_grab.center_y = y - 14

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
            #generate new game
            game1 = Game("heshi","aiden")
            game_view = game1.board
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
