from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Inventaire import Inventaire




class ObjetPermanent :
    """
    Objet permanent
    Un objet permanent a un nom et s'applique à l'inventaire
    """
    
    nom : str = "obj_perm"  # attribut de classe, obj_perm = valeur par défaut
     
    def appliquer (self, inv : 'Inventaire') -> None :  
        # enregistrer possession + appliquer les effets (si effets à appliquer)
        is_new = inv.enregistrer_possession_obj_perm(self)
        if not is_new :
            return
        self._appliquer_effets(inv) 

    def _appliquer_effets (self, inv : 'Inventaire') -> None :
        pass  # par défaut rein ne se passe (implémenté éventuellement dans classes filles)
    



class Pelle (ObjetPermanent) :
    """ Permet de creuser à certains endroits, permettant de trouver certains objets"""
    nom = "pelle"
    pass




class Marteau (ObjetPermanent) :
    """ Permet de briser les cadenas des coffres, permettant de les ouvrir sans dépenser de clé """
    nom = "marteau"
    pass




class KitCrochetage (ObjetPermanent) :
    """ Permet d'ouvrir certaines portes, sans dépenser de clé"""
    nom = "kit_crochetage"
    pass




class DetecteurMetaux (ObjetPermanent) :
    """ Augmente la chance de trouver des clés et des pièces dans le manoir"""
    nom = "detecteur_metaux"
    def _appliquer_effets(self, inv : 'Inventaire') -> None:
        inv.chance_cles += 0.10  # faire cas où top 100%
        inv.chance_piecesOr += 0.10  # faire cas où top 100%




class PatteLapin (ObjetPermanent) :
    """ Augmente la chance de trouver des objets (y compris des objets permanents) dans le manoir"""
    nom = "patte_lapin"
    def _appliquer_effets (self, inv : 'Inventaire') -> None :
        inv.chance_objets +=  0.10  # faire cas où top 100%
