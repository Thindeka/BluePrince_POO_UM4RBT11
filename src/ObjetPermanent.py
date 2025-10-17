class ObjetPermanent :
    """
    Objet permanent
    Un objet permanent a un nom et s'applique à l'inventaire
    """
    
    nom : str = "obj_perm"  # attribut de classe, obj_perm = valeur par défaut
     
    def appliquer (self, inv) :  
        raise NotImplementedError
    



class Pelle (ObjetPermanent) :
    """ Permet de creuser à certains endroits, permettant de trouver certains objets"""
    nom = "pelle"
    def appliquer (self, inv) :
        inv.peut_creuser = True 



class Marteau (ObjetPermanent) :
    """ Permet de briser les cadenas des coffres, permettant de les ouvrir sans dépenser de clé """
    nom = "marteau"
    def appliquer (self, inv) :
        inv.peut_briser = True 



class KitCrochetage (ObjetPermanent) :
    """ Permet d'ouvrir certaines portes, sans dépenser de clé"""
    nom = "kit_crochetage"
    def appliquer (self, inv) :
        inv.peut_ouvrir = True 



class DetecteurMetaux (ObjetPermanent) :
    """ Augmente la chance de trouver des clés et des pièces dans le manoir"""
    nom = "detecteur_metaux"
    def appliquer(self, inv):
        inv.chance_cles += 0.10  # faire cas où top 100%
        inv.chance_piecesOr += 0.10  # faire cas où top 100%



class PatteLapin (ObjetPermanent) :
    """ Augmente la chance de trouver des objets (y compris des objets permanents) dans le manoir"""
    nom = "patte_lapin"
    def appliquer (self, inv) :
        inv.chance_objets +=  0.10  # faire cas où top 100%
