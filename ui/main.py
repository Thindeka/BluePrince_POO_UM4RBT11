# point d'entrée du programme 
# boucle principale pygame

import pygame
import sys
from src.Game import Game
from ui.input_handler import InputHandler


# DONNEES AFFICHAGE
TAILLE_CELLULE = 64     # px
MARGE = 20              # px
HUD_H = 50              # px (hauteur du bandeau HUD)
FPS = 60 

# COULEURS (À MODIFIER)
COLOR_BG = (15, 16, 20)
COLOR_GRID = (55, 60, 70)
COLOR_CELL = (26, 28, 35)
COLOR_PLAYER = (220, 220, 255)
COLOR_TEXT = (235, 235, 235)


def coords_to_px (x, y) :
    """"
    donne les coordonnées (x,y) à l'échelle de l'ecran en pixels """
    new_x = MARGE + x * TAILLE_CELLULE
    new_y = HUD_H + MARGE + y * TAILLE_CELLULE
    return (x,y)












def main() :
    pygame.init()
    pygame.display.set_caption('BluePrince')  # caption pour l'écran

    game = Game()

    LARGEUR = MARGE*2 + game.grille.largeur * TAILLE_CELLULE
    HAUTEUR =  HUD_H + MARGE*2 + game.grille.hauteur * TAILLE_CELLULE
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))  # (largeur, hauteur)

    # horloge 
    clock = pygame.time.Clock()

    # police
    police = pygame.font.SysFont(None, 20)

    # input handler
    input_handler = InputHandler()



    # --------------- BOUCLE DE JEU ---------------

    running = True

    while running :
        
        actions = input_handler.actions()

        # SORTIE DU JEU
        if input_handler.get_quit :  
            runnig = False
            break

        # EXECUTER LES ACTIONS DEMANDEES
        if 'deplacement' in actions :
            dx, dy = actions['deplacement']
            deplacement, ouverture_porte, pas_consommes = game.grille.deplacer_joueur(game.joueur, game.joueur.inventaire, dx, dy)

            if ouverture_porte :
                game.state = "tirage" # il y aura l'écran de tirage qui s'affiche à ce moment

        if actions.get('ouvrir') : pass    # à compléter
        if actions.get('creuser') : pass    # à compléter
        if actions.get('relancer_tirage') and game.state == "tirage" : pass    # à compléter
        if actions.get('confirmer') and game.state == "tirage" : pass    # à compléter


        ecran.fill(COLOR_BG)

        # suite de ce code avec CHATGPT (à voir si c'est compatible)

        # HUD simple (compteurs)  
        inv = game.joueur.inventaire
        hud_text = f"Pas: {inv.pas}   Gemmes: {inv.gemmes}   Clés: {inv.cles}   Dés: {inv.des}"
        txt = police.render(hud_text, True, COLOR_TEXT)
        ecran.blit(txt, (MARGE, (HUD_H - txt.get_height()) // 2))

        # Grille (cases)
        for y in range(game.grille.hauteur):
            for x in range(game.grille.largeur):
                sx, sy = coords_to_px(x, y)
                pygame.draw.rect(
                    ecran, COLOR_CELL,
                    pygame.Rect(sx, sy, TAILLE_CELLULE, TAILLE_CELLULE),
                    border_radius=6
                )
                # (Option) dessiner le quadrillage
                pygame.draw.rect(
                    ecran, COLOR_GRID,
                    pygame.Rect(sx, sy, TAILLE_CELLULE, TAILLE_CELLULE),
                    width=1,
                    border_radius=6
                )

        # Joueur (cercle au centre de la case)
        px, py = game.joueur.position  # source de vérité unique :contentReference[oaicite:4]{index=4}
        cx = MARGE + px * TAILLE_CELLULE + TAILLE_CELLULE // 2
        cy = HUD_H + MARGE + py * TAILLE_CELLULE + TAILLE_CELLULE // 2
        pygame.draw.circle(ecran, COLOR_PLAYER, (cx, cy), TAILLE_CELLULE // 4)
        
        # Flip
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()