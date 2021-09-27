import threading


class Environnement(threading.Thread):
    def __init__(self):
        super().__init__()
        # attributs (grille 5x5)
        self.performance = 0
        self.grid = [{"dust": False, "diamond": False}, {"dust": False, "diamond": False},
                     {"dust": False, "diamond": False}, {"dust": False, "diamond": False},
                     {"dust": False, "diamond": False},
                     {"dust": False, "diamond": False}, {"dust": False, "diamond": False},
                     {"dust": False, "diamond": False}, {"dust": False, "diamond": False},
                     {"dust": False, "diamond": False},
                     {"dust": False, "diamond": False}, {"dust": False, "diamond": False},
                     {"dust": False, "diamond": False}, {"dust": False, "diamond": False},
                     {"dust": False, "diamond": False},
                     {"dust": False, "diamond": False}, {"dust": False, "diamond": False},
                     {"dust": False, "diamond": False}, {"dust": False, "diamond": False},
                     {"dust": False, "diamond": False},
                     {"dust": False, "diamond": False}, {"dust": False, "diamond": False},
                     {"dust": False, "diamond": False}, {"dust": False, "diamond": False},
                     {"dust": False, "diamond": False}]

    def run(self):
        while self.gameIsRunning():
            if self.shouldThereBeANewDustyPlace():
                self.generateDust()
            if self.shouldThereBeANewLostDiamond():
                self.generateDiamond()

    # generation poussière
    def generateDust(self):
        pass

    # generation de diamant
    def generateDiamond(self):
        pass

    def shouldThereBeANewDustyPlace(self):
        pass

    def shouldThereBeANewLostDiamond(self):
        pass

    def gameIsRunning(self):
        return True

    # mesure performance
    def evaluatePerformance(self):
        pass

    def getGrid(self):
        return self.grid
