from tkinter import *
from modele import *

DIM = 30
COULEURS = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "dark grey", "black"]
SUIVANT = 6

class VueTetris:
    
    def __init__(self, modele=ModeleTetris):
        self.__modele = modele
        self.__fenetre = Tk()
        
        # Partie Principale
        self.__can_terrain = Canvas(self.__fenetre, height=DIM * self.__modele.get_hauteur(), width=DIM * self.__modele.get_largeur())
        self.__can_terrain.pack(side=LEFT)
        self.__les_cases = [[None for _ in range(self.__modele.get_largeur())] for _ in range(self.__modele.get_hauteur())]
        for hauteur in range(len(self.__les_cases)):
            for largeur in range(len(self.__les_cases[hauteur])):
                rectangle = self.__can_terrain.create_rectangle(DIM * largeur, DIM * hauteur, DIM * (largeur+1), DIM * (hauteur+1), outline="gray", fill=COULEURS[self.__modele.get_valeur(hauteur, largeur)])
                self.__les_cases[hauteur][largeur] = rectangle
        
        # Partie Latérale
        self.__buttons_frame = Frame(self.__fenetre)
        Label(self.__buttons_frame, text="Forme suivante :").pack()
        self.__can_fsuivante = Canvas(self.__fenetre, height=DIM * SUIVANT, width=DIM * SUIVANT)
        self.__can_fsuivante.pack()
        self.__lbl_score = Label(self.__buttons_frame, text="Score : 0")
        self.__lbl_score.pack()
        self.__button_exit = Button(self.__buttons_frame, command=self.__fenetre.destroy, text="Quitter")
        self.__button_exit.pack()
        self.__les_suivants = [[None for _ in range(SUIVANT)] for _ in range(SUIVANT)]
        for h in range(SUIVANT):
            for l in range(SUIVANT):
                rectangle = self.__can_fsuivante.create_rectangle(DIM * l, DIM * h, DIM * (l+1), DIM * (h+1), outline="gray", fill=COULEURS[-1])
                self.__les_suivants[h][l] = rectangle
        self.__buttons_frame.pack()

    def fenetre(self):
        return self.__fenetre

    def dessine_case(self, l, c, coul):
        self.__can_terrain.itemconfigure(self.__les_cases[l][c], fill=COULEURS[coul])

    def dessine_terrain(self):
        for l in range(self.__modele.get_hauteur()):
            for c in range(self.__modele.get_largeur()):
                color = self.__modele.get_valeur(l, c)
                self.dessine_case(l, c, color)

    def dessine_forme(self, coords, couleur):
        for x, y in coords:
            self.dessine_case(y, x, couleur)
            
    def met_a_jour_score(self, val):
        self.__lbl_score["text"]="Score : "+str(val)
      
    def dessine_case_suivante(self, x, y, coul):
        self.__can_fsuivante.itemconfigure(self.__les_suivants[x][y], fill=COULEURS[coul])
        
    def nettoie_forme_suivante(self):
        for l in range(SUIVANT):
            for c in range(SUIVANT):
                self.dessine_case_suivante(l, c, -1)
                
    def dessine_forme_suivante(self, coords, coul):
        self.nettoie_forme_suivante()
        for x, y in coords:
            self.dessine_case_suivante(y+3, x+3, coul)
