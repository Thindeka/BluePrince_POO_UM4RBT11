from src.Grille import Grille
from src.Joueur import Joueur
from src.Piece import Piece
from src.AutreObjet import Pomme, Banane, Gateau, Sandwich, Repas
from src.Pioche import Pioche

class Game:  # a compléter 
    """
    Représente la logique principale du jeu.
    """

    def __init__(self, grille : Grille, joueur : Joueur, pioche_pieces):
        self.grille = grille
        self.joueur = joueur
        self.inv = joueur.inventaire # à voir si cela est une bonne idée (incooherences?)
        self.pioche_pieces = pioche_pieces






