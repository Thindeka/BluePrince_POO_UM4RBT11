import random
from src.AutreObjet import AutreObjet
from src.Inventaire import Inventaire
from src.ObjetPermanent import ObjetPermanent
from src.AutreObjet import Pomme, Banane, Gateau, Sandwich, Repas, Coffre, Casier, EndroitCreuser

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

    def __init__(self, nom="piece", rarete=1, cout=1, porte=2):
        """rareté, coût"""
        self._nom = nom
        self._rarete = rarete
        self._cout = cout
        self._porte = porte
        self.objets: list[AutreObjet | ObjetPermanent | Coffre | Casier | EndroitCreuser] = []
        self.initialiser_contenu()
        ### à quel moment définir les pièces disponibles et leur probabilité de tirage ?
        self._pieces_disponibles = [] ### définir les pièces disponibles dans le manoir
        # Chaque incrément du niveau de rareté doit diviser par trois la probabilité de tirer la pièce.
        self.probability_distribution = [] ### définir la distribution de probabilité en fonction de la rareté des pièces
        nom : str = "piece"   ### nom est un attribut donc il va à l'intérieur du constructeur
        """Comment définir l'orientation d'une pièce et donc son nombre de portes"""
        """récupérer placement du joueur : condition de placement"""
        """Définir l'intéraction du joueur avec la pièce : contenu de celle-ci"""
        """Définir une pioche"""
    
    def initialiser_contenu(self):
        """Ajoute du contenu aléatoire à la pièce."""
        tirage = random.random()
        if tirage < 0.3:
            self.objets.append(Coffre())
        elif tirage < 0.5:
            self.objets.append(Casier())
        elif tirage < 0.6:
            self.objets.append(EndroitCreuser())
        elif tirage < 0.8:
            self.objets.append(AutreObjet(nom="gemme", effet="bonus")) # 20 % des pièces vides

    def random_tirage(self):
        """Tirage aléatoire de pièces
        Doit vérifier la rareté, le coût en gemmes (au moins 1 pièce = 0) et la condition de placement
        Rareté : créer une liste des pièces disponibles et l'autre ses probzabilités
        Cout en gemme : créer 2 listes, une : des pièces coutant des gemmes (dont on tirera 2 pièces) 
        et l'autre n'en coutant pas (dont on en tirera 1 pièce)
        """
        #pieces = [random.choice(self._pieces_disponibles) for i in range(3)]
        pieces = random.choice(self._pieces_disponibles, 3, p=self.probability_distribution)
        print("choisi une pièce où te diriger")

    def choisir_piece(self):
        """Le joueur choisit une pièce parmi les 3 tirées aléatoirement"""
        piece = [] ### à modifier : choix du joueur parmi les 3 pièces, renvoie vers la fonction correspondante
        del self._pieces_disponibles[piece] # supprimer la pièce de la pioche une fois utilisée
    
    def appliquer (self, inv : Inventaire) :  
        raise NotImplementedError

    def interagir(self, inv: Inventaire):
        messages = []
        for obj in self.objets:
            if isinstance(obj, AutreObjet):
                obj.appliquer(inv)
                messages.append(f"Objet ramassé : {obj.nom}")
            elif isinstance(obj, (Coffre, Casier, EndroitCreuser)):
                pass
        return messages


class Jaunes(Piece):
    """type de pièce : magasin"""
    
    def __init__(self):
        super().__init__()  ### il manque les paramètres du constructeur


    def Commissariat(self):
        nom = "Commissariat"
        self._rarete = 1
        self._cout = 1
        self._porte = 2 ### faut-il indiquer l'orientation de la porte (gauche, droite etc..) ? Doit faire référence à la classe grille ?
        
        def achat_ObjetPermanent(self):
            #### définir Pelle, Marteau, DetecteurMetaux comme attributs de classe dans ObjetPermanent
            """Permet d'acheter si le joueur possède des pièces d'or.
            Paramètres
            ----------
        
            Returns
            -------
            str
                Message indiquant l'achat du joueur.
            """
            ###### mauvais acces pour les objets permanents, un joueur a un inventaire, cet inventaire contient une liste d objets permanents (a coder) 
            ### vérifier inventaire (surtout le "4*Inventaire.gemmes")
            articles = {Inventaire.gemmes: 3, Inventaire.Pelle: 6, Inventaire.Marteau: 8, Inventaire.DetecteurMetaux: 10, 4*Inventaire.gemmes: 10, Inventaire.cles: 10}
            articles_update = articles.copy()
            for nom in articles_update.keys():
                if Inventaire.possede_obj_permanent(nom) == True :
                    del articles_update[nom]
            articles_disponibles = [random.choice(articles_update) for i in range(4)]
            objet = [] # renvoie "objet" choisi
            ### en fonction du choix du joueur, débiter de son inventaire le montant en pièces d'or
            if Inventaire.depenser_pieceOr(articles_disponibles[objet]):
                Inventaire.ajouter_obj_permanent(objet)
                return f" Vous avez acheté : {objet.nom}"

    def Cuisine(self):
        nom = "Cuisine"
        """Nouriture à vendre"""
        self._rarete = 0
        self._cout = 1
        def achat_AutreObjet(self):
            #### définir Pelle, Marteau, DetecteurMetaux comme attributs de classe dans ObjetPermanent
            """Permet d'acheter si le joueur possède des pièces d'or.
            Paramètres
            ----------

            Returns
            -------
            str
                Message indiquant l'achat du joueur.
            """
            ###### mauvais acces pour les objets permanents, un joueur a un inventaire, cet inventaire contient une liste d objets permanents (a coder) 
            ### vérifier inventaire 
            articles_disponibles = {Inventaire.Banane: 2, Inventaire.Sandwich: 8}
            objet = [] # renvoie "objet" choisi
            ### en fonction du choix du joueur, débiter de son inventaire le montant en pièces d'or
            if Inventaire.depenser_pieceOr(articles_disponibles[objet]):
                Inventaire.autres_objets.append(objet) ### à vérifier ??
                return f" Vous avez acheté : {objet.nom}"
        
        def contenu_cuisine(self):
            """Contenu possible de la cuisine"""
            contenu_possibles = [None, Inventaire.clé, Inventaire.gemmes, 2*Inventaire.piecesOr, 3*Inventaire.piecesOr, 5*Inventaire.piecesOr]
            return random.choice(contenu_possibles)

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

# Problème > Classes Jaunes, vertes incomplètes. 
# Il faut Passer inventaire ou game pour pouvoir interagir.
# Ajouter contenu réel : Coffre(), EndroitCreuser(), AutreObjet().
