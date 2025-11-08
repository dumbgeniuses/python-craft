from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk

wind = Tk()
paper=Canvas(wind,width=500,height=500)
dirt_image=Image.open("dirt.png").convert("RGBA")
dirt=ImageTk.PhotoImage(dirt_image)
paper.create_image(1,1,image = dirt)
paper.pack()
wind.mainloop()