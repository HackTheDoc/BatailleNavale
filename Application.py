import tkinter as tk
from Tools import Tools
from Player import Player

class Application:
    """Classe représentant l'Application, permet sa création et son fonctionnement logique
    
    Attributs :
        self.root               : la fenetre du jeu
        self.player1            : l'object joueur 1
        self.player2            : l'object joueur 2
        self.currentPlayerName  : nom du joueur qui joue actuellement
        self.tools              : object des outils (boutons et boite d'information)
    
    Methodes :
        createPlayer(name, playerNumber)    : permet la creation d'un joueur (de sa grille et le placement de ses bateaux)
        createTools()                       : permet la creation des outils
        setWidgetText(widgetName, text)     : permet la modification du texte d'un label de l'application
        setButtonState(buttonName, state)   : permet d'activer et désactiver un bouton
        changeCurrentPlayerName()           : permet de changer le nom du joueur qui joue lors du changement de tour
        victory()                           : ouvre une fenetre pop-up permettant d'afficher le gagnant
        isWinner()                          : permet de savoir si le joueur du tour actuel a gagné et de changer de tour
        validAction()                       : permet de valider une action du joueur (lorsque l'on clique sur "VALIDER")
        startGame()                         : permet le lancement de la phase de jeu
        runt()                              : lance l'application
    """

    def __init__(self, title="Application", size="480x320", rezisable=True) -> None:
        """Création et lancement de l'application comme étant une fenetre du module tkinter"""

        # Configuration du Root de l'application (fenetre principale)
        self.root = tk.Tk()
        self.root.title(title.title())
        self.root.geometry(size)
        self.root.resizable(rezisable, rezisable)

        # Création du JOUEUR 1
        self.player1 = self.createPlayer(name="joueur 1", playerNumber=1)
        ## Placement des bateaux du joueur
        self.player1.placeBoats()

        # Creation du JOUEUR 2
        self.player2 = self.createPlayer(name="joueur 2", playerNumber=2)
        ## Placement des bateaux du joueur
        self.player2.placeBoats()

        # Nom du joueur qui joue le tour courrant
        ## On commence avec le joueur 1
        self.currentPlayerName = "joueur 1"

        # Création des outils
        self.tools = self.createTools()

        # Lancement de l'application
        self.run()
    

    def createPlayer(self, name, playerNumber:int):
        """Créé un joueur"""

        # Defini la position du plateau de ce joueur sur l'application
        ## Position GAUCHE
        if playerNumber == 1:
              position = 'gauche'
        
        ## Position DROITE
        elif playerNumber == 2:
                position = 'droite'
        
        ## Position invalide
        else:
                print("LogError : Création d'un joueur inutile (en trop)")

        # Création du joueur
        player = Player(app=self, master=self.root, name=name, position=position)

        return player


    def createTools(self):
        """Creation de la frame des outils et creation/parametrage de ces derniers"""
        
        # Creation de la frame
        tools = Tools(self, self.root)

        # Creation des outils de la phase de jeu
        tools.createPlayPhaseTools()

        # retour de la frame paramettrée
        return tools


    def setWidgetText(self, widgetName , text):
        """Modifie le texte d'un label en fonction du nom de ce dernier'"""
        
        # Modification de l'affichage d'un widget indicant le nombre de bateau restant
        if widgetName == 'lbl_boats':

            widgetName += "_"+self.currentPlayerName
            text = self.currentPlayerName.title() + "\n" + str(text)

            widget = self.tools.getTool(widgetName)
            widget.configure(text= text)

        # Modification de l'affichage d'un autre widget
        else:
            widget = self.tools.getTool(widgetName)
            widget.configure(text= text)


    def setButtonState(self, buttonName, state):
        """2 state différents : 'normal' ou 'disable'"""

        widget = self.tools.getTool(buttonName)
        widget.configure(state= state)


    def getCurrentPlayerName(self):
        """Renvoie le nom du joueur qui joue actuellement le tour"""
        
        return self.currentPlayerName


    def changeCurrentPlayer(self):
        """On passe au tour du joueur suivant"""

        # Si c'est le JOUEUR 1 qui jouait :
        if self.currentPlayerName == "joueur 1":

                # On désactive la grille du joueur 1
                self.player1.configureBoard(state= 'disable')
                # On active la grille du joueur 2
                self.player2.configureBoard(state= 'enable')
                # On change le nom du joueur qui joue
                self.currentPlayerName = "joueur 2"
                self.setWidgetText("lbl_current_player", "Tour De\n"+self.currentPlayerName.upper())

        # Si c'est le JOUEUR 2 qui jouait :  
        elif self.currentPlayerName == "joueur 2":

                # On désactive la grille du joueur 2
                self.player2.configureBoard(state= 'disable')
                # On active la grille du joueur 1
                self.player1.configureBoard(state= 'enable')
                # On change le nom du joueur qui joue
                self.currentPlayerName = "joueur 1"
                self.setWidgetText("lbl_current_player", "Tour De\n"+self.currentPlayerName.upper())


    def victory(self):
        """Fin du JEU : affichage du gagnant"""

        # Configuration de la fenetre du gagnant
        victoryWindow = tk.Toplevel(self.root)
        victoryWindow.geometry("480x320")
        victoryWindow.title("Bataille Navale : Gagnant")
        victoryWindow.resizable(False, False)

        # Création des components de la fenetre
        lbl = tk.Label(
            master= victoryWindow,
            text= "Le Vainqueur est :\n" + self.currentPlayerName.upper(),
            font= (None, 22),
            relief= 'ridge',
            bd= 10,
            height= 5
        )

        btn = tk.Button(
            master= victoryWindow,
            text= "QUITTER",
            font= (None, 22),
            command= self.root.destroy
        )

        # Affichage des components
        lbl.pack(fill= 'both', expand= True, padx= 10, pady= 10)
        btn.pack(fill='both', expand=True, padx= 10, pady= 10)


    def isWinner(self):
        """regarde si le joueur actuel a gagné"""

        # Si c'est le JOUEUR 1
        if self.currentPlayerName == "joueur 1":

            # On regarde combien de bateau il reste
            nbBoats = self.player1.getRemainingBoatsNumber()

            # Si le joueur 1 a détruit tout les bateaux :
            if nbBoats == 0:
                # On affiche les bateaux encore en vie de l'adversaire
                self.player2.showAliveBoats()

                # On affiche que le joueur a gagner
                self.victory()
        
        # Si c'est le JOUEUR 2
        elif self.currentPlayerName == "joueur 2":

            # On regarde combien de bateau il reste
            nbBoats = self.player2.getRemainingBoatsNumber()

            # Si le joueur 2 a détruit tout les bateaux :
            if nbBoats == 0:
                # On affiche les bateaux encore en vie de l'adversaire
                self.player1.showAliveBoats()

                # On affiche que le joueur a gagner
                self.victory()
        
        # Si AUCUN vainqueur
        return False


    def validAction(self):
        """validation de l'action du joueur (et mise en effet)"""

        # Si c'est le joueur 1 qui joue
        if self.currentPlayerName == "joueur 1":
            # Le joueur 1 attaque
            self.player1.attack()

            # On change de joueur
            self.changeCurrentPlayer()
        
        # Si c'est le joueur 2 qui joue
        elif self.currentPlayerName == "joueur 2":
            # Le joueur 2 attaque
            self.player2.attack()

            # On change de joueur
            self.changeCurrentPlayer()


    def startGame(self):
        """lancement de la phase de jeu"""

        # Affichage des components
        self.player1.display()
        self.tools.display()
        self.player2.display()

        # On active la grille du joueur qui commence
        self.player1.configureBoard(state= 'enable')
        # et désactive celle de l'autre joueur
        self.player2.configureBoard(state= 'disable')


    def run(self):
        """Charge les elements de l'application avant de la lancer"""

        # Lancement de la phase de jeu
        self.startGame()
        
        # Lance l'application
        self.root.mainloop()


# Creation de l'application
## Taille de la fenetre pour une grille seulement : 510x500
## Taille de la fenetre pour les outils seulement : 215x500

app = Application("Bataille Navale", "1235x500", False)
