from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
import random
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from src.Inventaire import Inventaire



class AutreObjet(ABC) :
    """
    Classe de base pour tous les objets utilisables dans le jeu.

    Attributs de classe
    -------------------
    nom : str
        Nom de l'objet (valeur par défaut : "autre_obj").
    """
    nom : str = "autre_obj"  # attribut de classe, valeur par défaut

    @abstractmethod
    def appliquer (self, inv : 'Inventaire') :  
        raise NotImplementedError



class Pomme(AutreObjet):
    """ 
    Classe fille de AutreObjet représentant une pomme.
    Effet : Redonne 2 pas 
    
    """

    nom = "pomme"

    def appliquer(self, inv: 'Inventaire'):
        """
        Ajoute 2 pas à l’inventaire du joueur.

        Paramètres
        ----------
        inv : Inventaire
            Inventaire du joueur.

        Returns
        -------
        None
        """
        inv.ramasser_pas(2)  



class Banane(AutreObjet):
    """ 
    Classe fille de AutreObjet représentant une banane.
    Effet : Redonne 3 pas 
    """
    nom = "banane"

    def appliquer(self, inv: 'Inventaire'):
        """
        Ajoute 3 pas à l’inventaire du joueur.

        Paramètres
        ----------
        inv : Inventaire
            Inventaire du joueur.

        Returns
        -------
        None
        """
        inv.ramasser_pas(3)  



class Gateau(AutreObjet):
    """ 
    Classe fille de AutreObjet représentant un gâteau.
    Effet : Redonne 10 pas 
    """
    nom = "gateau"

    def appliquer(self, inv: 'Inventaire'):
        """
        Ajoute 10 pas à l’inventaire du joueur.

        Paramètres
        ----------
        inv : Inventaire
            Inventaire du joueur.

        Returns
        -------
        None
        """
        inv.ramasser_pas(10)  



class Sandwich(AutreObjet):
    """ 
    Classe fille de AutreObjet représentant un sandwich.
    Effet : Redonne 15 pas 
    """
    nom = "sandwich"

    def appliquer(self, inv: 'Inventaire'):
        """
        Ajoute 15 pas à l’inventaire du joueur.

        Paramètres
        ----------
        inv : Inventaire
            Inventaire du joueur.

        Returns
        -------
        None
        """
        inv.ramasser_pas(15)  # Le joueur gagne 15 pas



class Repas(AutreObjet):
    """ 
    Classe fille de AutreObjet représentant un repas.
    Effet : Redonne 25 pas 
    """
    nom = "repas"

    def appliquer(self, inv: 'Inventaire'):
        """
        Ajoute 25 pas à l’inventaire du joueur.

        Paramètres
        ----------
        inv : Inventaire
            Inventaire du joueur.

        Returns
        -------
        None
        """
        inv.ramasser_pas(25)  # Le joueur gagne 25 pas



class Coffre :
    """Coffre ouvrable avec une clé ou un marteau.
    Contient un nombre aléatoire d'AutreObjet.

    Paramètres
    -----------
    min_objets : int
        Nombre minimum d'objets à générer lors de l'ouverture.
    max_objets : int
        Nombre maximum d'objets à générer lors de l'ouverture.
    contenu_possibles : Optional[List[Optional[AutreObjet]]]
        Liste d'objets possibles (None représente un emplacement vide).

    Attributs
    ---------
    contenu_possibles : List[AutreObjet] 
        Objets disponibles dans le coffre.
    nb_objets : int
        Nombre d'objets qui seront tirés aléatoirement à l'ouverture.

    Méthodes
    --------
    ouvrir(inv: Inventaire) -> str
        Tente d'ouvrir le coffre en appelant 'inv.ouvrir_coffre()'.
        Si l'ouverture échoue, renvoie un message d'erreur.
        Sinon applique les objets trouvés à l'inventaire et retourne un résumé des objets récupérés.
    """
    
    def __init__(self, min_objets: int = 1, max_objets: int = 3, contenu_possibles: Optional[List[AutreObjet]] = None):
        # Par défaut, le coffre peut contenir un des objets consommables
        if contenu_possibles is None:
            contenu_possibles = [Pomme(), Banane(), Gateau(), Sandwich(), Repas()]
        self.contenu_possibles = contenu_possibles
        self.nb_objets = random.randint(min_objets, max_objets)  # Nombre d'objets réellement dans le coffre

    def ouvrir(self, inv : 'Inventaire') -> str :
        """Ouvre le coffre si le joueur possède une clé ou un marteau."""
        if not inv.ouvrir_coffre() :   # inv.ouvrir_coffre encapsule la règle 
            return "Le coffre est verrouillé. Il faut une clé ou un marteau"
        
        objets_trouves = random.choices(self.contenu_possibles, k=self.nb_objets)
        noms_trouves = []
        for obj in objets_trouves:
            obj.appliquer(inv)
            noms_trouves.append(obj.nom)
        return f"Le coffre contenait : {', '.join(noms_trouves)}"




