from planche import *

class Compteur:
    def __init__(self, planche, timer, parent):
        self.planche = planche
        self.timer = timer
        if self.timer:
            self.coordx = self.planche.largeur*16 - 34
            self.valeur = 0
        else:
            self.coordx = 17
            self.valeur = self.planche.bombes
        self.coordy = 18
        self.img_compteur = {}
        for i in range(10):
            self.img_compteur[str(i)] = PhotoImage(file='res/c' + str(i) + '.gif', master=parent)

        self.placer(self.valeur)

    def placer(self, valeur):
        self.planche.delete('compteur' + str(self.timer))
        self.planche.create_image(self.coordx, self.coordy, image=self.img_compteur[str(valeur//100)],
                          tags='compteur' + str(self.timer), anchor='nw')
        self.planche.create_image(self.coordx + 13, self.coordy, image=self.img_compteur[str((valeur % 100)//10)],
                                  tags='compteur' + str(self.timer), anchor='nw')
        self.planche.create_image(self.coordx + 26, self.coordy, image=self.img_compteur[str(valeur % 10)],
                                  tags='compteur' + str(self.timer), anchor='nw')

    def decre(self):
        self.valeur -=1
        self.placer(self.valeur)

    def incre(self):
        self.valeur += 1
        self.placer(self.valeur)

    def update_timer(self):
        self.valeur += 1
        self.placer(self.valeur)
        if self.planche.premier_clic_effectue and not self.planche.partie_finie:
            self.planche.after(1000, self.update_timer)