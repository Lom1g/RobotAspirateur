class Capteur:
    def __init__(self, environnement):
        self.etatPiece = []
        self.performance = 0
        self.environnement = environnement
        self.posRobotX = None
        self.posRobotY = None

    # agent observe
    def observeEnvironment(self):
        self.etatPiece = self.environnement.getGrid()
        self.performance = self.environnement.getPerformance()
        self.posRobotX, self.posRobotY = self.environnement.getPosRobot()

    def getObservations(self):
        return self.etatPiece, self.performance, self.posRobotX, self.posRobotY
