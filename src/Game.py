from src.Grille import Grille
from src.Joueur import Joueur
from src.Piece2 import Piece2, CouleurPiece
from src.Pioche2 import Pioche2
from src.AutreObjet import Coffre, Casier, EndroitCreuser
from typing import Dict, Optional, Any

class Game:
    """
    Représente la logique principale du jeu.
    """

    def __init__(self):
        
        self.grille = Grille()
        self.joueur = Joueur()
        self.inv = self.joueur.inventaire
        self.pioche_pieces = Pioche2()
        self.state : str = "exploration"  # autres états : "tirage", "victoire", "game_over"
        self.tour = 0  # compteur de tours

        self.tirage_en_cours : Optional[Dict[str, Any]] = None  # dictionnaire à clés texte, valeurs de types mélangés”
        # self.boost_couleur

        # il faut qu il y ait une piece au depart a la position du joueur 
        x0, y0 = self.joueur.position

        if not self.grille.deplacement_permis(x0,y0) :
            x0 = self.grille.largeur // 2
            y0 = self.grille.hauteur - 1
            self.joueur.position = (x0, y0)

        if self.grille.get_piece(x0,y0) is None :
            from src.Piece2 import Piece2, FORME_CROIX 
            piece_a_placer = Piece2("départ", CouleurPiece.BLEU, FORME_CROIX)
            self.grille.placer_piece(x0, y0, piece_a_placer)



    def handle_deplacement(self, dx : int, dy : int) -> None : # gestion globale du moove du jouer / différent de def dans classe grille qui gère les aspects spatiaux 
        """
        Déplace le joueur dans une direction donnée.
        """
       
        if self.state != "exploration" :
            return  # deplacement impossible car on est pas en exploration
        
        deplacement, ouverture, pas_consommes = self.grille.deplacer_joueur(self.joueur, self.inv, dx, dy)

        if deplacement and pas_consommes :
            self.inv.utiliser_pas(pas_consommes)  # il faut consommer les pas si on s est deplacé

        if ouverture :
            x, y = self.joueur.position
            new_x = x + dx
            new_y = y + dy
            dir_entree = self._direction_vect(dx, dy)

            pieces = self.pioche_pieces.tirage_3_pieces(self.grille, new_x, new_y, dir_entree)

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

        if self.state != "tirage" or not self.tirage_en_cours :
            return  
        
        pieces = self.tirage_en_cours["pieces"]
        index = self.tirage_en_cours["index"]
        index = (index + mvt) % len(pieces) # modulo pour rester bien dan sles bornes
        self.tirage_en_cours["index"] = index 


    def handle_confirmation_tirage (self) -> None :
        
        if self.state != "tirage" or not self.tirage_en_cours :
            return  
        
        cible_x, cible_y = self.tirage_en_cours["cible"]
        piece : Piece2 = self.tirage_en_cours['pieces'][self.tirage_en_cours["index"]]

        # gestion des gemmes 
        if piece.cout_gemmes > 0 :
            if not self.inv.depenser_gemmes(piece.cout_gemmes) :
                return # on ne peut pas valider si on a pas assex de gemmes
            

        piece.poser_piece(self.grille, cible_x, cible_y)
        piece.effet_tirage(self)

        self.tirage_en_cours = None # fin phase tirage
        self.state = "exploration"



    
    def handle_re_tirage (self) -> None :
        # avec un dé on peut relancer le tirage des pieces 
        
        if self.state != "tirage" or not self.tirage_en_cours :
            return

        if not self.inv.depenser_des(1) :  # pas de dé pour faire le tirage
            return

        cible_x, cible_y = self.tirage_en_cours["cible"]
        dir_entree = self.tirage_en_cours["dir_entree"]

        pieces = self.pioche_pieces.tirage_3_pieces(self.grille, cible_x, cible_y, dir_entree)
        
        if not pieces :
            return

        self.tirage_en_cours["pieces"] = pieces
        self.tirage_en_cours["index"] = 0



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
    



    ##### FONCTIONS AUXILIAIRES

    def _direction_vect (self, dx : int, dy : int) :
        correspondances = {
            (0, -1): "N",
            (0, 1): "S",
            (1, 0): "E",
            (-1, 0): "O",
        }
        return correspondances[(dx, dy)]

    def _verifier_conditions_fin(self) -> None :
        if self.inv.pas <= 0 :
            self.state = "game_over"
            return 
        if self.joueur.position == self.grille.sortie :
            self.state = "victoire"
            return 
        