class Casier:
    """Casier ouvrable uniquement avec une clé dans la pièce vestiaire.

    Paramètres
    -----------
    min_objets (int): nombre minimum d'objets à générer lors de l'ouverture.
    max_objets (int): nombre maximum d'objets à générer lors de l'ouverture.
    contenu_possibles (Optional[List[Optional[AutreObjet]]]): liste d'objets possibles (None représente un emplacement vide).

    Attributs
    ---------
    contenu_possibles (List[Optional[AutreObjet]]): options d'objets disponibles dans le casier.
    nb_objets (int): nombre d'objets qui seront tirés aléatoirement à l'ouverture.

    Méthodes
    --------
    ouvrir_casier(inv: Inventaire) -> str
        Tente d'ouvrir le casier en dépensant une clé depuis l'inventaire `inv`.
        Si la clé manque, renvoie un message d'erreur.
        Sinon, applique les objets trouvés à l'inventaire et retourne un résumé des objets récupérés.
    """
    
    def __init__(self, min_objets: int = 1, max_objets: int = 2, contenu_possibles: Optional[List[Optional[AutreObjet]]] = None):
        if contenu_possibles is None:
            contenu_possibles = [None, Pomme(), Gateau(), Repas(), Sandwich(), Banane()]
        self.contenu_possibles = contenu_possibles
        self.nb_objets = random.randint(min_objets, max_objets)

    def ouvrir_casier(self, inv: 'Inventaire') -> str :
        """Ouvre le casier si le joueur possède une clé."""
        if not inv.depenser_cles(1) :
            return "Vous avez besoin d'une clé pour ouvrir ce casier."
        
        objets_trouves = random.choices(self.contenu_possibles, k=self.nb_objets)
        noms_trouves = []
        for obj in objets_trouves:
            if obj:
                obj.appliquer(inv)
                noms_trouves.append(obj.nom)
        if noms_trouves:
            return f"Vous avez trouvé : {', '.join(noms_trouves)}"
        return "Le casier était vide."



class EndroitCreuser :
    """
    Représente un endroit où le joueur peut creuser pour trouver des objets.
    Paramètres
    -----------
    min_objets (int): nombre minimum d'objets à générer lors du creusage.
    max_objets (int): nombre maximum d'objets à générer lors du creusage.
    contenu_possibles (Optional[List[Optional[AutreObjet]]]): liste d'objets possibles (None représente un emplacement vide).
    Attributs
    ---------
        contenu_possibles (List[Optional[AutreObjet]]): Liste des objets pouvant être trouvés.
        nb_objets (int): Nombre d'objets à trouver lors du creusage.
    Méthodes
    ---------
        creuser(inv: 'Inventaire') -> str: 
            Permet de creuser si le joueur possède une pelle et retourne les objets trouvés.
    """
    
    def __init__(self, min_objets: int = 1, max_objets: int = 2, contenu_possibles: Optional[List[Optional[AutreObjet]]] = None):
        if contenu_possibles is None:
            contenu_possibles = [None, Pomme(), Banane()]
        self.contenu_possibles = contenu_possibles
        self.nb_objets = random.randint(min_objets, max_objets)

    def creuser(self, inv: 'Inventaire'):
        """Creuse si le joueur possède une pelle."""

        if not inv.creuser() :
            return " Vous avez besoin d'une pelle pour creuser."
        
        objets_trouves = random.choices(self.contenu_possibles, k=self.nb_objets)
        noms_trouves = []
        for obj in objets_trouves:
            if obj:
                obj.appliquer(inv)
                noms_trouves.append(obj.nom)
        if noms_trouves:
            return f"Vous avez trouvé : {', '.join(noms_trouves)}"
        return "L'endroit à creuser est vide"