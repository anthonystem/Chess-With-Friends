class Pieces():
    """ Pieces go here"""

    def __init__(self):
        """ Initializer """
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

    def legal_move(self):
        pass

    def generate_pieces(self):
        pass

# Subclasses for the individual pieces
class King(Pieces):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.type = 'King'

    def __str__(self):
        return self.color + ' ' + self.type

class Queen(Pieces):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.type = 'Queen'

    def __str__(self):
        return self.color + ' ' + self.type

class Knight(Pieces):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.type = 'Knight'

    def __str__(self):
        return self.color + ' ' + self.type

class Rook(Pieces):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.type = 'Rook'

    def __str__(self):
        return self.color + ' ' + self.type

class Pawn:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.type = 'Pawn'

    def __str__(self):
        return self.color + ' ' + self.type