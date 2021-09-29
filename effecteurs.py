class Effecteur:
    def __init__(self, environnement):
        self.environnement = environnement

    # deplacement vers le bas
    def move_forward(self):
        self.environnement.move_forward()

    # deplacement vers le haut
    def move_backward(self):
        self.environnement.move_backward()

    # deplacement vers la droite
    def move_right(self):
        self.environnement.move_right()

    # deplacement vers la gauche
    def move_left(self):
        self.environnement.move_left()

    # ramassage objet
    def pick(self):
        self.environnement.pick()

    # agent aspire
    def vacuum(self):
        self.environnement.vacuum()

