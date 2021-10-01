class Node:
    def __init__(self, x, y, depth, cost, action, item_clean=0, previous=None):
        self.coord = (x, y)
        self.depth = depth
        self.cost = cost
        self.action = action
        self.item_clean = item_clean
        self.previous = previous
