import operator
import threading
import time

from capteurs import Capteur
from effecteurs import Effecteur
from node import Node


class Agent(threading.Thread):
    def __init__(self, environnement):
        super().__init__()

        # coordonnees du robot (centre de la matrice)
        environnement.posRobotX = self.posRobotX = 2
        environnement.posRobotY = self.posRobotY = 2

        # vie du robot
        self.life = True

        # etat Belief Desire Intention
        self.etatBDI = {"etatPiece": [], "nombreItem": 0, "performance": 0}

        # plan d'action
        self.plan = []

        # interface du robot
        self.capteurs = Capteur(environnement)
        self.effecteurs = Effecteur(environnement)

    # mise en fonctionnement de l'agent
    def run(self):
        while self.amIAlive():
            self.observeEnvironnmentWithAllMySensors()
            self.updateMyState()
            self.chooseAnAction()
            self.justDoIt()

    # exploration informée
    def informe(self):
        pass

    # exploration non informée
    def noInforme(self):
        self.plan = self.dls()

    def dls(self):
        if self.etatBDI["nombreItem"] != 0:
            # limite de profondeur
            depth_max = 9
            # liste des noeuds à explorer
            liste_a_traite = []
            # liste des noeuds exploré
            liste_traite = []
            # liste des actions a realiser
            liste_action = []
            # liste noeud potentiellement exploitable
            liste_noeud = []

            # creation du noeud principal
            if self.etatBDI["etatPiece"][self.posRobotX + self.posRobotY * 5]["diamond"]:
                if self.etatBDI["etatPiece"][self.posRobotX + self.posRobotY * 5]["dust"]:
                    if self.etatBDI["nombreItem"] == 2:
                        n = Node(self.posRobotX, self.posRobotY, 0, 2, ["aspirer", "ramasser"], 2)
                        liste_action += n.action
                        return liste_action
                    else:
                        liste_a_traite.insert(0, Node(self.posRobotX, self.posRobotY, 0, 2, ["aspirer", "ramasser"], 1))
                else:
                    if self.etatBDI["nombreItem"] == 1:
                        n = Node(self.posRobotX, self.posRobotY, 0, 1, ["ramasser"], 1)
                        liste_action += n.action
                        return liste_action
                    else:
                        liste_a_traite.insert(0, Node(self.posRobotX, self.posRobotY, 0, 1, ["ramasser"], 1))
            elif self.etatBDI["etatPiece"][self.posRobotX + self.posRobotY * 5]["dust"]:
                if self.etatBDI["nombreItem"] == 1:
                    n = Node(self.posRobotX, self.posRobotY, 0, 1, ["aspirer"], 1)
                    liste_action += n.action
                    return liste_action
                else:
                    liste_a_traite.insert(0, Node(self.posRobotX, self.posRobotY, 0, 1, ["aspirer"], 1))
            else:
                liste_a_traite.insert(0, Node(self.posRobotX, self.posRobotY, 0, 0, [], 0))

            # on boucle tant que la liste des noeuds a traiter n'est pas vide
            while liste_a_traite:
                for i in range(0, depth_max - liste_a_traite[0].depth):
                    x, y = liste_a_traite[0].coord
                    # on expand la fontière
                    # case a droite
                    if x + 1 < 5:
                        if self.etatBDI["etatPiece"][x + 1 + y * 5]["diamond"]:
                            if self.etatBDI["etatPiece"][x + 1 + y * 5]["dust"]:
                                # verification d'atteinte de l'objectif
                                if self.etatBDI["nombreItem"] == liste_a_traite[0].item_clean + 2:
                                    n = Node(x + 1, y, liste_a_traite[0].depth + 1, liste_a_traite[0].cost + 3,
                                             ["aspirer", "ramasser", "droite"], liste_a_traite[0].item_clean + 2,
                                             liste_a_traite[0])
                                    liste_noeud.append(n)
                                else:
                                    liste_a_traite.insert(1, Node(x + 1, y, liste_a_traite[0].depth + 1,
                                                                  liste_a_traite[0].cost + 3,
                                                                  ["aspirer", "ramasser", "droite"],
                                                                  liste_a_traite[0].item_clean + 2, liste_a_traite[0]))
                            else:
                                # verification d'atteinte de l'objectif
                                if self.etatBDI["nombreItem"] == liste_a_traite[0].item_clean + 1:
                                    n = Node(x + 1, y, liste_a_traite[0].depth + 1, liste_a_traite[0].cost + 2,
                                             ["ramasser", "droite"], liste_a_traite[0].item_clean + 2,
                                             liste_a_traite[0])
                                    liste_noeud.append(n)
                                else:
                                    liste_a_traite.insert(1, Node(x + 1, y, liste_a_traite[0].depth + 1,
                                                                  liste_a_traite[0].cost + 2, ["ramasser", "droite"],
                                                                  liste_a_traite[0].item_clean + 1, liste_a_traite[0]))
                        elif self.etatBDI["etatPiece"][x + 1 + y * 5]["dust"]:
                            # verification d'atteinte de l'objectif
                            if self.etatBDI["nombreItem"] == liste_a_traite[0].item_clean + 1:
                                n = Node(x + 1, y, liste_a_traite[0].depth + 1, liste_a_traite[0].cost + 2,
                                         ["aspirer", "droite"], liste_a_traite[0].item_clean + 1, liste_a_traite[0])
                                liste_noeud.append(n)
                            else:
                                liste_a_traite.insert(1, Node(x + 1, y, liste_a_traite[0].depth + 1,
                                                              liste_a_traite[0].cost + 2, ["aspirer", "droite"],
                                                              liste_a_traite[0].item_clean + 1, liste_a_traite[0]))
                        else:
                            liste_a_traite.insert(1, Node(x + 1, y, liste_a_traite[0].depth + 1,
                                                          liste_a_traite[0].cost + 1, ["droite"],
                                                          liste_a_traite[0].item_clean, liste_a_traite[0]))
                    # case a gauche
                    if x - 1 >= 0:
                        if self.etatBDI["etatPiece"][x - 1 + y * 5]["diamond"]:
                            if self.etatBDI["etatPiece"][x - 1 + y * 5]["dust"]:
                                # verification d'atteinte de l'objectif
                                if self.etatBDI["nombreItem"] == liste_a_traite[0].item_clean + 2:
                                    n = Node(x - 1, y, liste_a_traite[0].depth + 1, liste_a_traite[0].cost + 3,
                                             ["aspirer", "ramasser", "gauche"],
                                             liste_a_traite[0].item_clean + 2, liste_a_traite[0])
                                    liste_noeud.append(n)
                                else:
                                    liste_a_traite.insert(1, Node(x - 1, y, liste_a_traite[0].depth + 1,
                                                                  liste_a_traite[0].cost + 3,
                                                                  ["aspirer", "ramasser", "gauche"],
                                                                  liste_a_traite[0].item_clean + 2, liste_a_traite[0]))
                            else:
                                # verification d'atteinte de l'objectif
                                if self.etatBDI["nombreItem"] == liste_a_traite[0].item_clean + 1:
                                    n = Node(x - 1, y, liste_a_traite[0].depth + 1, liste_a_traite[0].cost + 2,
                                             ["ramasser", "gauche"],
                                             liste_a_traite[0].item_clean + 1, liste_a_traite[0])
                                    liste_noeud.append(n)
                                else:
                                    liste_a_traite.insert(1, Node(x - 1, y, liste_a_traite[0].depth + 1,
                                                                  liste_a_traite[0].cost + 2,
                                                                  ["ramasser", "gauche"],
                                                                  liste_a_traite[0].item_clean + 1, liste_a_traite[0]))
                        elif self.etatBDI["etatPiece"][x - 1 + y * 5]["dust"]:
                            # verification d'atteinte de l'objectif
                            if self.etatBDI["nombreItem"] == liste_a_traite[0].item_clean + 1:
                                n = Node(x - 1, y, liste_a_traite[0].depth + 1, liste_a_traite[0].cost + 2,
                                         ["aspirer", "gauche"],
                                         liste_a_traite[0].item_clean + 1, liste_a_traite[0])
                                liste_noeud.append(n)
                            else:
                                liste_a_traite.insert(1, Node(x - 1, y, liste_a_traite[0].depth + 1,
                                                              liste_a_traite[0].cost + 2,
                                                              ["aspirer", "gauche"],
                                                              liste_a_traite[0].item_clean + 1, liste_a_traite[0]))
                        else:
                            liste_a_traite.insert(1, Node(x - 1, y, liste_a_traite[0].depth + 1,
                                                          liste_a_traite[0].cost + 1, ["gauche"],
                                                          liste_a_traite[0].item_clean, liste_a_traite[0]))
                    # case en bas
                    if y + 1 < 5:
                        if self.etatBDI["etatPiece"][x + (y + 1) * 5]["diamond"]:
                            if self.etatBDI["etatPiece"][x + (y + 1) * 5]["dust"]:
                                # verification d'atteinte de l'objectif
                                if self.etatBDI["nombreItem"] == liste_a_traite[0].item_clean + 2:
                                    n = Node(x, y + 1, liste_a_traite[0].depth + 1, liste_a_traite[0].cost + 3
                                    ["aspirer", "ramasser", "bas"],
                                             liste_a_traite[0].item_clean + 2, liste_a_traite[0])
                                    liste_noeud.append(n)
                                else:
                                    liste_a_traite.insert(1, Node(x, y + 1, liste_a_traite[0].depth + 1,
                                                                  liste_a_traite[0].cost + 3,
                                                                  ["aspirer", "ramasser", "bas"],
                                                                  liste_a_traite[0].item_clean + 2, liste_a_traite[0]))
                            else:
                                # verification d'atteinte de l'objectif
                                if self.etatBDI["nombreItem"] == liste_a_traite[0].item_clean + 1:
                                    n = Node(x, y + 1, liste_a_traite[0].depth + 1, liste_a_traite[0].cost + 2,
                                             ["ramasser", "bas"],
                                             liste_a_traite[0].item_clean + 1, liste_a_traite[0])
                                    liste_noeud.append(n)
                                else:
                                    liste_a_traite.insert(1, Node(x, y + 1, liste_a_traite[0].depth + 1,
                                                                  liste_a_traite[0].cost + 2,
                                                                  ["ramasser", "bas"],
                                                                  liste_a_traite[0].item_clean + 1, liste_a_traite[0]))
                        elif self.etatBDI["etatPiece"][x + (y + 1) * 5]["dust"]:
                            # verification d'atteinte de l'objectif
                            if self.etatBDI["nombreItem"] == liste_a_traite[0].item_clean + 1:
                                n = Node(x, y + 1, liste_a_traite[0].depth + 1, liste_a_traite[0].cost + 2,
                                         ["aspirer", "bas"],
                                         liste_a_traite[0].item_clean + 1, liste_a_traite[0])
                                liste_noeud.append(n)
                            else:
                                liste_a_traite.insert(1, Node(x, y + 1, liste_a_traite[0].depth + 1,
                                                              liste_a_traite[0].cost + 2,
                                                              ["aspirer", "bas"],
                                                              liste_a_traite[0].item_clean + 1, liste_a_traite[0]))
                        else:
                            liste_a_traite.insert(1, Node(x, y + 1, liste_a_traite[0].depth + 1,
                                                          liste_a_traite[0].cost + 1, ["bas"],
                                                          liste_a_traite[0].item_clean, liste_a_traite[0]))
                    # case en haut
                    if y - 1 >= 0:
                        if self.etatBDI["etatPiece"][x + (y - 1) * 5]["diamond"]:
                            if self.etatBDI["etatPiece"][x + (y - 1) * 5]["dust"]:
                                # verification d'atteinte de l'objectif
                                if self.etatBDI["nombreItem"] == liste_a_traite[0].item_clean + 2:
                                    n = Node(x, y - 1, liste_a_traite[0].depth + 1, liste_a_traite[0].cost + 3,
                                             ["aspirer", "ramasser", "haut"],
                                             liste_a_traite[0].item_clean + 2, liste_a_traite[0])
                                    liste_noeud.append(n)
                                else:
                                    liste_a_traite.insert(1, Node(x, y - 1, liste_a_traite[0].depth + 1,
                                                                  liste_a_traite[0].cost + 3,
                                                                  ["aspirer", "ramasser", "haut"],
                                                                  liste_a_traite[0].item_clean + 2, liste_a_traite[0]))
                            else:
                                # verification d'atteinte de l'objectif
                                if self.etatBDI["nombreItem"] == liste_a_traite[0].item_clean + 1:
                                    n = Node(x, y - 1, liste_a_traite[0].depth + 1, liste_a_traite[0].cost + 2,
                                             ["ramasser", "haut"],
                                             liste_a_traite[0].item_clean + 1, liste_a_traite[0])
                                    liste_noeud.append(n)
                                else:
                                    liste_a_traite.insert(1, Node(x, y - 1, liste_a_traite[0].depth + 1,
                                                                  liste_a_traite[0].cost + 2,
                                                                  ["ramasser", "haut"],
                                                                  liste_a_traite[0].item_clean + 1, liste_a_traite[0]))
                        elif self.etatBDI["etatPiece"][x + (y - 1) * 5]["dust"]:
                            # verification d'atteinte de l'objectif
                            if self.etatBDI["nombreItem"] == liste_a_traite[0].item_clean + 1:
                                n = Node(x, y - 1, liste_a_traite[0].depth + 1, liste_a_traite[0].cost + 2,
                                         ["aspirer", "haut"],
                                         liste_a_traite[0].item_clean + 1, liste_a_traite[0])
                                liste_noeud.append(n)
                            else:
                                liste_a_traite.insert(1, Node(x, y - 1, liste_a_traite[0].depth + 1,
                                                              liste_a_traite[0].cost + 2,
                                                              ["aspirer", "haut"],
                                                              liste_a_traite[0].item_clean + 1, liste_a_traite[0]))
                        else:
                            liste_a_traite.insert(1, Node(x, y - 1, liste_a_traite[0].depth + 1,
                                                          liste_a_traite[0].cost + 1, ["haut"],
                                                          liste_a_traite[0].item_clean, liste_a_traite[0]))
                    liste_traite.append(liste_a_traite[0])
                    liste_a_traite.pop(0)
                    i += 1
                # on retire les feuilles (4 max) de notre branche pour pouvoir revenir au noeud precedent
                for j in range(0, 4):
                    if liste_a_traite and liste_a_traite[0].depth == depth_max:
                        liste_traite.append(liste_a_traite[0])
                        liste_a_traite.pop(0)
            # si on a des noeuds de reussite d'objectif on choisit celui avec le cout le moins eleve
            if liste_noeud:
                liste_noeud.sort(key=lambda c: c.cost)
                n = liste_noeud[0]
            # si on qu'une reussite partielle de l'objectif on tri par item ramassé et par cout
            else:
                # on tri d'abord par item max ramasse
                liste_traite.sort(key=lambda c: c.item_clean, reverse=True)
                # on ne garde que les noeuds capable de ramasse le max d'item
                liste_traite = list(filter(lambda c: c.item_clean == liste_traite[0].item_clean, liste_traite))
                # on tri ces noeuds par cout
                liste_traite.sort(key=lambda c: c.cost)
                # le noeud qui nous interesse est le premier
                n = liste_traite[0]
            while n.previous is not None:
                liste_action += n.action
                n = n.previous
            return liste_action
        else:
            return "pas d'item dans le manoir"

    # critère d'arret
    def amIAlive(self):
        return self.life

    # appel des capteurs
    def observeEnvironnmentWithAllMySensors(self):
        self.capteurs.observeEnvironment()

    # MAJ de l'etat de l'environnement
    def updateMyState(self):
        self.etatBDI["etatPiece"], self.etatBDI[
            "performance"], self.posRobotX, self.posRobotY = self.capteurs.getObservations()
        self.etatBDI["nombreItem"] = 0
        for i in range(len(self.etatBDI["etatPiece"])):
            if self.etatBDI["etatPiece"][i]["dust"]:
                self.etatBDI["nombreItem"] += 1
            if self.etatBDI["etatPiece"][i]["diamond"]:
                self.etatBDI["nombreItem"] += 1

    # algo d'exploration
    def chooseAnAction(self):
        self.noInforme()

    # déplacement
    # aspiration poussière
    # ramassage bijoux
    # MAJ BDI
    # performances
    # apprentissage épisodique
    def justDoIt(self):
        self.plan = list(reversed(self.plan))
        print(self.plan)
        for action in self.plan:
            if action == "droite":
                self.effecteurs.move_right()
                time.sleep(0.4)
            elif action == "gauche":
                self.effecteurs.move_left()
                time.sleep(0.4)
            elif action == "bas":
                self.effecteurs.move_forward()
                time.sleep(0.4)
            elif action == "haut":
                self.effecteurs.move_backward()
                time.sleep(0.4)
            elif action == "aspirer":
                self.effecteurs.vacuum()
                time.sleep(0.4)
            elif action == "ramasser":
                self.effecteurs.pick()
                time.sleep(0.4)
