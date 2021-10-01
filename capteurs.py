class Capteur:
    def __init__(self, environnement):
        self.etatPiece = []
        self.penitence = 0
        self.environnement = environnement
        self.posRobotX = None
        self.posRobotY = None

    # agent observe
    def observeEnvironment(self):
        self.etatPiece = self.environnement.getGrid()
        self.penitence = self.environnement.getPenitence()
        self.posRobotX, self.posRobotY = self.environnement.getPosRobot()

    def getObservations(self):
        return self.etatPiece, self.penitence, self.posRobotX, self.posRobotY
