from __future__ import annotations
# ui/renderer.py

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Game import Game

import os
import pygame

CELL = 64  # taille d'une case de la grille
OFFSET_X = 20
OFFSET_Y = 120


class Renderer:
    def __init__(self) -> None:
        pygame.font.init()
        self.font_title = pygame.font.SysFont("Arial", 22, bold=True)
        self.font = pygame.font.SysFont("Arial", 18)
        self.small = pygame.font.SysFont("Arial", 14)

        # cache d'images pour ne pas recharger à chaque frame
        self.images_cache: dict[tuple[str, int], pygame.Surface] = {}
        # dossier où tu as mis tes images
        self.dir_images = os.path.join("assets", "images_pieces")

    # ----------------------------------------------------------
    # point d'entrée
    # ----------------------------------------------------------
    def render(self, ecran: pygame.Surface, game: "Game") -> None:
        # fond global
        ecran.fill((10, 10, 15))

        # HUD en haut
        self.render_hud(ecran, game)

        # grille + joueur
        self.render_grille(ecran, game)

        # écrans en overlay selon l'état
        if game.state == "tirage":
            self.render_ecran_tirage(ecran, game)
        elif game.state == "shop":
            self.render_shop(ecran, game)
        elif game.state == "game_over":
            self.render_game_over(ecran)
        elif game.state == "victoire":
            self.render_victoire(ecran)

    # ----------------------------------------------------------
    # HUD : ressources + piece actuelle
    # ----------------------------------------------------------
    def render_hud(self, ecran: pygame.Surface, game: "Game") -> None:
        inv = game.inv
        x, y = game.joueur.position
        piece = game.grille.get_piece(x, y)

        # fond du HUD
        pygame.draw.rect(ecran, (25, 25, 35), (0, 0, ecran.get_width(), 110))

        # titre
        titre = self.font_title.render("Blue Prince (version POO)", True, (240, 240, 240))
        ecran.blit(titre, (15, 8))

        # inventaire de base
        txt = (
            f"Pas: {inv.pas}   Or: {inv.piecesOr}   Gemmes: {inv.gemmes}   "
            f"Clés: {inv.cles}   Dés: {inv.des}"
        )
        surf = self.font.render(txt, True, (230, 230, 230))
        ecran.blit(surf, (15, 40))

        # objets permanents
        y_perm = 65
        if inv.noms_objets_permanents:
            txt_perm = "Objets permanents: " + ", ".join(sorted(inv.noms_objets_permanents))
        else:
            txt_perm = "Objets permanents: (aucun)"
        ecran.blit(self.small.render(txt_perm, True, (200, 200, 200)), (15, y_perm))

        # autres objets (pomme, etc.)
        y_autres = y_perm + 18
        if inv.autres_objets:
            noms = [o.nom for o in inv.autres_objets]
            txt_autres = "Objets: " + ", ".join(noms)
        else:
            txt_autres = "Objets: (aucun)"
        ecran.blit(self.small.render(txt_autres, True, (200, 200, 200)), (15, y_autres))

        # pièce actuelle
        if piece is not None:
            nom_piece = piece.nom
            txt_piece = f"Pièce actuelle : {nom_piece}  (x={x}, y={y})"
        else:
            txt_piece = f"Aucune pièce (x={x}, y={y})"
        ecran.blit(self.small.render(txt_piece, True, (180, 220, 255)), (400, 40))

        # état du jeu
        ecran.blit(self.small.render(f"État: {game.state}", True, (240, 180, 120)), (400, 60))

    # ----------------------------------------------------------
    # rendu principal de la grille
    # ----------------------------------------------------------
    def render_grille(self, ecran: pygame.Surface, game: "Game") -> None:
        grille = game.grille
        sortie_x, sortie_y = grille.sortie 

        for gy in range(grille.hauteur):
            for gx in range(grille.largeur):
                px = OFFSET_X + gx * CELL
                py = OFFSET_Y + gy * CELL

                # fond de case
                pygame.draw.rect(ecran, (25, 28, 45), (px, py, CELL, CELL))
                pygame.draw.rect(ecran, (50, 50, 70), (px, py, CELL, CELL), 1)

                piece = grille.get_piece(gx, gy)

                if gx == sortie_x and gy == sortie_y:
                    self._render_antechamber(ecran, px, py)

                if piece is not None:
                    self._render_piece_image(ecran, piece, px, py)
                # portes par-dessus
                portes_case = grille.dict_portes(gx, gy)
                self._render_portes_case(ecran, px, py, CELL, portes_case)

        # dessiner le joueur par-dessus tout
        jx, jy = game.joueur.position
        jpx = OFFSET_X + jx * CELL + CELL // 2
        jpy = OFFSET_Y + jy * CELL + CELL // 2
        pygame.draw.circle(ecran, (245, 245, 245), (jpx, jpy), CELL // 3)

    def _render_antechamber(self, ecran: pygame.Surface, px: int, py: int) -> None:
        """
        Dessine l'antichambre, même si la grille n'a pas encore de pièce ici.
        """
        filename = "Antechamber.png"
        path = os.path.join(self.dir_images, filename)

        if os.path.exists(path):
            key = (filename, CELL)
            if key not in self.images_cache:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.smoothscale(img, (CELL, CELL))
                self.images_cache[key] = img
            ecran.blit(self.images_cache[key], (px, py))
        else:
            # fallback si jamais le fichier n'existe pas
            pygame.draw.rect(ecran, (180, 150, 60), (px + 2, py + 2, CELL - 4, CELL - 4))
            ecran.blit(self.small.render("ANTICH", True, (0, 0, 0)), (px + 4, py + 4))



    # ----------------------------------------------------------
    # dessine UNE pièce (image ou fallback)
    # ----------------------------------------------------------
    def _render_piece_image(self, ecran: pygame.Surface, piece, px: int, py: int) -> None:
        filename = piece.nom.replace(" ", "_") + ".png"
        path = os.path.join(self.dir_images, filename)

        if os.path.exists(path):
            key = (filename, CELL)
            if key not in self.images_cache:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.smoothscale(img, (CELL, CELL))
                self.images_cache[key] = img
            ecran.blit(self.images_cache[key], (px, py))
        else:
            # fallback si pas d’image
            pygame.draw.rect(ecran, (210, 210, 210), (px + 2, py + 2, CELL - 4, CELL - 4))
            short = piece.nom[:12]
            ecran.blit(self.small.render(short, True, (0, 0, 0)), (px + 4, py + 4))

    # ----------------------------------------------------------
    # rendu des portes d'une case
    # portes: dict[str, Porte]
    # ----------------------------------------------------------
    def _render_portes_case(self, ecran, px, py, cell, portes: dict) -> None:
        # épaisseur
        th = 5
        for d, porte in portes.items():
            # couleur selon état
            if porte.ouverte:
                col = (0, 220, 0)  # vert
            else:
                if porte.niveau == 0:
                    col = (240, 240, 0)   # jaune
                elif porte.niveau == 1:
                    col = (255, 140, 0)   # orange
                else:
                    col = (220, 0, 0)     # rouge

            if d == "N":
                pygame.draw.rect(ecran, col, (px + 8, py, cell - 16, th))
                if not porte.ouverte and porte.niveau > 0:
                    txt = self.small.render(str(porte.niveau), True, (255, 255, 255))
                    ecran.blit(txt, (px + cell // 2 - 4, py + 2))
            elif d == "S":
                pygame.draw.rect(ecran, col, (px + 8, py + cell - th, cell - 16, th))
                if not porte.ouverte and porte.niveau > 0:
                    txt = self.small.render(str(porte.niveau), True, (255, 255, 255))
                    ecran.blit(txt, (px + cell // 2 - 4, py + cell - th - 12))
            elif d == "E":
                pygame.draw.rect(ecran, col, (px + cell - th, py + 8, th, cell - 16))
                if not porte.ouverte and porte.niveau > 0:
                    txt = self.small.render(str(porte.niveau), True, (255, 255, 255))
                    ecran.blit(txt, (px + cell - th - 2, py + cell // 2 - 6))
            elif d == "O":
                pygame.draw.rect(ecran, col, (px, py + 8, th, cell - 16))
                if not porte.ouverte and porte.niveau > 0:
                    txt = self.small.render(str(porte.niveau), True, (255, 255, 255))
                    ecran.blit(txt, (px + 2, py + cell // 2 - 6))

    # ----------------------------------------------------------
    # écran de tirage (state == "tirage")
    # ----------------------------------------------------------
    def render_ecran_tirage(self, ecran: pygame.Surface, game: "Game") -> None:
        data = game.tirage_en_cours
        # sécurité
        if not data:
            return

        pieces = data["pieces"]
        index = data["index"]

        # overlay sombre
        surf = pygame.Surface(ecran.get_size(), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 160))
        ecran.blit(surf, (0, 0))

        w, h = ecran.get_size()
        center_y = h // 2
        center_x = w // 2

        # on dessine les 3 choix
        spacing = 200
        base_x = center_x - spacing
        for i, piece in enumerate(pieces):
            px = base_x + i * spacing
            py = center_y - 100
            rect = pygame.Rect(px, py, 150, 150)

            # fond
            col = (90, 90, 120) if i != index else (160, 160, 220)
            pygame.draw.rect(ecran, col, rect, border_radius=8)
            pygame.draw.rect(ecran, (255, 255, 255), rect, 2, border_radius=8)

            # nom
            ecran.blit(self.font.render(piece.nom, True, (10, 10, 10)), (px + 8, py + 8))

            # coût gemmes
            if getattr(piece, "cout_gemmes", 0) > 0:
                cg = piece.cout_gemmes
                ecran.blit(self.small.render(f"Coût: {cg} gemme(s)", True, (0, 0, 0)), (px + 8, py + 35))

        # aide
        aide = self.small.render("← / → pour choisir   Entrée pour valider   Espace pour relancer (si dé)", True, (255, 255, 255))
        ecran.blit(aide, (w // 2 - aide.get_width() // 2, center_y + 90))

    # ----------------------------------------------------------
    # écran de shop
    # ----------------------------------------------------------
    def render_shop(self, ecran: pygame.Surface, game: "Game") -> None:
        data = game.contexte_achat
        if not data:
            return
        offres = data.get("offres", [])

        surf = pygame.Surface(ecran.get_size(), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 160))
        ecran.blit(surf, (0, 0))

        w, h = ecran.get_size()
        box = pygame.Rect(w // 2 - 200, h // 2 - 150, 400, 300)
        pygame.draw.rect(ecran, (40, 40, 60), box, border_radius=10)
        pygame.draw.rect(ecran, (240, 240, 240), box, 2, border_radius=10)

        ecran.blit(self.font.render("Magasin", True, (255, 255, 255)), (box.x + 20, box.y + 15))
        ecran.blit(self.small.render("(O) pour acheter, ESC pour sortir", True, (220, 220, 220)), (box.x + 20, box.y + 45))

        y = box.y + 80
        for label, prix, code in offres:
            ligne = f"{label} - {prix} or"
            ecran.blit(self.font.render(ligne, True, (230, 230, 230)), (box.x + 20, y))
            y += 35

    # ----------------------------------------------------------
    # écrans de fin
    # ----------------------------------------------------------
    def render_game_over(self, ecran: pygame.Surface) -> None:
        w, h = ecran.get_size()
        txt = self.font_title.render("GAME OVER", True, (255, 50, 50))
        ecran.blit(txt, (w // 2 - txt.get_width() // 2, h // 2 - txt.get_height() // 2))

    def render_victoire(self, ecran: pygame.Surface) -> None:
        w, h = ecran.get_size()
        txt = self.font_title.render("VICTOIRE !", True, (80, 255, 120))
        ecran.blit(txt, (w // 2 - txt.get_width() // 2, h // 2 - txt.get_height() // 2))
