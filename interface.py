from planche import *


class Interface(Tk):
    def __init__(self):
        super().__init__()
        planche = Planche(self, 32, 16, 99)
        planche.pack()
