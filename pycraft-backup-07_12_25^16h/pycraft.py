import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from random import *
import time
import os
from pathlib import Path
import winsound


class Block():
    """
    Un block standard
    """
    def __init__(self, typpe, x_debut, y_debut,textur):
        """
        Consrtucteur de la classe Block.
        * type (str) : le type de block
        * debut (tuple) : les coordonnes (x, y) de début du block
        * fin (tuple) : les coordonnes (x, y) de fin du bock
        """
        self.type   = typpe
        self.x_debut  = x_debut
        self.y_debut = y_debut
        self.textur = textur

    def get_type(self):
        return self.type

    def texture(self,canva):
        self.id = canva.create_image(self.x_debut,self.y_debut,image = self.textur,anchor="nw",tags=("block",))

    def resistance(self):
        self.soliditer = 1


class Python_Craft(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Python Craft")
        self.attributes("-fullscreen", True)
        #liste du monde et des block
        self.monde = []
        self.blocks = {}
        self.chunk = {}
        self.image_liste={}
        self.image_liste_PIl={}
        # variable de la physique du monde
        self.long_world = 5000
        self.large_world=3000

        self.gravite = 1.3
        self.gravite_saut = -20
        self.vitesse_joueur = 5
        self.vitesse_verticale = 0
        self.ausol = False

        self.etat = {"droite": True,"marche": False,"mine":False}
        self.timing = time.time()
        self.delai_animation  = 0.12
        self.timing_animation = time.time()
        self.anim_index = 0
        self.anim_index_m = 0

        for fichier in os.listdir("texturing"):
            chemin_complet = os.path.join("texturing", fichier)
            image = Image.open(chemin_complet).convert("RGBA")
            image = image.resize((50, 50))
            self.image_liste[os.path.splitext(fichier)[0]] = ImageTk.PhotoImage(image)
            self.image_liste_PIl[os.path.splitext(fichier)[0]] = image
        

        air_img = Image.new("RGBA",(50,50),(0,0,0,0))
        self.air = ImageTk.PhotoImage(air_img)

        #creation et modification du canva
        self.sw = tk.Canvas(self,width=self.long_world,height = self.large_world,bg="skyblue",
                            scrollregion=(0,0,self.long_world,self.large_world))
        self.sw.pack()
        
        self.joueur = self.sw.create_image(400, 100, image = self.image_liste["steeve"],anchor="nw")

        self.create_world()
        self.charge_world()
        self.update()

        self.x_visible=self.winfo_width()
        self.y_visible=self.winfo_height()
        self.touches_presser={}
        self.delai_touche =1.8

        self.casser_animation()
        self.deplacement_animation()
        self.sw.tag_bind("block", "<ButtonPress-1>", self.click_maintenue)
        self.sw.tag_bind("block", "<ButtonRelease-1>", self.click_lacher)
        self.sw.tag_bind("block","<Button-3>",self.poser_block)
        #self.sw.tag_bind("block","<Button-1>",self.casser_block)
        self.bind_all("<KeyPress>", self.touche_appuyer, add="+")
        self.bind_all("<KeyRelease>", self.touche_relacher, add="+")
        self.bind("<Escape>", lambda e: self.destroy)
        self.bind("<Configure>", lambda e: self.taille_visible(e))
        self.bind("<FocusOut>", lambda e: self.touche_effacer())

        #focus sur le canevas
        self.sw.focus_set()
        self.sw.focus_force()

        self.type_block_choisie = "rock"
        self.textur_block_choisie= self.image_liste["dirt"]

        #fonctionnement du monde
        self.after(16, self.jeu_a_jour)
        self.after(16, self.physique_a_jour)
        #self.after(500, self.touche_nettoyer)

    #génère tout les blocks du monde dans la liste monde
    def create_world(self):
    # on utilise self.long_world, self.large_world pour la grille
        coordonnes= self.long_world // 50
        couche = self.large_world // 50
        for y in range(couche):
            for x in range(coordonnes):
                if y <=2:
                    self.monde.append(Block("bedrock", x*50, y*50, self.image_liste["bedrock"]))
                elif 2 <= y < 40:
                        self.monde.append(Block("rock", x*50, y*50, self.image_liste["stone"]))
                elif 55 < y < 60:
                    self.monde.append(Block("dirt", x*50, y*50, self.image_liste["dirt"]))
                elif 55 <= y < 56:
                    self.monde.append(Block("grass_block", x*50, y*50, self.image_liste["grass_block"]))
                elif 54 <= y < 55:
                    a = randint(1,3)
                    if a == 1:
                        self.monde.append(Block("grass", x*50, y*50, self.image_liste["g1"]))
                    elif a == 3:
                        self.monde.append(Block("grass", x*50, y*50, self.image_liste["g1s"]))
                    else:
                        self.monde.append(Block("air", x*50, y*50, self.air))
                else:
                    self.monde.append(Block("air", x*50, y*50, self.air))

    #charge les textures des block de la liste monde et un ad un id pour chaque texture de blocok
    def charge_world(self):
        for bloc in self.monde:
            bloc.texture(self.sw)
            self.blocks[bloc.id] = bloc
            chunk = bloc.x_debut//50, bloc.y_debut//50
            self.chunk[chunk] = bloc


    def touche_appuyer(self, evenement):
        touche = evenement.keysym.lower()
        code = getattr(evenement,"keycode", None)
        press_touch = self.touches_presser.get(touche)
        if press_touch is None:
            self.touches_presser[touche] = {"temps": self.timing, "codes": set()}
        else:
            press_touch["temps"] = self.timing
        if code is not None:
            self.touches_presser[touche]["codes"].add(code)
        if touche in("space","z","w") and self.ausol:
            self.vitesse_verticale = self.gravite_saut
            self.ausol= False

    def touche_relacher(self, evenement):
        touche =evenement.keysym.lower()
        code = getattr(evenement,"keycode",None)
        supprimer =False
        if touche in self.touches_presser:
            self.touches_presser.pop(touche,None)
            supprimer= True
        else:
            for nom, entre in list(self.touches_presser.items()):
                if code in entre["codes"]:
                    self.touches_presser.pop(nom,None)
                    supprimer = True
                    break
        try:
            self.sw.focus_force()
        except Exception:
            pass

    def touche_effacer(self):
        self.touches_presser.clear()
    """
    def touche_nettoyer(self):
        actuellement= time.time()
        touche_a_supprimer =[touche for touche, entre in self.touches_presser.items() if actuellement - entre["temps"]>self.delai_touche]
        for touche in touche_a_supprimer:
            self.touches_presser.pop(touche, None)
        self.after(500,self.touche_nettoyer)
    """
    def verifier_focus(self):
        if not self.focus_displayof():
            try:
                self.sw.focus_force()
            except Exception:
                pass
        self.after(1000, self.verifier_focus)

    def taille_visible(self, evenement):
        self.large_world = evenement.height
        self.long_world = evenement.width

    def jeu_a_jour(self):
        touche =set(self.touches_presser.keys())
        deplacement_x = 0
        if "left" in touche or "q" in touche:
            self.etat["droite"] = False
            deplacement_x -= self.vitesse_joueur
        if "right" in touche or "d" in touche:
            self.etat["droite"] = True
            deplacement_x += self.vitesse_joueur
        if deplacement_x != 0:
            self.deplacement_joueur(deplacement_x,0)
        self.etat["marche"] = deplacement_x != 0
        self.after(16, self.jeu_a_jour)

    def physique_a_jour(self):
        self.vitesse_verticale += self.gravite
        self.deplacement_joueur(0,self.vitesse_verticale)
        self.after(16,self.physique_a_jour)

    def deplacement_joueur(self,deplacement_x, deplacement_y):
        self.sw.move(self.joueur,deplacement_x,deplacement_y)
        x1,y1 =self.sw.coords(self.joueur)
        x2 = x1 + 50
        y2 = y1 + 50
        collisions = False

        voisins = self.blocs_autour(x1, y1)
        for bloc in voisins:
            if bloc.get_type() == "air" or bloc.get_type() == "grass":
                continue
            bx1, by1 = bloc.x_debut, bloc.y_debut
            bx2, by2 = bx1 + 50, by1 +50
            if not (x2 <= bx1 or x1 >= bx2 or y2 <= by1 or y1 >= by2):
                if deplacement_y > 0 and y1 < by1:
                    self.sw.move(self.joueur, 0, by1 - y2)
                    self.vitesse_verticale = 0
                    self.ausol = True
                elif deplacement_y < 0 and y2 > by2:
                    self.sw.move(self.joueur, 0, by2 - y1)
                    self.vitesse_verticale = 0
                elif deplacement_x > 0 and x1 < bx1:
                    self.sw.move(self.joueur, bx1 - x2, 0)
                elif deplacement_x < 0 and x2 > bx2:
                    self.sw.move(self.joueur, bx2 - x1, 0)
                collisions = True
                break

        if not collisions and deplacement_y >= 0:
            self.ausol = False

        x1,y1 =self.sw.coords(self.joueur)
        x2 = x1 + 50
        y2 = y1 + 50
        if x1 < 0:
            self.sw.move(self.joueur, -x1,0)
        elif x2 > self.long_world:
            self.sw.move(self.joueur,self.long_world - x2,0)
        if y2 > self.large_world:
            self.sw.move(self.joueur,0, self.large_world- y2)
            self.vitesse_verticale = 0
            self.ausol = True
        self.camera_centrer()

    def camera_centrer(self):
        x1,y1 =self.sw.coords(self.joueur)
        x2 = x1 + 50
        y2 = y1 + 50
        pos_x = (x1 + x2) / 2
        pos_y = (y1 + y2) / 2
        vue_x = (pos_x - self.x_visible / 2) / self.long_world
        vue_y = (pos_y - self.y_visible / 2) / self.large_world
        self.sw.xview_moveto(max(0, min(1, vue_x)))
        self.sw.yview_moveto(max(0, min(1, vue_y)))
        self.chunk_render()


#prend l'id des block et les supprimes et delte leur texture en prennant le click souris
    def casser_block(self,event):
        clicked = self.sw.find_withtag("current")
        if clicked:
            block_id = clicked[0]
            block = self.blocks.get(block_id)
            block_type = block.type
            if block_type != "air":
                self.sw.delete(block_id)
                del self.blocks[block_id]
                block.type = "air"
                block.textur = self.air
                block.texture(self.sw)
                self.blocks[block.id] = block
                self.click_gauche = False
                self.timing = 0
                



    def click_maintenue(self,event):
        self.click_gauche = True
        self.timing= time.time()
        clicked = self.sw.find_withtag("current")
        block_id = clicked[0]
        block = self.blocks.get(block_id)
        if block.type == "air" or block.type =="grass":
            return
        else:
            self.etat["mine"] = True
            winsound.PlaySound("casserv1.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.maintien_continu(event)

    def click_lacher(self,event):
        self.click_gauche = False
        self.timing = 0
        self.etat["mine"] = False
        winsound.PlaySound(None, winsound.SND_PURGE)
        self.anim_index_m = 0

    def maintien_continu(self,event):
        if not self.click_gauche:
            self.etat["mine"] = False
            return 
        if time.time() - self.timing >= 1:
            clicked = self.sw.find_withtag("current")
            block_id = clicked[0]
            block = self.blocks.get(block_id)
            assemblage = Image.alpha_composite(self.image_liste_PIl["dirt"],self.image_liste_PIl["casser"])
            block.textur = ImageTk.PhotoImage(assemblage)
            block.texture(self.sw)
            self.blocks[block.id] = block
        if time.time() - self.timing >= 2:
            self.etat["mine"] = True
            self.casser_block(event)
        self.after(50, lambda: self.maintien_continu(event))


    def poser_block(self, event):
        clicked = self.sw.find_withtag("current")
        block_id = clicked[0]
        if clicked:
            block = self.blocks.get(block_id)
            block_type = block.type
            if block_type == "air" or block_type == "grass":
                block.type = self.type_block_choisie
                block.textur = self.textur_block_choisie
                block.texture(self.sw)
                self.blocks[block.id] = block

    def chunk_render(self):
        for item in self.sw.find_withtag("render"):
            self.sw.delete(item)

            x1, y1, x2, y2 = self.sw.coords(self.joueur)
            chunkx = int(x1 // 50)
            chunky = int(y1 // 50)

            view_x = self.x_visible // 50 + 2
            view_y = self.y_visible // 50 + 2

            visibility_x_base = (chunkx - view_x) // 2
            visibility_x_end   = (chunkx + view_x) // 2
            visibility_y_base = (chunky - view_y) // 2
            visibility_y_end   = (chunky + view_y) // 2

            for gy in range(visibility_y_base, visibility_y_end):
                for gx in range(visibility_x_base, visibility_x_end):
                    block = self.chunk.get((gx, gy))
                    if block:
                        block.id = self.sw.create_image(
                            block.x_debut,
                            block.y_debut,
                            image=block.textur,
                            anchor="nw",
                            tags=("render", "block"))

    def blocs_autour(self, px, py):
        gx = int(px // 50)
        gy = int(py // 50)

        voisins = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                bloc = self.chunk.get((gx + dx, gy + dy))
                if bloc and bloc.type != "air":
                    voisins.append(bloc)
        return voisins

    def deplacement_animation(self):
        self.delai_frame = time.time()
        self.walk_rightframe = [self.image_liste["steeve_walk"],self.image_liste["steeve"]]
        self.walk_leftframe = [self.image_liste["steeve_reverse_walk"],self.image_liste["steeve_reverse"]]
        if self.etat["marche"] and (self.delai_frame - self.timing) >= self.delai_animation:
                self.timing_animation = self.delai_frame
                self.anim_index = (self.anim_index + 1) % max(1, len(self.walk_rightframe))

        if self.etat["droite"]:
            if self.etat["marche"]:
                frame = self.walk_rightframe[self.anim_index % len(self.walk_rightframe)]
            else:
                frame = self.image_liste["steeve"]
        else:
            if self.etat["marche"]:
                frame = self.walk_leftframe[self.anim_index % len(self.walk_leftframe)]
            else:
                frame = self.image_liste["steeve_reverse"]

        if not self.etat["mine"]:
            self.sw.itemconfig(self.joueur, image=frame)
        self.after(100, self.deplacement_animation)

    def casser_animation(self):
        self.delai_frame_m = time.time()
        self.mineframe_r = [self.image_liste["steeve_mine"],self.image_liste["steeve"]]
        self.mineframe_l = [self.image_liste["steeve_mine_reverse"],self.image_liste["steeve_reverse"]]
        delai_animation = 0.5
        if self.etat["mine"] and (self.delai_frame_m - self.timing_animation) >= delai_animation:
                self.timing_animation = self.delai_frame_m
                self.anim_index_m = (self.anim_index_m + 1) % max(1, len(self.mineframe_r))

        if self.etat["droite"]:
            if self.etat["mine"]:
                frame = self.mineframe_r[self.anim_index_m % len(self.mineframe_r)]
            else:
                frame = self.image_liste["steeve"]
        else:
            if self.etat["mine"]:
                frame = self.mineframe_l[self.anim_index_m % len(self.mineframe_l)]
            else:
                frame = self.image_liste["steeve_reverse"]

        self.sw.itemconfig(self.joueur, image=frame)
        self.after(100, self.casser_animation)



if __name__ == "__main__":
    jeux = Python_Craft()
    jeux.mainloop()