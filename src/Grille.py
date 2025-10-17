from typing import Dict, Tuple

from src.Porte import Porte


DIRECTIONS = {"N" : (0,-1), "S" : (0,1), "E" : (1,0), "O" : (-1,0)}  # on suit la convention des interfaces graphiques de cmettre l'origine en haut à gauche 
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


    def voisin (self, x, y, direction) -> Tuple[int, int] :
        """ Renvoie la case voisine dans la direction demandéee"""
        delta_x, delta_y = DIRECTIONS[direction]
        return x + delta_x, y + delta_y
       

    def garantie_porte (self, x, y, direction, niveau) -> Porte :
        """ Retourne la porte demandée """
        ############## COMPLETER ##############
        new_x, new_y = self.voisin(x, y, direction)

        if not self.deplacement_permis(new_x, new_y) :
            return None # type: ignore ############# compléter
        
        portes_case_courante = self.dict_portes(x,y)
        portes_case_new = self.dict_portes(new_x, new_y)

        if direction not in portes_case_courante :   # la porte n'existe pas
            if niveau is None :
               # niveau dépend de la rangée
            
        return None  # type: ignore


        
