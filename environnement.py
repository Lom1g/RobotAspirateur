import random
import threading


class Environnement(threading.Thread):
    def __init__(self):
        super().__init__()

        # vie de l'environnement
        self.life = True

        # coordonnees du robot
        self.posRobotX = None
        self.posRobotY = None

        # performance du robot
        self.performance = 0

        # grille du manoir
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
        prob = random.randint(0, 10 ** 6)
        if prob == 1:
            return True
        else:
            return False

    def shouldThereBeANewLostDiamond(self):
        prob = random.randint(0, 10 ** 7)
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

    def vacuum(self):  # ajouter la performance
        self.grid[self.posRobotX + self.posRobotY * 5]["dust"] = False
        self.grid[self.posRobotX + self.posRobotY * 5]["diamond"] = False

    def pick(self):  # ajouter la performance
        self.grid[self.posRobotX + self.posRobotY * 5]["diamond"] = False

    def move_forward(self):
        if (self.posRobotY + 1) >= 5:
            pass
        else:
            self.posRobotY += 1

    def move_backward(self):
        if (self.posRobotY - 1) < 0:
            pass
        else:
            self.posRobotY -= 1

    def move_right(self):
        if (self.posRobotX + 1) >= 5:
            pass
        else:
            self.posRobotX += 1

    def move_left(self):
        if (self.posRobotX - 1) < 0:
            pass
        else:
            self.posRobotX -= 1
