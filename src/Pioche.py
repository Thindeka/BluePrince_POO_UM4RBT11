from __future__ import annotations
import random
from typing import List, Optional, Dict, TYPE_CHECKING

from src.Piece import (
    Piece2,
    FORME_COULOIR_EO,
    FORME_COULOIR_NS,
    FORME_ANGLE_NE,
    FORME_ANGLE_ES,
    FORME_ANGLE_SO,
    FORME_ANGLE_ON,
    FORME_CROIX,
    FORME_IMPASSE_N,
    FORME_IMPASSE_S,
    FORME_IMPASSE_E,
    FORME_IMPASSE_O,
    CouleurPiece,
    FORME_CARRE,
    FORME_T_NES,
    FORME_T_ESO,
    FORME_T_SON,
    FORME_T_ONE,
)


if TYPE_CHECKING:
    from src.Grille import Grille

# gestion de la rareté des pieces 
def correspondance_poids_rarete (rarete : int) -> int :
    correspondances = {0 : 27, 1 : 9, 2 : 3, 3 : 1} # rarete : (0 à 3) : (commonplace, standard, unusual, rare)
    return correspondances.get(rarete, 1)


class Pioche2 :
    """Gestion de la pioche de pièces.

    Attributs
    ---------
    catalogue : List[Piece2]
        Liste des Piece2 disponibles (modèles).
    bonus_couleur : Dict[int, float] 
        Multiplicateur de poids.
    _constructeurs : Dict[str, Callable[[], Piece2]]
        Constructeurs rapides pour quelques pièces spéciales.
    _par_nom : Dict[str, Piece2]
        Index des pièces par nom pour recherches/ajouts rapides.

    Méthodes
    -------
    _creer_catalogue() -> List[Piece2]
        Construit la liste initiale de modèles.
    _garder_pieces_compatibles(grille, x, y, dir_entree): 
        Filtre les pièces posables.
    _poids(piece) -> float 
        Calcule le poids de tirage d'une pièce.
    tirage_3_pieces(...) -> List[Piece2]
        Renvoie jusqu'à 3 pièces proposées pour un emplacement.
    ajouter_piece_modele(modele) -> None
        Ajoute un modèle par instance ou par nom.
    """

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


        # ----------------- PIECESS VIOLETTES -----------------

        # Bedroom
        pieces.append(Piece2("Bedroom", CouleurPiece.VIOLET, FORME_ANGLE_SO))
        pieces.append(Piece2("Bedroom", CouleurPiece.VIOLET, FORME_ANGLE_ES))
        pieces.append(Piece2("Bedroom", CouleurPiece.VIOLET, FORME_ANGLE_NE))
        pieces.append(Piece2("Bedroom", CouleurPiece.VIOLET, FORME_ANGLE_ON))


        # Master Bedroom
        pieces.append(Piece2("Master Bedroom", CouleurPiece.VIOLET, FORME_IMPASSE_S, cout_gemmes=1, rarete=3))
        pieces.append(Piece2("Master Bedroom", CouleurPiece.VIOLET, FORME_IMPASSE_N, cout_gemmes=1, rarete=3))
        pieces.append(Piece2("Master Bedroom", CouleurPiece.VIOLET, FORME_IMPASSE_E, cout_gemmes=1, rarete=3))
        pieces.append(Piece2("Master Bedroom", CouleurPiece.VIOLET, FORME_IMPASSE_O, cout_gemmes=1, rarete=3))


        # Nursery
        pieces.append(Piece2("Nursery", CouleurPiece.VIOLET, FORME_IMPASSE_S))
        pieces.append(Piece2("Nursery", CouleurPiece.VIOLET, FORME_IMPASSE_N))
        pieces.append(Piece2("Nursery", CouleurPiece.VIOLET, FORME_IMPASSE_E))
        pieces.append(Piece2("Nursery", CouleurPiece.VIOLET, FORME_IMPASSE_O))



        # ----------------- PIECESS BLEUES -----------------

        # Pantry
        pieces.append(Piece2("Pantry", CouleurPiece.BLEU, FORME_ANGLE_SO))
        pieces.append(Piece2("Pantry", CouleurPiece.BLEU, FORME_ANGLE_ES))
        pieces.append(Piece2("Pantry", CouleurPiece.BLEU, FORME_ANGLE_NE))
        pieces.append(Piece2("Pantry", CouleurPiece.BLEU, FORME_ANGLE_ON))

        #Parlor
        pieces.append(Piece2("Parlor", CouleurPiece.BLEU, FORME_ANGLE_SO))
        pieces.append(Piece2("Parlor", CouleurPiece.BLEU, FORME_ANGLE_ES))
        pieces.append(Piece2("Parlor", CouleurPiece.BLEU, FORME_ANGLE_NE))
        pieces.append(Piece2("Parlor", CouleurPiece.BLEU, FORME_ANGLE_ON))

        # Office
        office_so = Piece2("Office", CouleurPiece.BLEU, FORME_ANGLE_SO)
        office_es = Piece2("Office", CouleurPiece.BLEU, FORME_ANGLE_ES)
        office_ne = Piece2("Office", CouleurPiece.BLEU, FORME_ANGLE_NE)
        office_on = Piece2("Office", CouleurPiece.BLEU, FORME_ANGLE_ON)
        for o in (office_so, office_es, office_ne, office_on):
            o.or_dans_piece = 3  # tu peux ajuster (2, 3, 5, etc.)
            pieces.append(o)
        """  
        pieces.append(Piece2("Office", CouleurPiece.BLEU, FORME_ANGLE_SO))
        pieces.append(Piece2("Office", CouleurPiece.BLEU, FORME_ANGLE_ES))
        pieces.append(Piece2("Office", CouleurPiece.BLEU, FORME_ANGLE_NE))
        pieces.append(Piece2("Office", CouleurPiece.BLEU, FORME_ANGLE_ON))
        """ 

         # Vault : beaucoup d'or
        vault_s = Piece2("Vault", CouleurPiece.BLEU, FORME_IMPASSE_S, cout_gemmes=2, rarete=3)
        vault_n = Piece2("Vault", CouleurPiece.BLEU, FORME_IMPASSE_N, cout_gemmes=2, rarete=3)
        vault_e = Piece2("Vault", CouleurPiece.BLEU, FORME_IMPASSE_E, cout_gemmes=2, rarete=3)
        vault_o = Piece2("Vault", CouleurPiece.BLEU, FORME_IMPASSE_O, cout_gemmes=2, rarete=3)
        for v in (vault_s, vault_n, vault_e, vault_o):
            v.or_dans_piece = 40  
            pieces.append(v)

        # Chamber of Mirrors
        pieces.append(Piece2("Chamber of Mirrors", CouleurPiece.BLEU, FORME_IMPASSE_S, cout_gemmes=2, rarete=2))
        pieces.append(Piece2("Chamber of Mirrors", CouleurPiece.BLEU, FORME_IMPASSE_N, cout_gemmes=2, rarete=2))
        pieces.append(Piece2("Chamber of Mirrors", CouleurPiece.BLEU, FORME_IMPASSE_E, cout_gemmes=2, rarete=2))
        pieces.append(Piece2("Chamber of Mirrors", CouleurPiece.BLEU, FORME_IMPASSE_O, cout_gemmes=2, rarete=2))

        # Pool
        pieces.append(Piece2("Pool", CouleurPiece.BLEU, FORME_T_NES, cout_gemmes=1, rarete=1))
        pieces.append(Piece2("Pool", CouleurPiece.BLEU, FORME_T_ESO, cout_gemmes=1, rarete=1))
        pieces.append(Piece2("Pool", CouleurPiece.BLEU, FORME_T_SON, cout_gemmes=1, rarete=1))
        pieces.append(Piece2("Pool", CouleurPiece.BLEU, FORME_T_ONE, cout_gemmes=1, rarete=1))
        

        # Gallery
        pieces.append(Piece2("Gallery", CouleurPiece.BLEU, FORME_ANGLE_SO))
        pieces.append(Piece2("Gallery", CouleurPiece.BLEU, FORME_ANGLE_ES))
        pieces.append(Piece2("Gallery", CouleurPiece.BLEU, FORME_ANGLE_NE))
        pieces.append(Piece2("Gallery", CouleurPiece.BLEU, FORME_ANGLE_ON))

        # Rotunda
        pieces.append(Piece2("Rotunda", CouleurPiece.BLEU, FORME_ANGLE_SO, cout_gemmes=2, rarete=2))
        pieces.append(Piece2("Rotunda", CouleurPiece.BLEU, FORME_ANGLE_ES, cout_gemmes=2, rarete=2))
        pieces.append(Piece2("Rotunda", CouleurPiece.BLEU, FORME_ANGLE_NE, cout_gemmes=2, rarete=2))
        pieces.append(Piece2("Rotunda", CouleurPiece.BLEU, FORME_ANGLE_ON, cout_gemmes=2, rarete=2))

        # Den
        pieces.append(Piece2("Den", CouleurPiece.BLEU, FORME_T_NES))
        pieces.append(Piece2("Den", CouleurPiece.BLEU, FORME_T_ESO))
        pieces.append(Piece2("Den", CouleurPiece.BLEU, FORME_T_SON))
        pieces.append(Piece2("Den", CouleurPiece.BLEU, FORME_T_ONE))


        # ----------------- PIECESS VERTES -----------------

        # Patio
        pieces.append(Piece2("Patio", CouleurPiece.VERT, FORME_ANGLE_SO))
        pieces.append(Piece2("Patio", CouleurPiece.VERT, FORME_ANGLE_ES))
        pieces.append(Piece2("Patio", CouleurPiece.VERT, FORME_ANGLE_NE))
        pieces.append(Piece2("Patio", CouleurPiece.VERT, FORME_ANGLE_ON))

        # Greenhouse
        pieces.append(Piece2("Greenhouse", CouleurPiece.VERT, FORME_IMPASSE_S, cout_gemmes=1))
        pieces.append(Piece2("Greenhouse", CouleurPiece.VERT, FORME_IMPASSE_N, cout_gemmes=1))
        pieces.append(Piece2("Greenhouse", CouleurPiece.VERT, FORME_IMPASSE_E, cout_gemmes=1))
        pieces.append(Piece2("Greenhouse", CouleurPiece.VERT, FORME_IMPASSE_O, cout_gemmes=1))

        # Veranda
        pieces.append(Piece2("Veranda", CouleurPiece.VERT, FORME_COULOIR_NS, rarete=2))
        pieces.append(Piece2("Veranda", CouleurPiece.VERT, FORME_COULOIR_NS, rarete=2)) # afin de garder des chances de tirage équivalents aux autres pièces
        pieces.append(Piece2("Veranda", CouleurPiece.VERT, FORME_COULOIR_EO, rarete=2))
        pieces.append(Piece2("Veranda", CouleurPiece.VERT, FORME_COULOIR_EO, rarete=2)) # afin de garder des chances de tirage équivalents

        # Secret Garden
        pieces.append(Piece2("Garden", CouleurPiece.VERT, FORME_T_NES))
        pieces.append(Piece2("Garden", CouleurPiece.VERT, FORME_T_ESO))
        pieces.append(Piece2("Garden", CouleurPiece.VERT, FORME_T_SON))
        pieces.append(Piece2("Garden", CouleurPiece.VERT, FORME_T_ONE))
       

        # ----------------- PIECES ROUGES -----------------

        # Furnace 
        pieces.append(Piece2("Furnace", CouleurPiece.ROUGE, FORME_IMPASSE_N, rarete=3))
        pieces.append(Piece2("Furnace", CouleurPiece.ROUGE, FORME_IMPASSE_S, rarete=3)) # afin de garder des chances de tirage équivalents aux autres pièces
        pieces.append(Piece2("Furnace", CouleurPiece.ROUGE, FORME_IMPASSE_O, rarete=3))
        pieces.append(Piece2("Furnace", CouleurPiece.ROUGE, FORME_IMPASSE_E, rarete=3)) 

        # Maid's Chamber
        pieces.append(Piece2("MaidsChamber", CouleurPiece.ROUGE, FORME_ANGLE_SO))
        pieces.append(Piece2("MaidsChamber", CouleurPiece.ROUGE, FORME_ANGLE_ES))
        pieces.append(Piece2("MaidsChamber", CouleurPiece.ROUGE, FORME_ANGLE_NE))
        pieces.append(Piece2("MaidsChamber", CouleurPiece.ROUGE, FORME_ANGLE_ON))

        # Chapel
        pieces.append(Piece2("Chapel", CouleurPiece.ROUGE, FORME_T_NES))
        pieces.append(Piece2("Chapel", CouleurPiece.ROUGE, FORME_T_ESO))
        pieces.append(Piece2("Chapel", CouleurPiece.ROUGE, FORME_T_SON))
        pieces.append(Piece2("Chapel", CouleurPiece.ROUGE, FORME_T_ONE))




        # ----------------- PIECESS ORANGES -----------------
        
        # Hallway
        pieces.append(Piece2("Hallway", CouleurPiece.ORANGE, FORME_T_NES))
        pieces.append(Piece2("Hallway", CouleurPiece.ORANGE, FORME_T_ESO))
        pieces.append(Piece2("Hallway", CouleurPiece.ORANGE, FORME_T_SON))
        pieces.append(Piece2("Hallway", CouleurPiece.ORANGE, FORME_T_ONE))

        # Passageway
        pieces.append(Piece2("Passageway", CouleurPiece.ORANGE, FORME_CROIX))
        pieces.append(Piece2("Passageway", CouleurPiece.ORANGE, FORME_CROIX)) # afin de garder des chances de tirage équivalents aux autres pièces
        pieces.append(Piece2("Passageway", CouleurPiece.ORANGE, FORME_CROIX))
        pieces.append(Piece2("Passageway", CouleurPiece.ORANGE, FORME_CROIX))

        


        # ----------------- PIECESS JAUNES -----------------
        
        # Locksmith 
        pieces.append(Piece2("Locksmith", CouleurPiece.JAUNE, FORME_IMPASSE_N))
        pieces.append(Piece2("Locksmith", CouleurPiece.JAUNE, FORME_IMPASSE_S))
        pieces.append(Piece2("Locksmith", CouleurPiece.JAUNE, FORME_IMPASSE_E))
        pieces.append(Piece2("Locksmith", CouleurPiece.JAUNE, FORME_IMPASSE_O))

        # Commissary
        pieces.append(Piece2("Commissary", CouleurPiece.JAUNE, FORME_ANGLE_SO))
        pieces.append(Piece2("Commissary", CouleurPiece.JAUNE, FORME_ANGLE_ES))
        pieces.append(Piece2("Commissary", CouleurPiece.JAUNE, FORME_ANGLE_NE))
        pieces.append(Piece2("Commissary", CouleurPiece.JAUNE, FORME_ANGLE_ON))

        # Kitchen 
        pieces.append(Piece2("Kitchen", CouleurPiece.JAUNE, FORME_ANGLE_SO))
        pieces.append(Piece2("Kitchen", CouleurPiece.JAUNE, FORME_ANGLE_ES))
        pieces.append(Piece2("Kitchen", CouleurPiece.JAUNE, FORME_ANGLE_NE))
        pieces.append(Piece2("Kitchen", CouleurPiece.JAUNE, FORME_ANGLE_ON))


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
        """
        Tirage de 3 pièces possibles pour un emplacement donné.

        Paramètres
        ----------
        grille : Grille
            grille actuelle du jeu.
        x : int
        y : int
        dir_entree : str
            Direction d'entrée ('N', 'S', 'E', 'O').
        boosts : Dict[CouleurPiece, int] Defaults to None
            Bonus de poids par couleur.

        Returns
        -------
            List[Piece2]: Liste des pièces proposées (jusqu'à 3).

        Notes
        -----
        on ne garde que les pièces posables à cet endroit
        1) on garde seulement les pièces posables
        1) pièces posables
        """

        valides = [p for p in self.catalogue if p.peut_etre_posee(grille, x, y, dir_entree)]
        if not valides:
            return []

        tirage = random.sample(valides, k=min(3, len(valides)))

        if not any(p.cout_gemmes == 0 for p in tirage):
            gratuites = [p for p in valides if p.cout_gemmes == 0]
            if gratuites:
                tirage[0] = random.choice(gratuites)

        
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
        Ajoute un modèle dans la pioche.

        Paramètres
        ----------
        modele : str | Piece2
            - Si c'est une instance de Piece2, elle est ajoutée telle quelle.
            - Si c'est une chaîne, on tente d'ajouter un modèle correspondant
              (utilisant éventuellement self._constructeurs si défini) ou
              on crée une pièce par défaut à partir du nom.

        Returns
        -------
            None
        """
        # vraie pièce
        if isinstance(modele, Piece2):
            self.catalogue.append(modele)
            self._par_nom[modele.nom] = modele
            return

        #  chaîne  
        nom = modele

        if nom in self._par_nom:
            return

        #  interpréteur 
        nom_lower = nom.lower()

        if nom_lower in ("couloir_ns", "couloir-ns", "ns"):
            p = Piece2("Couloir NS", CouleurPiece.ORANGE, FORME_COULOIR_NS)
        elif nom_lower in ("couloir_eo", "couloir-eo", "eo", "couloir"):
            p = Piece2("Dynamic Corridor EO", CouleurPiece.ORANGE, FORME_COULOIR_EO)
        elif nom_lower in ("carre", "square", "room"):
            p = Piece2("Dynamic Room", CouleurPiece.BLEU, FORME_CARRE)
        elif nom_lower in ("croix", "cross", "plus"):
            p = Piece2("Dynamic Cross", CouleurPiece.BLEU, FORME_CROIX)
        else:
            # valeur inconnue  on fait un carré par défaut
            p = Piece2(nom, CouleurPiece.BLEU, FORME_CARRE)

        self.catalogue.append(p)
        self._par_nom[p.nom] = p
