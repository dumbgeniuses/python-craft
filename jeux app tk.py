from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk


class Block():
    """
    Un block standard
    """
    def __init__(self, type, debut:tuple, fin:tuple):
        """
        Consrtucteur de la classe Block.
        * type (str) : le type de block
        * debut (tuple) : les coordonnes (x, y) de début du block
        * fin (tuple) : les coordonnes (x, y) de fin du bock
        """
        self.type   = type
        self.debut  = debut
        self.fin    = fin
        self.texture= f'./textures/{type}.png'

    def get_localisation(self):
        return self.debut, self.fin

    

class Python_Craft(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Python Craft")
        self.attributes("-fullscreen", True)
        self.monde = []
        
    def create_world(self,monde):
        long_world = 1920
        large_world = 1080
        for y in range(1,long_world//19.20):
            for x in range(1,large_world//19.20):
                self.monde.append(Block("dirt",(x-1)*50,x*50,(y-1)*50,y*50))

if __name__ == "__main__":
    jeux = Python_Craft()
    jeux.mainloop()