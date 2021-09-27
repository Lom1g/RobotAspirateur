import threading

from capteurs import Capteur
from effecteurs import Effecteur


class Agent(threading.Thread):
    def __init__(self, environnement):
        super().__init__()
        # attributs de l'agent
        self.etatBDI = {"etatPiece": [], "performance": 0} # a compléter (etats precedents)
        self.capteurs = Capteur(environnement)
        self.effecteurs = Effecteur(environnement)

    # mise en fonctionnement de l'agent
    def run(self):
        while self.amIAlive():
            self.observeEnvironnmentWithAllMySensors()
            self.updateMyState()
            self.chooseAnAction()
            self.justDoIt()
            print("agent")

    # exploration informée
    def informe(self):
        pass

    # exploration non informée
    def noInforme(self):
        pass

    # critère d'arret
    def amIAlive(self):
        return True

    # appel des capteurs
    def observeEnvironnmentWithAllMySensors(self):
        self.capteurs.observeEnvironment()

    # MAJ graph
    def updateMyState(self):
        self.etatBDI["etatPiece"], self.etatBDI["performance"] = self.capteurs.getObservations()

    # algo d'exploration
    def chooseAnAction(self):
        pass

    # déplacement
    # aspiration poussière
    # ramassage bijoux
    # MAJ BDI
    # performances
    # apprentissage épisodique
    def justDoIt(self):
        pass

