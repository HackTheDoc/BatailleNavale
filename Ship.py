from random import randint

class Ship:
    """Definie un bateau selon ses paramettres

    Attributs :
        self.length         : longueur du bateau
        self.hp             : points de vie du bateau (necessaire pour verifier sa destruction)
        self.orientation    : orientation aléatoire (Horizontal ou Vertical)
        self.coordinates    : liste de taille fixe des coordoonnées de chaques cases du bateau
    
    Methodes :
        getOrientation()    : accesseur de l'orientation actuelle du bateau
        setCoordinates(r,c) : permet de deffinir les coordonnées des cases du bateau à partir d'une case d'origine donnée
        getCoordinates()    : renvoie une liste de toute les coordonnées
        isTouched(r,c)      : permet de savoir si la case donnée appartiens au bateau (et donc s'il est touché)
        isDestroy()         : permet de savoir si le bateau n'a plus de vie
    """

    def __init__(self, length) -> None:
        
        # longueur du bateau
        self.length = length

        # vie du bateau
        self.hp = length

        # Orientation du bateau | 0 ou 1 | Horizontal ou Vertical
        ## Choix aléatoire de l'orientation du bateau
        self.orientation = randint(0, 1)

        # repertoire des coordonnées des cases du bateau
        self.coordinates =  [[None, None]]*self.length      # coordinates[numeroCase] = [rowIndex, columnIdex]


    def getOrientation(self):
        """Renvoie l'orientation du bateau (sous la forme binaire)"""
        return self.orientation


    def setCoordinates(self, case1_r, case1_c):
        """associe les coordonnees adequates à chaque case du bateau
         a partir des coordonnées x et y d'une case d'origine"""
        
        for i in range(self.length): # pour chaque case

            # Le Bateau est a l'horizontal
            if self.orientation == 0:
                self.coordinates[i] = [case1_r, case1_c+i]
            
            # Le bateau est a la vertical
            elif self.orientation == 1:
                self.coordinates[i] = [case1_r+i, case1_c]


    def getCoordinates(self):
        """Renvoie la liste des coordonnées de chaque case du bateau"""
        return self.coordinates


    def isTouched(self, r, c)->bool:
        """Dis si la case donnée appartiens à ce bateau"""

        # On regarde toute les coordonnées du bateau
        for coord in self.coordinates:
            # On verifie si les coordonnées correspondent :
            if [r,c] == coord:
                # Le bateau perd 1 HP
                self.hp -= 1

                # Ce bateau est touché
                return True
        
        # Ce bateau n'est pas touché
        return False


    def isDestroy(self):
        """Renvoie true si le bateau est detruit"""

        if self.hp == 0:
            return True
        return False
