# point d'entrée du programme 
# boucle principale pygame

import pygame
import sys
from src.Game import Game
from ui.input_handler import InputHandler
from src.AutreObjet import Pomme, Banane, Gateau, Sandwich, Repas, Coffre, Casier, EndroitCreuser
from ui.renderer import render_grille, render_hud, render_piece


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
    return (new_x,new_y)


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
            running = False
            break

        # EXECUTER LES ACTIONS DEMANDEES
        if 'deplacer' in actions:
            dx, dy = actions['deplacer']
            msg = game.deplacer_joueur({k for k,v in DIRECTIONS.items() if v==(dx,dy)}.pop())
            if "nouvelle pièce" in msg:
                game.state = "tirage" # il y aura l'écran de tirage qui s'affiche à ce moment

        if actions.get('ouvrir'):
            # Exemple : ouvrir un coffre à côté du joueur
            for objet in game.grille.pieces[game.joueur.position[1]][game.joueur.position[0]]:
                if isinstance(objet, (Coffre, Casier)):
                    print(game.ouvrir_coffre(objet))

        if actions.get('creuser'):
            for objet in game.grille.pieces[game.joueur.position[1]][game.joueur.position[0]]:
                if isinstance(objet, EndroitCreuser):
                    print(game.creuser_endroit(objet))

        if actions.get('relancer_tirage') and game.state == "tirage":
            print(game.tirer_nouvelle_piece())
        if actions.get('confirmer') and game.state == "tirage":
            print(game.tirer_nouvelle_piece())

        ecran.fill(COLOR_BG)

        ecran.fill((10, 10, 10))
        render_grille(ecran, game)
        render_hud(ecran, game)
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()

        # quit avant voir la compatibilité des deux prop
        # suite de ce code avec CHATGPT (à voir si c'est compatible)
        
        # HUD simple (compteurs)
        # 
        # mit en commentaire pr l'instant methode plus facile   


#        inv = game.joueur.inventaire
#        hud_text = f"Pas: {inv.pas}   Gemmes: {inv.gemmes}   Clés: {inv.cles}   Dés: {inv.des}"
#        txt = police.render(hud_text, True, COLOR_TEXT)
#        ecran.blit(txt, (MARGE, (HUD_H - txt.get_height()) // 2))

        # Grille (cases)
#        for y in range(game.grille.hauteur):
#            for x in range(game.grille.largeur):
#                sx, sy = coords_to_px(x, y)
#               pygame.draw.rect(
#                    ecran, COLOR_CELL,
#                    pygame.Rect(sx, sy, TAILLE_CELLULE, TAILLE_CELLULE),
#                    border_radius=6
#                )
#                # (Option) dessiner le quadrillage
#                pygame.draw.rect(
#                    ecran, COLOR_GRID,
#                    pygame.Rect(sx, sy, TAILLE_CELLULE, TAILLE_CELLULE),
#                    width=1,
#                   border_radius=6
#                )
#
        # Joueur (cercle au centre de la case)
#        px, py = game.joueur.position  # source de vérité unique :contentReference[oaicite:4]{index=4}
#        cx = MARGE + px * TAILLE_CELLULE + TAILLE_CELLULE // 2
#        cy = HUD_H + MARGE + py * TAILLE_CELLULE + TAILLE_CELLULE // 2
#        pygame.draw.circle(ecran, COLOR_PLAYER, (cx, cy), TAILLE_CELLULE // 4)
        
        # Flip
#        pygame.display.flip()
#        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()