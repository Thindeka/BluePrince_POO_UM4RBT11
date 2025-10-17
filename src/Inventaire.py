from dataclasses import dataclass, field
from typing import List, Set

from src.ObjetPermanent import ObjetPermanent



@dataclass
class Inventaire :
    """ 
    METTRE SOUS BON FORMAT !!!!!!
    
    Inventaire du joueur ou de la joueuse 
    
    Objets consommables : 
    - pas  -> initialement à 70, le joueur ou la joueuse perd 1 pas à chaque déplacement (passer d'une pièce à une autre)
    - piecesOr -> initialement à 0, le joueur ou la joueuse peut ramasser des pièces dans le manoir, et les dépenser dans certaines salles en échange d'autres objets
    - gemmes -> initialement à 2, le joueur ou la joueuse peut ramasser des gemmes dans le manoir, et les dépenser pour choisir certaines salles lors du tirage au sort.
    - cles -> initialement à 0, le joueur ou la joueuse peut ramasser des clés dans le manoir, et les dépenser pour ouvrir des portes fermées à clé, ou des coffres pouvant contenir des objets.
    - des ->  initialement à 0, le joueur ou la joueuse peut ramasser des dés dans le manoir, et les dépenser pour tirer à nouveau au sort les pièces proposées lorsqu'on ouvre une nouvelle porte.
    
    Objets permanents :
    ###### expliquer

    dataclass pour eviter code repetitif, pour code lisible et code evolutif (Ajout/suppresion attributs facilité)
    """

    ##### Objets consommables
    pas : int = 70
    piecesOrd : int = 0
    gemmes : int = 2
    cles : int = 0
    des : int  = 0 

    ##### Pouvoirs 
    peut_creuser : bool = False
    peut_briser : bool = False
    peut_ouvrir : bool = False

    
    ##### Avantages 
    chance_cles : float = 0.0
    chance_piecesOr : float = 0.0
    chance_objets : float = 0.0

    
    ##### Objets permanents 

    # à chaque fois qu'on instancie Inventaire, set() est appelé pour créer un nouvel sous ensemble vide indépendant
    # on stocke les noms des objets permanents
    ens_objets_permanents : Set[str] = field(default_factory=set)  
    
    # on stocke les instances des objets permanents 
    liste_objets_permanents : List[ObjetPermanent] = field(default_factory=list)
    



