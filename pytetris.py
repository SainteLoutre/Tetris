from modele import *
from vue import *
#import time

class Controleur:
    
    def __init__(self, modele=ModeleTetris):
        self.__tetris = modele
        self.__vue = VueTetris(self.__tetris)
        self.__fen = self.__vue.fenetre()
        self.__fen.bind("<Key-Left>",self.forme_a_gauche)
        self.__fen.bind("<Key-Right>",self.forme_a_droite)
        self.__fen.bind("<Key-Down>",self.forme_tombe)
        self.__fen.bind("<Key-Up>",self.forme_tourne)
        self.__delai = 320
        self.joue()
        self.__fen.mainloop()

    def joue(self):
        """
        Controleur -> None
        boucle principale du jeu. Fait tomber une forme d'une ligne.
        """
        if not self.__tetris.fini():
            self.affichage()
        self.__fen.after(self.__delai, self.joue)

    def affichage(self):
        if self.__tetris.forme_tombe():
            self.__delai=320        
        self.__vue.dessine_terrain()
        self.__vue.dessine_forme(self.__tetris.get_coords_forme(), self.__tetris.get_couleur_forme())
        self.__vue.met_a_jour_score(self.__tetris.get_score())
        self.__vue.dessine_forme_suivante(self.__tetris.get_coords_suivante(), self.__tetris.get_couleur_suivante())

    def forme_a_gauche(self, event):
        self.__tetris.forme_a_gauche()
        
    def forme_a_droite(self, event):
        self.__tetris.forme_a_droite()
        
    def forme_tombe(self, event):
        self.__delai=170
        
    def forme_tourne(self, event):
        self.__tetris.forme_tourne()
        
if __name__ == "__main__":
    # création du modèle
    tetris = ModeleTetris()
    # création du contrôleur. c’est lui qui créé la vue
    # et lance la boucle d'écoute des évts
    ctrl = Controleur(tetris)