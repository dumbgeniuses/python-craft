##----- Importation des Modules -----##
from tkinter import *
from PIL import Image, ImageTk

##----- Création de la fenêtre -----##
fen = Tk()
fen.title('Tracer dans un canevas')

##----- Création des boutons -----##
bouton_quitter = Button(fen, text='Quitter', command=fen.destroy)
bouton_quitter.grid(row = 1, column = 1, padx = 3, pady = 3, sticky=E)

##----- Création du canevas -----##
dessin = Canvas(fen, width = 500, height = 400, bg = 'white')
dessin.grid(row = 0, column = 0, columnspan = 2, padx = 3, pady = 3)

##----- Dessiner dans le canevas -----##
ligne1 = dessin.create_line(250, 175, 250, 225, width=4, fill='#d05e82')
rect1 = dessin.create_rectangle(175, 250, 325, 327, width=2, outline='#d05e82')
ovale1 = dessin.create_oval(75, 25, 425, 375, width=2, outline='#fb8007')
ovale2 = dessin.create_oval(180, 140, 230, 190, width=0, fill='#d05e82')
ovale3 = dessin.create_oval(270, 140, 320, 190, width=0, fill='#d05e82')
dessin.create_text(254, 90, text='  Bienvenue\nà la formation', fill='#fb8007', font='Arial 20')
dirt_image=Image.open("dirt.png").convert("RGBA")
dirt=ImageTk.PhotoImage(dirt_image)
logo1 = dessin.create_image(0, 0, image = dirt )
fen.mainloop()