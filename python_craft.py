class Entite:
    """
    une entité (joueur, animal, créature...)
    """
    def __init__(self, coordonnees:tuple, vie:int, degat:int, ceinture:list):
        """
        Constructeur de la classe Entité.
        * coordonnees (tuple) : coordoonnees x / y de l'entité dans le monde
        * vie (int) : nombre de points de vie actuels (pas le maximum)
        * degat (int) : nombre de degats infligés par l'entité par défaut (sans arme en main)
        * ceinture (list) : liste de 5 'items' accessibles en main par l'entite
        """
        self.coordonnees = coordonnees
        self.vie = vie
        self.degat = degat
        self.ceinture = ceinture

    def get_coordonnees(self):
        """ Retourne la valeur de l'attribut coordonnees de l'entité. """
        return self.coordonnees

    def set_coordonnees(self, newCoordonnees:tuple):
        """ Remplace la valeur de l'attribut coordonnees de l'entité. """
        self.coordonnees = newCoordonnees

    def get_vie(self):
        """ Retourne la valeur de l'attribut vie de l'entité. """
        return self.vie

    def set_vie(self, newVie:int):
        """ Remplace la valeur de l'attribut vie de l'entité. """
        self.vie = newVie

    def get_degat(self):
        """ Retourne la valeur de l'attribut degat de l'entité. """
        return self.degat

    # pas set_degat(self): car on ne change jamais les dégâts faits par l'entité
    # attaque() prend déjà en charge le port d'arme

    def get_ceinture(self):
        """ Retourne la valeur de l'attribut ceinture de l'entité. """
        return self.ceinture

    def set_ceinture(self, slot:int, item):
        """ Remplace l'item à l'emplacement de numéro slot de ceinture par item. """
        self.ceinture[slot] = item


    def attaque(self, victime):
        if isinstance(self.ceinture[0], Arme):
            victime.set_vie(victime.get_vie() - self.ceinture[0].degat)
        else:
            victime.set_vie(victime.get_vie() - self.degat)










class Joueur(Entite):
    """
    le joueur
    """
    def __init__(self, coordonnees:tuple, vie:int, degat:int, ceinture:list):
        """
        Constructeur de joueur.
        """
        super().__init__(coordonnees, vie, degat, ceinture)



    def poser_bloc(self):
        pass


class Arme:
    pass
################################################################################

joueur = Joueur((0, 0), 100, 5, ['air' for _ in range(0, 5)])
monstre = Joueur((0, 0), 50, 10, ['air' for _ in range(0, 5)])

################################################################################

# voir ceinture pour changr slot en main:
# attribut main qui réfère a un slot de la ceinture