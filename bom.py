class Bom(Entite):
    """ An hostile entity called the Bom. """
    def __init__(self, coordonnees, vie, degat, ceinture, texture):
        super().__init__(coordonnees, vie, degat, ceinture)
        self.texture = texture

    def distanceToPlayer(self, player):
        return directDistance(self.coordinates, player.getCoordinates) # rename distance_directe, vérif méthode getCoordinates dans Player (ou Entite)

    def goToPlayer(self):
        if self.distanceToPlayer() <= 6:

