import random
import threading


class Environnement(threading.Thread):
    def __init__(self):
        super().__init__()
        # attributs (grille 5x5)
        self.life = True
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
        prob = random.randint(0, 24)
        self.grid[prob]["dust"] = True

    # generation de diamant
    def generateDiamond(self):
        prob = random.randint(0, 24)
        self.grid[prob]["diamond"] = True

    def shouldThereBeANewDustyPlace(self):
        prob = random.randint(0, 10**6)
        if prob == 1:
            return True
        else:
            return False

    def shouldThereBeANewLostDiamond(self):
        prob = random.randint(0, 2*10**6)
        if prob == 1:
            return True
        else:
            return False

    def gameIsRunning(self):
        return self.life

    # mesure performance
    def evaluatePerformance(self):
        pass

    def getGrid(self):
        return self.grid
