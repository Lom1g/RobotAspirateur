class Node:
    def __init__(self, x, y, depth, cost, action, item_clean=0, previous=None, heuristic=None):
        self.coord = (x, y)
        self.depth = depth
        self.cost = cost
        self.action = action
        self.item_clean = item_clean
        self.previous = previous
        self.heuristic = heuristic

    def changeHeuristic(self, xa, ya, previous):
        list_action = []
        xtmp = xa - self.coord[0]
        ytmp = ya - self.coord[1]
        if xtmp > 0:
            while xtmp > 0:
                list_action += ["gauche"]
                self.heuristic += 1
                self.cost += 1
                xtmp -= 1
        elif xtmp < 0:
            while xtmp < 0:
                list_action += ["droite"]
                self.heuristic += 1
                self.cost += 1
                xtmp += 1
        if ytmp > 0:
            while ytmp > 0:
                list_action += ["haut"]
                self.heuristic += 1
                self.cost += 1
                ytmp -= 1
        elif ytmp < 0:
            while ytmp < 0:
                list_action += ["bas"]
                self.heuristic += 1
                self.cost += 1
                ytmp += 1
        self.action += list_action
        self.previous = previous
        self.cost += previous.cost
        self.heuristic += previous.heuristic



