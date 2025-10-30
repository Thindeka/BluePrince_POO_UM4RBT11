import random

class Pioche :

    """def __init__(self, pieces) -> None:
        self.pieces = pieces
    """
    
    
    def __init__(self) -> None:  # version pas bonne mais je la mets comme ça pour pouvoir utilsier la classe Picohe dans  ui/main.py
        self.pieces = []

    def objets_dans_piece(piece_nom: str) -> list:
        objets = []
        if piece_nom == "Den":
            objets.append("gemme")  # toujours
            if random.random() < 0.3:
                objets.append("coffre")
        elif piece_nom == "Veranda":
            if random.random() < 0.2:
                objets.append("patte_lapin")
        # ajouter d'autres pièces et probabilités ici
        return objets

    def tirage_3_pieces(self):
        """Tire 3 pièces aléatoires (à mettre dans Pioche)."""
        pieces_possibles = ["Veranda", "Maid's Chamber", "Furnace", "Greenhouse", "Solarium", "Den"]
        return random.choices(pieces_possibles, k=3)
