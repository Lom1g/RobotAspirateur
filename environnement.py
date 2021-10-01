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
        self.cost = 0
        self.penitence = 0

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
        prob = random.randint(0, 10 ** 6)
        if prob == 1:
            return True
        else:
            return False

    def gameIsRunning(self):
        return self.life

    def getGrid(self):
        return self.grid

    def getPenitence(self):
        return self.penitence

    def getCost(self):
        return self.cost

    def setPenitence(self, penitence):
        self.penitence = penitence

    def setCost(self, cost):
        self.cost = cost

    def getPosRobot(self):
        return self.posRobotX, self.posRobotY

    def vacuum(self):
        self.cost += 1
        self.grid[self.posRobotX + self.posRobotY * 5]["dust"] = False
        # si on aspire un dimant on reçoit une penitence
        if self.grid[self.posRobotX + self.posRobotY * 5]["diamond"]:
            self.grid[self.posRobotX + self.posRobotY * 5]["diamond"] = False
            self.penitence += 1

    def pick(self):
        self.cost += 1
        self.grid[self.posRobotX + self.posRobotY * 5]["diamond"] = False

    def move_forward(self):
        self.cost += 1
        if (self.posRobotY + 1) >= 5:
            pass
        else:
            self.posRobotY += 1

    def move_backward(self):
        self.cost += 1
        if (self.posRobotY - 1) < 0:
            pass
        else:
            self.posRobotY -= 1

    def move_right(self):
        self.cost += 1
        if (self.posRobotX + 1) >= 5:
            pass
        else:
            self.posRobotX += 1

    def move_left(self):
        self.cost += 1
        if (self.posRobotX - 1) < 0:
            pass
        else:
            self.posRobotX -= 1
