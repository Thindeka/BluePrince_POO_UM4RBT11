import random

class Pioche :

    def __init__(self, pieces) -> None:
        self.pieces = pieces

    def tirage_3_pieces (self) :
        return random.sample(self.pieces, 3)