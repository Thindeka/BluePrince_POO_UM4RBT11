from src.Grille import Grille
from src.Joueur import Joueur
from src.Piece import Piece
from src.AutreObjet import Pomme, Banane, Gateau, Sandwich, Repas
from src.Pioche import Pioche

class Game:  # a compléter 
    """
    Représente la logique principale du jeu.
    """

    def __init__(self):
        self.grille = Grille()
        self.joueur = Joueur()
        self.inv = self.joueur.inventaire # à voir si cela est une bonne idée (incooherences?)
        self.pioche_pieces = Pioche()
        self.state = "exploration"   # exploration au départ, sinon : "tirage", "victoire", "game_over"






