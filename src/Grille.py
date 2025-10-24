from typing import Dict, Tuple

from src.Porte import Porte
from src.Joueur import Joueur
from src.Inventaire import Inventaire


DIRECTIONS = {"N" : (0,-1), "S" : (0,1), "E" : (1,0), "O" : (-1,0)}  # on suit la convention des interfaces graphiques de cmettre l'origine en haut à gauche 
DIRECTIONS_REVERSE = {(0,-1):"N",(0,1):"S",(1,0):"E",(-1,0):"O"}
OPPOSE = {"N" : "S", "S" : "N", "E" : "W", "W" : "E"}




class Grille :

    """ Représente le manoir """

    def __init__(self, largeur=5, hauteur=9) :
        self.__largeur = largeur
        self.__hauteur = hauteur
        # self.__pieces = instnaciation objet classe Piece
        self.__portes : Dict[Tuple[int,int], Dict[str, Porte]] = {}


    @property
    def largeur (self) :
        """ getter de l'attribut __largeur """
        return self.__largeur
    
    @property
    def hauteur (self) :
        """ getter de l'attribut __hauteur """
        return self.__hauteur
    
    """
    @property
    def pieces (self) :
        return self.__pieces
    """

    @property
    def portes (self) :
        """ getter de l'attribut __portes """
        return self.__portes
    

    

    #### FOCNTIONS AUXILIAIRES

    def deplacement_permis (self, x, y) -> bool :
        """ 
        Retourne vrai si la case (x,y) est dans les bornes 
        """
        return 0 <= x < self.__largeur and 0 <= y < self.__hauteur
    

    def dict_portes (self, x, y) -> Dict[str, Porte] :
        """ 
        Retourne le dictionnaire des portes de la case (x,y)
        S'il n'est pas encore existant, le crée vide 
        """
        return self.portes.setdefault((x,y), {})


    def voisin (self, x : int, y : int, direction : str) -> Tuple[int, int] :
        """ Renvoie la case voisine dans la direction demandéee"""
        delta_x, delta_y = DIRECTIONS[direction]
        return x + delta_x, y + delta_y
       

    def niveau_porte(self, y : int) -> int :
        """ Statut aléatoire sauf pour rangée du bas et du haut 
        peut etre optimisee 
        """
        
        y = max(0, min(self.__hauteur - 1, y))  # on s'assure qu y est dans les bornes
        
        if y == self.__hauteur - 1 :   # rangée du bas
            return 0
        if y == 0 : # rangée du haut
            return 2 
        
        hauteur_norm = (self.__hauteur - 1 - y) / (self.__hauteur - 1)    # hauteur normalisee de la grille

        if hauteur_norm < 0.33 :
            return 0
        elif hauteur_norm < 0.66 :
            return 1
        else :
            return 0


    def garantie_porte (self, x, y, direction, niveau=None) -> Porte :
        """ Retourne la porte demandée (et son mirroir) en s'assurant qu'elle existe bien avant de l'utiliser
        Initialisation paresseuse
        """

        # 1) trouver le voisin
        new_x, new_y = self.voisin(x, y, direction)
        portes_case_courante = self.dict_portes(x,y)

        # 2) Gestion des bords de la grille
        if not self.deplacement_permis(new_x, new_y) :  # deplacement non permis
            return portes_case_courante.setdefault(direction, Porte(niveau=0, ouverte=False))
        
        portes_case_new = self.dict_portes(new_x, new_y)

        # 3) Création de la porte (x,y) si non existante
        if direction not in portes_case_courante :   # la porte n'existe pas
            if niveau is None :
               niveau = self.niveau_porte(min(y, new_y))
            portes_case_courante[direction] = Porte(niveau=niveau, ouverte=False)
            
        # 4) on fait de même du côté opposé
        portes_case_new.setdefault(
            OPPOSE[direction], 
            Porte(niveau=portes_case_courante[direction].niveau, ouverte=portes_case_courante[direction].ouverte)
        )

        return portes_case_courante[direction]



    def deplaceer_joueur (self, joueur : Joueur, inventaire : Inventaire, dx : int, dy : int) -> Tuple[bool, bool, int]:
        
        # on récupere la valeur associée a la cle (dx,dy)
        d = DIRECTIONS_REVERSE[(dx,dy)]
        if d is None or (dx == 0 and dy == 0) :
            return False, False, 0

        x = joueur.position[0]
        y = joueur.position[1]

        new_x, new_y = self.voisin(x, y, direction=d)

        if not self.deplacement_permis(x, y) :
            return False, False, 0

        # porte séparant (x,y) et (new_x, new)y
        porte = self.garantie_porte(joueur.position[0], joueur.position[1], d)

        if not porte.ouverte :
            niv = porte.niveau
            porte_ouverte = False

            if niv == 0 :  # on ouvre la porte
                porte_ouverte = True 

            elif niv == 1 :  # on essaye d'ouvrir la porte avec une cle ou le kit de crochetage

                if inventaire.cles > 0 and inventaire.depenser_cles(1) :
                    porte_ouverte = True

                elif inventaire.peut_ouvrir :
                    porte_ouverte = True
            
            elif niv == 2 :   # on essaye ouverture avec une cle
                if inventaire.cles > 0 and inventaire.depenser_cles(1) :
                    porte_ouverte = True

            if not porte_ouverte :   # on reste dans la meme case si on a pas reussi a ouvrir la porte
                return False, False, 0
            
            # on met a jour le statut des portes voisinnes

            porte.ouverte = True
            self.dict_portes(new_x, new_y)[OPPOSE[d]].ouverte = True

            if self.__portes[new_x][new_y] is None :
                return False, True, 0
            

            ################## A COMPLETER