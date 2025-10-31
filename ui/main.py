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


        
        # EXECUTER LES ACTIONS DEMANDEES

        if game.state == "exploration" :
            if "deplacer" in actions :
                dx, dy = actions["deplacer"]
                game.handle_deplacement(dx, dy)

        
        elif game.state == "tirage" :
            if "deplacer" in actions :
                dx, dy = actions["deplacer"]
                
                if dx == -1 :  # gauche
                    game.handle_choix_tirage(-1)

                if dx == 1 :  # droite
                    game.handle_choix_tirage(1)

            if 'confirmer' in actions :
                game.handle_confirmation_tirage()

            if 'relancer_tirage' in actions :
                game.handle_confirmation_tirage()

            if 'annuler' in actions :
                pass
            
            # AJOUTER ACTION ACHAT

        # affichage
        renderer.render(ecran, game)
        pygame.display.flip()  # on eneregistre les changememts

        clock.tick(FPS)   
    
    pygame.quit()


if __name__ == "__main__":
    main()