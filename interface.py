from planche import *


class Interface(Tk):
    def __init__(self):
        super().__init__()
        planche = Planche(self, 15, 15, 38)
        planche.pack()
