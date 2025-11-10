# Créé par pierre.jaillet, le 10/11/2025 en Python 3.7
import tkinter as tk
from PIL import Image, ImageTk


class Block():
    """
    Un block standard
    """
    def __init__(self, type, x_debut, y_debut):
        """
        Consrtucteur de la classe Block.
        * type (str) : le type de block
        * debut (tuple) : les coordonnes (x, y) de début du block
        * fin (tuple) : les coordonnes (x, y) de fin du bock
        """
        self.type   = type
        self.x_debut  = x_debut
        self.y_debut = y_debut

    def get_localisation(self):
        return self.x_debut, self.y_debut

    def texture(self,canva,textur):
        canva.create_image(self.x_debut,self.y_debut,image=textur)
        print(canva, textur,self.x_debut,self.y_debut)

class Python_Craft(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Python Craft")
        self.attributes("-fullscreen", True)
        monde = []
        self.sw = tk.Canvas(self,width=5000,height = 3000)
        self.create_world(monde)
        self.charge_world(monde)
        self.sw.pack()

    def create_world(self,monde):
        long_world = 5000
        large_world = 3000
        for y in range(long_world//50):
            for x in range(large_world//50):
                monde.append(Block("air",x*50,y*50))

    def charge_world(self,liste):
        dirt_image = Image.open("dirt.png").convert("RGBA")
        dirt_image = dirt_image.resize((50, 50))
        dirt = ImageTk.PhotoImage(dirt_image)
        for i in liste:
            i.texture(self.sw,dirt)

if __name__ == "__main__":
    jeux = Python_Craft()
    jeux.mainloop()
