class Pomme(AutresObjets):
    """ Redonne 2 pas """
    nom = "pomme"

    def appliquer(self, inv):
        inv.ramasser_pas(2)  

class Banane(AutresObjets):
    """ Redonne 3 pas """
    nom = "banane"

    def appliquer(self, inv):
        inv.ramasser_pas(3)  

class Gateau(AutresObjets):
    """ Redonne 10 pas """
    nom = "gateau"

    def appliquer(self, inv):
        inv.ramasser_pas(10)  

class Sandwich(AutresObjets):
    """ Redonne 15 pas """
    nom = "sandwich"

    def appliquer(self, inv):
        inv.ramasser_pas(15)  # Le joueur gagne 15 pas

class Repas(AutresObjets):
    """ Redonne 25 pas """
    nom = "repas"

    def appliquer(self, inv):
        inv.ramasser_pas(25)  # Le joueur gagne 25 pas

class Coffre:
    """Coffre qu'on peut ouvrir avec une clé ou un marteau."""
    
    def __init__(self, contenu_possibles=None):
        # Par défaut, le coffre peut contenir un des objets consommables
        if contenu_possibles is None:
            contenu_possibles = [Pomme(), Banane(), Gateau(), Sandwich(), Repas()]
        self.contenu_possibles = contenu_possibles

    def ouvrir(self, inv):
        """Ouvre le coffre si le joueur possède une clé ou un marteau."""
        if inv.depense_cles(1) or inv.possede("marteau"):
            objet = random.choice(self.contenu_possibles)
            objet.appliquer(inv)
            return f" Le coffre contenait : {objet.nom}"
        return " Le coffre est verrouillé. Il faut une clé ou un marteau."


class Casier:
    """Casier qu'on peut ouvrir uniquement avec une clé."""
    
    def __init__(self, contenu_possibles=None):
        if contenu_possibles is None:
            contenu_possibles = [None, Pomme(), Gateau(), Repas()]
        self.contenu_possibles = contenu_possibles

    def ouvrir(self, inv):
        """Ouvre le casier si le joueur possède une clé."""
        if inv.depense_cles(1):
            objet = random.choice(self.contenu_possibles)
            if objet:
                objet.appliquer(inv)
                return f" Vous avez trouvé : {objet.nom}"
            return " Le casier était vide."
        return " Vous avez besoin d'une clé pour ouvrir ce casier."


class EndroitCreuser:
    """Endroit où creuser avec une pelle pour trouver des objets."""
    
    def __init__(self, contenu_possibles=None):
        if contenu_possibles is None:
            contenu_possibles = [None, Pomme(), Banane()]
        self.contenu_possibles = contenu_possibles

    def creuser(self, inv):
        """Creuse si le joueur possède une pelle."""
        if not inv.possede("pelle"):
            return " Vous n'avez pas de pelle."
        objet = random.choice(self.contenu_possibles)
        if objet:
            objet.appliquer(inv)
            return f" Vous avez trouvé : {objet.nom}"
        return " Vous n'avez rien trouvé cette fois."