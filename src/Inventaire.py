from dataclasses import dataclass, field
from typing import List, Set

from src.ObjetPermanent import ObjetPermanent
from src.AutreObjet import AutreObjet



@dataclass
class Inventaire :
    """ 
    
    Inventaire du joueur ou de la joueuse 
    
    Objets consommables : 
    - pas  -> initialement à 70, le joueur ou la joueuse perd 1 pas à chaque déplacement (passer d'une pièce à une autre)
    - piecesOr -> initialement à 0, le joueur ou la joueuse peut ramasser des pièces dans le manoir, et les dépenser dans certaines salles en échange d'autres objets
    - gemmes -> initialement à 2, le joueur ou la joueuse peut ramasser des gemmes dans le manoir, et les dépenser pour choisir certaines salles lors du tirage au sort.
    - cles -> initialement à 0, le joueur ou la joueuse peut ramasser des clés dans le manoir, et les dépenser pour ouvrir des portes fermées à clé, ou des coffres pouvant contenir des objets.
    - des ->  initialement à 0, le joueur ou la joueuse peut ramasser des dés dans le manoir, et les dépenser pour tirer à nouveau au sort les pièces proposées lorsqu'on ouvre une nouvelle porte.
    
    Objets permanents :
    - pelle -> permet de creuser à certains endroits, permettant de trouver certains objets.
    - marteau -> permet de briser les cadenas des coffres, permettant de les ouvrir sans dépenser de clé.
    - kit de crochetage -> permet d'ouvrir certaines portes, sans dépenser de clé.
    - détecteur de métaux -> augmente la chance de trouver des clés et des pi`eces dans le manoir
    - patte de lapin -> augmente la chance de trouver des objets (y compris des objets permanents) dans le manoir

    dataclass pour eviter code repetitif, pour code lisible et code evolutif (facilité ajout/suppresion attributs)
    
    """

    ##### OBJETS CONSOMMABLES
    pas : int = 70
    piecesOr : int = 0
    gemmes : int = 2
    cles : int = 0
    des : int  = 0 

    ##### AVANTAGES 
    chance_cles : float = 0.0
    chance_piecesOr : float = 0.0
    chance_objets : float = 0.0

    
    ##### OBJETS PERMANENTS
    # à chaque fois qu'on instancie Inventaire, set() est appelé pour créer un nouvel sous ensemble vide indépendant
    noms_objets_permanents : Set[str] = field(default_factory=set)             # on stocke les noms des objets permanents
    objets_permanents : List[ObjetPermanent] = field(default_factory=list)     # on stocke les instances des objets permanents


    ####### AUTRES OBJETS
    
    noms_autres_objets : Set[str] = field(default_factory=set)        # noms des autres objets 
    autres_objets : List[AutreObjet] = field(default_factory=list)    # instances des autres objets 


    def enregistrer_possession_obj_perm (self, obj_perm : ObjetPermanent) -> bool :
        """
        Enregistre possession d'un objet permament
        True si ajouté
        False si on l'avait deja
        """
        if obj_perm.nom in self.noms_objets_permanents :
            return False
        self.noms_objets_permanents.add(obj_perm.nom)
        self.objets_permanents.append(obj_perm)
        return True




    def utiliser_pas (self, n : int = 1) -> None :
        """ Utilsie n pas
        
        Parametres 
        ----------
        n : int 
           nombre de pas
        
        Returns
        -------
        None
        
        """
        self.pas = max(0, self.pas - max(0,n))

    def ramasser_pas(self, n : int) :
        self.pas += max(0,n)   # on évite le comportement indésirables de faire un ajout avec un nombre négatif


    def ramasser_pieceOr (self, n : int) -> None :
        self.piecesOr += max(0,n)  # on évite le comportement indésirables de faire un ajout avec un nombre négatif

    def depenser_pieceOr (self, n : int) -> bool :
        if self.piecesOr >= n and n >= 0 :
            self.piecesOr -= max(0,n)
            return True
        return False
    


    def ramasser_gemmes (self, n : int) -> None :
        self.gemmes += max(0,n) 

    def depenser_gemmes (self, n : int) -> bool :
        if self.gemmes >= n and n >= 0 :
            self.gemmes -= max(0,n)
            return True
        return False
    


    def ramasser_cles (self, n : int) -> None :
        self.cles += max(0,n)  

    def depenser_cles (self, n : int = 1) -> bool :
        n = max (0,n)
        if self.cles < n :
            return False 
        self.cles -= n 
        return True
    


    def ramasser_des (self, n) -> None :
        self.des += max(0,n)  

    def depenser_des (self, n) -> bool :
        if self.des > 0 :
            self.des -= 1
            return True
        return False


 
    def ajouter_obj_permanent (self, obj_perm : ObjetPermanent) -> bool :   # wrapper 
        """ Ajoute objet permanent à l'inventaire si pas présent 
        ne fait rien si objet deja present 
        """
        present = obj_perm.nom in self.noms_objets_permanents
        obj_perm.appliquer(self)
        return not present

    
    def possede_obj_permanent (self, nom : str) -> bool :
        """ Retourne vrai si l'inventaire possède l'objet permanent en paramètre"""
        return True if nom in self.noms_objets_permanents else  False  # code redondant
    


    #### OUVRIR PORTE
    def peut_ouvrir_porte(self, niveau: int) -> bool:
        return self.ouvrir_porte(niveau, dry_run=True)
    

    def ouvrir_porte (self, niveau : int, dry_run : bool = False) -> bool :   # dry_run pour l'UI
        """ dry_run permet de pre-verifier action sans la comettre """
        if niveau <= 0:
            return True
        if niveau == 1:
            if self.cles > 0:
                if not dry_run:
                    self.cles -= 1
                return True
            if self.possede_obj_permanent("kit_de_crochetage"):
                return True  
            return False
        if niveau == 2:
            if self.cles > 0:
                if not dry_run:
                    self.cles -= 1
                return True
            return False
        return False
    

    ####### CRUSER
    def peut_creuser (self) -> bool :
        return self.creuser(dry_run=True)
    
    def creuser (self, dry_run : bool = False) -> bool :
        if self.possede_obj_permanent("pelle") :
            return True 
        return False
    
   
    

    ####### OUVRIR COFFRE
    def peut_ouvrir_coffre (self) -> bool :
        return self.ouvrir_coffre(dry_run=True)

    def ouvrir_coffre(self, dry_run : bool = False) -> bool :
        if self.possede_obj_permanent("marteau") :  # ouverture avec le marteau
            return True
        return (self.cles > 0) if dry_run else self.depenser_cles(1)