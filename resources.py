class Entite:
    """
    une entité (joueur, animal, créature...)
    """
    def __init__(self, coordonnees:tuple=(0,0), vie:int=None, degat:int=None, ceinture:list=[], main:int=0):
        """
        Constructeur de la classe Entité.
        * coordonnees (tuple) : coordonnees x / y de l'entité dans le monde
        * vie (int) : nombre de points de vie actuels (pas le maximum)
        * degat (int) : nombre de degats infligés par l'entité par défaut (sans arme en main)
        * ceinture (list) : liste de 6 'items' accessibles en main par l'entite
        """
        self.coordonnees = coordonnees
        self.vie = vie
        self.degat = degat
        self.ceinture = ceinture
        self.main = 0

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
        """ Remplace l'item à l'emplacement d'index {slot} (de la ceinture) par {item}. """
        self.ceinture[slot] = item

    def get_main(self):
        """ Retourne la valeur de l'attribut main de l'entité. """
        return self.main

    def set_main(self, glissement):
        """ Remplace l'index de la ceinture actuellement en main. """
        if glissement < 0:
            negatif= True               # 
            glissement= -1*glissement   # passe le glissement en positif pour le calcul

        while (self.get_main() + glissement) > 6:
            glissement -= 6

        if negatif:
            self.main = 6 - glissement
        else:
            self.main = glissement

    def attaque(self, victime):
        if isinstance(self.ceinture[self.get_main()], Arme):
            victime.set_vie(victime.get_vie() - self.ceinture[self.get_main()].degat)
        else:
            victime.set_vie(victime.get_vie() - self.degat)

#class Nom(AutreClasse) fait hériter Nom de toutes les propriétés de AutreClasse
class Joueur(Entite):
    """
    le joueur
    """
    def __init__(self, coordonnees:tuple=(0,0), vie:int=100, degat:int=10, ceinture:list=[], sac:list=[]):
        """
        Constructeur de la classe Joueur.
        * coordonnees (tuple) : coordonnées x / y du joueur dans le monde
        * vie (int) : nombre de points de vie actuels (pas le maximum)
        * degat (int) : nombre de dégâts infligés par le joueur par défaut (sans arme en main)
        * ceinture (list) : liste de 6 'items' accessibles en main par le joueur
        * sac (list) : liste de tous les 'items' dans l'inventaire du joueur
        """
        # pour bien transmettre les paramètres passés dans Joueur dans ceux hérités de Entite
        super().__init__(coordonnees, vie, degat, ceinture)
        self.sac    = sac

    def poser_bloc(self):
        pass

    def verification_ennemis(self, ennemis:list=[]):
        """
        Retourne la liste de tous les ennemis qui voient le joueur, ou None si aucune.
        Fonction utilisée automatiquement à chaque déplacement du joueur.
        * ennemis (list) : liste de toutes les entités hostiles dans le monde
        """
        # vérifier si blocks entre joueur et entité :
        #   si oui, passer à la suivante, sinon passer à la vérif suivante
        # vérifier si distance joueur-entité est 7 ou plus :
        #   si oui, passer à la suivante, sinon passer à la vérif suivante
        ennemis_proches = []

        for entite in ennemis:
            # si il n'y a pas de blocks entre le joueur et l'ennemi
            if not presence_block(self.coordonnees, entite.coordonnees):
                if distance(self.coordonnees, entite.coordonnees) <= 6:
                    ennemis_proches.append(entite)
        
        if len(ennemis_proches) <= 0:
            return None
        return ennemis_proches


class Arme:
    """
    une arme
    """
    def __init__(self, degat:int, texture:str='./textures/missing.png'):
        """
        Constructeur de la classe Arme.
        * degat (int) : nombre de dégâts infligés par l'arme
        * texture (str) : chemin d'accès à la texture de l'arme
        """
        self.degat  = degat
        self.texture= texture


def presence_block(point_1:tuple, point_2:tuple):
    """
    Retourne True si il y a des blocks entre les deux points donnés et False sinon.
    * point_1 (tuple) : coordonnees (x, y) du premier point
    * point_2 (tuple) : coordonnees (x, y) du deuxième point
    """
    # trouver points de départ avec Pierre
    # –> besoin de liste des blocks compris entre point_1 et point_2
    zone    = []
    

def distance(point_1:tuple, point_2:tuple):
    """
    Retourne sous forme de tuple la distance (horizontale puis verticale) entre deux points.
    * point_1 (tuple) : coordonnees (x, y) du premier point
    * point_2 (tuple) : coordonnees (x, y) du deuxième point
    """
    return abs(point_1[0] - point_2[0]), abs(point_1[1] - point_2[1])


################################################################################

joueur  = Joueur((0, 0), 100, 5, ['air' for _ in range(0, 6)])
monstre = Entite((0,0), 50, 10, [Arme(20)])
epee    = Arme(20)

################################################################################

# TODO: line 122 (class Arme / def init) –> gérer texture avec Tkinter