# pour éviter imports croisés
from __future__ import annotations
from typing import TYPE_CHECKING, Tuple
from src.Inventaire import Inventaire

if TYPE_CHECKING :
    from src.Grille import Grille

DIRECTIONS = {"N" : (0,-1), "S" : (0,1), "E" : (1,0), "O" : (-1,0)}  # on suit la convention des interfaces graphiques de cmettre l'origine en haut à gauche 

class Joueur:
    """
    Représente le joueur ou la joueuse.

    Attributs
    ----------
    inventaire : Inventaire
        Contient les objets et le nombre de pas disponibles.
    position : tuple(int, int)
        Coordonnées (x, y) du joueur dans la grille.
    """
    def __init__(self) -> None :
        self.inventaire = Inventaire()
        self.position = (2, 8)  # Position initiale dans la grille (peut être modifiée selon le jeu) ###### a modifier
    


    def deplacer_str(self, direction : str, grille : 'Grille'):
        """
        Déplace le joueur dans la direction donnée si le déplacement est permis.

        Paramètres
        ----------
        direction : str
            Direction du déplacement ('N', 'S', 'E' ou 'O').
        grille : objet Grille
            Représente la grille du jeu contenant la méthode `deplacement_permis(x, y)`.

        Returns
        -------
        bool
            True si le déplacement a eu lieu, False sinon.
        """
        x, y = self.position
        dx, dy = DIRECTIONS[direction]
        new_x, new_y = x + dx, y + dy
        
        #if not grille.deplacement_permis(new_x, new_y):
        #    return "Déplacement impossible dans cette direction."
        
        #if not grille.peut_entrer(new_x, new_y, self.inventaire):
        #    return "Impossible d'entrer, vous n'avez pas de clés"

        if grille.deplacement_permis(new_x, new_y):
            self.position = new_x, new_y
            self.inventaire.utiliser_pas(1)  # Consomme 1 pas par déplacement
            return True
        return False
    


    def deplacer_coords(self, direction : Tuple[int,int], grille : 'Grille'):
        """
        Déplace le joueur dans la direction donnée si le déplacement est permis.

        Paramètres
        ----------
        direction : str
            Direction du déplacement ('N', 'S', 'E' ou 'O').
        grille : objet Grille
            Représente la grille du jeu contenant la méthode `deplacement_permis(x, y)`.

        Returns
        -------
        bool
            True si le déplacement a eu lieu, False sinon.
        """
        x, y = self.position
        dx, dy = direction
        new_x, new_y = x + dx, y + dy
        
        if grille.deplacement_permis(new_x, new_y):
            self.position = new_x, new_y
            return True
        return False
    


    def ramasser_objet(self, objet):
        """
        Ramasse un objet et applique ses effets à l'inventaire.

        Paramètres
        ----------
        objet : objet
            L’objet à ramasser, contenant une méthode `appliquer(inventaire)`.

        Returns
        -------
        None
        """
        objet.appliquer(self.inventaire)
