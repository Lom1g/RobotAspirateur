class Agent:
    def __init__(self):
        pass

    #attributs
    etatBDI = []

    #exploration non-informée
    def NonInforme(self):
        while(self.amIAlive()):
            self.OserveEnvironnmentWithAllMySensors()
            self.UpdateMyState()
            self.ChooseAnAction()
            self.JustDoIt()
        return self.etatBDI

    #exploration informée
    def Informe(self):
        pass

    #critère d'arret
    def amIAlive(self):
        pass

    #appel des capteurs
    def OserveEnvironnmentWithAllMySensors(self):
        pass

    #MAJ graph
    def UpdateMyState(self):
        pass

    #consultation du graph
    def ChooseAnAction(self):
        pass

    #déplacement
    #aspiration poussière
    #ramassage bijoux
    #MAJ BDI
    #performances
    #apprentissage épisodique
    def JustDoIt(self):
        pass
