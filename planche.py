from tkinter import Canvas, Tk, PhotoImage
from jeu import *
from compteur import *

class Planche(Canvas):
    def __init__(self, parent, largeur, hauteur, bombes):
        self.parent = parent
        self.margeH, self.margeV, self.margeN, self.margeS, self.margeE, self.margeW = 20, 65, 57, 8, 8, 12
        super().__init__(parent, width=largeur * 16 + self.margeH, height=hauteur * 16 + self.margeV)
        self.largeur, self.hauteur, self.bombes= largeur, hauteur, bombes
        self.img_cases = {'brique':PhotoImage(file='res/brique.gif', master=parent),
                          '-1': PhotoImage(file='res/-1.gif', master=parent),
                          '-1r': PhotoImage(file='res/-1r.gif', master=parent),
                          '0': PhotoImage(file='res/case.gif', master=parent),
                          'drapeau': PhotoImage(file='res/drapeau.gif', master=parent)}
        for i in range(1, 9):
            self.img_cases[str(i)] = PhotoImage(file='res/' + str(i) +'.gif', master=parent)
        self.img_cadre = {'NW': PhotoImage(file='res/coinNW.gif', master=parent),
                          'NE': PhotoImage(file='res/coinNE.gif', master=parent),
                          'SW': PhotoImage(file='res/coinSW.gif', master=parent),
                          'SE': PhotoImage(file='res/coinSE.gif', master=parent),
                          'N': PhotoImage(file='res/segmentN.gif', master=parent),
                          'W': PhotoImage(file='res/segmentW.gif', master=parent),
                          'E': PhotoImage(file='res/segmentE.gif', master=parent),
                          'S': PhotoImage(file='res/segmentS.gif', master=parent)}
        self.img_emoji = {'sourire': PhotoImage(file='res/ebase.gif', master=parent),
                          'sourire_appuye': PhotoImage(file='res/eappuye.gif', master=parent),
                          'wow': PhotoImage(file='res/ewow.gif', master=parent),
                          'mort': PhotoImage(file='res/emort.gif', master=parent),
                          'cool': PhotoImage(file='res/ecool.gif', master=parent)}

        self.bind('<Button-1>', self.glisser)
        self.bind('<Button-3>', self.drapeau)
        self.bind('<B1-Motion>', self.glisser)
        self.bind('<ButtonRelease-1>', self.clic)
        self.premier_clic_effectue = False
        self.jeu = Jeu(self.largeur, self.hauteur, self.bombes)
        self.drapeaux = []
        self.compteur_bombes = Compteur(self, False, self.parent)
        self.timer = Compteur(self, True, self.parent)
        self.partie_finie = False
        self.renitialiser()


    def glisser(self, event):
        self.delete('glisse')
        self.delete('wow')
        self.delete('appuye')
        if not self.partie_finie and not self.dans_emoji(event):
            self.create_image(8 * self.largeur - 1, 17, image=self.img_emoji['wow'], tags='wow', anchor='nw')
            if self.dans_grille(event):
                x, y = (event.x - self.margeW) // 16, (event.y - self.margeN) // 16
                if (self.largeur * y + x) not in self.jeu.cases_devoilees and (self.largeur * y + x) not in self.drapeaux:
                    self.create_image(16 * x + self.margeW, 16 * y + self.margeN, image=self.img_cases['0'], tags='glisse', anchor='nw')
        elif self.dans_emoji(event):
            self.create_image(8 * self.largeur - 1, 17, image=self.img_emoji['sourire_appuye'], tags='appuye', anchor='nw')


    def clic(self, event):
        self.delete('glisse')
        self.delete('wow')
        self.delete('appuye')
        if self.dans_grille(event) and not self.partie_finie:
            x, y = (event.x - self.margeW) // 16, (event.y - self.margeN) // 16
            if not self.premier_clic_effectue and (self.largeur * y + x) not in self.drapeaux:
                self.jeu = Jeu(self.largeur, self.hauteur, self.bombes, (x, y))
                self.premier_clic_effectue = True
                self.after(1000, self.timer.update_timer)
            if (self.largeur * y + x) not in self.jeu.cases_devoilees and (self.largeur * y + x) not in self.drapeaux:
                self.create_image(16 * x + self.margeW, 16 * y + self.margeN, image=self.img_cases[str(self.jeu.grille[self.largeur * y + x])], tags='devoilees', anchor='nw')
                if self.jeu.grille[self.largeur * y + x] == -1:
                    self.create_image(16 * x + self.margeW, 16 * y + self.margeN, image=self.img_cases['-1r'], tags='devoilees', anchor='nw')
                    self.create_image(8 * self.largeur - 1, 17, image=self.img_emoji['mort'], anchor='nw')
                    self.partie_finie = True
                cases_a_devoiler = self.jeu.devoiler(self.largeur * y + x)
                for case in cases_a_devoiler:
                    if case not in self.drapeaux:
                        self.create_image(16 * (case % self.largeur) + self.margeW, 16 * (case // self.largeur) + self.margeN, image=self.img_cases[str(self.jeu.grille[case])], tags='devoilees', anchor='nw')
        elif self.dans_emoji(event):
            self.renitialiser()

    def dans_grille(self, event):
        if self.margeW < event.x < self.margeW + 16*self.largeur and self.margeN < event.y < self.margeN + 16*self.hauteur:
            return True
        return False

    def dans_emoji(self, event):
        if 8*self.largeur - 1 < event.x < 8*self.largeur + 25 and 17 < event.y < 43:
            return True
        return False

    def drapeau(self, event):
        x, y = (event.x - self.margeW) // 16, (event.y - self.margeN) // 16
        if (self.largeur * y + x) in self.drapeaux:
            self.delete('drapeau'+str(x) + '_' + str(y))
            self.drapeaux.remove(self.largeur * y + x)
            self.compteur_bombes.incre()
        elif (self.largeur * y + x) not in self.jeu.cases_devoilees and not self.partie_finie and self.dans_grille(event):
            self.create_image(16 * x + self.margeW, 16 * y + self.margeN, image=self.img_cases['drapeau'], tags='drapeau'+str(x)+ '_' + str(y), anchor='nw')
            self.drapeaux += [self.largeur * y + x]
            self.compteur_bombes.decre()
            self.check_victoire()

    def check_victoire(self):
        self.delete('victoire')
        if len(self.drapeaux) == self.bombes and len(self.jeu.cases_devoilees) == self.largeur*self.hauteur-self.bombes:
            self.create_image(8 * self.largeur - 1, 17, image=self.img_emoji['cool'], tags='victoire', anchor='nw')
            self.partie_finie = False


    def construire_cadre(self, largeur, hauteur):
        self.create_image(0, 0, image=self.img_cadre['NW'], anchor='nw')
        self.create_image(largeur * 16 + self.margeH, 0, image=self.img_cadre['NE'], anchor='ne')
        self.create_image(0, hauteur * 16 + self.margeV, image=self.img_cadre['SW'], anchor='sw')
        self.create_image(largeur * 16 + self.margeH, hauteur * 16 + self.margeV, image=self.img_cadre['SE'], anchor='se')
        for case in range(3, largeur-3):
            self.create_image(self.margeW + case*16, 0, image=self.img_cadre['N'], anchor='nw')
            self.create_image(self.margeW + case * 16, hauteur * 16 + self.margeV, image=self.img_cadre['S'], anchor='sw')
        for case in range(hauteur):
            self.create_image(0, case * 16 + self.margeN, image=self.img_cadre['W'], anchor='nw')
            self.create_image(largeur * 16 + self.margeH, case * 16 + self.margeN, image=self.img_cadre['E'], anchor='ne')

    def renitialiser(self):
        self.delete('all')
        self.construire_cadre(self.largeur, self.hauteur)
        for i in range(self.largeur):
            for j in range(self.hauteur):
                self.create_image(16*i + self.margeW, 16*j + self.margeN, image=self.img_cases['brique'], tags='brique' + str(i) + '_' + str(j), anchor='nw')
        self.premier_clic_effectue = False
        self.drapeaux = []
        self.partie_finie = False
        self.compteur_bombes.placer(self.bombes)
        self.compteur_bombes.valeur = self.bombes
        self.timer.placer(0)
        self.timer.valeur = -1
        self.jeu = Jeu(self.largeur, self.hauteur, self.bombes)
        self.create_image(8*self.largeur - 1, 17, image=self.img_emoji['sourire'], anchor='nw')




