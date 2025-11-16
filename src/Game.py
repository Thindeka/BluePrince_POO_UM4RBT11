from src.Grille import Grille
from src.Joueur import Joueur
from src.Piece import Piece2, CouleurPiece, FORME_CROIX
from src.Pioche import Pioche2
from src.AutreObjet import Coffre, Casier, EndroitCreuser
from typing import Dict, Optional, Any
import random
from src.AutreObjet import AutreObjet, Banane, Gateau, Pomme, Repas, Sandwich
from src.ObjetPermanent import DetecteurMetaux, KitCrochetage, Marteau, ObjetPermanent, PatteLapin, Pelle
from src.Piece import FORME_T_ONE, OPPOSE

class Game:
    """
    Représente la logique principale du jeu.

    Attributs
    ---------
    grille : Grille
        Instance de la grille du jeu.
    joueur : Joueur
        Instance du joueur.
    inv : Inventaire
        Inventaire du joueur.
    pioche_pieces : Pioche2
        Instance de la pioche de pièces.
    state : str
        État actuel du jeu (exploration, tirage, victoire, game_over, achat).
    tour : int
        Compteur de tours.
    last_message : str
        Dernier message à afficher à l'écran.
    boosts_pioche_par_couleur : Dict[CouleurPiece, int]
        Boosts de pioche par couleur.
    boosts_loot : Dict[str, int]
        Ressources lootées.
    ressources_grille : Dict[tuple[int,int], Dict[str,int]]
        Ressources présentes sur la grille.
    tirage_en_cours : Optional[Dict[str, Any]]
        Détails du tirage en cours.
    contexte_achat : Optional[Dict[str, Any]]
        Contexte d'achat en cours.
    contexte_special : Optional[Dict[str, Any]]
        Contexte spécial de la pièce courante.
    game_over_selection : int
        Sélection pour l'écran de fin de partie.
    rejouer_options : List[str]
        Options pour rejouer ou quitter.

    Méthodes
    --------
    __init__() :
        Initialise la partie, la grille, le joueur, la pioche et les états.
    _verifier_conditions_fin()
        Vérifie conditions de fin de partie (épuisement, blocage, sortie).
    handle_deplacement(dx, dy)
        Gère le déplacement du joueur en mode exploration.
    handle_choix_tirage(mvt) 
        Change la sélection lors d'un tirage de pièces.
    handle_confirmation_tirage() 
        Valide et applique la pièce choisie lors d'un tirage.
    handle_ouvrir_sur_piece_courante()
        Ouvre un coffre/casier/point à creuser s'il existe un contexte spécial.
    handle_re_tirage()
        Relance le tirage (consomme un dé).
    handle_confirmation_magasin() 
        Valide l'achat sélectionné en magasin.
    utiliser_objet(objet_nom)
        Utilise un objet consommable de l'inventaire.
    ouvrir_coffre(coffre) 
        Ouvre un coffre (délègue à l'objet Coffre).
    ouvrir_casier(casier) 
        Ouvre un casier (délègue à l'objet Casier).
    creuser_endroit(endroit) 
        Creuse un endroit (délègue à EndroitCreuser).
    statut() 
        Retourne un résumé utile pour le debug.
    entree_magasin(piece) 
        Prépare le contexte d'achat lors de l'entrée dans une pièce magasin.
    handle_navigation_magasin(delta) 
        Navigue entre les offres du magasin.
    handle_quitter_magasin() 
        Quitte le mode achat et revient en exploration.
    _direction_vect(dx, dy) 
        Convertit un vecteur (dx,dy) en direction (N/S/E/O).
    handle_navigation_game_over(dx) 
        Déplace le curseur sur l'écran de Game Over.
    handle_confirmation_game_over() 
        Valide le choix sur l'écran de Game Over (rejouer/quitter).
    _diagnostic_blocage() 
        Affiche des informations de debug pour expliquer un blocage.
    """

    def __init__(self):

        self.grille = Grille()
        self.joueur = Joueur()
        self.inv = self.joueur.inventaire
        self.pioche_pieces = Pioche2()
        self.state : str = "exploration"  # autres états : "tirage", "victoire", "game_over", "achat"
        self.tour = 0  # compteur de tours
        self.last_message = "" # dernier message temporaire à afficher à l'écran
        
        self.boosts_pioche_par_couleur : Dict[CouleurPiece, int] = {c : 0 for c in CouleurPiece}
        self.boosts_loot : Dict[str, int] = {
            "gemmes": 0,
            "piecesOr": 0,
            "cles": 0,
            "obj_perm": 0,
        }

        self.ressources_grille : Dict[tuple[int,int], Dict[str,int]] = {}  # exemple " {(3,4): {"or": 1}, (1,1): {"gemmes": 2}}"

        self.tirage_en_cours : Optional[Dict[str, Any]] = None  # dictionnaire à clés texte, valeurs de types mélangés” 
        self.contexte_achat : Optional[Dict[str, Any]] = None
        self.contexte_special: dict | None = None

        # il faut qu il y ait une piece au depart a la position du joueur 
        x0, y0 = self.joueur.position

        if not self.grille.deplacement_permis(x0,y0) :
            x0 = self.grille.largeur // 2
            y0 = self.grille.hauteur - 1
            self.joueur.position = (x0, y0)

        if self.grille.get_piece(x0,y0) is None :
            piece_a_placer = Piece2("Entrance", CouleurPiece.BLEU, FORME_T_ONE)
            self.grille.placer_piece(x0, y0, piece_a_placer)


        nx, ny = self.grille.voisin(x0, y0, "N")
        if self.grille.deplacement_permis(nx, ny):
            porte_n = self.grille.garantie_porte(x0, y0, "N", niveau=0)
            porte_n.ouverte = True
            # miroir
            self.grille.dict_portes(nx, ny)["S"].ouverte = True

        # Fin de partei, rejouer ?
        self.game_over_selection = 0  # 0 = Oui, 1 = Non
        self.rejouer_options = ["Oui", "Non"]

    def _verifier_conditions_fin(self):

        """
        Vérifie si le joueur a plus de pas

        Paramètres
        ----------
            None

        Returns
        -------
            Message, Etat du jeu
        """

        if self.inv.pas <= 0:
            self.state = "game_over"
            self.last_message = "Vous n'avez plus de pas — partie terminée."
            return

        # Vérifie si le joueur est bloqué
        x, y = self.joueur.position
        blocked = True
        for dx, dy in [(0,-1),(0,1),(1,0),(-1,0)]:
            nx, ny = x+dx, y+dy
            if self.grille.deplacement_permis(nx, ny):
                blocked = False
                break
        if blocked:
            self.last_message = "Vous êtes entouré(e) — partie terminée."
            self.state = "game_over"
            return

        # Vérifie si le joueur atteint la sortie
        if self.joueur.position == self.grille.sortie:
            self.state = "victoire"
            self.last_message = "Félicitations ! Vous avez trouvé la sortie."
            return

    def handle_deplacement(self, dx : int, dy : int) -> None : # gestion globale du moove du jouer / différent de def dans classe grille qui gère les aspects spatiaux 
        """
        Déplace le joueur dans une direction donnée.

        Paramètres
        ----------
            dx (int): Déplacement en x (-1, 0, 1).
            dy (int): Déplacement en y (-1, 0, 1).

        Returns
        -------
            None
        """
       
        if self.state != "exploration" :
            return  # deplacement impossible car on est pas en exploration
        
        deplacement, ouverture, pas_consommes, message = self.grille.deplacer_joueur(self.joueur, self.inv, dx, dy) #  booeleens 

        if message:
            self.last_message = message
            return message
    
        if deplacement :
            if pas_consommes :
                self.inv.utiliser_pas(pas_consommes)  # il faut consommer les pas si on s est deplacé

            x, y = self.joueur.position
            piece = self.grille.get_piece(x,y)

            if piece is not None :
                piece.effet_entree(self)

        if ouverture :
            x, y = self.joueur.position
            new_x = x + dx
            new_y = y + dy
            dir_entree = OPPOSE[self._direction_vect(dx, dy)]

            pieces = self.pioche_pieces.tirage_3_pieces(self.grille, new_x, new_y, dir_entree, boosts=self.boosts_pioche_par_couleur)

            if not pieces :
                return 
            
            self.tirage_en_cours = {
                "cible" : (new_x, new_y),   # où on va poser la piece
                "dir_entree" : dir_entree,  # d'où on arrive
                "pieces" : pieces,  # les pieces proposées par le tirage
                "index" : 0,   # la piece selectionnee
            }


            self.state = "tirage"
            return 

        self._verifier_conditions_fin()  

    def handle_choix_tirage (self, mvt : int) -> None :
        """
        Gère le déplacement du curseur de sélection durant le tirage.
        Si l'état courant n'est pas "tirage" ou s'il n'existe pas de tirage en cours, la méthode ne modifie rien.
        Le paramètre mvt est ajouté à l'index courant de la liste des pièces et l'index est normalisé
        par un opérateur modulo pour rester dans les bornes valides.

        Paramètres
        ----------
            mvt (int): incrément du curseur (positif pour avancer, négatif pour reculer)

        Returns
        -------
            None
        """

        if self.state != "tirage" or not self.tirage_en_cours :
            return  
        
        pieces = self.tirage_en_cours["pieces"]
        index = self.tirage_en_cours["index"]
        index = (index + mvt) % len(pieces) # modulo pour rester bien dans les bornes
        self.tirage_en_cours["index"] = index 


    def handle_confirmation_tirage (self) -> None :
        """
        Valide le choix de pièce lors d'un tirage et l'applique à la grille.

        Paramètres
        ----------
            None

        Returns
        -------
            None
        """

        message = ""
        if self.state != "tirage" or not self.tirage_en_cours :
            return  
        
        cible_x, cible_y = self.tirage_en_cours["cible"]
        piece : Piece2 = self.tirage_en_cours['pieces'][self.tirage_en_cours["index"]]

        # gestion des gemmes 
        if piece.cout_gemmes > 0 :
            if not self.inv.depenser_gemmes(piece.cout_gemmes) :
                message = "Vous n'avez pas assez de gemmes pour valider ce tirage."
                self.last_message = message
                return # on ne peut pas valider si on a pas assex de gemmes
            

        piece.poser_piece(self.grille, cible_x, cible_y)
        piece.effet_tirage(self)
        piece.effet_modif_pioche(self)
        piece.effet_modif_objets(self)
        piece.effet_ajout_catalogue(self)
        # (la dispersion peut être déclenchée ici aussi si c'est une pièce de ce type)
        if "dispersion" in piece.tags:
            piece.effet_dispersion(self)

        self.tirage_en_cours = None
        self.state = "exploration"

        self.tirage_en_cours = None # fin phase tirage
        self.state = "exploration"


    def handle_ouvrir_sur_piece_courante(self):
        
        """
        Appelé par l'UI quand le joueur appuie sur 'O' en exploration.
        On regarde si la pièce courante avait laissé un contexte spécial.

        Paramètres
        ----------
            None

        Returns
        -------
            None
        """

        if self.state != "exploration":
            return

        if not self.contexte_special:
            return

        kind = self.contexte_special.get("type")

        # casier -> 2.2 : "ouverts uniquement avec des clés"
        if kind == "casier":
            if self.inv.ouvrir_casier():
                # on donne un consommable aléatoire
                obj = random.choice([Pomme(), Banane(), Gateau(), Sandwich(), Repas()])
                obj.appliquer(self.inv)
                # on peut vider le contexte après ouverture
                self.contexte_special = None
            else:
                # pas de clé => on peut garder le contexte pour réessayer plus tard
                message = "Vous n'avez pas de clé pour ouvrir ce casier."
                self.last_message = message
                pass

        # coffre
        elif kind == "coffre":
            if self.inv.ouvrir_coffre():
                obj = random.choice([Pomme(), Banane(), Gateau(), Sandwich(), Repas()])
                obj.appliquer(self.inv)
                self.contexte_special = None
            else:
                message = "Vous n'avez pas de clé ni de marteau pour ouvrir ce coffre."
                self.last_message = message
                pass

        # endroit à creuser
        elif kind == "creuser":
            if self.inv.creuser():
                obj = random.choice([Pomme(), Banane(), Gateau()])
                obj.appliquer(self.inv)
                self.contexte_special = None
            else:
                message = "Vous n'avez pas de pelle pour creuser."
                self.last_message = message
                pass

    
    def handle_re_tirage (self) -> None :
        """
        Relancer le tirage des pièces avec un dé.

        Paramètres
        ----------
            None

        Returns
        -------
            None
        """

        message = "" 
        
        if self.state != "tirage" or not self.tirage_en_cours :
            return

        if not self.inv.depenser_des(1) :  # pas de dé pour faire le tirage
            message = "Vous n'avez pas de dé pour relancer le tirage."
            self.last_message = message
            return

        cible_x, cible_y = self.tirage_en_cours["cible"]
        dir_entree = self.tirage_en_cours["dir_entree"]

        pieces = self.pioche_pieces.tirage_3_pieces(self.grille, cible_x, cible_y, dir_entree)
        
        if not pieces :
            return

        self.tirage_en_cours["pieces"] = pieces
        self.tirage_en_cours["index"] = 0


    def handle_confirmation_magasin(self) -> None:
        """
        Valide l'achat sélectionné en magasin.

        Paramètres
        ----------
            None

        Returns
        -------
            None
        """        

        if self.state != "achat" or not self.contexte_achat:
            return

        offres = self.contexte_achat["offres"]
        i = self.contexte_achat.get("index", 0)
        nom, prix, code = offres[i]

        if not self.inv.depenser_pieceOr(prix):  # on essaye de voir si on assez d or
            self.last_message = "Vous n'avez pas assez de pièces d'or pour cet achat."
            return

        # appliquer l'achat
        if code == "cle":
            self.inv.ramasser_cles(1)
            self.last_message = "vous avez acheté une clé."
        elif code == "de":
            self.inv.ramasser_des(1)
            self.last_message = "vous avez acheté un dé."
        elif code == "pomme":
            Pomme().appliquer(self.inv)
            self.last_message = "vous avez acheté une pomme (+2 pas)."
        elif code == "pelle":
            self.inv.ajouter_obj_permanent(Pelle())
            self.last_message = "vous avez acheté une pelle."

        self.handle_quitter_magasin()


    def utiliser_objet(self, objet_nom: str):
        """
        Interaction avec les objets 

        Paramètres
        ----------
            None

        Returns
        -------
            None
        """        
   
        for obj in self.inv.autres_objets:
            if obj.nom == objet_nom:
                obj.appliquer(self.inv)
                self.inv.autres_objets.remove(obj)
                return f"Vous avez utilisé une {obj.nom}."
        return "Objet non trouvé dans l'inventaire."


    def ouvrir_coffre(self, coffre: Coffre):
        """Ouvre un coffre avec objets aléatoires."""
        return coffre.ouvrir(self.inv)

    def ouvrir_casier(self, casier: Casier):
        """Ouvre un casier avec objets aléatoires."""
        return casier.ouvrir_casier(self.inv)

    def creuser_endroit(self, endroit: EndroitCreuser):
        """Creuse un endroit avec objets aléatoires."""
        return endroit.creuser(self.inv)

    def statut(self):   # statut du jeu
        """
        Retourne un résumé de la partie (utile pour le debug).
        """
        return (
            f"État : {self.state}\n"
            f"Position : {self.joueur.position}\n"
            f"Pas restants : {self.inv.pas}\n"
            f"Pièces d'or : {self.inv.piecesOr}\n"
            f"Gemmes : {self.inv.gemmes}\n"
            f"Clés : {self.inv.cles}\n"
            f"Dés : {self.inv.des}"
        )
    
    def entree_magasin(self, piece) -> None:
        """
        Appelé quand on entre dans une pièce jaune.
        On prépare les offres et on passe en état 'achat'.
        """
        # offres à diversifier
        offres = [
            ("Clé", 3, "cle"),
            ("Dé", 4, "de"),
            ("Pomme", 1, "pomme"),
            ("Pelle (permanent)", 6, "pelle"),
        ]

        self.contexte_achat = {
            "piece": piece,
            "offres": offres,
            "index": 0,   # offre sélectionnée
        }
        self.state = "achat"

    
    def handle_navigation_magasin (self, delta: int) -> None:
        """
        delta = -1 (gauche) ou 1 (droite)
        """
        if self.state != "achat" or not self.contexte_achat:
            return
        offres = self.contexte_achat["offres"]
        i = self.contexte_achat.get("index", 0)
        i = (i + delta) % len(offres)
        self.contexte_achat["index"] = i

    def handle_quitter_magasin (self) -> None :
        self.contexte_achat = None
        self.state = "exploration"


    def _direction_vect (self, dx : int, dy : int) :
        correspondances = {
            (0, -1): "N",
            (0, 1): "S",
            (1, 0): "E",
            (-1, 0): "O",
        }
        return correspondances[(dx, dy)]

    def handle_navigation_game_over(self, dx: int) -> None:
        """
        Déplacement du curseur sur l’écran de Game Over (Oui / Non)
        """
        if self.state != "game_over":
            return

        # -1 = gauche / +1 = droite
        self.game_over_selection = (self.game_over_selection + (1 if dx > 0 else -1)) % len(self.rejouer_options)


    def handle_confirmation_game_over(self) -> None:
        """
        Valide le choix sur l’écran de Game Over.
        """
        if self.state != "game_over":
            return

        choix = self.rejouer_options[self.game_over_selection]

        if choix == "Oui":
            # Relancer une nouvelle partie
            self.__init__()
            self.last_message = "Nouvelle partie !"
        else:
            # Quitter le jeu proprement
            self.state = "quit"
            self.last_message = "Merci d’avoir joué !"
            
    def _diagnostic_blocage(self):
        """
        Affiche pourquoi le joueur est considéré bloqué : pour debug.
        """
        x, y = self.joueur.position
        print("=== DIAGNOSTIC BLOCAGE ===")
        print(f"Position joueur: {(x,y)}; Pas: {self.inv.pas}; Etat: {self.state}")
        for dx, dy, name in [(0,-1,'N'),(0,1,'S'),(1,0,'E'),(-1,0,'O')]:
            nx, ny = x+dx, y+dy
            in_bounds = 0 <= nx < self.grille.largeur and 0 <= ny < self.grille.hauteur
            print(f"Voisin {name} -> {(nx,ny)} ; in_bounds: {in_bounds}", end="")
            if not in_bounds:
                print(" (hors bornes)")
                continue
            piece = self.grille.get_piece(nx, ny)
            portes = self.grille.dict_portes(nx, ny) if hasattr(self.grille, "dict_portes") else {}
            print(f" | piece: {None if piece is None else piece.nom}", end="")
            if portes:
                for d, p in portes.items():
                    print(f" | porte[{d}]: ouverte={getattr(p,'ouverte',None)} niveau={getattr(p,'niveau',None)}", end="")
            else:
                print(" | portes: (aucune)", end="")
            # est-ce que la grille permet de s'y déplacer ?
            try:
                perm = self.grille.deplacement_permis(nx, ny)
            except Exception as e:
                perm = f"ERREUR deplacement_permis: {e}"
            print(f" | deplacement_permis: {perm}")
        print("=== FIN DIAGNOSTIC ===")

    def _verifier_conditions_fin(self) -> None :
        if self.inv.pas <= 0 :
            self.state = "game_over"
            self.last_message = "Vous êtes épuisée... plus de pas disponibles !"
        
            return 
        if self.joueur.position == self.grille.sortie :
            self.state = "victoire"
            self.last_message = "Bravo ! Vous avez trouvé la sortie !"
        
            return 

        # 3. Vérifier si le joueur est bloqué (aucun déplacement possible)
        x, y = self.joueur.position
        blocked = True

        for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            try:
                if self.grille.deplacement_permis(nx, ny):
                    blocked = False
                    break
            except Exception as e:
                # En cas d'erreur, on considère la case non praticable
                print(f"Erreur déplacement ({nx},{ny}) : {e}")

        # 4. Si bloqué → afficher message et fin de partie
        if blocked:
            self.last_message = "Vous êtes complètement bloqué(e) — partie terminée."
            print("=== DIAGNOSTIC BLOCAGE ===")
            print(f"Position joueur : {self.joueur.position}")
            for dx, dy, name in [(0, -1, 'Nord'), (0, 1, 'Sud'), (1, 0, 'Est'), (-1, 0, 'Ouest')]:
                nx, ny = x + dx, y + dy
                in_bounds = 0 <= nx < self.grille.largeur and 0 <= ny < self.grille.hauteur
                print(f"{name} -> {(nx, ny)} (in_bounds={in_bounds})", end="")
                if not in_bounds:
                    print(" (hors limites)")
                    continue
                try:
                    perm = self.grille.deplacement_permis(nx, ny)
                except Exception as e:
                    perm = f"Erreur : {e}"
                print(f" | déplacement permis : {perm}")
            print("=== FIN DIAGNOSTIC ===")

            self.state = "game_over"
            return    


