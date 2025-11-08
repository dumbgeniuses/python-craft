from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk


class block():
    def __init__(self,types,x_debut,x_fin,y_debut,y_fin):
        self.type= types
        self.x_debut = x_debut
        self.x_fin = x_fin
        self.y_debut = y_debut
        self.y_fin = y_fin

    def get_localisation(self):
        return self.x_debut, self.x_fin, self.y_debut, self.y_fin

    

class Python_Craft(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("python craft")
        self.attributes("-fullscreen", True)
        monde = []
        
    def create_world(self,monde):
        long_world = 5000
        large_world = 3000
        for y in range(1,long_world//50):
            for x in range(1,large_world//50):
                monde.append(block("dirt",(x-1)*50,x*50,(y-1)*50,y*50))

if __name__ == "__main__":
    jeux = Python_Craft()
    jeux.mainloop()