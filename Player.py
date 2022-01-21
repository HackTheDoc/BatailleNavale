from random import randint
import tkinter as tk
from Ship import Ship

class Player:
    """Classe représentant 1 joueur de bataille navale et sa grille
    
    Attributs :
        self._GRID_SIZE : taille de la grille (constante)
        self._SHIPS     : dictionnaire permettant de définir quels bateaux seront utilisés et de leur donné une taille (constante)
        self.name
        self.frame
        self.position   : position de la frame sur l'application
        self.waterColor
        self.selectionColor
        self.missColor
        self.touchedColor
        self.destroyColor
        self.aliveColor
        self.grid       : grille permettant le placement des bateaux et de verifier si les bateaux sont touchés
        self.board      : grille de Button permettant l'affichage de la grille, bateaux cachés, dans l'application
        self.selectedCaseCoordinates    : coordonnées de la case sélectionnée
        self.boatsRepertory             : enregistre les objects bateaux selon leur noms
    
    Methodes :
        createBoard()                   : creation du plateau d'affichage
        configureBoard(state)           : active/desactive les cases du plateau
        selectCase(r, c)                : permet de gerer le comportement à adapter lorsque le joueur sélectionne une case
        attack()                        : permet de tirer sur une case
        saveShipCoordinatesInGrid(ship) : permet d'enregistrer la position des bateaux dans la variable self.grid
        placeBoat()                     : placement automatique de tout les bateaux à une position aléatoire
        getRemainingBoatsNumber()       : accesseur permettant de savoir combien de joueur il reste au joueur (pour l'afficher)
        display()                       : affiche le plateau dans l'application selon la position self.position
        showAliveBoats()                : affiche les bateaux encore vivant à la fin de la partie
    """

    # Variables Constantes
    _GRID_SIZE = 10
    # format _SHIP = {"shipName":shipSize}
    _SHIPS = {"porte-avion":5, "croiseur":4, "sous-marin 1":3, "sous-marin 2":3, "torpilleur":2}

    def __init__(self, app, master, name, position) -> None:

        self.name = name

        # Application a laquelle le joueur appartient
        self.app = app

        # Creation de la frame (element graphique) contenant la grille
        self.frame = tk.LabelFrame(
            master= master,
            text= "--- " + name.upper() + " ---",
            labelanchor= 'n'
        )
        ## Position de la frame sur l'application
        self.position = position

        # Variables de couleurs :
        self.waterColor = "#00bfff" 
        self.selectionColor = "#0066cc"
        self.missColor = "#000000"
        self.touchedColor = "#ff0000"
        self.destroyColor = "#ff0000"
        self.aliveColor = "#00ff00"
        
        # Creation de la grille (variable tableau en 2 dimension)
        ## 0 représente une case vide | 1 une case de bateau | -1 une case où on ne peut pas placer de bateau
        self.grid = [[0]*self._GRID_SIZE for x in range(self._GRID_SIZE)]
        ## Plateau de jeu (grille qui s'affiche)
        self.board = self.createBoard()

        # Case selectionnée (par défaut aucune donc [-1, -1])
        self.selectedCaseCoordinates = [-1, -1]

        # Répertoire des bateaux
        self.boatsRepertory = {}


    def createBoard(self):
        """Creation de la grille (composee de boutons)"""

        # Creation de la grille vide
        grid = [ [tk.Button]*self._GRID_SIZE for _ in range(self._GRID_SIZE) ]

        for r in range(self._GRID_SIZE): # pour chaque ligne (row)
            # Indexage des Lignes
            tk.Label(master= self.frame, text= chr(65+r) ).grid(row= r+1, column= 0)
            ## Rajoute une marge interne au cadre de la frame (pour l'aspect visuel)
            tk.Label(master= self.frame, text= "   " ).grid(row= r+1, column= 11)

            # Indexage des Colonnes
            tk.Label(master= self.frame, text= r+1 ).grid(row= 0, column= r+1)
            ## Rajoute une marge interne au cadre de la frame (pour l'aspect visuel)
            tk.Label(master= self.frame, text= "" ).grid(row= 11, column= r+1)
        
            for c in range(10): # pour chaque colonne (column)
                
                # Creation d'une case (sous forme de bouton)
                case = tk.Button(
                    master= self.frame,
                    text= "",
                    relief= "solid",
                    font= (None, 16),
                    background= self.waterColor,
                    foreground= self.waterColor,
                    command= lambda row=r, column=c: self.selectCase(row, column),
                    width= 3
                )
                
                # Assigne la case dans la grille
                grid[r][c] = case

                # Affichage de la case
                case.grid(row=r+1, column=c+1)

        # retourne la grille pour pouvoir la modifier/reutiliser
        return grid


    def configureBoard(self, state:str):
        """Permet d'activer/desactiver la grille:
        'enable', 'disable'"""

        if state.lower() == 'enable':

            # On active la grille (on peut sélectionner une case)
            for row in range(self._GRID_SIZE):
                for column in range(self._GRID_SIZE):

                    # On récupère la case concernée
                    case = self.board[row][column]
                    
                    # On active la case
                    case.configure(state= "normal")
        
        elif state.lower() == 'disable':

            # On désactive la grille (on NE peut PAS sélectionner une case)
            for row in range(self._GRID_SIZE):
                for column in range(self._GRID_SIZE):

                    # On récupère la case concernée
                    case = self.board[row][column]
                    
                    # On désactive la case
                    case.configure(state= "disable")
        
        else:
            # Une entrée est invalide
            print("LogError player.grid.configure : Unknow Entry")


    def selectCase(self, r, c):
        """permet au systeme de réagir avec la case séléctionnée"""

        def showSelectedCase(r, c):
            """Permet l'affichage de la case sélectionée"""

            # Reset la couleur de l'ancienne case selectionnée
            oldCase = self.board[ self.selectedCaseCoordinates[0] ][ self.selectedCaseCoordinates[1] ]
            oldCase.configure(bg = self.waterColor)
            
            # Modification de la couleur de la nouvelle case selectionnée
            newCase = self.board[r][c]
            self.selectedCaseColor = newCase["background"]
            newCase.configure(bg= self.selectionColor)

            # Enregistrement des coordonnées de la case selectionnée
            self.selectedCaseCoordinates = [r, c]

            ## Affichage des coordonnées de la case sélectionnée
            self.app.setWidgetText("row", chr(65+r))
            self.app.setWidgetText("column", str(c+1))
        
        
        # on récupère d'abord la case concernée
        case = self.board[r][c]

        # Si la case est marquée d'un X
        if case["text"] == "X":
            # Alors la case a déjà été jouée et on ne fait rien
            pass

        else:
            # Alors la case n'a PAS ENCORE été jouée et on peut l'affiché et la jouée
            showSelectedCase(r, c)
            self.app.setButtonState("btn_validation", "normal")

            # On modifie aussi le texte de la box d'information
            self.app.setWidgetText("lbl_information", "Sélectionnez\nune case où jouer.")


    def attack(self):
        """permet d'attaquer la case sélectionnée"""

        def isBoatTouched(row, column):
            """Renvoie le nom du bateau touché, si aucun bateau n'est touché on renvoie 'None'"""

            # Aucun bateau touché
            touchedBoat = "None"

            if self.grid[row][column] == 1:
                # Un bateau est touché !
                print(f"Log : bateau touché en {chr(65+row)}, {column+1}")

                # On cherche a savoir quel bateau a été touché
                for boat in self.boatsRepertory:
                    # On récupère le bateau en question
                    ship = self.boatsRepertory[boat]

                    # Si le bateau en question est touché
                    if ship.isTouched(r, c) == True:
                        touchedBoat = boat

            return touchedBoat
        
        # On recupere la case visée
        r,c = self.selectedCaseCoordinates
        case = self.board[r][c]

        
        # On désactive le bouton valider (plus rien à valider)
        self.app.setButtonState("btn_validation", "disable")
        # et on enlève l'affichage de la case sélectionnée
        case.configure(background= self.waterColor)
        ## et on désélectionne la case
        self.selectedCaseCoordinates = [-1,-1]

        # Si aucun bateau n'est touché :
        boat = isBoatTouched(r,c)
        if boat == "None":
            # On affiche l'endroit ou on à joué
            case.configure(text= "X", foreground= self.missColor)
            # Et on affiche dans la boite d'information que le tir est raté
            text = "Vous avez raté\nvotre tir !"
            self.app.setWidgetText("lbl_information", text)

        # Si un bateau est touché :
        else:
            # Si le bateau est detruit :
            ship = self.boatsRepertory[boat]
            if ship.isDestroy() == True:

                # On affiche le bateau comme détruit
                coords = ship.getCoordinates()

                for coord in coords:
                    r, c = coord
                    self.grid[r][c] = 2
                    # Modification de l'affichage
                    case = self.board[r][c]
                    case.configure(text= "X", background=self.destroyColor, foreground=self.missColor)
                
                # et quel bateau est detruit
                text = "Vous avez détruit le\n" + boat.upper()
                self.app.setWidgetText("lbl_information", text)

                # on enleve le bateau du repertoire
                self.boatsRepertory.pop(boat)

                # On change l'affichage du nombre de bateau restant à detruire
                self.app.setWidgetText("lbl_boats", len(self.boatsRepertory))

            
            # Si le bateau n'est PAS detruit :
            else:
                # On affiche l'endroit ou on a touché le bateau
                case.configure(text= "X", foreground= self.touchedColor)
                # et quel bateau est touché
                text = "Vous avez touchez le\n" + boat.title()
                self.app.setWidgetText("lbl_information", text)
        
        # On regarde si on a un gagnant
        self.app.isWinner()


    def saveShipCoordinateInGrid(self, ship:Ship):
        """Enregistre les coordonnées d'un bateau donné dans la grille"""

        # Récupération des coordonnées du bateau
        coordinates = ship.getCoordinates()
                
        # On enregistre les cases DU BATEAU
        for case in coordinates:
            # on récupère les coordoonées de la case
            r, c = case

            # On modifie la valeur de la case associé dans la grille
            ## 1 pour dire que la case appartient à un bateau
            self.grid[r][c] = 1


    def placeBoats(self):
        """Création automatique des bateaux du joueur et placement de ces bateaux à des endroits aléatoires"""
        
        def isEmptyCase(row, column):
            """Renvoie True si la case de coordonnée donnée est vide, sinon False"""
            isEmpty = True

            try:
                if self.grid[row][column] == 1:
                    isEmpty = False
            except:
                isEmpty = True
            
            return isEmpty

        def searchLocations(boatLength, boatOrientation)->list:
            """Cherche les positions disponible pour un bateau donné
            et renvoie la liste des coordonnées de case d'origine de ces positions"""
            # Répertoire des coordonnées de case d'origines de chaques positions disponibles
            emptyPositions = [] 
            
            # Tant que aucune position n'est trouvé on essaye
            while len(emptyPositions) == 0:

                # Si le bateau est à l'HORIZONTAL
                if boatOrientation == 0:
                    # Pour chaque ligne
                    for row in range(self._GRID_SIZE):
                        # Pour chaque case de la ligne ou la case d'origine peut être placé
                        for column in range(self._GRID_SIZE - boatLength + 1):
                            while True:
                                # Par defaut la position est valide
                                isValidPosition = True

                                # On regarde toute les cases ou il ne doit pas y avoir de bateau
                                for r in range(row-1, row+2):
                                    for c in range(column-1, column+boatLength+2):

                                        # Si on est bien dans la grile
                                        if r != -1 and c != -1:
                                            isValidPosition = isEmptyCase(r, c)

                                        
                                        # Si la case est occupé on passe à la position suivante
                                        if isValidPosition == False:
                                            break
                                    
                                    if isValidPosition == False:
                                        break
                                
                                if isValidPosition == False:
                                    break  
                                elif isValidPosition == True:
                                    emptyPositions.append([row, column])
                                    break

                # Si le bateau est à la VERTICAL
                elif boatOrientation == 1:
                    
                    for column in range(self._GRID_SIZE):
                        # Pour chaque case de la colonne ou la case d'origine peut être placé
                        for row in range(self._GRID_SIZE- boatLength + 1):
                            while True:
                                # Par defaut la position est valide
                                isValidPosition = True

                                # On regarde toute les cases ou il ne doit pas y avoir de bateau
                                for r in range(row-1, row+boatLength+2):
                                    for c in range(column-1, column+2):

                                        # Si on est bien dans la grile
                                        if r != -1 and c != -1:
                                            isValidPosition = isEmptyCase(r, c)

                                        
                                        # Si la case est occupé on passe à la position suivante
                                        if isValidPosition == False:
                                            break
                                    
                                    if isValidPosition == False:
                                        break
                                
                                if isValidPosition == False:
                                    break
                                elif isValidPosition == True:
                                    emptyPositions.append([row, column]) 
                                    break


                
                # Si aucune position trouvé, on change l'orientation du bateau
                if len(emptyPositions):
                    if boatOrientation == 0:
                        boatOrientation = 1
                    else:
                        boatOrientation = 0

            # Retourne la liste des positions possibles (des cases d'origines)
            return emptyPositions

        def createShip(length):
            """Place un bateau d'une taille donnée à une position aléatoire sur la grille"""

            # Création du bateau
            ship = Ship(length)
            
            # Récupération des positions possible du bateau
            boatOrientation = ship.getOrientation()
            emptyPositions = searchLocations(length, boatOrientation)

            # Choix aléatoire d'une position parmis la liste des positions possibles
            position = emptyPositions[randint(0, len(emptyPositions)-1)]
            r, c = position

            # Attribution des coordonnées au bateau
            ship.setCoordinates(r, c)

            # Enregistrement des coordonnées dans la grille
            self.saveShipCoordinateInGrid(ship)

            return ship

        
        # Création des bateaux selon leur taille
        for name, size in self._SHIPS.items():
            ship = createShip(size)
            self.boatsRepertory[name] = ship
        
        # Placement des bateaux réussit !
        print(f"Log {self.name}: Placement des bateaux reussit")


    def getRemainingBoatsNumber(self):
        """renvoie le nombre de bateau restant"""

        return len(self.boatsRepertory)


    def display(self):
        """Format position : 'droite' ou 'gauche'
        \naffiche la grille sur l'application"""


        """
        # AFFICHAGE CONSOLE DE LA GRILLE - DESACTIVE

        print("Log: grille du", self.name.upper())
        for r in range(self._GRID_SIZE):
            print(" ".join(str(c) for c in self.grid[r]))
        """

        # Affichage de la grille sur l'APPLICATION
        ## Si on affiche à droite :
        if self.position == 'droite':
            self.frame.grid(row=0, column=2, padx=8, pady=8)
        
        ## Si on affiche à gauche
        elif self.position == 'gauche':
            self.frame.grid(row=0, column=0, padx=8, pady=8)
        
        ## Si la position donnée est invalide
        else:
            print("LogError : Position d'affichage de la grille invalide")


    def showAliveBoats(self):
        """affiche sur le plateau les bateaux encore en vie"""

        # Pour chaque bateau :
        for boat in self.boatsRepertory:

            # On recupere le bateau en question
            ship = self.boatsRepertory[boat]

            # Pour chaque case du bateau :
            coords = ship.getCoordinates()
            for coord in coords:

                # On recupere la case concernée
                r,c = coord
                case = self.board[r][c]

                # Si la case a été touchée
                # donc on a tirer sur cette case
                if case["text"] == "X":
                    # On change l'affichage de la case pour montrée qu'elle a été touchée
                    case.configure(background= self.touchedColor, foreground= self.aliveColor)
                
                # Sinon, la case en question n'a pas été jouée
                # donc on a pas tirer sur cette case
                else:
                    # On affiche la case vivante
                    case.configure(background= self.aliveColor)
