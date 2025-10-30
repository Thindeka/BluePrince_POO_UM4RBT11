from __future__ import annotations
import random
from typing import List, Optional, Dict, TYPE_CHECKING

from src.Piece2 import (
    Piece2, CouleurPiece,
    FORME_CROIX, FORME_COULOIR_NS, FORME_COULOIR_EO,
    FORME_IMPASSE_E, FORME_IMPASSE_N, FORME_IMPASSE_S, FORME_IMPASSE_O,
    FORME_ANGLE_NE, FORME_ANGLE_ES, FORME_ANGLE_SO, FORME_ANGLE_ON,
)

if TYPE_CHECKING:
    from src.Grille import Grille

# gestion de la rareté des pieces 
def correspondance_poids_rarete (rarete : int) -> int :
    correspondances = {0 : 27, 1 : 9, 2 : 3, 3 : 1}
    return correspondances.get(rarete, 1)


class Pioche2 :

    def __init__(self) -> None : 
        self.liste_pieces : List[Piece2] = self.construire_liste_pieces()
        self.bonus_couleur : Dict[int, float] = {}   # le int correspond a la couleur

    def construire_liste_pieces (self) -> List[Piece2] :

        l : List[Piece2] = []

        # LISTE PROPOSÉE PAR CHATGPT POUR ALLER PLUS VITE (à modifier par la suite)


        # --- BLEU (communes, toujours utiles) ---
        l.append(Piece2("Bleu - croix", CouleurPiece.BLEU, FORME_CROIX, cout_gemmes=0, rarete=0))
        l.append(Piece2("Bleu - couloir NS", CouleurPiece.BLEU, FORME_COULOIR_NS, cout_gemmes=0, rarete=0))
        l.append(Piece2("Bleu - angle NE", CouleurPiece.BLEU, FORME_ANGLE_NE, cout_gemmes=0, rarete=0))

        # --- ORANGE (plutôt couloirs) ---
        l.append(Piece2("Orange - couloir EO", CouleurPiece.ORANGE, FORME_COULOIR_EO, cout_gemmes=0, rarete=0))
        l.append(Piece2("Orange - T (NEO)", CouleurPiece.ORANGE, FORME_CROIX, cout_gemmes=1, rarete=1))

        # --- VERT (jardin / un peu plus cher) ---
        l.append(Piece2("Vert - angle ES", CouleurPiece.VERT, FORME_ANGLE_ES, cout_gemmes=1, rarete=1))

        # --- VIOLET (chambre) ---
        l.append(Piece2("Violet - angle ON", CouleurPiece.VIOLET, FORME_ANGLE_ON, cout_gemmes=1, rarete=1))

        # --- JAUNE (magasin) ---
        l.append(Piece2("Jaune - angle NE", CouleurPiece.JAUNE, FORME_ANGLE_NE, cout_gemmes=0, rarete=2))

        # --- ROUGE (moins sympa) ---
        l.append(Piece2("Rouge - couloir NS", CouleurPiece.ROUGE, FORME_COULOIR_NS, cout_gemmes=0, rarete=2))

        return l



    def _garder_pieces_compatibles (self, grille : 'Grille', x : int, y : int, dir_entree : str) -> List[Piece2] :
        return [p for p in self.liste_pieces if p.peut_etre_posee(grille, x, y, dir_entree)]
    

    def _poids (self, piece : Piece2) -> float :
        # retourne le poids de la piece
        p = correspondance_poids_rarete(piece.rarete)
        bonus = self.bonus_couleur.get(piece.couleur, 0.0)
        return p * (1.0+bonus)


    def tirage_3_pieces (self, grille : 'Grille', x : int, y : int, dir_entree : str) -> List[Piece2] :

        pieces_compatibles = self._garder_pieces_compatibles(grille, x, y, dir_entree)

        if not pieces_compatibles : 
            return []
        
        liste_poids = [self._poids(piece) for piece in pieces_compatibles]

        if len(pieces_compatibles) >= 3 :
            k = 3
        else :
            k = len(pieces_compatibles)

        tirage = random.choices(pieces_compatibles, weights=liste_poids, k=k)

        # contrinate  : au moins une des trois pièces proposées aun coût en gemmes égal à 0
        if all(piece.cout_gemmes > 0 for piece in tirage) :
            pieces_cout_0 = [piece for piece in pieces_compatibles if piece.cout_gemmes == 0] 
            if pieces_cout_0 :
                tirage[0] = random.choice(pieces_cout_0)
        
        return tirage



