from __future__ import annotations
import random
from typing import List, Optional, Dict, TYPE_CHECKING

"""
from src.Piece2 import (
    Piece2, CouleurPiece,
    FORME_CROIX, FORME_COULOIR_NS, FORME_COULOIR_EO,
    FORME_IMPASSE_E, FORME_IMPASSE_N, FORME_IMPASSE_S, FORME_IMPASSE_O,
    FORME_ANGLE_NE, FORME_ANGLE_ES, FORME_ANGLE_SO, FORME_ANGLE_ON,
)"""

from src.Piece2 import (
    Piece2,
    FORME_COULOIR_EO,
    FORME_COULOIR_NS,
    FORME_ANGLE_NE,
    FORME_CROIX,
    CouleurPiece,
    FORME_CARRE
)


if TYPE_CHECKING:
    from src.Grille import Grille

# gestion de la rareté des pieces 
def correspondance_poids_rarete (rarete : int) -> int :
    correspondances = {0 : 27, 1 : 9, 2 : 3, 3 : 1}
    return correspondances.get(rarete, 1)


class Pioche2 :

    def __init__(self) -> None : 
        self.catalogue : List[Piece2] = self._creer_catalogue()
        self.bonus_couleur : Dict[int, float] = {}   # le int correspond a la couleur
        self._constructeurs = {
            "couloir_NS": lambda: Piece2("Couloir N-S", CouleurPiece.ORANGE, FORME_COULOIR_NS),
            "couloir_EO": lambda: Piece2("Couloir E-O", CouleurPiece.ORANGE, FORME_COULOIR_EO),
            "salle_tresor": lambda: Piece2("Salle au trésor", CouleurPiece.JAUNE, FORME_CROIX, cout_gemmes=2, rarete=3),
        }
        self._par_nom: Dict[str, Piece2] = {p.nom: p for p in self.catalogue}


    def _creer_catalogue (self) -> List[Piece2] :
        pieces: List[Piece2] = []

        # ——— pièces “normales” (carrées) ———
        pieces.append(Piece2("Bedroom", CouleurPiece.VIOLET, FORME_CARRE))
        pieces.append(Piece2("Master Bedroom", CouleurPiece.VIOLET, FORME_CARRE, cout_gemmes=1, rarete=1))
        pieces.append(Piece2("Nursery", CouleurPiece.BLEU, FORME_CARRE))
        pieces.append(Piece2("Pantry", CouleurPiece.BLEU, FORME_CARRE))
        pieces.append(Piece2("Parlor", CouleurPiece.BLEU, FORME_CARRE))
        pieces.append(Piece2("Office", CouleurPiece.BLEU, FORME_CARRE))
        pieces.append(Piece2("Patio", CouleurPiece.VERT, FORME_CARRE))
        pieces.append(Piece2("Greenhouse", CouleurPiece.VERT, FORME_CARRE, cout_gemmes=1))
        pieces.append(Piece2("Furnace", CouleurPiece.ROUGE, FORME_CARRE))
        pieces.append(Piece2("Veranda", CouleurPiece.VERT, FORME_CARRE))
        pieces.append(Piece2("Maid's Chamber", CouleurPiece.VIOLET, FORME_CARRE))
        pieces.append(Piece2("Chamber of Mirrors", CouleurPiece.BLEU, FORME_CARRE, cout_gemmes=2, rarete=2))
        pieces.append(Piece2("Pool", CouleurPiece.BLEU, FORME_CARRE, cout_gemmes=1, rarete=1))

        # ——— couloirs horizontaux ———
        pieces.append(Piece2("Hallway", CouleurPiece.ORANGE, FORME_COULOIR_EO))
        pieces.append(Piece2("Passageway", CouleurPiece.ORANGE, FORME_COULOIR_EO))

        # ——— éventuellement un couloir vertical (si tu veux) ———
        pieces.append(Piece2("Spare Foyer", CouleurPiece.ORANGE, FORME_COULOIR_NS))

        # ——— angles ———
        pieces.append(Piece2("Entrance", CouleurPiece.BLEU, FORME_ANGLE_NE))
        pieces.append(Piece2("Gallery", CouleurPiece.BLEU, FORME_ANGLE_NE))

        # ——— croix ———
        pieces.append(Piece2("Rotunda", CouleurPiece.BLEU, FORME_CROIX, cout_gemmes=2, rarete=2))

        return pieces
        



    def _garder_pieces_compatibles (self, grille : 'Grille', x : int, y : int, dir_entree : str) -> List[Piece2] :
        return [p for p in self.catalogue if p.peut_etre_posee(grille, x, y, dir_entree)]
    

    def _poids (self, piece : Piece2) -> float :
        # retourne le poids de la piece
        p = correspondance_poids_rarete(piece.rarete)
        bonus = self.bonus_couleur.get(piece.couleur.value, 0.0)
        return p * (1.0+bonus)


    """
    def tirage_3_pieces (self, grille : 'Grille', x : int, y : int, dir_entree : str, boosts=None) -> List[Piece2] :

        pieces_compatibles = self._garder_pieces_compatibles(grille, x, y, dir_entree)

        if not pieces_compatibles : 
            return []
        
        poids = []
        for piece in pieces_compatibles:
            base = correspondance_poids_rarete(piece.rarete)  # ex: 27, 9, 3, 1
            if boosts and piece.couleur in boosts:
                # chaque boost augmente un peu le poids
                base = int(base * (1 + 0.3 * boosts[piece.couleur]))
            poids.append(base)

        # 3) on tire 3 distinctes si possible
        selection = []
        for _ in range(3):
            if not pieces_compatibles:
                break
            piece = random.choices(pieces_compatibles, weights=poids, k=1)[0]
            selection.append(piece)
            # on enlève pour éviter doublons
            idx = pieces_compatibles.index(piece)
            pieces_compatibles.pop(idx)
            poids.pop(idx)


        # contrinate  : au moins une des trois pièces proposées aun coût en gemmes égal à 0
        if all(piece.cout_gemmes > 0 for piece in selection) :
            pieces_cout_0 = [piece for piece in pieces_compatibles if piece.cout_gemmes == 0] 
            if pieces_cout_0 :
                selection[0] = random.choice(pieces_cout_0)
        
        return selection
    """
    def tirage_3_pieces(self, grille, x: int, y: int, dir_entree: str, boosts=None) -> List[Piece2]:
        # on ne garde que les pièces posables à cet endroit
        # 1) on garde seulement les pièces posables
        # 1) pièces posables
        valides = [p for p in self.catalogue if p.peut_etre_posee(grille, x, y, dir_entree)]
        if not valides:
            return []

        tirage = random.sample(valides, k=min(3, len(valides)))

        # 2) garantir coût 0
        if not any(p.cout_gemmes == 0 for p in tirage):
            gratuites = [p for p in valides if p.cout_gemmes == 0]
            if gratuites:
                tirage[0] = random.choice(gratuites)

        # 3) garantir une sortie vers le haut si on est TOUT EN BAS
        est_derniere_ligne = (y == grille.hauteur - 1)
        if est_derniere_ligne:
            if not any(p.a_porte("N") for p in tirage):
                # on cherche parmi les valides une pièce qui a N
                candidates_nord = [p for p in valides if p.a_porte("N")]
                if candidates_nord:
                    tirage[-1] = random.choice(candidates_nord)

        return tirage


    def ajouter_piece_modele(self, modele: str | Piece2) -> None:
        """
        Permet à une pièce spéciale (Chamber of Mirrors, Pool, etc.)
        d'ajouter dynamiquement un modèle dans la pioche.

        - si on reçoit un Piece2 → on l'ajoute tel quel
        - si on reçoit un str → on crée une pièce standard selon le nom
        """
        # 1) si c'est déjà une vraie pièce
        if isinstance(modele, Piece2):
            self.catalogue.append(modele)
            self._par_nom[modele.nom] = modele
            return

        # 2) si c'est une chaîne → on essaie d'interpréter
        nom = modele

        # si on l'a déjà, on ne duplique pas
        if nom in self._par_nom:
            return

        # petit interpréteur très simple
        nom_lower = nom.lower()

        if nom_lower in ("couloir_ns", "couloir-ns", "ns"):
            p = Piece2("Dynamic Corridor NS", CouleurPiece.ORANGE, FORME_COULOIR_NS)
        elif nom_lower in ("couloir_eo", "couloir-eo", "eo", "couloir"):
            p = Piece2("Dynamic Corridor EO", CouleurPiece.ORANGE, FORME_COULOIR_EO)
        elif nom_lower in ("carre", "square", "room"):
            p = Piece2("Dynamic Room", CouleurPiece.BLEU, FORME_CARRE)
        elif nom_lower in ("croix", "cross", "plus"):
            p = Piece2("Dynamic Cross", CouleurPiece.BLEU, FORME_CROIX)
        else:
            # valeur inconnue → on fait un carré par défaut
            p = Piece2(nom, CouleurPiece.BLEU, FORME_CARRE)

        self.catalogue.append(p)
        self._par_nom[p.nom] = p
