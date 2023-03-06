class Pieces():
    """ Pieces go here"""

    def __init__ (self):
        pass

    def legal_move(self):
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