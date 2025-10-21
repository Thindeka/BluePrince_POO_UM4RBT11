class Piece :
    """
    Classe de base pout toutes les pièces du manoir
    Attributs
    ----------
    nom : str
        nom de la pièce

    image : 
        chaque pièce est associée à une image

    portes  :
        ménent vers des directions différentes. >= 1 (au min 1 : porte par laquelle la pièce a été ouverte)
        
    coût : int
        coût en gemmes à dépenser pour pouvoir tirer la pièce

    interaction : 
        interargir avec des objets de la pièce

    effet spécial : 
        Certaines pièces ont des effets spéciales

    rareté : int
        rareté d'une pièce (0 à 3) chaque incrémenent de rareté divise par 3 la probabilité de tirer la pièce

    condition de placement :
        Certaines pièces ne peuvent être tiréees qu'à certains endroits. 
    -----
    couleur : str
        type de porte (jaunes, vertes, violettes, oranges, rouges, bleues)

    pioche : 
        quand une pièce est ajoutée au manoir, elle est retirée de la "pioche" et ne peut plus être tirée 
        (sauf si elle et en plusieurs exemplaires) -> définir nb exemplaire de chaque pièce
    """
    nom : str = "piece"

    def appliquer (self, inv : Pioche) :  
        raise NotImplementedError

    class Jaunes(Piece):
        """type de pièce : magasin"""
        def Commissary(Piece):
            nom = "Commissary"
            """Autres objets à vendre"""
        def Kitchen(piece):
            nom = "Kitchen"
            """Nouriture à vendre"""
        def Kitchen(piece):
            nom = "Kitchen"
            """Nouriture à vendre"""
        def Kitchen(piece):
            nom = "Kitchen"
        """Nouriture à vendre"""
        def Kitchen(piece):
            nom = "Kitchen"
        """Nouriture à vendre"""

    class vertes(Piece):
        """jardins d'intérieur"""

    class tirage_pieces(Piece):
        """condition : porte ouverte
            3 pièces sont tirés alétoirement, dont 1 des 3 à un coût en gemmes = 0
            attributs : condition de placement, rareté,
            """

    class dés:
        """possibilité de retirer aléatoirement des pièces si le joueur possède un dé"""
    