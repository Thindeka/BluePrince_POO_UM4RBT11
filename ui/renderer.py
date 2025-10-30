# fonctions d'affichage

import pygame

# Valeurs reprises du main
TAILLE_CELLULE = 64
MARGE = 20
HUD_H = 50
COLOR_CELL = (26, 28, 35)
COLOR_JOUEUR = (220, 220, 255)


def coords_to_px(x, y):
    return (
        MARGE + x * TAILLE_CELLULE,
        HUD_H + MARGE + y * TAILLE_CELLULE,
    )

def render_grille(ecran, game):
    """Affiche les pièces, les portes, et le joueur."""
    for y in range(game.grille.hauteur):
        for x in range(game.grille.largeur):
            sx, sy = coords_to_px(x, y)
            rect = pygame.Rect(sx, sy, TAILLE_CELLULE, TAILLE_CELLULE)
            pygame.draw.rect(ecran, COLOR_CELL, rect, 1)

            piece = game.grille.pieces[y][x] if hasattr(game.grille, "pieces") else None
            if piece and hasattr(piece, "objets"):
                for i, obj in enumerate(piece.objets):
                    couleur = (200, 200, 50)
                    pygame.draw.circle(ecran, couleur, (sx + 10 + i * 12, sy + 10), 4)

    print("Position joueur :", game.joueur.position)

    # Dessine le joueur
    if hasattr(game, "joueur"):
        x, y = game.joueur.position
        sx, sy = coords_to_px(x, y)
        pygame.draw.circle(ecran, COLOR_JOUEUR, (sx + 20, sy + 20), 10)

def render_hud(ecran, game):
    """Affiche les infos du joueur en haut."""
    font = pygame.font.SysFont("Arial", 18)
    texte = f"Pas restants: {getattr(game.inv, 'pas', '?')} | État: {getattr(game, 'state', '?')}"
    text_surface = font.render(texte, True, (255, 255, 255))
    ecran.blit(text_surface, (10, 10))

def render_piece(ecran, piece, position):
    """(Optionnel) Affiche une pièce individuelle — utile pour debug."""
    x, y = position
    sx, sy = coords_to_px(x, y)
    rect = pygame.Rect(sx, sy, TAILLE_CELLULE, TAILLE_CELLULE)
    pygame.draw.rect(ecran, (100, 100, 255), rect, 2)
