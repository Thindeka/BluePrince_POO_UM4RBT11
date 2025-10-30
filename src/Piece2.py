from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING, Set, Optional

if TYPE_CHECKING:
    from src.Grille import Grille


DIRECTIONS = {"N" : (0,-1), "S" : (0,1), "E" : (1,0), "O" : (-1,0)}  # on suit la convention des interfaces graphiques de cmettre l'origine en haut à gauche 
DIRECTIONS_REVERSE = {(0,-1):"N",(0,1):"S",(1,0):"E",(-1,0):"O"}
OPPOSE = {"N" : "S", "S" : "N", "E" : "O", "O" : "E"}


# énumération
class CouleurPiece :
    JAUNE = auto()  # -> 1
    VERT = auto()   # -> 2 ...
    VIOLET = auto()
    ORANGE = auto()
    ROUGE = auto()
    BLEU = auto()



class FormePiece :
    """ correspond a l meplacement des portes de la piece """
    nom : str
    ens_portes : Set[str]

    def __init__(self, nom, ens_portes) -> None:
        self.nom = nom
        self.ens_portes = ens_portes
 
    def a_porte (self, direction : str) -> bool :
        return direction in self.ens_portes
    

# FORMES DE PIECE (pas exhaustif)

# COULOIR
FORME_COULOIR_NS = FormePiece("couloir_ns", {"N", "S"})
FORME_COULOIR_EO =  FormePiece("couloir_eo", {"E", "O"})

# CROIX
FORME_CROIX = FormePiece("croix", {"N", "S", "E", "O"})

# IMPASSE
FORME_IMPASSE_N = FormePiece("cul_n", {"N"})
FORME_IMPASSE_S = FormePiece("cul_s", {"S"})
FORME_IMPASSE_E = FormePiece("cul_e", {"E"})
FORME_IMPASSE_O = FormePiece("cul_o", {"O"})

# DEX A DEUX EN ANGLES
FORME_ANGLE_NE = FormePiece("angle_ne", {"N", "E"})
FORME_ANGLE_ES = FormePiece("angle_es", {"E", "S"})
FORME_ANGLE_SO = FormePiece("angle_so", {"S", "O"})
FORME_ANGLE_ON = FormePiece("angle_on", {"O", "N"})


class Piece2 :

    nom : str
    couleur : int
    forme : FormePiece
    cout_gemmes : int = 0   # cout en gemmes a deoenser pour tirer la piece
    rarete : int = 0  # influence proba de tirer une piece
    # image (a voir apres)


    def __init__(self, nom: str, couleur : int, forme : FormePiece, cout_gemmes=0, rarete=0) -> None:
        self.nom = nom
        self.couleur = couleur
        self.forme = forme
        self.cout_gemmes = cout_gemmes
        self.rarete = rarete


    def a_porte (self, direction : str) -> bool :
        return self.forme.a_porte(direction)
    

    def peut_etre_posee (self, grille : 'Grille', x : int, y : int, dir_entree : str) -> bool :
        """ verification pour le tirage 2.7 
            -> piece doit avoir une porte du cote de l arrivee
            -> chaque porte de la piece doit etre dans les bornes
            -> si un voisin existe avec une porte vers la case actuelle, il faut avoir la porte de retour
        """

        # entree bloquee
        if dir_entree not in DIRECTIONS or not self.a_porte(dir_entree) :
            return False
        
        # hors bornes
        for d in self.forme.ens_portes :
            new_x, new_y = grille.voisin(x, y, d)   # case voisinne dans direction demandée
            if not grille.deplacement_permis(new_x, new_y) :
                return False
            
        
        for d in DIRECTIONS :
            new_x, new_y = grille.voisin(x, y, d)  # case voisinne dans direction demandée
            # ignorer ce voisin car il est hors bornes

            voisin = grille.deplacement_permis(new_x, new_y)
            if voisin is None :
                continue ########### à completer comportement plus tard par grille.piece_at()

            if isinstance(voisin, Piece2) :
                if voisin.a_porte(OPPOSE[d] and not self.a_porte(d)) :
                    return False # car c est incoherent si le voisin a une porte vers la case courante masi que la case courant en a pas de porte vers le voisin
        
        return True
    

    def poser_piece (self, grille : 'Grille', x : int, y : int) -> None :
        """" On pose la piece et on ouvre les portes 'mirroirs' """
        
        grille.placer_piece(x,y,self) 
        
        for d in self.forme.ens_portes :
            
            new_x, new_y = grille.voisin(x, y, d)

            if not grille.deplacement_permis(new_x, new_y) :
                continue # on ne place pas de porte la ou on ne peut pas

            porte = grille.garantie_porte(x, y, d)
            voisin = grille.get_piece(x,y)

            if isinstance(voisin, Piece2) and voisin.a_porte(OPPOSE[d]) :
                porte.ouverte = True   # j ouvre la porte de al case courante 
                grille.dict_portes(new_x, new_y)[OPPOSE[d]].ouverte = True    # j ouvre la porte de la case voisinne


    
    def effet_entree (self, game) :
        # a completer
        return 

    def effet_tirage (self, game) -> None :
        # a completer 
        return 
