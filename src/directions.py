# pour suivre la logigue pygame

DIR_VECT = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "O": (-1, 0),
}

OPPOSITE = {
    "N": "S",
    "S": "N",
    "E": "O",
    "O": "E",
}

def voisin(x: int, y: int, direction: str) -> tuple[int, int]:
    dx, dy = DIR_VECT[direction]
    return x + dx, y + dy