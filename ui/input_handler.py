# gestion des touches
# "ce qui écoute le clavier"

import pygame

# correspondance touche avec les vecteurs de deplacement
TOUCHE_DEPLACEMENT = {   # enlever fleches si nécéssaire
    pygame.K_UP:    (0, -1),
    pygame.K_DOWN:  (0,  1),
    pygame.K_LEFT:  (-1, 0),
    pygame.K_RIGHT: (1,  0),
    pygame.K_z:     (0, -1),
    pygame.K_s:     (0,  1),
    pygame.K_q:     (-1, 0),
    pygame.K_d:     (1,  0),
}

class InputHandler :
    """
    Gestion des touches
    Pas de logique de jeu
    On renvoie qu ece que le joueur veut faire à ce laps de temps
    """

    def __init__(self) -> None:
        self._quit = False
    

    @property
    def quit_requested(self) -> bool :
        """ getter self._quit """
        return self._quit
    

    def actions (self) -> dict :
        """
        Retour :
        {
        'deplacer': (dx, dy),           # déplacement validé 
        'ouvrir': True,                 
        'creuser': True,                
        'confirmer': True,              # ENTER (valider un choix)
        'relancer_tirage': True,        # SPACE (relancer un tirage)
        'annuler': True,                # ESC
        }
        mise à vide pour le laps suivant

        """
        intentions = {}

        for event in pygame.event.get() :
            
            if event.type == pygame.QUIT :  # on ferme la fenetre
                self._quit = True

            
            elif event.type == pygame.KEYDOWN :  # touche a été pressée
                touche = event.key

                if touche == pygame.K_ESCAPE:  # sortir
                    intentions['annuler'] = True

                elif touche in TOUCHE_DEPLACEMENT :  # deplacement
                    intentions['deplacer'] = TOUCHE_DEPLACEMENT[touche]

                elif touche in (pygame.K_RETURN, pygame.K_KP_ENTER) :  # confirmation (ENTER)
                    intentions['confirmer'] = True

                elif touche == pygame.K_SPACE :  # re-tirage (ESPACE)
                    intentions['relancer_tirage'] = True

                # AUTRES ACTIONS 
                elif touche == pygame.K_o:   # ouvrir ('O')
                    intentions['ouvrir'] = True

                elif touche == pygame.K_c:   # creuser ('C')
                    intentions['creuser'] = True

                

        return intentions
        

