import random

class Pioche :

    """def __init__(self, pieces) -> None:
        self.pieces = pieces
    """
    
    
    def __init__(self) -> None:  # version pas bonne mais je la mets comme ça pour pouvoir utilsier la classe Picohe dans  ui/main.py
        self.pieces = []

    def tirage_3_pieces (self) :
        return random.sample(self.pieces, 3)