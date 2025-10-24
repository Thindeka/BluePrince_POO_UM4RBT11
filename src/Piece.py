import random
from src.AutreObjet import AutresObjets
from src.Inventaire import Inventaire
from src.ObjetPermanent import ObjetPermanent

class Piece :
    """
    Classe de base pout toutes les pièces du manoir
    Attributs
    ----------
    nom : str
        nom de la pièce

    portes  :
        ménent vers des directions différentes. >= 1 (au min 1 : porte par laquelle la pièce a été ouverte)
        
    coût : int
        coût en gemmes à dépenser pour pouvoir tirer la pièce

    interaction : 
        interargir avec des objets de la pièce

    effet spécial : 
        Certaines pièces ont des effets spéciales

    rareté : int
        rareté d'une pièce (0 à 3) : (commonplace, standard, unusual, rare) chaque incrémenent de rareté divise par 3 la probabilité de tirer la pièce

    condition de placement :
        Certaines pièces ne peuvent être tiréees qu'à certains endroits. 
    -----

    pioche : 
        quand une pièce est ajoutée au manoir, elle est retirée de la "pioche" et ne peut plus être tirée 
        (sauf si elle et en plusieurs exemplaires) -> définir nb exemplaire de chaque pièce
    """

    def __init__(self, rarete, cout, porte):
        """rareté, coût"""
        self._rarete = rarete
        self._cout = cout
        self._porte = porte
        self._pieces_disponibles = [] # définir les pièces disponibles dans le manoir]
        nom : str = "piece"   ### nom est un attribut donc il va à l'intérieur du constructeur
        """Comment définir l'orientation d'une pièce et donc son nombre de portes"""
        """récupérer placement du joueur : condition de placement"""
        """Définir l'intéraction du joueur avec la pièce : contenu de celle-ci"""
        """Définir une pioche"""
    
    def random_tirage(self):
        """Tirage aléatoire de pièces
        Doit vérifier la rareté, le coût en gemmes (au moins 1 pièce = 0) et la condition de placement
        """
        pieces = [random.choice(self._pieces_disponibles) for i in range(3)] 
        print("choisi une pièce où te diriger")
    
    

class Jaunes(Piece):
    """type de pièce : magasin"""
    
    def __init__(self):
        super().__init__()  ### il manque les paramètres du constructeur

    def Commissariat(self):
        nom = "Commissariat"
        self._rarete = 1
        self._cout = 1
        self._porte = 2
        self._pieces_disponibles = self._pieces_disponibles - nom # à modifier mais c'est l'idée
        
        def achat(self, inv):
            #### définir Pelle, Marteau, DetecteurMetaux comme attributs de classe dans ObjetPermanent
            """Permet d'acheter si le joueur possède des pièces d'or.
            Paramètres
            ----------
            inv : str
                Inventaire du joueur.

            Returns
            -------
            str
                Message indiquant l'achat du joueur.
            """
            ###### mauvais acces pour les objets permanents, un joueur a un inventaire, cet inventaire contient une liste d objets permanents (a coder) 
            articles_disponibles = {Inventaire.gemmes: 3, ObjetPermanent.Pelle: 6, ObjetPermanent.Marteau: 8, ObjetPermanent.DetecteurMetaux: 10, 4*Inventaire.gemmes: 10, Inventaire.cles: 10}
            objet = [random.choice(self.articles_disponibles) for i in range(4)]
            ### en fonction du choix du joueur, débiter de son inventaire le montant en pièces d'or
            if inv.depenser_pieceOr():
                objet.appliquer(inv)
                return f" Vous avez acheté : {objet.nom}"

    def Cuisine(self):
        nom = "Cuisine"
        """Nouriture à vendre"""

    def Serrurier(self):
        nom = "Serrurier"
        """clés à vendre"""

    def Salle_Exposition(self):
        nom = "Salle_Exposition"
        """produit de luxe à vendre"""

    def Buanderie(self):
        nom = "Buanderie"
        """blanchir de l'argent"""

    def Librairie(self):
        nom = "Librairie"
        """livres à vendre"""

    def Armurerie(self):
        nom = "Armurerie"
        """blanchir de l'argent"""

        

class vertes(Piece):
    """jardins d'intérieur"""


class dés:
    """possibilité de retirer aléatoirement des pièces si le joueur possède un dé"""


