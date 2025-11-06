from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING, Set, Optional
import random

from src.AutreObjet import AutreObjet, Banane, Gateau, Pomme, Repas, Sandwich
from src.ObjetPermanent import DetecteurMetaux, KitCrochetage, Marteau, ObjetPermanent, PatteLapin, Pelle


if TYPE_CHECKING:
    from src.Grille import Grille
    from src.Inventaire import Inventaire
    from src.Game import Game
    from src.Porte import Porte
    

DIRECTIONS = {"N" : (0,-1), "S" : (0,1), "E" : (1,0), "O" : (-1,0)}  # on suit la convention des interfaces graphiques de cmettre l'origine en haut à gauche 
DIRECTIONS_REVERSE = {(0,-1):"N",(0,1):"S",(1,0):"E",(-1,0):"O"}
OPPOSE = {"N" : "S", "S" : "N", "E" : "O", "O" : "E"}


# énumération
class CouleurPiece(Enum) :
    JAUNE = auto()  # -> 1
    VERT = auto()   # -> 2 ...
    VIOLET = auto()
    ORANGE = auto()
    ROUGE = auto()
    BLEU = auto()


class FormePiece :
    """ correspond a l meplacement des portes de la piece """
    nom : str
    ens_portes : Set[str]

    def __init__(self, nom, ens_portes) -> None:
        self.nom = nom
        self.ens_portes = ens_portes
 
    def a_porte (self, direction : str) -> bool :
        return direction in self.ens_portes
    

# FORMES DE PIECE

# COULOIR
FORME_COULOIR_NS = FormePiece("couloir_ns", {"N", "S"})
FORME_COULOIR_EO =  FormePiece("couloir_eo", {"E", "O"})

# CROIX
FORME_CROIX = FormePiece("croix", {"N", "S", "E", "O"})

# CARRE (presque idem croix)
FORME_CARRE = FormePiece("carre", {"N", "S", "E", "O"})

# IMPASSE
FORME_IMPASSE_N = FormePiece("cul_n", {"N"})
FORME_IMPASSE_S = FormePiece("cul_s", {"S"})
FORME_IMPASSE_E = FormePiece("cul_e", {"E"})
FORME_IMPASSE_O = FormePiece("cul_o", {"O"})

# DEX A DEUX EN ANGLES
FORME_ANGLE_NE = FormePiece("angle_ne", {"N", "E"})
FORME_ANGLE_ES = FormePiece("angle_es", {"E", "S"})
FORME_ANGLE_SO = FormePiece("angle_so", {"S", "O"})
FORME_ANGLE_ON = FormePiece("angle_on", {"O", "N"})

# TROIS VOIES 
FORME_T_NES = FormePiece("t_nes", {"N", "E", "S"})
FORME_T_ESO = FormePiece("t_eso", {"E", "S", "O"})
FORME_T_SON = FormePiece("t_son", {"S", "O", "N"})
FORME_T_ONE = FormePiece("t_one", {"O", "N", "E"})


