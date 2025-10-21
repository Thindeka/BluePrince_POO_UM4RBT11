from src.Grille import Grille
from src.Joueur import Joueur
# from src.Piece import Piece
from src.AutresObjets import Pomme, Banane, Gateau, Sandwich, Repas

class Game:

    def __init__(self):
        self.grille = Grille()
        self.joueur = Joueur()
        self.position_joueur = (0,0)  # position à revoir et joueur.position
        # self.objets_choisis = {}  on l a deja dans Joueur (inventaire)

    def deplacer_joueur(self, direction: str) -> str:
        """Déplace le joueur si possible"""
        x, y = self.position_joueur
        if direction not in ["N", "S", "E", "O"]:
            return "Direction invalide"

        new_x, new_y = self.grille.voisin(x, y, direction)
        if not self.grille.deplacement_permis(new_x, new_y):
            return "Mur en face, déplacement impossible"

        # appeler joueur.deplacer 
        #self.position_joueur = (new_x, new_y)
        # self.joueur.inventaire.utiliser_pas(1)
        return f"Déplacement réussi vers {self.position_joueur}"


    #def ajouter_piece(self, x: int, y: int, piece: Piece):
       # """Ajoute une pièce à la grille"""
        #self.objets_choisis[(x, y)] = piece

    #def ramasser_objets(self):
        #"""Ramasse tous les objets présents dans la pièce actuelle"""
        #objet = self.objets_choisis.get(self.position_joueur)
        #if not objet:
            #return "Aucune pièce ici"
"""     messages = []
        for o in objet.objets[:]: 
            msg = objet.interagir_objet(o, self.joueur)
            messages.append(msg)
        return messages"""
        
