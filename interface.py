from planche import *


class Interface(Tk):
    def __init__(self):
        super().__init__()
        planche = Planche(self, 10, 10, 3)
        planche.pack()
