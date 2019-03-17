from tkinter import Canvas, PhotoImage
from planche import *
from tkinter.filedialog import askopenfilename

class Options(Canvas):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, width=500, height=40)
        self.pack()
        self.planche = Planche(parent, 16, 16, 40)
        self.planche.pack()
        self.bind('<ButtonRelease-1>', self.clic)
        self.img_options = PhotoImage(file='res/options.gif', master=parent)
        self.create_image(0, 0, image=self.img_options, anchor='nw')

    def clic(self, event):
        if 0 <= event.x < 100:
            self.planche.destroy()
            self.planche = Planche(self.parent, 9, 9, 10)
            self.planche.pack()
        elif 100 <= event.x < 200:
            self.planche.destroy()
            self.planche = Planche(self.parent, 16, 16, 40)
            self.planche.pack()
        elif 200 <= event.x < 300:
            self.planche.destroy()
            self.planche = Planche(self.parent, 32, 16, 99)
            self.planche.pack()
        elif 300 <= event.x < 400:
            self.planche.destroy()
            self.planche = Planche(self.parent, 48, 48, 399)
            self.planche.pack()
        elif 400 <= event.x < 500:
            self.gugusse_fichier()

    def gugusse_fichier(self):
        filename = askopenfilename()
        file = open(filename, 'r')
        grille = file.readline()
        self.planche.destroy()
        self.planche = Planche(self.parent, int(grille[1]), int(grille[3]), grille.count('*'), True, grille)
        self.planche.pack()