# fonctions d'affichage
from __future__ import annotations
import pygame
import os 

from typing import TYPE_CHECKING


if TYPE_CHECKING :
    from src.Game import Game
    from src.Piece2 import Piece2


# Valeurs reprises du main
TAILLE_CELLULE = 64
MARGE = 20
HUD_H = 50
COLOR_CELL = (26, 28, 35)
COLOR_JOUEUR = (220, 220, 255)



class Renderer :
    
    def __init__(self) -> None:
        self.petite_police = pygame.font.SysFont(None, 20)
        self.moyenne_police = pygame.font.SysFont(None, 25)
        self.images_pieces = {}  # nom_piece -> pygame.Surface
        self.load_images()
    
    def load_images(self):
        folder = "assets/images_pieces"
        for filename in os.listdir(folder):
            if filename.endswith((".png", ".jpg")):
                name = os.path.splitext(filename)[0]  # "Entrance", "Antechamber", etc.
                path = os.path.join(folder, filename)
                self.images_pieces[name] = pygame.image.load(path).convert_alpha()

    def render (self, ecran, game :'Game') :
        ecran.fill((0,0,0))
        self.render_grille(ecran, game)   # afficher grille
        self.render_joueur(ecran, game)  # afficher joueur
        self.render_hud(ecran, game)  # afficher hud

        if game.state == "tirage" and game.tirage_en_cours :
            self.render_ecran_tirage(ecran, game)

        if game.state == "game_over" :
            self.render_texte_centre(ecran, "GAME OVER", (200, 50, 50))
        elif game.state == "victoire" :
            self.render_texte_centre(ecran, "VICTOIRE", (50, 200, 50))


    def render_ecran_tirage(self, ecran : pygame.Surface, game : 'Game'):
        
        data = game.tirage_en_cours

        if not data :
            return 
        
        pieces = data["pieces"]
        index = data["index"]

        w, h = ecran.get_size()

        # fond semi-transparent
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        ecran.blit(overlay, (0, 0))

        card_w = 180
        card_h = 120
        gap = 20
        total_w = len(pieces) * card_w + (len(pieces) - 1) * gap
        start_x = (w - total_w) // 2
        y = h // 2 - card_h // 2

        for i, piece in enumerate(pieces):
            x = start_x + i * (card_w + gap)
            # cadre
            color = (255, 255, 255)
            if i == index:
                color = (255, 220, 0)
            pygame.draw.rect(ecran, color, (x, y, card_w, card_h), width=3)

            # nom
            name_surf = self.petite_police.render(piece.nom, True, (255, 255, 255))
            ecran.blit(name_surf, (x + 10, y + 10))

            # coût
            cost_surf = self.petite_police.render(f"{piece.cout_gemmes} gemme(s)", True, (220, 220, 220))
            ecran.blit(cost_surf, (x + 10, y + 35))

            # couleur
            col_surf = self.petite_police.render(piece.couleur.name, True, (200, 200, 200))
            ecran.blit(col_surf, (x + 10, y + 60))

        # aide
        help_surf = self.petite_police.render("←/→ pour choisir, Entrée pour valider, Espace pour relancer", True, (255, 255, 255))
        ecran.blit(help_surf, (w // 2 - help_surf.get_width() // 2, y + card_h + 15))


    def render_grille(self, ecran: pygame.Surface, game: 'Game') -> None:
        
        grille = game.grille

        for y in range(grille.hauteur):
            for x in range(grille.largeur):
                px, py = self.coords_to_px(x, y)
       
                # fond de case
                pygame.draw.rect(ecran, (30, 30, 50), (px, py, TAILLE_CELLULE   , TAILLE_CELLULE))

                # si pièce présente, on la dessine
                piece = grille.get_piece(x, y)
                if piece is not None:
                    img = self.images_pieces.get(piece.nom)
                    if img:
                        ecran.blit(pygame.transform.scale(img, (TAILLE_CELLULE, TAILLE_CELLULE)), (px, py))
                    else:
                        # couleur selon la couleur de la pièce
                        col = self._color_for_piece(piece)
                        pygame.draw.rect(ecran, col, (px + 4, py + 4, TAILLE_CELLULE - 8, TAILLE_CELLULE - 8))
                        # nom (petit)
                        txt = self.petite_police.render(piece.nom[:10], True, (0, 0, 0))
                        ecran.blit(txt, (px + 6, py + 6))

                # contour
                pygame.draw.rect(ecran, (60, 60, 90), (px, py, TAILLE_CELLULE, TAILLE_CELLULE), width=1)


    def render_hud(self, ecran : pygame.Surface, game : 'Game') -> None :
        """Affiche les infos du joueur en haut """
        inv = game.inv
        pygame.draw.rect(ecran, (10, 10, 20), (0, 0, ecran.get_width(), HUD_H))
        # texte
        txt = self.petite_police.render(
            f"Pas: {inv.pas}  |  Gemmes: {inv.gemmes}  |  Or: {inv.piecesOr}  |  Clés: {inv.cles}  |  Dés: {inv.des}",
            True,
            (230, 230, 230)
        )
        ecran.blit(txt, (MARGE, 20))

        # état
        state_txt = self.petite_police.render(f"État: {game.state}", True, (180, 180, 180))
        ecran.blit(state_txt, (MARGE, 48))


    def render_porte (self, ecran : pygame.Surface, game : 'Game') -> None :
        # dessine les portes ouvertes 

        grille = game.grille

        for (x, y), dico in grille.portes.items() :
            
            x_bis, y_bis = self.coords_to_px(x,y)
            
            for d, porte in dico.items():
                if not porte.ouverte:
                    continue
                if d == "N":
                    pygame.draw.line(ecran, (200, 200, 0),
                                     (x_bis + TAILLE_CELLULE // 2, y_bis),
                                     (x_bis + TAILLE_CELLULE // 2, y_bis - 8), 3)
                elif d == "S":
                    pygame.draw.line(ecran, (200, 200, 0),
                                     (x_bis + TAILLE_CELLULE // 2, y_bis + TAILLE_CELLULE),
                                     (x_bis + TAILLE_CELLULE // 2, y_bis + TAILLE_CELLULE + 8), 3)
                elif d == "E":
                    pygame.draw.line(ecran, (200, 200, 0),
                                     (x_bis + TAILLE_CELLULE, y_bis + TAILLE_CELLULE // 2),
                                     (x_bis + TAILLE_CELLULE + 8, y_bis + TAILLE_CELLULE // 2), 3)
                elif d == "O":
                    pygame.draw.line(ecran, (200, 200, 0),
                                     (x_bis, y_bis + TAILLE_CELLULE // 2),
                                     (x_bis - 8, y_bis + TAILLE_CELLULE // 2), 3)
                    

    def render_joueur(self, ecran : pygame.Surface, game : 'Game') -> None :
        # dessine le joueur
        x, y = game.joueur.position
        px = MARGE + x * TAILLE_CELLULE + TAILLE_CELLULE // 2
        py = HUD_H + MARGE + y * TAILLE_CELLULE + TAILLE_CELLULE // 2
        pygame.draw.circle(ecran, (240, 240, 240), (px, py), TAILLE_CELLULE // 3)

        piece = game.grille.get_piece(x, y)
        if piece:
            if piece.nom == "Antechamber":  # end game
                game.state = "victoire"
            elif piece.nom == "Entrance":   # start game
                pass
    
    ######### FOCNTIONS AUXILIAIRES

    def render_piece(ecran, piece, position):
        """(Optionnel) Affiche une pièce individuelle — utile pour debug."""
        x, y = position
        sx, sy = coords_to_px(x, y)
        rect = pygame.Rect(sx, sy, TAILLE_CELLULE, TAILLE_CELLULE)
        pygame.draw.rect(ecran, (100, 100, 255), rect, 2)

    def _color_for_piece (self, piece : Piece2) -> tuple[int, int, int] :
        
        c = piece.couleur

        if c == "JAUNE" : 
            return (230, 220, 120)
        
        if c == "VERT" : 
            return (100, 200, 120)
        
        if c == "VIOLET" : 
            return (170, 120, 200)
        
        if c == "ORANGE" : 
            return (230, 160, 80)
        
        if c == "ROUGE" : 
            return (230, 80, 80)

        if c == "BLEU" : 
            return (120, 150, 255)
        
        return (200, 200, 200)


    def render_texte_centre (self, ecran: pygame.Surface, text: str, color: tuple[int, int, int]) -> None: 
        surf = self.moyenne_police.render(text, True, color)
        w, h = ecran.get_size()
        ecran.blit(surf, (w // 2 - surf.get_width() // 2, h // 2 - surf.get_height() // 2))



    def coords_to_px(self, x, y):
        return (
            MARGE + x * TAILLE_CELLULE,
            HUD_H + MARGE + y * TAILLE_CELLULE,
        )
