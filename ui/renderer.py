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
ORIENTATION = {
    "couloir_ns": "NS",
    "couloir_eo": "EO",
    "croix": "NSEO",
    "carre": "NSEO",

    "cul_n": "N",
    "cul_s": "S",
    "cul_e": "E",
    "cul_o": "O",

    "angle_ne": "NE",
    "angle_es": "ES",
    "angle_so": "SO",
    "angle_on": "ON",

    "t_nes": "NES",
    "t_eso": "ESO",
    "t_son": "SON",
    "t_one": "ONE",
}



class Renderer :
    """
    Classe Renderer pour gérer l'affichage du jeu.
    
    Attributs
    ---------
    font_title : pygame.font.Font
        Police pour les titres.
    font : pygame.font.Font
        Police pour le texte standard.
    small : pygame.font.Font
        Police pour le texte petit.
    images_cache : dict[tuple[str, int], pygame.Surface]
        Cache d'images pour éviter de recharger les images à chaque frame.
    dir_images : str
        Répertoire contenant les images des pièces.
    
    Méthodes
    -------
    render -> None
        Point d'entrée pour dessiner l'écran de jeu.
    render_hud -> None
        Dessine le HUD en haut de l'écran.
    render_grille -> None 
        Dessine la grille de jeu et les éléments.
    render_ecran_tirage -> None  
        Affiche l'écran de tirage des pièces.
    render_magasin -> None 
        Affiche l'interface du magasin.
    render_game_over -> None  
        Affiche l'écran de fin de jeu.
    render_victoire -> None  
        affiche l'écran de victoire.
    """

    def __init__(self) -> None:
        pygame.font.init()
        self.font_title = pygame.font.SysFont("Arial", 22, bold=True)
        self.font = pygame.font.SysFont("Arial", 18)
        self.small = pygame.font.SysFont("Arial", 14)

        # cache d'images pour ne pas recharger à chaque frame
        self.images_cache: dict[tuple[str, int], pygame.Surface] = {}
        self.dir_images = os.path.join("assets", "images_pieces2")




    def render(self, ecran: pygame.Surface, game: "Game") -> None:
        """
        Point d'entrée pour dessiner l'écran de jeu.

        Paramètres
        ----------
        ecran : pygame.Surface
            Surface pygame où dessiner le jeu.
        game : Game
            Instance du jeu

        Returns
        -------
        None
        """

        # fond global
        ecran.fill((10, 10, 15))

        # HUD en haut
        self.render_hud(ecran, game)

        # grille + joueur
        self.render_grille(ecran, game)

        # écrans en overlay selon l'état
        if game.state == "tirage":
            self.render_ecran_tirage(ecran, game)
        elif game.state == "achat":
            self.render_magasin(ecran, game)
        elif game.state == "game_over":
            self.render_game_over(ecran, game)
        elif game.state == "victoire":
            self.render_victoire(ecran)



   
    def render_hud(self, ecran: pygame.Surface, game: "Game") -> None:
        """
        Affiche le HUD en haut : 
            - stats de base (pas/or/gemmes/clés/dés)
            - objets permanents (liste de noms) si présente
            - autres objets consommables (listes d'objets avec.nom) si présente
            - pièce actuelle + état du jeu 
            - message temporaire game.last_message (si défini)
        On utilise getattr pour être tolérant si l'inventaire n'expose pas exactement les mêmes attributs
        
        Paramètres
        ----------
        ecran : pygame.Surface
            Surface pygame où dessiner le HUD.
        game : Game
            Instance du jeu.
        
        Returns
        -------
        None
        """

        inv = game.inv
        x, y = game.joueur.position
        piece = game.grille.get_piece(x, y)

        # fond du HUD
        pygame.draw.rect(ecran, (25, 25, 35), (0, 0, ecran.get_width(), 110))

        # titre
        titre = self.font_title.render("Blue Prince", True, (240, 240, 240))
        ecran.blit(titre, (15, 8))

        # inventaire de base
        pas = getattr(inv, "pas", 0)
        pieces_or = getattr(inv, "piecesOr", 0)
        gemmes = getattr(inv, "gemmes", 0)
        cles = getattr(inv, "cles", 0)
        des = getattr(inv, "des", 0)

        txt = (
            f"Pas: {inv.pas}   Or: {inv.piecesOr}   Gemmes: {inv.gemmes}   "
            f"Clés: {inv.cles}   Dés: {inv.des}"
        )
        surf = self.font.render(txt, True, (230, 230, 230))
        ecran.blit(surf, (15, 40))

        # objets permanents
        y_perm = 65
        noms_perm = getattr(inv, "noms_objets_permanents", None)
        if noms_perm:
            if isinstance(noms_perm, (list, tuple)):
                try:
                    noms_display = [n if isinstance(n, str) else n for n in noms_perm]
                    txt_perm = "Objets permanents: " + ", ".join(sorted(noms_display))
                except Exception:
                    txt_perm = "Objets permanents: (erreur affichage)"
            else:
                txt_perm = "Objets permanents: (aucun)"
        else:
            txt_perm = "Objets permanents: (aucun)"
        ecran.blit(self.small.render(txt_perm, True, (200, 200, 200)), (15, y_perm))

        # autres objets (pomme, etc.)
        y_autres = y_perm + 18
        autres = getattr(inv, "autres_objets", None)
        if autres:
            noms = []
            for o in autres:
                nom = getattr(o, "nom", None)
                if nom:
                    noms.append(nom)
                else:
                    try:
                        noms.append(str(o))
                    except Exception:
                        noms.append("<objet>")
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

        # message temporaire  
        if getattr(game, "last_message", ""):  
            ecran.blit(self.small.render(game.last_message, True, (255, 255, 200)), (400, 80))  




    def render_grille(self, ecran: pygame.Surface, game: "Game") -> None:
        """
        Dessine la grille de jeu et les éléments.

        Paramètres
        ----------
        ecran : pygame.Surface
            Surface pygame où dessiner la grille.
        game : Game
            Instance du jeu.

        Returns
        -------
        None
        """

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

                if gx == 2 and gy == 8 :
                    self._render_entrance(ecran, px, py)

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
        pygame.draw.circle(ecran, (245, 245, 245), (jpx, jpy), CELL // 6)




    def _render_entrance(self, ecran: pygame.Surface, px: int, py: int) -> None :
        """
        Dessine l'antichambre, même si la grille n'a pas encore de pièce ici.

        Paramètres
        ----------
        ecran : pygame.Surface
            Surface pygame où dessiner la grille.
        px : int
        py : int
            Représentent les coordonnées pixel (ou écran) calculées à partir des coordonnées grille (gx, gy)

        Returns
        -------
        None
        """
        filename = "Entrance.png"
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
            ecran.blit(self.small.render("ENTRANCE", True, (0, 0, 0)), (px + 4, py + 4))




    def _render_antechamber(self, ecran: pygame.Surface, px: int, py: int) -> None:
        """
        Dessine l'antichambre, même si la grille n'a pas encore de pièce ici.

        Paramètres
        ----------
        ecran : pygame.Surface
            Surface pygame où dessiner la grille.
        px : int
        py : int
            Représentent les coordonnées pixel (ou écran) calculées à partir des coordonnées grille (gx, gy)

        Returns
        -------
        None
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
            ecran.blit(self.small.render("ENTRACNCE", True, (0, 0, 0)), (px + 4, py + 4))




    def _get_piece_image(self, nom_piece: str, size: int) -> pygame.Surface | None :

        filename = nom_piece.replace(" ", "_") + ".png"
        path = os.path.join(self.dir_images, filename)

        if not os.path.exists(path):
            return None

        key = (filename, size)
        if key not in self.images_cache:
            img = pygame.image.load(path).convert_alpha()
            if img.get_width() != size or img.get_height() != size:
                img = pygame.transform.smoothscale(img, (size, size))
            self.images_cache[key] = img
        return self.images_cache[key]
        



    def _orientation_piece(self, piece) -> str:
    
        forme = getattr(piece, "forme", None)
        if forme is None:
            return "NSEO"

        nom_forme = getattr(forme, "nom", "")
        if nom_forme in ORIENTATION :
            return ORIENTATION[nom_forme]

        # fallback 
        portes = getattr(forme, "ens_portes", set()) or set()
        key = "".join(sorted(portes))  

        mapping_par_portes = {
            "N": "N",
            "S": "S",
            "E": "E",
            "O": "O",
            "NS": "NS",
            "EO": "EO",
            "EN": "NE",
            "ES": "ES",
            "NO": "ON",
            "OS": "SO",
            "ENS": "NES",
            "EOS": "ESO",
            "NOS": "SON",
            "ENO": "ONE",
            "ENOS": "NSEO",
        }
        return mapping_par_portes.get(key, "NSEO")
    


 
    def _get_piece_image_oriente(self, piece, size: int) -> pygame.Surface | None:
        nom_base = piece.nom.replace(" ", "_")
        suffix_logique = self._orientation_piece(piece)  
        suffix_fichier = self._map_suffix_to_image(suffix_logique)  

        candidats: list[str] = []
        if suffix_fichier:
            candidats.append(f"{nom_base}_{suffix_fichier}.png")

        if len(suffix_fichier) > 1:
            principaux = {
                "NS": "N",
                "EO": "E",
                "NE": "N",
                "ES": "E",
                "SO": "S",
                "ON": "O",
                "NES": "N",
                "ESO": "E",
                "SON": "S",
                "ONE": "O",
                "NSEO": "N",
            }
            card = principaux.get(suffix_fichier)
            if card:
                candidats.append(f"{nom_base}_{card}.png")

        candidats.append(f"{nom_base}.png")

        filename_choisi = None
        for fname in candidats:
            path = os.path.join(self.dir_images, fname)
            if os.path.exists(path):
                filename_choisi = fname
                break

        if filename_choisi is None:
            return None

        key = (filename_choisi, size)
        if key not in self.images_cache:
            # debug
            print(f"{key}")
            img = pygame.image.load(os.path.join(self.dir_images, filename_choisi)).convert_alpha()
            if img.get_width() != size or img.get_height() != size:
                img = pygame.transform.smoothscale(img, (size, size))
            self.images_cache[key] = img
        return self.images_cache[key]




    def _map_suffix_to_image(self, suffixe : str) -> str :
        return suffixe



    def _render_piece_image(self, ecran: pygame.Surface, piece, px: int, py: int) -> None:
        img = self._get_piece_image_oriente(piece, CELL)
        if img is not None:
            ecran.blit(img, (px, py))
        else:
            # fallback texte
            pygame.draw.rect(ecran, (210, 210, 210), (px + 2, py + 2, CELL - 4, CELL - 4))
            short = piece.nom[:12]
            ecran.blit(self.small.render(short, True, (0, 0, 0)), (px + 4, py + 4))
        


    def _render_portes_case(self, ecran, px, py, cell, portes: dict) -> None:
        """


        Paramètres
        ----------
        ecran : pygame.Surface
            Surface pygame où dessiner la grille.
        px : int
        py : int
            Représentent les coordonnées pixel (ou écran) calculées à partir des coordonnées grille (gx, gy)
        cell : _type_

        portes : dict
        
        Returns
        -------
        None

        """
        # épaisseur
        th = 1
        for d, porte in portes.items():
            # couleur selon état
            if porte.ouverte:
                col = (0, 220, 0)  # vert
        
            if porte.ouverte:
                col = (0, 200, 0)  # vert = ouvert
            else:
                if porte.niveau == 0:
                    col = (128, 128, 128)  # gris = porte niveau 0 pas encore utilisee
                elif porte.niveau == 1:
                    col = (255, 165, 0)  # orange = nécessite clé ou crochetage
                elif porte.niveau == 2:
                    col = (255, 0, 0)  # rouge = verrou ultime

            if d == "N":
                pygame.draw.rect(ecran, col, (px + 8, py, cell - 16, th)) # type: ignore
                if not porte.ouverte and porte.niveau > 0:
                    txt = self.small.render(str(porte.niveau), True, (255, 255, 255))
                    ecran.blit(txt, (px + cell // 2 - 4, py + 2))
            elif d == "S":
                pygame.draw.rect(ecran, col, (px + 8, py + cell - th, cell - 16, th)) # type: ignore
                if not porte.ouverte and porte.niveau > 0:
                    txt = self.small.render(str(porte.niveau), True, (255, 255, 255))
                    ecran.blit(txt, (px + cell // 2 - 4, py + cell - th - 12))
            elif d == "E":
                pygame.draw.rect(ecran, col, (px + cell - th, py + 8, th, cell - 16)) # type: ignore
                if not porte.ouverte and porte.niveau > 0:
                    txt = self.small.render(str(porte.niveau), True, (255, 255, 255))
                    ecran.blit(txt, (px + cell - th - 2, py + cell // 2 - 6))
            elif d == "O":
                pygame.draw.rect(ecran, col, (px, py + 8, th, cell - 16)) # type: ignore
                if not porte.ouverte and porte.niveau > 0:
                    txt = self.small.render(str(porte.niveau), True, (255, 255, 255))
                    ecran.blit(txt, (px + 2, py + cell // 2 - 6))



    def render_ecran_tirage(self, ecran: pygame.Surface, game: "Game") -> None:
        """
        Ecran pop-up du tirage des pièces

        paramètres
        ---------
        ecran : pygame.Surface
            Surface pygame où dessiner la grille.
        game : Game
            Instance du jeu

        Returns
        -------
        None
        """

        data = game.tirage_en_cours
        if not data:
            return

        pieces = data["pieces"]
        index = data["index"]

        grille = game.grille
        grid_right = OFFSET_X + grille.largeur * CELL
        panel_x = grid_right + 20
        panel_y = OFFSET_Y
        panel_w = ecran.get_width() - panel_x - 20
        panel_h = ecran.get_height() - panel_y - 20

        # fond + cadre
        pygame.draw.rect(ecran, (8, 8, 10), (panel_x, panel_y, panel_w, panel_h))
        pygame.draw.rect(ecran, (220, 220, 220), (panel_x, panel_y, panel_w, panel_h), 2)

        # titre
        titre = self.font.render("Choisissez une salle", True, (255, 255, 255))
        ecran.blit(titre, (panel_x + 16, panel_y + 12))

        nb = len(pieces)
        if nb == 0:
            return

        # zone dispo pour les tuiles
        tiles_top = panel_y + 60
        tiles_height = panel_h - 110  # laisse de la place pour l'aide
        spacing = 20

        # largeur max pour chaque colonne
        col_width = (panel_w - spacing * (nb + 1)) // nb
        # taille de l'image carrée
        img_size = min(col_width, tiles_height - 40)  # 40px txt

        for i, piece in enumerate(pieces):
            
            col_x = panel_x + spacing + i * (col_width + spacing)
            img_x = col_x + (col_width - img_size) // 2
            img_y = tiles_top

            # image orientée
            img = self._get_piece_image_oriente(piece, img_size)
            if img is not None:
                # cadre de sélection
                if i == index:
                    pygame.draw.rect(
                        ecran,
                        (200, 200, 80),
                        (img_x - 4, img_y - 4, img_size + 8, img_size + 8),
                        3,
                    )
                ecran.blit(img, (img_x, img_y))
            else:
                # fallback 
                rect = pygame.Rect(img_x, img_y, img_size, img_size)
                if i == index:
                    pygame.draw.rect(ecran, (200, 200, 80), rect, 3)
                pygame.draw.rect(ecran, (180, 180, 180), rect)
                short = piece.nom[:10]
                txt = self.small.render(short, True, (0, 0, 0))
                ecran.blit(
                    txt,
                    (rect.centerx - txt.get_width() // 2,
                     rect.centery - txt.get_height() // 2),
                )

            nom = piece.nom
            txt_nom = self.small.render(nom, True, (220, 220, 255 if i == index else 200))
            txt_x = col_x + (col_width - txt_nom.get_width()) // 2
            txt_y = img_y + img_size + 6
            ecran.blit(txt_nom, (txt_x, txt_y))

            # cout gemmes 
            cg = getattr(piece, "cout_gemmes", 0)
            if cg > 0:
                txt_cg = self.small.render(f"Coût : {cg} gemme(s)", True, (200, 200, 200))
                cg_x = col_x + (col_width - txt_cg.get_width()) // 2
                cg_y = txt_y + txt_nom.get_height() + 2
                ecran.blit(txt_cg, (cg_x, cg_y))
                #####
                debug_y = cg_y + txt_cg.get_height() + 2
                ####
            else :
                debug_y = txt_y + txt_nom.get_height() + 2

        # --- DEBUG ORIENTATION ---
            nom_forme = getattr(piece.forme, "nom", "?")
            ports = "".join(sorted(getattr(piece.forme, "ens_portes", [])))
            txt_debug = self.small.render(f"{nom_forme} ({ports})", True, (180, 180, 180))
            debug_x = col_x + (col_width - txt_debug.get_width()) // 2
            ecran.blit(txt_debug, (debug_x, debug_y))

        aide_txt = "<- / -> pour choisir   Entrée pour valider   Espace pour relancer (si dé)"
        aide = self.small.render(aide_txt, True, (230, 230, 230))
        ecran.blit(aide, (panel_x + 16, panel_y + panel_h - 30))



    def render_magasin(self, ecran: pygame.Surface, game: "Game") -> None:
        """
        Ecran pop-up du magasin (shop)

        paramètres
        ---------
        ecran : pygame.Surface
            Surface pygame où dessiner la grille.
        game : Game
            Instance du jeu

        Returns
        -------
        None
        """

        ctx = game.contexte_achat
        if not ctx:
            return

        inv = game.inv
        offres = ctx["offres"]
        index = ctx.get("index", 0)

        # panneau
        grid_droite = OFFSET_X + game.grille.largeur * CELL

        panneau_x = grid_droite + 20
        panneau_y = OFFSET_Y
        panneau_w = ecran.get_width() - panneau_x - 20
        panneau_h = ecran.get_height() - panneau_y - 20
    
        pygame.draw.rect(ecran, (15, 15, 15), (panneau_x, panneau_y, panneau_w, panneau_h))
        pygame.draw.rect(ecran, (220, 220, 220), (panneau_x, panneau_y, panneau_w, panneau_h), 2)

        # titre
        piece = ctx.get("piece")
        nom_piece = piece.nom if piece else "Magasin"
        nom_piece = nom_piece.lower()


        if "kitchen" in nom_piece:
            titre_txt = "Kitchen"
            sous_titre_txt = "Consommables"
        elif "commissary" in nom_piece:
            titre_txt = "Commissary"
            sous_titre_txt = "Objets Permanents"
        elif "locksmith" in nom_piece:
            titre_txt = "Locksmith"
            sous_titre_txt = "Clés et kits de crochetage"
        else:
            titre_txt = f"Magasin : {nom_piece}"
            sous_titre_txt = "Mag"
    
        titre = self.font.render(f"Magasin : {nom_piece}", True, (255, 255, 255))
        ecran.blit(titre, (panneau_x + 16, panneau_y + 12))
        # sous-titre
        sous_titre = self.small.render(sous_titre_txt, True, (200, 200, 200))
        ecran.blit(sous_titre, (panneau_x + 16, panneau_y + 36))
        
        # ressources du joueur
        info = self.small.render(
            f"",
            True,
            (230, 230, 230),
        )
        ecran.blit(info, (panneau_x + 16, panneau_y + 40))

        # zone des offres
        list_y = panneau_y + 70
        line_h = 34

        for i, off in enumerate(offres):
            # normalisation
            if isinstance(off, dict):
                label = off.get("label", "???")
                prix = off.get("prix", 0)
            else:  # tuple ou liste
                label, prix, _code = off

            # fond 
            rect = pygame.Rect(panneau_x + 12, list_y + i * line_h, panneau_w - 24, line_h - 4)
            if i == index:
                pygame.draw.rect(ecran, (130, 140, 50), rect)
            else:
                pygame.draw.rect(ecran, (40, 40, 40), rect)

            # texte doffre
            txt = self.small.render(f"{label}  -  {prix} or", True, (255, 255, 255))
            ecran.blit(txt, (rect.x + 8, rect.y + 6))

        # aide
        aide = self.small.render(
            "Entrée / O : acheter    Échap : quitter   <- / ->  ou QD : changer d'article",
            True,
            (230, 230, 230),
        )
        ecran.blit(aide, (panneau_x + 16, panneau_y + panneau_h - 30))




    def render_game_over(self, ecran: pygame.Surface, game) -> None:
        """
        Affiche un écran 'Game Over' avec une capsule et le choix Rejouer Oui / Non.
        selection : 0 = Oui, 1 = Non

        paramètres
        ---------
        ecran : pygame.Surface
            Surface pygame où dessiner la grille.
        game : Game
            Instance du jeu
        selection : int (0 par défaut)

        Returns
        -------
        None
        """
        
        w, h = ecran.get_size()
        selec= getattr(game, "game_over_selection", 0)


        # Fond semi-transparent noir
        fond = pygame.Surface((w, h))
        fond.set_alpha(180)
        fond.fill((0, 0, 0))
        ecran.blit(fond, (0, 0))

        # Capsule centrale
        capsule_w, capsule_h = 500, 300
        rect = pygame.Rect(
            (w - capsule_w) // 2,
            (h - capsule_h) // 2,
            capsule_w,
            capsule_h
        )
        pygame.draw.rect(ecran, (30, 30, 30), rect, border_radius=20)
        pygame.draw.rect(ecran, (200, 0, 0), rect, 4, border_radius=20)

        # Titre
        titre = self.font_title.render("GAME OVER", True, (255, 80, 80))
        ecran.blit(titre, (w // 2 - titre.get_width() // 2, rect.y + 40))

        # Message
        texte_msg = getattr(game, "last_message", "") or "Vous ne pouvez plus avancer..."
        msg = self.small.render(texte_msg, True, (255, 200, 200))
        ecran.blit(msg, (w // 2 - msg.get_width() // 2, rect.y + 120))

        # Choix Oui / Non
        options = ["Oui", "Non"]
        y_options = rect.y + 200
        esp = 160  
        x_centre = w // 2

        for i, opt in enumerate(options):
            # position de base
            x = x_centre + (i - 0.5) * esp

            # couleur texte
            col = (255, 255, 255) if i != selec else (255, 200, 0)
            texte = self.font.render(opt, True, col)
            texte_rect = texte.get_rect(center=(int(x), y_options))

            if i == selec :
                pad = 10
                cadre_rect = pygame.Rect(
                    texte_rect.left - pad,
                    texte_rect.top - pad,
                    texte_rect.width + 2 * pad,
                    texte_rect.height + 2 * pad,
                )
                pygame.draw.rect(ecran, (255, 200, 0), cadre_rect, width=3, border_radius=8)

                # flèche à gauche
                fleche = self.font.render("▶", True, (255, 200, 0))
                fleche_rect = fleche.get_rect(midright=(cadre_rect.left - 10, cadre_rect.centery))
                ecran.blit(fleche, fleche_rect)

            ecran.blit(texte, texte_rect)
            


    def render_victoire(self, ecran: pygame.Surface) -> None:
        w, h = ecran.get_size()
        txt = self.font_title.render("VICTOIRE !", True, (80, 255, 120))
        ecran.blit(txt, (w // 2 - txt.get_width() // 2, h // 2 - txt.get_height() // 2))
