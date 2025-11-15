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
    """
    Représente la grille du manoir — gère les pièces, les portes et les déplacements du joueur.

    Paramètres
    ----------
    largeur : int
        Nombre de colonnes (axe x), défaut 5.
    hauteur : int
        Nombre de lignes (axe y), défaut 9.

    Attributs
    ---------
    __largeur : int
    __hauteur : int
    __pieces : list[list[Piece2 | None]]
        Matrice des pièces indexée par [y][x].
    __portes : Dict[Tuple[int,int], Dict[str, Porte]]
        Portes par case et direction.
    sortie : Tuple[int,int]
        Coordonnées de la sortie.

    Méthodes
    --------
    largeur(), hauteur(), pieces(), portes() 
        Propriétés d'accès.
    placer_piece(x, y, piece) -> None 
        Place une pièce aux coordonnées données.
    get_piece(x, y) -> Piece2 | None 
        Retourne la pièce à (x,y) ou None.
    deplacement_permis(x, y) -> bool
        Indique si (x,y) est dans les bornes.
    dict_portes(x, y) -> Dict[str, Porte]
        Récupère (ou crée) le dict de portes pour une case.
    voisin(x, y, direction) -> Tuple[int,int]
        Calcule la case voisine selon DIRECTIONS.
    niveau_porte(y) -> int
        Calcule un niveau de porte (logique probabiliste selon la rangée).
    garantie_porte(x, y, direction, niveau=None) -> Porte
        Crée/synchronise la porte et son miroir.
    deplacer_joueur(joueur, inventaire, dx, dy) -> (bool, bool, int, str)
       Tente un déplacement et gère l'ouverture de porte (retour : (déplacé, ouverture_effectuée, pas_consumés, message)).
    objets_a_position(x, y)
        Retourne la liste d'objets présents si une pièce existe.

    Notes
    -----
    - Directions valides : 'N','S','E','O'.
    - Coordonnées : (x, y) avec origine en haut à gauche.
    """

    def __init__(self, largeur=5, hauteur=9) :
        self.__largeur = largeur
        self.__hauteur = hauteur
        self.__pieces = [[None for _ in range(self.__largeur)] for __ in range(self.__hauteur)]
        self.__portes : Dict[Tuple[int,int], Dict[str, Porte]] = {}   # __portes[(x,y)] = {"S" : Porte(...), "E" : Porte(...), "O" : Porte)...}, 
        self.sortie = (2, 0)  # (x, y) => x=2, y=0


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
        """
        Statut aléatoire sauf pour rangée du bas et du haut

        Paramètres
        ----------
        y : int 
            hauteur de la grille

        Returns
        -------
        p0, p1, p2 : int
            probabilités associés aux niveaux de la porte (0, 1 ou 2)
        """      
         
        y = max(0, min(self.__hauteur - 1, y))  # on s'assure qu y est dans les bornes
        
        if y == self.__hauteur - 1 :   # rangée du bas
            print("niveau_porte: y bas", y, "-> 0")
            return 0
        if y == 0 : # rangée du haut
            print("niveau_porte: y haut", y, "-> 2")
            return 2 
        
        hauteur_norm = (self.__hauteur - 1 - y) / (self.__hauteur - 1)
        
        p0 = max(0.5 - 0.5 * hauteur_norm, 0.1)  # probabilité niveau 0 etccc
        p1 = 0.3
        p2 = 1 - p0 - p1
        choix = random.choices([0, 1, 2], weights=[p0, p1, p2])[0]
        print(f"niveau_porte: y={y}, hauteur_norm={hauteur_norm:.3f}, p=[{p0:.3f},{p1:.3f},{p2:.3f}] -> {choix}")
        return choix



    def garantie_porte (self, x : int, y : int, direction : str, niveau=None) -> 'Porte' :
        """
        Retourne la porte demandée (et son mirroir) en s'assurant qu'elle existe bien avant de l'utiliser
        Initialisation paresseuse
        Paramètres
        ----------
        x : int
            Coordonnée x (colonne) de la case courante.
        y : int
            Coordonnée y (ligne) de la case courante.
        direction : str
            Direction depuis la case courante vers la case voisine (doit être un identifiant reconnu
            par self.voisin et présent dans la table OPPOSE).
        niveau : int | None, optionnel
            Niveau de la porte à créer. Si None, le niveau est déterminé paresseusement via
            self.niveau_porte(new_y) (où new_y est la coordonnée y du voisin).
        
        Returns
        -------
        Porte
            L'objet Porte correspondant à la porte depuis la case (x, y) dans la direction fournie.
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
                niveau = self.niveau_porte(new_y)
            print(f"[garantie_porte] création porte en {(x,y)} dir={direction} -> niveau={niveau}")
            portes_case_courante[direction] = Porte(niveau=niveau, ouverte=False)
            
        # 4) on fait de même du côté opposé
        o = OPPOSE[direction] 
        if o not in portes_case_vosin :
            portes_case_vosin[o] = Porte(
                niveau = portes_case_courante[direction].niveau, 
                ouverte = portes_case_courante[direction].ouverte
            )
        
        print(f"ouverte : {portes_case_courante[direction].ouverte}") # ouverture : vrai automatiquement quand on se déplace vers une porte,pourquoi ?
        return portes_case_courante[direction]



    #### GESTION DEPLACEMENT JOUEUR

    def deplacer_joueur (self, joueur : 'Joueur', inventaire : 'Inventaire', dx : int, dy : int) -> Tuple[bool, bool, int, str] :
        """
        Déplace le joueur d'une case selon un vecteur (dx, dy), en gérant l'ouverture des portes
        et le tirage éventuel d'une nouvelle pièce.

        Paramètres
        ----------
        joueur : Joueur
            Objet représentant le joueur ; sa position est modifiée si le déplacement est effectué.
        inventaire : Inventaire
            Inventaire utilisé pour tenter d'ouvrir une porte (consommation de ressources selon le niveau).
        dx : int
            Déplacement relatif en x (colonne).
        dy : int
            Déplacement relatif en y (ligne).

        Returns
        ------
        Tuple[bool, bool, int, str]
            - deplacement (bool) : True si le joueur a effectivement été déplacé.
            - ouverture_porte (bool) : True si une porte a été ouverte lors de la tentative (et qu'il faut éventuellement tirer une pièce).
            - pas_consommes (int) : Nombre de pas consommés (1 si déplacement effectué, 0 sinon).
            - message (str) : Message à destination de l'utilisateur expliquant l'issue de l'action (vide si pas d'information).
        """
        
        message = ""
        # on récupere la valeur associée a la cle (dx,dy)
        d = DIRECTIONS_REVERSE.get((dx, dy))
        if d is None or (dx == 0 and dy == 0) :   # Si (0,0) je ne fais rien
            return False, False, 0, message

        x,y = joueur.position
        piece_actuelle  = self.get_piece(x,y)
        
        if piece_actuelle is not None and not piece_actuelle.a_porte(d):
            # pas de porte dans cette direction → on ne tente même pas
            message = f"Il n'y a pas de porte vers le {d}."
            return False, False, 0, message

        new_x, new_y = self.voisin(x, y, d)

        if not self.deplacement_permis(new_x, new_y) :   ### déplacement non permis (bords)
            message = "Vous ne pouvez pas aller dans cette direction."
            print(f"[Grille] mouvement refusé : hors-limites {(new_x, new_y)}")
            return False, False, 0, message

        # porte séparant (x,y) et (new_x, new_y)
        porte = self.garantie_porte(x, y, d)


        if not porte.ouverte :    # porte fermee
            print("porte fermée, tentative d'ouverture...")
            if not inventaire.ouvrir_porte(porte.niveau) :  # porte ne peut pas etre ouverte
                print(f"Porte niveau {porte.niveau} NON OUVERTE (pos {(x,y)} -> {(new_x,new_y)})") 
                message = "Vous ne pouvez pas ouvrir cette porte (ressource manquante)."
                return False, False, 0, message
            else:
                print(f"Porte niveau {porte.niveau} OUVERTE (pos {(x,y)} -> {(new_x,new_y)})")
                porte.ouverte = True  # la porte peut etre ouverte
                self.dict_portes(new_x, new_y)[OPPOSE[d]].ouverte = True

            # il faut assurer coherence entre les deux cases opposées pour garantir que l'on puisse faire des aller-retour sans consommer de ressources davantage
            # il faut faire le tirage aleatoire d piece si le côté opposé est vide
                if self.get_piece(new_x, new_y) is None :
                    return False, True, 0, message
        
        if self.get_piece(new_x, new_y) is not None :
            joueur.deplacer_coords((new_x-x, new_y-y), self)
            return True, False, 1, message  # porte ouverte et si piece existe => deplacement
        
        return False, True, 0, message  # porte ouverte mais pas de piece => tirage 


    def objets_a_position(self, x, y):
        piece = self.pieces[y][x]
        if piece:
            return piece.objets
        return []







