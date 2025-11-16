from __future__ import annotations
import random
from typing import List, Optional, Dict, TYPE_CHECKING


from src.Piece import (
    Piece,
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




class Pioche :
    """Gestion de la pioche de pièces.

    Attributs
    ---------
    catalogue : List[Piece]
        Liste des Piece disponibles (modèles).
    bonus_couleur : Dict[int, float] 
        Multiplicateur de poids.
    _constructeurs : Dict[str, Callable[[], Piece]]
        Constructeurs rapides pour quelques pièces spéciales.
    _par_nom : Dict[str, Piece]
        Index des pièces par nom pour recherches/ajouts rapides.

    Méthodes
    -------
    _creer_catalogue() -> List[Piece]
        Construit la liste initiale de modèles.
    _garder_pieces_compatibles(grille, x, y, dir_entree): 
        Filtre les pièces posables.
    _poids(piece) -> float 
        Calcule le poids de tirage d'une pièce.
    tirage_3_pieces(...) -> List[Piece]
        Renvoie jusqu'à 3 pièces proposées pour un emplacement.
    ajouter_piece_modele(modele) -> None
        Ajoute un modèle par instance ou par nom.
    """

    def __init__(self) -> None : 
        self.catalogue : List[Piece] = self._creer_catalogue()
        self.bonus_couleur : Dict[int, float] = {}   # le int correspond a la couleur
        self._constructeurs = {
            "couloir_NS": lambda: Piece("Couloir N-S", CouleurPiece.ORANGE, FORME_COULOIR_NS),
            "couloir_EO": lambda: Piece("Couloir E-O", CouleurPiece.ORANGE, FORME_COULOIR_EO),
            "salle_tresor": lambda: Piece("Salle au trésor", CouleurPiece.JAUNE, FORME_CROIX, cout_gemmes=2, rarete=3),
        }
        self._par_nom: Dict[str, Piece] = {p.nom: p for p in self.catalogue}




    def _creer_catalogue (self) -> List[Piece] :
        pieces: List[Piece] = []


        # ----------------- PIECESS VIOLETTES -----------------

        # Bedroom
        pieces.append(Piece("Bedroom", CouleurPiece.VIOLET, FORME_ANGLE_SO))
        pieces.append(Piece("Bedroom", CouleurPiece.VIOLET, FORME_ANGLE_ES))
        pieces.append(Piece("Bedroom", CouleurPiece.VIOLET, FORME_ANGLE_NE))
        pieces.append(Piece("Bedroom", CouleurPiece.VIOLET, FORME_ANGLE_ON))


        # Master Bedroom
        pieces.append(Piece("Master Bedroom", CouleurPiece.VIOLET, FORME_IMPASSE_S, cout_gemmes=1, rarete=3))
        pieces.append(Piece("Master Bedroom", CouleurPiece.VIOLET, FORME_IMPASSE_N, cout_gemmes=1, rarete=3))
        pieces.append(Piece("Master Bedroom", CouleurPiece.VIOLET, FORME_IMPASSE_E, cout_gemmes=1, rarete=3))
        pieces.append(Piece("Master Bedroom", CouleurPiece.VIOLET, FORME_IMPASSE_O, cout_gemmes=1, rarete=3))


        # Nursery
        pieces.append(Piece("Nursery", CouleurPiece.VIOLET, FORME_IMPASSE_S))
        pieces.append(Piece("Nursery", CouleurPiece.VIOLET, FORME_IMPASSE_N))
        pieces.append(Piece("Nursery", CouleurPiece.VIOLET, FORME_IMPASSE_E))
        pieces.append(Piece("Nursery", CouleurPiece.VIOLET, FORME_IMPASSE_O))



        # ----------------- PIECESS BLEUES -----------------

        # Locker
        pieces.append(Piece("Locker", CouleurPiece.BLEU, FORME_COULOIR_NS))
        pieces.append(Piece("Locker", CouleurPiece.BLEU, FORME_COULOIR_EO))

        # Pantry
        pieces.append(Piece("Pantry", CouleurPiece.BLEU, FORME_ANGLE_SO))
        pieces.append(Piece("Pantry", CouleurPiece.BLEU, FORME_ANGLE_ES))
        pieces.append(Piece("Pantry", CouleurPiece.BLEU, FORME_ANGLE_NE))
        pieces.append(Piece("Pantry", CouleurPiece.BLEU, FORME_ANGLE_ON))

        #Parlor
        pieces.append(Piece("Parlor", CouleurPiece.BLEU, FORME_ANGLE_SO))
        pieces.append(Piece("Parlor", CouleurPiece.BLEU, FORME_ANGLE_ES))
        pieces.append(Piece("Parlor", CouleurPiece.BLEU, FORME_ANGLE_NE))
        pieces.append(Piece("Parlor", CouleurPiece.BLEU, FORME_ANGLE_ON))

        # Office
        office_so = Piece("Office", CouleurPiece.BLEU, FORME_ANGLE_SO)
        office_es = Piece("Office", CouleurPiece.BLEU, FORME_ANGLE_ES)
        office_ne = Piece("Office", CouleurPiece.BLEU, FORME_ANGLE_NE)
        office_on = Piece("Office", CouleurPiece.BLEU, FORME_ANGLE_ON)
        for o in (office_so, office_es, office_ne, office_on):
            o.or_dans_piece = 3 
            pieces.append(o)

        pieces.append(office_so)
        pieces.append(office_es)
        pieces.append(office_ne)
        pieces.append(office_on)
        
        # Security
        pieces.append(Piece("Security", CouleurPiece.BLEU, FORME_T_NES))
        pieces.append(Piece("Security", CouleurPiece.BLEU, FORME_T_ESO))
        pieces.append(Piece("Security", CouleurPiece.BLEU, FORME_T_SON))
        pieces.append(Piece("Security", CouleurPiece.BLEU, FORME_T_ONE))


        # Vault 
        vault_s = Piece("Vault", CouleurPiece.BLEU, FORME_IMPASSE_S, cout_gemmes=2, rarete=3)
        vault_n = Piece("Vault", CouleurPiece.BLEU, FORME_IMPASSE_N, cout_gemmes=2, rarete=3)
        vault_e = Piece("Vault", CouleurPiece.BLEU, FORME_IMPASSE_E, cout_gemmes=2, rarete=3)
        vault_o = Piece("Vault", CouleurPiece.BLEU, FORME_IMPASSE_O, cout_gemmes=2, rarete=3)
        for v in (vault_s, vault_n, vault_e, vault_o):
            v.or_dans_piece = 40  
            pieces.append(v)

        # Chamber of Mirrors
        pieces.append(Piece("Chamber of Mirrors", CouleurPiece.BLEU, FORME_IMPASSE_S, cout_gemmes=2, rarete=2))
        pieces.append(Piece("Chamber of Mirrors", CouleurPiece.BLEU, FORME_IMPASSE_N, cout_gemmes=2, rarete=2))
        pieces.append(Piece("Chamber of Mirrors", CouleurPiece.BLEU, FORME_IMPASSE_E, cout_gemmes=2, rarete=2))
        pieces.append(Piece("Chamber of Mirrors", CouleurPiece.BLEU, FORME_IMPASSE_O, cout_gemmes=2, rarete=2))

        # Pool
        pieces.append(Piece("Pool", CouleurPiece.BLEU, FORME_T_NES, cout_gemmes=1, rarete=1))
        pieces.append(Piece("Pool", CouleurPiece.BLEU, FORME_T_ESO, cout_gemmes=1, rarete=1))
        pieces.append(Piece("Pool", CouleurPiece.BLEU, FORME_T_SON, cout_gemmes=1, rarete=1))
        pieces.append(Piece("Pool", CouleurPiece.BLEU, FORME_T_ONE, cout_gemmes=1, rarete=1))
        

        # Gallery
        pieces.append(Piece("Gallery", CouleurPiece.BLEU, FORME_COULOIR_NS))
        pieces.append(Piece("Gallery", CouleurPiece.BLEU, FORME_COULOIR_EO))

        # Rotunda
        pieces.append(Piece("Rotunda", CouleurPiece.BLEU, FORME_ANGLE_SO, cout_gemmes=2, rarete=2))
        pieces.append(Piece("Rotunda", CouleurPiece.BLEU, FORME_ANGLE_ES, cout_gemmes=2, rarete=2))
        pieces.append(Piece("Rotunda", CouleurPiece.BLEU, FORME_ANGLE_NE, cout_gemmes=2, rarete=2))
        pieces.append(Piece("Rotunda", CouleurPiece.BLEU, FORME_ANGLE_ON, cout_gemmes=2, rarete=2))

        # Den
        pieces.append(Piece("Den", CouleurPiece.BLEU, FORME_T_NES))
        pieces.append(Piece("Den", CouleurPiece.BLEU, FORME_T_ESO))
        pieces.append(Piece("Den", CouleurPiece.BLEU, FORME_T_SON))
        pieces.append(Piece("Den", CouleurPiece.BLEU, FORME_T_ONE))


        # ----------------- PIECESS VERTES -----------------

        # Patio
        pieces.append(Piece("Patio", CouleurPiece.VERT, FORME_ANGLE_SO))
        pieces.append(Piece("Patio", CouleurPiece.VERT, FORME_ANGLE_ES))
        pieces.append(Piece("Patio", CouleurPiece.VERT, FORME_ANGLE_NE))
        pieces.append(Piece("Patio", CouleurPiece.VERT, FORME_ANGLE_ON))

        # Greenhouse
        pieces.append(Piece("Greenhouse", CouleurPiece.VERT, FORME_IMPASSE_S, cout_gemmes=1))
        pieces.append(Piece("Greenhouse", CouleurPiece.VERT, FORME_IMPASSE_N, cout_gemmes=1))
        pieces.append(Piece("Greenhouse", CouleurPiece.VERT, FORME_IMPASSE_E, cout_gemmes=1))
        pieces.append(Piece("Greenhouse", CouleurPiece.VERT, FORME_IMPASSE_O, cout_gemmes=1))

        # Veranda
        pieces.append(Piece("Veranda", CouleurPiece.VERT, FORME_COULOIR_NS, rarete=2))
        pieces.append(Piece("Veranda", CouleurPiece.VERT, FORME_COULOIR_NS, rarete=2)) 
        pieces.append(Piece("Veranda", CouleurPiece.VERT, FORME_COULOIR_EO, rarete=2))
        pieces.append(Piece("Veranda", CouleurPiece.VERT, FORME_COULOIR_EO, rarete=2)) 

        # Secret Garden
        pieces.append(Piece("Garden", CouleurPiece.VERT, FORME_T_NES))
        pieces.append(Piece("Garden", CouleurPiece.VERT, FORME_T_ESO))
        pieces.append(Piece("Garden", CouleurPiece.VERT, FORME_T_SON))
        pieces.append(Piece("Garden", CouleurPiece.VERT, FORME_T_ONE))
       

        # ----------------- PIECES ROUGES -----------------

        # Furnace 
        pieces.append(Piece("Furnace", CouleurPiece.ROUGE, FORME_IMPASSE_N, rarete=3))
        pieces.append(Piece("Furnace", CouleurPiece.ROUGE, FORME_IMPASSE_S, rarete=3)) 
        pieces.append(Piece("Furnace", CouleurPiece.ROUGE, FORME_IMPASSE_O, rarete=3))
        pieces.append(Piece("Furnace", CouleurPiece.ROUGE, FORME_IMPASSE_E, rarete=3)) 

        # Maid's Chamber
        pieces.append(Piece("MaidsChamber", CouleurPiece.ROUGE, FORME_ANGLE_SO))
        pieces.append(Piece("MaidsChamber", CouleurPiece.ROUGE, FORME_ANGLE_ES))
        pieces.append(Piece("MaidsChamber", CouleurPiece.ROUGE, FORME_ANGLE_NE))
        pieces.append(Piece("MaidsChamber", CouleurPiece.ROUGE, FORME_ANGLE_ON))

        # Chapel
        pieces.append(Piece("Chapel", CouleurPiece.ROUGE, FORME_T_NES))
        pieces.append(Piece("Chapel", CouleurPiece.ROUGE, FORME_T_ESO))
        pieces.append(Piece("Chapel", CouleurPiece.ROUGE, FORME_T_SON))
        pieces.append(Piece("Chapel", CouleurPiece.ROUGE, FORME_T_ONE))


        # ----------------- PIECESS ORANGES -----------------
        
        # Hallway
        pieces.append(Piece("Hallway", CouleurPiece.ORANGE, FORME_T_NES))
        pieces.append(Piece("Hallway", CouleurPiece.ORANGE, FORME_T_ESO))
        pieces.append(Piece("Hallway", CouleurPiece.ORANGE, FORME_T_SON))
        pieces.append(Piece("Hallway", CouleurPiece.ORANGE, FORME_T_ONE))

        # Passageway
        pieces.append(Piece("Passageway", CouleurPiece.ORANGE, FORME_CROIX))
        
        # Corridor
        pieces.append(Piece("Corridor", CouleurPiece.ORANGE, FORME_COULOIR_NS))
        pieces.append(Piece("Corridor", CouleurPiece.ORANGE, FORME_COULOIR_EO))

        


        # ----------------- PIECESS JAUNES -----------------
        
        # Locksmith 
        pieces.append(Piece("Locksmith", CouleurPiece.JAUNE, FORME_IMPASSE_N))
        pieces.append(Piece("Locksmith", CouleurPiece.JAUNE, FORME_IMPASSE_S))
        pieces.append(Piece("Locksmith", CouleurPiece.JAUNE, FORME_IMPASSE_E))
        pieces.append(Piece("Locksmith", CouleurPiece.JAUNE, FORME_IMPASSE_O))

        # Commissary
        pieces.append(Piece("Commissary", CouleurPiece.JAUNE, FORME_ANGLE_SO))
        pieces.append(Piece("Commissary", CouleurPiece.JAUNE, FORME_ANGLE_ES))
        pieces.append(Piece("Commissary", CouleurPiece.JAUNE, FORME_ANGLE_NE))
        pieces.append(Piece("Commissary", CouleurPiece.JAUNE, FORME_ANGLE_ON))

        # Kitchen 
        pieces.append(Piece("Kitchen", CouleurPiece.JAUNE, FORME_ANGLE_SO))
        pieces.append(Piece("Kitchen", CouleurPiece.JAUNE, FORME_ANGLE_ES))
        pieces.append(Piece("Kitchen", CouleurPiece.JAUNE, FORME_ANGLE_NE))
        pieces.append(Piece("Kitchen", CouleurPiece.JAUNE, FORME_ANGLE_ON))


        return pieces
            



    def _garder_pieces_compatibles (self, grille : 'Grille', x : int, y : int, dir_entree : str) -> List[Piece] :
        return [p for p in self.catalogue if p.peut_etre_posee(grille, x, y, dir_entree)]
    



    def _poids (self, piece : Piece) -> float :
        # retourne le poids de la piece
        p = correspondance_poids_rarete(piece.rarete)
        bonus = self.bonus_couleur.get(piece.couleur.value, 0.0)
        return p * (1.0+bonus)




    def tirage_3_pieces(self, grille, x: int, y: int, dir_entree: str, boosts=None) -> List[Piece]:
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
            List[Piece]: Liste des pièces proposées (jusqu'à 3).

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
    
 

 
    def ajouter_piece_modele(self, modele: str | Piece) -> None:
        """
        Ajoute un modèle dans la pioche.

        Paramètres
        ----------
        modele : str | Piece
            - Si c'est une instance de Piece, elle est ajoutée telle quelle.
            - Si c'est une chaîne, on tente d'ajouter un modèle correspondant
              (utilisant éventuellement self._constructeurs si défini) ou
              on crée une pièce par défaut à partir du nom.

        Returns
        -------
            None
        """
        # vraie pièce
        if isinstance(modele, Piece):
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
            p = Piece("Couloir NS", CouleurPiece.ORANGE, FORME_COULOIR_NS)
        elif nom_lower in ("couloir_eo", "couloir-eo", "eo", "couloir"):
            p = Piece("Dynamic Corridor EO", CouleurPiece.ORANGE, FORME_COULOIR_EO)
        elif nom_lower in ("carre", "square", "room"):
            p = Piece("Dynamic Room", CouleurPiece.BLEU, FORME_CARRE)
        elif nom_lower in ("croix", "cross", "plus"):
            p = Piece("Dynamic Cross", CouleurPiece.BLEU, FORME_CROIX)
        else:
            # valeur inconnue  on fait un carré par défaut
            p = Piece(nom, CouleurPiece.BLEU, FORME_CARRE)

        self.catalogue.append(p)
        self._par_nom[p.nom] = p
