class Porte :
    """ Represente une porte du manoir
    
    Attributs
    ----------
    niveau : int 
        Le statut de la porte (0=deverouillee, 1=verouillée, 2=verouillée à double tour)
    ouverte : bool
        Vrai si la porte est ouverte
    
    """


    def __init__(self, niveau : int = 0, ouverte : bool =False) :
        self.__niveau = niveau
        self.ouverte = ouverte 


    @property
    def niveau (self) :
        """ getter de l'attribut statut """
        return self.__niveau