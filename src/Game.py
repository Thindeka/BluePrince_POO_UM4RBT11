from src.Grille import Grille
from src.Joueur import Joueur
from src.Piece import Piece
from src.AutreObjet import Pomme, Banane, Gateau, Sandwich, Repas, Coffre, Casier, EndroitCreuser
from src.Pioche import Pioche

class Game:
    """
    Représente la logique principale du jeu.
    """

    def __init__(self):
        
        self.grille = Grille()
        self.joueur = Joueur()
        self.inv = self.joueur.inventaire
        self.pioche_pieces = Pioche()
        self.state = "exploration"  # autres états : "tirage", "victoire", "game_over"
        self.tour = 0  # compteur de tours

    def update_state(self):   # état du jeu le long de la game 
        """
        Met à jour l’état du jeu selon les conditions actuelles.
        """
        if self.inv.pas <= 0:
            self.state = "game_over"
        elif self.victoire_atteinte():
            self.state = "victoire"
        else:
            self.state = "exploration"

    def victoire_atteinte(self) -> bool:
        """
        Vérifie si le joueur a atteint la sortie de la grille.
        """
        return self.joueur.position == self.grille.sortie 


    def deplacer_joueur(self, direction: str): # gestion globale du moove du jouer / différent de def dans classe grille qui gère les aspects spatiaux 
        """
        Déplace le joueur dans une direction donnée.
        """
        if self.state != "exploration":
            return "Déplacement impossible : pas en phase d’exploration."

        x, y = self.joueur.position
        dx, dy = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "O": (-1, 0)}.get(direction, (0, 0))

        deplacement, ouverture, pas_consommes = self.grille.deplacer_joueur(
            self.joueur, self.inv, dx, dy
        )

        if ouverture:
            self.state = "tirage"
            return "Une nouvelle pièce est à tirer !"

        if deplacement:
            self.inv.utiliser_pas(pas_consommes)
            self.update_state()
            return f"Vous vous êtes déplacé vers {direction}."

        return "Déplacement impossible."

    def tirer_nouvelle_piece(self):  # gestion du tirage des pièces 
        """
        Tire aléatoirement 3 nouvelles pièces quand le joueur ouvre une porte.
        """
        if self.state != "tirage":
            return "Aucune porte à franchir actuellement."

        tirage = self.pioche_pieces.tirage_3_pieces()
        self.state = "exploration"
        return f"3 pièces tirées : {', '.join([p.nom for p in tirage])}"

    def tour_suivant(self):  # avancement de la partie tour par tour 
        """
        Passe au tour suivant.
        """
        self.tour += 1
        self.update_state()
        if self.state == "game_over":
            return "Vous n’avez plus de pas. Partie terminée."
        if self.state == "victoire":
            return "Félicitations, vous avez gagné !"
        return f"Tour {self.tour} terminé. État actuel : {self.state}."

    def utiliser_objet(self, objet_nom: str):  # interaction avec les objets 
        """
        Utilise un objet consommable depuis l’inventaire.
        """
        for obj in self.inv.autres_objets:
            if obj.nom == objet_nom:
                obj.appliquer(self.inv)
                self.inv.autres_objets.remove(obj)
                return f"Vous avez utilisé une {obj.nom}."
        return "Objet non trouvé dans l’inventaire."

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
            f"Pièces d’or : {self.inv.piecesOr}\n"
            f"Gemmes : {self.inv.gemmes}\n"
            f"Clés : {self.inv.cles}\n"
            f"Dés : {self.inv.des}"
        )
