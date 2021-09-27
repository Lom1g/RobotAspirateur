class Capteur:
    def __init__(self, environnement):
        self.etatPiece = []
        self.performance = 0
        self.environnement = environnement

    # agent observe
    def observeEnvironment(self):
        self.etatPiece = self.environnement.getGrid()
        self.performance = self.environnement.performance

    def getObservations(self):
        return self.etatPiece, self.performance
