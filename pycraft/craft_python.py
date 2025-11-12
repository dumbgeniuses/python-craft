import tkinter as tk
from PIL import Image, ImageTk
from random import *


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

    def get_type(self):
        return self.type

    def texture(self,canva):
        self.id = canva.create_image(self.x_debut,self.y_debut,image = self.type,tags=("block",))

class Python_Craft(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Python Craft")
        self.attributes("-fullscreen", True)
        monde = []
        self.blocks = {}

        dirt_image = Image.open("dirt.png").convert("RGBA")
        dirt_image = dirt_image.resize((50, 50))
        self.dirt = ImageTk.PhotoImage(dirt_image)

        andesite_image = Image.open("andesite.png").convert("RGBA")
        andesite_image = andesite_image.resize((50, 50))
        self.andesite = ImageTk.PhotoImage(andesite_image)        
        
        bedrock_image = Image.open("bedrock.png").convert("RGBA")
        bedrock_image = bedrock_image.resize((50, 50))
        self.bedrock = ImageTk.PhotoImage(bedrock_image)        
        
        rock_image = Image.open("roche.png").convert("RGBA")
        rock_image = rock_image.resize((50, 50))
        self.rock = ImageTk.PhotoImage(rock_image)

        grass_block_image = Image.open("grass_block.png").convert("RGBA")
        grass_block_image = grass_block_image.resize((50, 50))
        self.grass_block = ImageTk.PhotoImage(grass_block_image)        
        
        self.sw = tk.Canvas(self,width=5000,height = 3000,bg="skyblue")
        self.create_world(monde)
        self.charge_world(monde)
        self.sw.pack()
        self.sw.tag_bind("block", "<Button-1>", self.on_click)

    def create_world(self,monde):
        long_world = 5000
        large_world = 3000
        for y in range(long_world//50):
            for x in range(large_world//50):
                if y == 21 or y==22 :
                    monde.append(Block(self.bedrock,x*50,y*50))
                elif y<21 and y>4:
                    nb = randint(0,8)
                    if nb ==0:
                        monde.append(Block(self.andesite,x*50,y*50))
                    else :
                        monde.append(Block(self.rock,x*50,y*50))
                elif y<=4 and y>=2:
                    monde.append(Block(self.dirt,x*50,y*50))
                elif y<2 and y>=1:
                    monde.append(Block(self.grass_block,x*50,y*50))


    def charge_world(self,liste):
        for bloc in liste:
            bloc.texture(self.sw)
            self.blocks[bloc.id] = bloc

    def on_click(self, event):
        clicked = self.sw.find_withtag("current")
        if clicked:
            block_id = clicked[0]
            block = self.blocks.get(block_id)
            if block:
                self.sw.delete(block_id)
                del self.blocks[block_id]

if __name__ == "__main__":
    jeux = Python_Craft()
    jeux.mainloop()