class Piece2 :
    """ 
    nom : str
    couleur : CouleurPiece
    jaune : JaunePiece  # uniquement pour les pieces jaunes (magasins)
    vert : VertPiece  # uniquement pour les pieces vertes (jardins)
    forme : FormePiece
    cout_gemmes : int = 0   # cout en gemmes a deoenser pour tirer la piece
    rarete : int = 0  # influence proba de tirer une piece, (0 à 3) : (commonplace, standard, unusual, rare)
    # image (a voir apres)
    """

    def __init__(self, nom: str, couleur : CouleurPiece, forme : FormePiece, cout_gemmes=0, rarete=0, tags=None) -> None:
        self.nom = nom
        self.couleur = couleur
        self.forme = forme
        self.cout_gemmes = cout_gemmes
        self.rarete = rarete
        ###
        self.tags = tags or []
        ###
        self.contenu: list[str] = []
        self.recompense_prise : bool = False  


    def a_porte (self, direction : str) -> bool :
        return self.forme.a_porte(direction)
    

    def peut_etre_posee (self, grille : 'Grille', x : int, y : int, dir_entree : str) -> bool :
        """ verification pour le tirage 2.7 
            -> piece doit avoir une porte du cote de l arrivee
            -> chaque porte de la piece doit etre dans les bornes
            -> si un voisin existe avec une porte vers la case actuelle, il faut avoir la porte de retour
        """

        # entree bloquee
        if dir_entree not in DIRECTIONS or not self.a_porte(dir_entree) :
            return False
        
        # hors bornes
        for d in self.forme.ens_portes :
            new_x, new_y = grille.voisin(x, y, d)   # case voisinne dans direction demandée
            if not grille.deplacement_permis(new_x, new_y) :
                return False
            
        
        for d in DIRECTIONS :
            new_x, new_y = grille.voisin(x, y, d)  # case voisinne dans direction demandée
            # ignorer ce voisin car il est hors bornes

            if not grille.deplacement_permis(new_x, new_y) :
                continue

            voisin = grille.get_piece(new_x, new_y)
            if voisin is None :
                continue ########### à completer comportement plus tard par grille.piece_at()

            if isinstance(voisin, Piece2) :
                if voisin.a_porte(OPPOSE[d]) :
                    if not self.a_porte(d) :
                        return False # car c est incoherent si le voisin a une porte vers la case courante masi que la case courant en a pas de porte vers le voisin
        
        return True
    

    def poser_piece (self, grille : 'Grille', x : int, y : int) -> None :
        """" On pose la piece et on ouvre les portes 'mirroirs' """
        
        grille.placer_piece(x,y,self) 
        
        for d in self.forme.ens_portes :
            porte = grille.garantie_porte(x, y, d)
            porte.ouverte = True
            new_x, new_y = grille.voisin(x, y, d)

            if not grille.deplacement_permis(new_x, new_y) :
                continue # on ne place pas de porte la ou on ne peut pas

            voisin = grille.get_piece(new_x, new_y)
            if voisin is None :
                continue

            portes_voisin = grille.dict_portes(new_x, new_y)
            porte_retour = portes_voisin.get(OPPOSE[d])

            if porte_retour is None :
                continue

            #porte.ouverte = True   # j ouvre la porte de al case courante 
            porte_retour.ouverte = True    # j ouvre la porte de la case voisinne
            porte_retour.set_niveau(0)


    
    def effet_entree (self, game : 'Game') :
        
        inv : 'Inventaire' = game.inv
        x, y = game.joueur.position
        nom = self.nom.lower()

        # récupérer les ressources déposées par d'autres pièces
        drop = game.ressources_grille.pop((x, y), None)
        if drop:
            if "gemmes" in drop:
                inv.ramasser_gemmes(drop["gemmes"])
            if "or" in drop:
                inv.ramasser_pieceOr(drop["or"])
            if "cles" in drop:
                inv.ramasser_cles(drop["cles"])

        if self.couleur is CouleurPiece.JAUNE or "shop" in nom or "magasin" in nom or "store" in nom:
            game.entree_magasin(self)
            return


        if self.recompense_prise : 
            return

        if "bedroom" in nom or "chambre" in nom:
            # regagner des pas
            inv.ramasser_pas(3)
            self.recompense_prise = True
            return

        if "chapel" in nom or "chapelle" in nom:
            # un peu d'or, c'est un lieu "positif" 
            inv.ramasser_pieceOr(2) ### pièce rouge avec normalement effet indésirable
            self.recompense_prise = True
            return

        if "garden" in nom or "veranda" in nom or "patio" in nom or "greenhouse" in nom :
            # gemme quasi systématique
            inv.ramasser_gemmes(1)
            inv.ramasser_pieceOr(2)

            # parfois un objet consommable de 2.2
            if random.random() < 0.4:
                obj = random.choice([Pomme(), Banane(), Gateau(), Sandwich(), Repas()])
                obj.appliquer(inv)

            # parfois un objet permanent
            if random.random() < 0.12:
                candidats = [
                    Pelle(),
                    Marteau(),
                    KitCrochetage(),
                    DetecteurMetaux(),
                    PatteLapin(),
                ]
                candidats = [c for c in candidats if not inv.possede_obj_permanent(c.nom)]
                if candidats:
                    inv.ajouter_obj_permanent(random.choice(candidats))

            # on peut aussi noter son contenu pour l'affichage
            if hasattr(self, "contenu"):
                if "Endroit à creuser" not in self.contenu:
                    self.contenu.append("Endroit à creuser")
            
            self.recompense_prise = True
            return
        
        if "locker" in nom or "vestiaire" in nom:
            # on ne l'ouvre pas automatiquement  c'est au joueur d'appuyer sur O
            # donc on indique juste au game qu'on est sur un casier
            game.contexte_special = {"type": "casier", "piece": self}
            if hasattr(self, "contenu"):
                if "Casier" not in self.contenu:
                    self.contenu.append("Casier")
            self.recompense_prise = True
            return

        if "shop" in nom or "store" in nom or "magasin" in nom:
            game.state = "shop"
            game.contexte_achat = {
                "piece": self,
                "offres": [             ### défini aussi dans la fonction entree_magasin de la classe Game, en double ??
                    ("Clé", 3, "cle"),
                    ("Dé", 4, "de"),
                    ("Pelle", 6, "pelle"),
                ],
            }
            self.recompense_prise = True
            return
        
        if "furnace" in nom or "fournaise" in nom or "trap" in nom:
            inv.utiliser_pas(1)
            self.recompense_prise = True
            return
        
        # MAID'S CHAMBER  boost + gemme (une fois)
        if "maid" in nom:
            inv.chance_objets = max(inv.chance_objets, 0.7)
            inv.ramasser_gemmes(1)
            self.recompense_prise = True
            return
    

        # MASTER BEDROOM 
        if "master bedroom" in nom:
            inv.ramasser_pas(5)
            self.recompense_prise = True
            return
        
        # PATIO , gemme + dépôt autour (mais une seule fois)
        if "patio" in nom:
            inv.ramasser_gemmes(1)
           
            for d, (dx, dy) in {"N": (0,-1), "S": (0,1), "E": (1,0), "O": (-1,0)}.items():
                nx, ny = x + dx, y + dy
                if game.grille.deplacement_permis(nx, ny):
                    game.ressources_grille.setdefault((nx, ny), {})
                    game.ressources_grille[(nx, ny)]["gemmes"] = \
                        game.ressources_grille[(nx, ny)].get("gemmes", 0) + 1
            self.recompense_prise = True
            return
        
        # OFFICE
        if "office" in nom:
            for d, (dx, dy) in {"N": (0,-1), "S": (0,1), "E": (1,0), "O": (-1,0)}.items():
                nx, ny = x + dx, y + dy
                if game.grille.deplacement_permis(nx, ny):
                    game.ressources_grille.setdefault((nx, ny), {})
                    game.ressources_grille[(nx, ny)]["or"] = \
                        game.ressources_grille[(nx, ny)].get("or", 0) + 2
            self.recompense_prise = True
            return
        
        # CHAMBER OF MIRRORS: ajoute des pièces (une fois)
        if "chamber of mirrors" in nom:
            if hasattr(game, "pioche_pieces") and game.pioche_pieces:
                game.pioche_pieces.ajouter_piece_modele("couloir_NS")
                game.pioche_pieces.ajouter_piece_modele("couloir_EO")
            self.recompense_prise = True
            return

        # POOL : soin une fois
        if "pool" in nom:
            inv.ramasser_pas(4)
            self.recompense_prise = True
            return


        return
        
    def effet_tirage (self, game : 'Game') -> None :
        """
        Appelé juste après avoir choisi cette pièce dans l'écran de tirage.
        Ici on peut donner/reprendre des ressources directement.
        """
        inv : 'Inventaire'= game.inv
        nom = self.nom.lower()

        # Master Bedroom : regagne des pas au moment où on la choisit
        if "master bedroom" in nom:
            inv.ramasser_pas(4) ### ca se répète avec l'effet d'entrée ?

        # Weight Room : retire des pas tout de suite
        if "weight room" in nom or "salle de sport" in nom:
            inv.utiliser_pas(2)

        # Furnace : rend plus probable le rouge après
        if "furnace" in nom or "fournaise" in nom:
            game.boosts_pioche_par_couleur[self.couleur.__class__.ROUGE] += 1

        # Greenhouse : booste le vert
        if "greenhouse" in nom:
            game.boosts_pioche_par_couleur[self.couleur.__class__.VERT] += 1

        # Veranda : booste la découverte d'objets
        if "veranda" in nom:
            game.boosts_loot["obj_perm"] += 1
            game.boosts_loot["gemmes"] += 1

        # Chamber of Mirrors : ajoute des pièces au catalogue
        if "chamber of mirrors" in nom or "chambre des miroirs" in nom:
            game.pioche_pieces.ajouter_piece_modele("couloir_NS")
            game.pioche_pieces.ajouter_piece_modele("couloir_EO")



    def effet_dispersion(self, game : 'Game') -> None:
        """
        Certaines pièces 'jettent' une ressource dans leurs voisines.
        On l'appelle depuis effet_a_l_entree OU depuis effet_tirage selon le type.
        """
        if "dispersion" not in self.tags:
            return

        grille = game.grille
        x, y = game.joueur.position
        for d in ("N", "S", "E", "O"):
            nx, ny = grille.voisin(x, y, d)
            if not grille.deplacement_permis(nx, ny):
                continue
            if grille.get_piece(nx, ny) is None:
                continue
            # on dépose 1 or dans la pièce voisine
            game.ressources_grille.setdefault((nx, ny), {})
            game.ressources_grille[(nx, ny)]["or"] = game.ressources_grille[(nx, ny)].get("or", 0) + 1

    # Effet de modif de proba de tirage 
    def effet_modif_pioche(self, game :'Game') -> None:
        """
        Modifie les chances de tirer certaines couleurs après que cette pièce a été posée.
        """
        if "boost_vert" in self.tags:
            game.boosts_pioche_par_couleur[self.couleur.__class__.VERT] += 1
        if "boost_bleu" in self.tags:
            game.boosts_pioche_par_couleur[self.couleur.__class__.BLEU] += 1
        if "boost_rouge" in self.tags:
            game.boosts_pioche_par_couleur[self.couleur.__class__.ROUGE] += 1

    #  Effet de modif de proba d'objets 
    def effet_modif_objets(self, game : 'Game') -> None:
        """
        Augmente les chances de trouver certains objets plus tard.
        """
        if "boost_gemmes" in self.tags:
            game.boosts_loot["gemmes"] += 1
        if "boost_obj_perm" in self.tags:
            game.boosts_loot["obj_perm"] += 1
        if "boost_cles" in self.tags:
            game.boosts_loot["cles"] += 1

    # Effet d'ajout au catalogue (Chamber of Mirrors, Pool) 
    def effet_ajout_catalogue(self, game : 'Game') -> None:
        """
        Certaines pièces ajoutent d'autres pièces à la pioche.
        On ajoute un nom ou un 'fournisseur' dans la pioche.
        """
        if "ajoute_couloir" in self.tags:
            game.pioche_pieces.ajouter_piece_modele("couloir_NS")
        if "ajoute_piece_rare" in self.tags:
            game.pioche_pieces.ajouter_piece_modele("salle_tresor")
