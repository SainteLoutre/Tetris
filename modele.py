from random import randint
LES_FORMES=[[(-1, 1), (-1, 0), (0, 0), (1, 0)],
            [(-1, -1), (0,-1), (0, 0), (1, 0)],
            [(-1, 0), (0, 0), (0, -1), (1, -1)],
            [(-1, 0), (0, 0), (1, 0), (-1, 1)],
            [(-1, 0), (0, 0), (0, -1), (1, 0)],
            [(-1, -1), (0, -1), (0, 0), (-1, 0)],
            [(-2, 0), (-1, 0), (0, 0), (1, 0)]]

class ModeleTetris:
    
    def __init__(self, lignes=24, colonnes=14):
        self.__haut = lignes
        self.__larg = colonnes
        self.__base = 4
        self.__terrain = [[-2 if j<self.__base else -1 for i in range(self.__larg)] for j in range(self.__haut)]
        self.__forme = Forme(self)
        self.__suivante = Forme(self)
        self.__score = 0

    def get_largeur(self):
        return self.__larg

    def get_hauteur(self):
        return self.__haut
    
    def get_score(self):
        return self.__score

    def get_valeur(self, ligne, colonne):
        return self.__terrain[ligne][colonne]

    def est_occupe(self, ligne, colonne):
        return self.__terrain[ligne][colonne] >= 0

    def get_couleur_forme(self):
        return self.__forme.get_couleur()

    def get_coords_forme(self):
        return self.__forme.get_coords()
    
    def get_coords_suivante(self):
        return self.__suivante.get_coords_relatives()
    
    def get_couleur_suivante(self):
        return self.__suivante.get_couleur()
    
    def ajoute_forme(self):
        for x, y in self.__forme.get_coords():
            self.__terrain[y][x] = self.__forme.get_couleur()

    def forme_tombe(self):
        if not self.__forme.tombe():
            return False
        else:
            self.ajoute_forme()
            self.__forme = self.__suivante
            self.__suivante= Forme(self)
            self.supprime_lignes_completes()
            return True

    def fini(self):
        for i in range(self.__larg):
            if self.__terrain[self.__base][i] >= 0:
                return True
        return False
    
    def forme_a_gauche(self):
        self.__forme.a_gauche()
        
    def forme_a_droite(self):
        self.__forme.a_droite()
        
    def forme_tourne(self):
        self.__forme.tourne()
        
    def est_ligne_complete(self, lig):
        for i in range(self.get_largeur()):
            if not(self.est_occupe(lig, i)):
                return False
        return True
    
    def supprime_ligne(self, lig):
        for i in range(lig, self.__base + 1, -1):
            self.__terrain[i] = self.__terrain[i-1].copy()
        self.__terrain[self.__base]=[-1 for _ in range(self.get_largeur())]
    
    def supprime_lignes_completes(self):
        for i in range(self.__base, self.get_hauteur()):
            if self.est_ligne_complete(i):
                self.supprime_ligne(i)
                self.__score += 1

class Forme():
    
    def __init__(self, modele):
        a=randint(0, len(LES_FORMES)-1)
        self.__modele = modele
        self.__couleur = a
        self.__forme = LES_FORMES[a]
        self.__x0 = randint(2, self.__modele.get_largeur()-2)
        self.__y0 = 1

    def get_couleur(self):
        return self.__couleur
    
    def get_forme(self):
        return self.__forme

    def get_coords(self):
        res = []
        for offset in self.__forme:
            res.append((self.__x0 + offset[0], self.__y0 + offset[1]))
        return res
    
    def get_coords_relatives(self):
        return self.__forme[:]
        
    def collision(self):
        for offset in self.__forme:
            if self.__y0 + offset[1] >= self.__modele.get_hauteur() - 1:
                return True
            elif self.__modele.est_occupe(self.__y0 + offset[1] + 1, self.__x0 + offset[0]):
                return True
        return False

    def tombe(self):
        if not self.collision():
            self.__y0 += 1
            return False
        return True
    
    def position_valide(self):
        coords = self.get_coords()
        for x, y in coords:
            if (x < 0 or x >= self.__modele.get_largeur()) or (y < 0 or y >= self.__modele.get_hauteur()):
                return False
            if self.__modele.est_occupe(y, x):
                return False
        return True
    
    def a_gauche(self):
        if self.__x0 != 0:
            self.__x0 -= 1
            if not(self.position_valide()):
                self.__x0 += 1
                
    def a_droite(self):
        if self.__x0 != self.__modele.get_largeur():
            self.__x0 += 1
            if not(self.position_valide()):
                self.__x0 -= 1
    
    def tourne(self):
        forme_prec=self.__forme.copy()
        a=[]
        for tup in self.__forme:
            a.append((-tup[1], tup[0]))
        self.__forme=a
        if not(self.position_valide()):
            self.__forme=forme_prec
    
f=Forme(ModeleTetris())
f.tourne()