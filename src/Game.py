from src.Grille import Grille
from src.Joueur import Joueur
from src.Piece import Piece
from src.AutresObjets import Pomme, Banane, Gateau, Sandwich, Repas

class Game:

    def __init__(self):
        self.grille = Grille()
        self.joueur = Joueur()
        self.position_joueur = (0, 0)  # position à revoir
        self.pieces_choisies = {} 

    def deplacer_joueur(self, direction: str) -> str:
        """Déplace le joueur si possible"""
        x, y = self.position_joueur
        if direction not in ["N", "S", "E", "O"]:
            return "Direction invalide"

        new_x, new_y = self.grille.voisin(x, y, direction)
        if not self.grille.deplacement_permis(new_x, new_y):
            return "Mur en face, déplacement impossible"

        self.position_joueur = (new_x, new_y)
        self.joueur.inventaire.utiliser_pas(1)
        return f"Déplacement réussi vers {self.position_joueur}"

    def ajouter_piece(self, x: int, y: int, piece: Piece):
        """Ajoute une pièce à la grille"""
        self.pieces_choisies[(x, y)] = piece

    def ramasser_objets(self):
        """Ramasse tous les objets présents dans la pièce actuelle"""
        piece = self.pieces_choisies.get(self.position_joueur)
        if not piece:
            return "Aucune pièce ici"

        messages = []
        for obj in piece.objets[:]: 
            msg = piece.interagir_objet(obj, self.joueur)
            messages.append(msg)
        return messages
