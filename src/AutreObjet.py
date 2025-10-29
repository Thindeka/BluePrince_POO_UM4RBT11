import random
from src.Inventaire import Inventaire


class AutreObjet :
    """
    Classe de base pour tous les objets utilisables dans le jeu.

    Attributs de classe
    -------------------
    nom : str
        Nom de l'objet (valeur par défaut : "autre_obj").
    """
    nom : str = "autre_obj"  # attribut de classe, valeur par défaut

    def appliquer (self, inv : Inventaire) :  
        raise NotImplementedError



class Pomme(AutreObjet):
    """ Redonne 2 pas """
    nom = "pomme"

    def appliquer(self, inv: Inventaire):
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
    """ Redonne 3 pas """
    nom = "banane"

    def appliquer(self, inv: Inventaire):
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
    """ Redonne 10 pas """
    nom = "gateau"

    def appliquer(self, inv: Inventaire):
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
    """ Redonne 15 pas """
    nom = "sandwich"

    def appliquer(self, inv: Inventaire):
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
    """ Redonne 25 pas """
    nom = "repas"

    def appliquer(self, inv: Inventaire):
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
    """Coffre qu'on peut ouvrir avec une clé ou un marteau."""
    
    def __init__(self, contenu_possibles=None):
        # Par défaut, le coffre peut contenir un des objets consommables
        if contenu_possibles is None:
            contenu_possibles = [Pomme(), Banane(), Gateau(), Sandwich(), Repas()]
        self.contenu_possibles = contenu_possibles

    def ouvrir(self, inv : Inventaire) -> str :
        """Ouvre le coffre si le joueur possède une clé ou un marteau."""
        if not inv.ouvrir_coffre() :   # inv.ouvrir_coffre encapsule la règle 
            return "Le coffre est verrouillé. Il faut une clé ou un marteau"
        objet = random.choice(self.contenu_possibles)
        objet.appliquer(inv)
        return f" Le coffre contenait : {objet.nom}"
        



class Casier:
    ####### implememnter fait que juste contenu dans piece vestiaire
    """Casier qu'on peut ouvrir uniquement avec une clé."""
    
    def __init__(self, contenu_possibles=None):
        if contenu_possibles is None:
            contenu_possibles = [None, Pomme(), Gateau(), Repas(), Sandwich(), Banane()]
        self.contenu_possibles = contenu_possibles

    def ouvrir_casier(self, inv: Inventaire) -> str :
        """Ouvre le casier si le joueur possède une clé."""
        if not inv.depenser_cles(1) :
            return "Vous avez besoin d'une clé pour ouvrir ce casier."
        objet = random.choice(self.contenu_possibles)
        if objet :  # le casier peut être vide
            objet.appliquer(inv)
            return f" Vous avez trouvé : {objet.nom}"
        return " Le casier était vide."




class EndroitCreuser:
    """Endroit où creuser avec une pelle pour trouver des objets."""
    
    def __init__(self, contenu_possibles=None):
        if contenu_possibles is None:
            contenu_possibles = [None, Pomme(), Banane()]
        self.contenu_possibles = contenu_possibles

    def creuser(self, inv: Inventaire):
        """Creuse si le joueur possède une pelle."""
        if not inv.creuser() :
            return " Vous avex besoin d'une pelle pour creuser."
        objet = random.choice(self.contenu_possibles)
        if objet:   # l'endroit peut ne rien contenir
            objet.appliquer(inv)
            return f" Vous avez trouvé : {objet.nom}"
        return "L'endroit à creuser est vide"