# pour éviter imports croisés
from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Tuple
import random

from src.Porte import Porte

if TYPE_CHECKING:
    from src.Joueur import Joueur
    from src.Inventaire import Inventaire  # si tu l’annotes aussi
    from src.Porte import Porte
    from src.Piece2 import Piece2




DIRECTIONS = {"N" : (0,-1), "S" : (0,1), "E" : (1,0), "O" : (-1,0)}  # on suit la convention des interfaces graphiques de cmettre l'origine en haut à gauche 
DIRECTIONS_REVERSE = {(0,-1):"N",(0,1):"S",(1,0):"E",(-1,0):"O"}
OPPOSE = {"N" : "S", "S" : "N", "E" : "O", "O" : "E"}




class Grille :

    """ Représente le manoir """

    def __init__(self, largeur=5, hauteur=9) :
        self.__largeur = largeur
        self.__hauteur = hauteur
        self.__pieces = [[None for _ in range(self.__largeur)] for __ in range(self.__hauteur)]
        self.__portes : Dict[Tuple[int,int], Dict[str, Porte]] = {}   # __portes[(x,y)] = {"S" : Porte(...), "E" : Porte(...), "O" : Porte)...}, 
        self.sortie = (2, 0)  # (x, y) => x=2, y=0
        self.last_message = "" # dernier message temporaire à afficher à l'écran


    @property
    def largeur (self) :
        """ getter de l'attribut __largeur """
        return self.__largeur
    
    @property
    def hauteur (self) :
        """ getter de l'attribut __hauteur """
        return self.__hauteur
    
    @property
    def pieces (self) :
        return self.__pieces
    
    @property
    def portes (self) :
        """ getter de l'attribut __portes """
        return self.__portes
    
    def placer_piece (self, x : int, y : int , piece) -> None :
        """ setter porte aux coords donnees """
        self.__pieces[y][x] = piece

    def get_piece (self, x : int, y : int) -> Piece2 | None :
        return self.__pieces[y][x]

    

    #### FOCNTIONS AUXILIAIRES

    def deplacement_permis (self, x : int, y : int) -> bool :
        """ 
        Retourne vrai si la case (x,y) est dans les bornes 
        """
        return 0 <= x < self.__largeur and 0 <= y < self.__hauteur
    

    def dict_portes (self, x : int, y : int) -> Dict[str, 'Porte'] :
        """ 
        Retourne le dictionnaire des portes de la case (x,y)
        S'il n'est pas encore existant, le crée vide 
        """
        return self.portes.setdefault((x,y), {})


    def voisin (self, x : int, y : int, direction : str) -> Tuple[int, int] :
        """ Renvoie la case voisine dans la direction demandéee"""
        dx, dy = DIRECTIONS[direction]
        return x + dx, y + dy
       

    def niveau_porte(self, y : int) -> int :
        """ Statut aléatoire sauf pour rangée du bas et du haut 
        peut etre optimisee 
        """
        
        y = max(0, min(self.__hauteur - 1, y))  # on s'assure qu y est dans les bornes
        
        if y == self.__hauteur - 1 :   # rangée du bas
            return 0
        if y == 0 : # rangée du haut
            return 2 
        
        hauteur_norm = (self.__hauteur - 1 - y) / (self.__hauteur - 1)
        
        p0 = max(0.5 - 0.5 * hauteur_norm, 0.1)  # probabilité niveau 0 etccc
        p1 = 0.3
        p2 = 1 - p0 - p1

        return random.choices([0, 1, 2], weights=[p0, p1, p2])[0]



    def garantie_porte (self, x : int, y : int, direction : str, niveau=None) -> 'Porte' :
        """ Retourne la porte demandée (et son mirroir) en s'assurant qu'elle existe bien avant de l'utiliser
        Initialisation paresseuse
        """

        # 1) trouver le voisin
        new_x, new_y = self.voisin(x, y, direction)
        portes_case_courante = self.dict_portes(x,y)

        # 2) Gestion des bords de la grille
        if not self.deplacement_permis(new_x, new_y) :  # deplacement non permis
            # retourne porte non franchissable
            return portes_case_courante.setdefault(direction, Porte(niveau=0, ouverte=False))
        
        portes_case_vosin = self.dict_portes(new_x, new_y)

        # 3) Création de la porte (x,y) si non existante
        if direction not in portes_case_courante :   # la porte n'existe pas
            if niveau is None :
                niveau = self.niveau_porte(min(y, new_y))
            portes_case_courante[direction] = Porte(niveau=niveau, ouverte=False)
            
        # 4) on fait de même du côté opposé
        o = OPPOSE[direction] 
        if o not in portes_case_vosin :
            portes_case_vosin[o] = Porte(
                niveau = portes_case_courante[direction].niveau, 
                ouverte = portes_case_courante[direction].ouverte
            )

        return portes_case_courante[direction]



    #### GESTION DEPLACEMENT JOUEUR

    def deplacer_joueur (self, joueur : 'Joueur', inventaire : 'Inventaire', dx : int, dy : int) -> Tuple[bool, bool, int] :
        """"
        RETOURNE (DEPLACEMENT : bool, OUVERTURE_PORTE : bool, PAS_COSOMMES : int)"""
        
        message = None
        # on récupere la valeur associée a la cle (dx,dy)
        d = DIRECTIONS_REVERSE.get((dx, dy))
        if d is None or (dx == 0 and dy == 0) :   # Si (0,0) je ne fais rien
            return False, False, 0

        x,y = joueur.position
        piece_actuelle  = self.get_piece(x,y)
        
        if piece_actuelle is not None and not piece_actuelle.a_porte(d):
            # pas de porte dans cette direction → on ne tente même pas
            message = f"Il n'y a pas de porte vers le {d}."
            self.last_message = message
            return False, False, 0

        new_x, new_y = self.voisin(x, y, d)

        if not self.deplacement_permis(new_x, new_y) :   ### déplacement non permis (bords)
            message = "Vous ne pouvez pas aller dans cette direction."
            self.last_message = message
            return False, False, 0

        # porte séparant (x,y) et (new_x, new_y)
        porte = self.garantie_porte(x, y, d)

        if not porte.ouverte :    # porte fermee
            
            if not inventaire.ouvrir_porte(porte.niveau) :  # porte ne peut pas etre ouverte
                print("Porte niveau", porte.niveau, "NON OUVERTE (pas de ressource)")   
                message = "Vous ne pouvez pas ouvrir cette porte (besoin d'une clé)."
                self.last_message = message
                return False, False, 0
            else:
                print("Porte niveau", porte.niveau, "OUVERTE")

            
            porte.ouverte = True  # la porte peut etre ouverte
            self.dict_portes(new_x, new_y)[OPPOSE[d]].ouverte = True

            # il faut assurer coherence entre les deux cases opposées pour garantir que l'on puisse faire des aller-retour sans consommer de ressources davantage
            # il faut faire le tirage aleatoire d piece si le côté opposé est vide
            if self.get_piece(new_x, new_y) is None :
                return False, True, 0
        
        if self.get_piece(new_x, new_y) is not None :
            joueur.deplacer_coords((new_x-x, new_y-y), self)
            return True, False, 1  # porte ouverte et si piece existe => deplacement
        
        return False, True, 0  # porte ouverte mais pas de piece => tirage 


    def objets_a_position(self, x, y):
        piece = self.pieces[y][x]
        if piece:
            return piece.objets
        return []







