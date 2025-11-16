# point d'entrée du programme 
# boucle principale pygame

import pygame
import sys
from src.Game import Game
from ui.input_handler import InputHandler
from src.AutreObjet import Pomme, Banane, Gateau, Sandwich, Repas, Coffre, Casier, EndroitCreuser
from ui.renderer import Renderer

# DONNEES AFFICHAGE
LARGEUR_ECRAN = 900
HAUTEUR_ECRAN = 720
FPS = 60 



def main() :
    """
    Fonction principale du jeu.
    Initialise pygame, crée les objets principaux et lance la boucle de jeu.

    Paramètres
    ----------
    None

    Returns
    -------
    None
    """
    pygame.init()
    ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))  
    pygame.display.set_caption('BluePrince')  # caption pour l'écran

    clock = pygame.time.Clock()
    game = Game()
    input_handler = InputHandler()
    renderer = Renderer()
    

    # --------------- BOUCLE DE JEU ---------------

    running = True

    while running :
        
        actions = input_handler.actions()

        # SORTIE DU JEU
        if input_handler.quit_requested :  
            running = False
            break
        
        # GAME OVER 
        if game.state == "game_over":
            if 'nav_game_over' in actions:
                game.handle_navigation_game_over(actions['nav_game_over'])
            if actions.get('confirmer'):
                game.handle_confirmation_game_over()
        else :
            
            
            # EXECUTER LES ACTIONS DEMANDEES

            if game.state == "exploration" :

                if "deplacer" in actions :
                    dx, dy = actions["deplacer"]
                    game.handle_deplacement(dx, dy)

                if "ouvrir" in actions:
                    game.handle_ouvrir_sur_piece_courante()
                    
                if "creuser" in actions :
                    game.handle_ouvrir_sur_piece_courante()

            
            if game.state == "tirage" :
                if "deplacer" in actions :
                    dx, dy = actions["deplacer"]
                    
                    if dx == -1 :  # gauche
                        game.handle_choix_tirage(-1)

                    if dx == 1 :  # droite
                        game.handle_choix_tirage(1)

                if 'confirmer' in actions :
                    game.handle_confirmation_tirage()

                if 'relancer_tirage' in actions :
                    game.handle_re_tirage()

                if 'annuler' in actions :
                    pass
            

            elif game.state == "achat":
                

                # ENTER : acheter l'offre sélectionnée
                if "confirmer" in actions or "ouvrir" in actions:
                    game.handle_confirmation_magasin()

                # ESC : quitter le magasin
                if "annuler" in actions:
                    # on revient à l'exploration
                    game.handle_quitter_magasin()
                elif "deplacer" in actions:
                    dx, dy = actions["deplacer"]
                    if dx != 0 or dy !=0:
                        game.handle_navigation_magasin(dx)

        # affichage
        renderer.render(ecran, game)
        pygame.display.flip()  # on eneregistre les changememts
        clock.tick(FPS)   
    
    pygame.quit()


if __name__ == "__main__":
    main()