import operator
import statistics
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

        # iteration dans le cadre de l'exploration informe
        self.iteration_min = 1
        self.iteration = 2
        self.iteration_max = 3

        # liste des couts reels des iterations du parcours informe
        self.liste_realCost = []

        # vie du robot
        self.life = True

        # etat Belief Desire Intention
        self.etatBDI = {"etatPiece": [], "nombreItem": 0, "penitence": 0}

        # plans d'action
        self.plan = []
        self.planInforme = []
        self.costInforme = 0
        self.planNoInforme = []
        self.costNoInforme = 0

        # interface du robot
        self.capteurs = Capteur(environnement)
        self.effecteurs = Effecteur(environnement)

    # mise en fonctionnement de l'agent
    def run(self):
        while self.amIAlive():
            self.observeEnvironnmentWithAllMySensors()
            self.updateMyState()
            self.chooseAnAction()
            # on choisit le plan d'action suivant son cout
            if self.costNoInforme is not None and self.costInforme is not None:
                if self.costNoInforme > self.costInforme:
                    self.plan = self.planInforme
                    self.justDoIt()
                else:
                    while 1:
                        self.plan = self.planNoInforme
                        # applique le parcours et analyse les performances
                        for i in range(0, self.iteration):
                            self.justDoIt()
                            self.realCost()
                        moy = statistics.mean(self.liste_realCost)
                        # si l'on detecte des penitence on adapte la frequence et on explore
                        if self.costInforme > moy:
                            if self.iteration - 1 <= self.iteration_min:
                                self.iteration = self.iteration_min
                            else:
                                self.iteration -= 1
                            break
                        # sinon on reitere le parcours et on adapte la frequence
                        else:
                            if self.iteration + 1 >= self.iteration_max:
                                self.iteration = self.iteration_max
                            else:
                                self.iteration += 1



    def realCost(self):
        realcost = self.capteurs.getCost() - self.capteurs.getPenitence()
        self.liste_realCost.append(realcost)
        self.effecteurs.setCost(0)
        self.effecteurs.setPenitence(0)

    # exploration informée
    def informe(self):
        self.planInforme, self.costInforme = self.greedy()

    def greedy(self):
        if self.etatBDI["nombreItem"] != 0:
            # limite de profondeur
            piece_max = 2
            # liste des objets
            liste_obj = []
            # liste des objets traites
            liste_traite = []
            # liste des actions a retourner
            liste_action = []
            # coordonees robot
            x = self.posRobotX
            y = self.posRobotY

            # noeud principal
            n_princ = Node(x, y, None, 0, [], None, None, 0)
            # implemente la liste des pieces avec des objets
            for i in range(len(self.etatBDI["etatPiece"])):
                if self.etatBDI["etatPiece"][i]["dust"] and self.etatBDI["etatPiece"][i]["diamond"]:
                    n = Node(i % 5, i // 5, None, 2, ["aspirer", "ramasser"], None, None, 0)
                    n.changeHeuristic(x, y, n_princ)
                    liste_obj.append(n)
                elif self.etatBDI["etatPiece"][i]["dust"]:
                    n = Node(i % 5, i // 5, None, 1, ["aspirer"], None, None, 0)
                    n.changeHeuristic(x, y, n_princ)
                    liste_obj.append(n)
                elif self.etatBDI["etatPiece"][i]["diamond"]:
                    n = Node(i % 5, i // 5, None, 1, ["ramasser"], None, None, 0)
                    n.changeHeuristic(x, y, n_princ)
                    liste_obj.append(n)
            # implement la liste des objets traite
            liste_traite.insert(0, n_princ)

            for item in range(1, piece_max):
                liste_obj.sort(key=lambda c: c.heuristic)
                liste_traite.insert(0, liste_obj[0])
                liste_obj.pop(0)
                # si la liste des objets a traite est vide on retourne le plan d'action
                if not liste_obj:
                    n = liste_traite[0]
                    cout = 0
                    while n.previous is not None:
                        liste_action += n.action
                        cout += n.cost
                        n = n.previous
                    return liste_action, cout
                xtmp, ytmp = liste_traite[0].coord
                # on "actualise" les heuristic
                for node in liste_obj:
                    node.changeHeuristic(xtmp, ytmp, liste_traite[0])
            # retourne le plan d'action qui correspond le mieux a l'objectif avec pour limite "item_max"
            n = liste_traite[0]
            cout = 0
            while n.previous is not None:
                liste_action += n.action
                cout += n.cost
                n = n.previous
            return liste_action, cout
        else:
            return "nothing", None

    # exploration non informée
    def noInforme(self):
        self.planNoInforme, self.costNoInforme = self.dls()

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
                        return liste_action, n.cost
                    else:
                        liste_a_traite.insert(0, Node(self.posRobotX, self.posRobotY, 0, 2, ["aspirer", "ramasser"], 1))
                else:
                    if self.etatBDI["nombreItem"] == 1:
                        n = Node(self.posRobotX, self.posRobotY, 0, 1, ["ramasser"], 1)
                        liste_action += n.action
                        return liste_action, n.cost
                    else:
                        liste_a_traite.insert(0, Node(self.posRobotX, self.posRobotY, 0, 1, ["ramasser"], 1))
            elif self.etatBDI["etatPiece"][self.posRobotX + self.posRobotY * 5]["dust"]:
                if self.etatBDI["nombreItem"] == 1:
                    n = Node(self.posRobotX, self.posRobotY, 0, 1, ["aspirer"], 1)
                    liste_action += n.action
                    return liste_action, n.cost
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
                                    n = Node(x, y + 1, liste_a_traite[0].depth + 1, liste_a_traite[0].cost + 3,
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
            cout = 0
            while n.previous is not None:
                cout += n.cost
                liste_action += n.action
                n = n.previous
            return liste_action, cout
        else:
            return "nothing", None

    # critère d'arret
    def amIAlive(self):
        return self.life

    # appel des capteurs
    def observeEnvironnmentWithAllMySensors(self):
        self.capteurs.observeEnvironment()

    # MAJ de l'etat de l'environnement
    def updateMyState(self):
        self.etatBDI["etatPiece"], self.etatBDI[
            "penitence"], self.posRobotX, self.posRobotY = self.capteurs.getObservations()
        self.etatBDI["nombreItem"] = 0
        for i in range(len(self.etatBDI["etatPiece"])):
            if self.etatBDI["etatPiece"][i]["dust"]:
                self.etatBDI["nombreItem"] += 1
            if self.etatBDI["etatPiece"][i]["diamond"]:
                self.etatBDI["nombreItem"] += 1

    # algo d'exploration
    def chooseAnAction(self):
        self.noInforme()
        self.informe()

    def justDoIt(self):
        # delai entre les actions du robot
        delai = 0.5

        self.plan = list(reversed(self.plan))
        for action in self.plan:
            if action == "droite":
                self.effecteurs.move_right()
                time.sleep(delai)
            elif action == "gauche":
                self.effecteurs.move_left()
                time.sleep(delai)
            elif action == "bas":
                self.effecteurs.move_forward()
                time.sleep(delai)
            elif action == "haut":
                self.effecteurs.move_backward()
                time.sleep(delai)
            elif action == "aspirer":
                self.effecteurs.vacuum()
                time.sleep(delai)
            elif action == "ramasser":
                self.effecteurs.pick()
                time.sleep(delai)
