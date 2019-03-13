from planche import *


class Interface(Tk):
    def __init__(self):
        super().__init__()
        planche = Planche(self, 48, 32, 299)
        planche.pack()
