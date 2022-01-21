import tkinter as tk

class Tools:
    """Systeme de création et affichage des labels et boutons de l'application
    
    Attributs :
        self.app    : application a laquelle appartient le systeme
        self.mainFrame      (frame)
        self.labelFrame     (frame)
        self.labelRepertory (list)
        self.boatsFrame     (frame)
        self.boatsRepertory (list)
        self.caseFrame      (frame)
        self.caseRepertory  (list)
        self.buttonFrame    (frame)
        self.buttonRepertory(list)
        self.repertory      (dict)
    
    Methodes :
        createPlayPhaseTools()  : creation automatique de tout les boutons
        display()               : permet l'affichage de tout les widgets selon un paterne définie
        getTool(toolName)       : permet d'obtenir un widget selon son nom (ex: pour le modifier)
    """

    def __init__(self, app, master) -> None:
    
        # Application à laquelle appartiennent les outils
        self.app = app

        # Frame principale (qui comprend tout le reste)
        self.mainFrame = tk.Frame(
            master= master
        )

        # Frame des labels
        self.labelFrame = tk.Frame(
            master= self.mainFrame
        )
        ## Repertoir des labels
        self.labelRepertory = []

        # Frame relative au nombre de bateaux restant de chaque joueur
        self.boatsFrame = tk.LabelFrame(
            master= self.mainFrame,
            text= "-- BATEAUX RESTANT --",
            labelanchor= 'n'
        )
        ## Repertoire des labels des bateaux restant
        self.boatsRepertory = []

        # Frame relative aux coordonnées de la case selectionnée
        self.caseFrame = tk.LabelFrame(
            master= self.mainFrame,
            text= "-- CASE SELECTIONNEE --",
            labelanchor= 'n'
        )
        ## Repertoire des labels des coordonnées
        self.caseRepertory = []

        # Frame des bouttons
        self.buttonFrame = tk.Frame(
            master= self.mainFrame
        )
        ## Repertoire des bouttons
        self.buttonRepertory = []

        # Repertoire complet de tout les outils selon leur nom
        self.repertory = {}


    def createPlayPhaseTools(self):
        """Création des outils nécéssaire à la phase de jeu"""

        def createLabel(master, text="None"):
            """Creer et retourne un label"""

            lbl = tk.Label(
                master= master,
                text= text,
                font= (None, 12),
                relief= "ridge",
                bd = 4,
                height=2
            )

            return lbl
        
        def createButton(master, text="None", command=None):
            """Creer un bouton et l'ajoute au repertoire des boutons de la frame"""

            btn = tk.Button(
                master= master,
                text= text,
                font= ( None, 24),
                command= command
            )

            return btn
        
        # Label sur la phase en cours :
        lbl = createLabel(master= self.labelFrame, text= "                 Phase De                 \nJEU")
        self.labelRepertory.append(lbl)
        self.repertory["lbl_gamephase"] = lbl

        # Label sur le joueur qui doit jouer
        player = self.app.getCurrentPlayerName()
        lbl = createLabel(master= self.labelFrame, text= "Tour De\n"+player.upper())
        self.labelRepertory.append(lbl)
        self.repertory["lbl_current_player"] = lbl

        # Label informatif sur l'action réalisé / à réalisé
        lbl = createLabel(master= self.labelFrame, text="Sélectionnez\nune case où jouer.")
        self.labelRepertory.append(lbl)
        self.repertory["lbl_information"] = lbl

        # Labels informatifs sur le nombre de bateaux restant de chaque joueur
        ## Joueur 1
        lbl = createLabel(master= self.boatsFrame, text="Joueur 1\n5")
        self.boatsRepertory.append(lbl)
        self.repertory["lbl_boats_joueur 1"] = lbl
        ## Joueur 2
        lbl = createLabel(master= self.boatsFrame, text="Joueur 2\n5")
        self.boatsRepertory.append(lbl)
        self.repertory["lbl_boats_joueur 2"] = lbl


        # Coordonnées de la case sélectionnée
        ## Row
        lbl = createLabel(master= self.caseFrame, text= "A")
        self.caseRepertory.append(lbl)
        self.repertory["row"] = lbl
        ## Column
        lbl = createLabel(master= self.caseFrame, text= "1")
        self.caseRepertory.append(lbl)
        self.repertory["column"] = lbl

        # Bouton VALIDER
        btn = createButton(master= self.buttonFrame, text= "VALIDER", command= self.app.validAction)
        self.buttonRepertory.append(btn)
        self.repertory["btn_validation"] = btn
        ## Rien à valider au début
        self.repertory["btn_validation"].configure(state= "disable")

        # Bouton QUITTER
        btn = createButton(master= self.buttonFrame, text= "QUITTER", command= self.app.root.destroy)
        self.buttonRepertory.append(btn)
        self.repertory["btn_quit"] = btn
    

    def display(self):
        """Affichage des outils et frame d'outils, ainsi que de la frame principale"""

        def show(object, row=0, column=0, pady=0, padx=0, ipadx=0, sticky='ew'):
            """Affiche un objet a une position row et column donnee, selon certains parametre pouvant etre modifié"""

            object.grid(row= row, column= column, pady= pady, padx= padx, ipadx= ipadx, sticky= sticky)
        

        # Affichage des frames
        show(object= self.mainFrame, row= 0, column= 1)
        show(object= self.labelFrame, row= 0, column= 0)
        show(object= self.boatsFrame, row= 1, column= 0)
        show(object= self.caseFrame, row= 2, column= 0)
        show(object= self.buttonFrame, row= 3, column= 0)
        
        # Affichage des labels
        for i in range(len(self.labelRepertory)):
            lbl = self.labelRepertory[i]
            show(object= lbl, row= i, pady= 8, sticky='nsew')
        
        # Affichage du nombre de bateaux restant de chaque joueur
        for i in range(len(self.boatsRepertory)):
            lbl = self.boatsRepertory[i]
            show(object= lbl, column= i, pady= 8, padx= 10, ipadx=6)

        # Affichage des coordonnées de la case sélectionnée
        for i in range(len(self.caseRepertory)):
            lbl = self.caseRepertory[i]
            #show(object= lbl, column= i, pady= 6, padx= 14, ipadx= 28)
            lbl.pack(side= 'left', expand=True, fill='x', padx= 8, pady= 6)
        
        # Affichage des bouttons
        for i in range(len(self.buttonRepertory)):
            btn = self.buttonRepertory[i]
            show(object= btn, row= i, pady= 4, ipadx=24, sticky='nsew')


    def getTool(self, toolName):
        """renvoie un outils (label ou bouton) en fonction de son nom"""
        return self.repertory[toolName.lower()]
