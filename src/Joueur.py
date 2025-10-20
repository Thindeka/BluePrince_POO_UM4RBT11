class Joueur:
    """ Représente le joueur ou la joueuse """
    
    def __init__(self):
        self.inventaire = Inventaire()
        self.position = (0, 0)  # Position initiale dans la grille (peut être modifiée selon le jeu)
    
    def deplacer(self, direction, grille):
        """ Déplace le joueur dans la direction donnée et met à jour son inventaire """
        x, y = self.position
        dx, dy = DIRECTIONS[direction]
        new_x, new_y = x + dx, y + dy
        
        if grille.deplacement_permis(new_x, new_y):
            self.position = new_x, new_y
            self.inventaire.utiliser_pas(1)  # Consomme 1 pas par déplacement
            return True
        return False
    
    def ramasser_objet(self, objet):
        """ Ramasse un objet et applique ses effets """
        objet.appliquer(self.inventaire)
