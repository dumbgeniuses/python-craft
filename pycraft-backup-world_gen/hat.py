import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from random import randint
import time
import os
import winsound
from math import sqrt

# --------------------- ENTITÉS ---------------------
class Entite:
    def __init__(self, texture, x_debut, y_debut, vie=None, degat=None, ceinture=list(), main=0):
        self.x_debut = x_debut
        self.y_debut = y_debut
        self.texture = texture
        self.vie = vie
        self.degat = degat
        self.ceinture = ceinture
        self.main = 0

    def get_coordonnees(self):
        return self.coordonnees

    def set_coordonnees(self, newCoordonnees):
        self.coordonnees = newCoordonnees

    def get_vie(self):
        return self.vie

    def set_vie(self, newVie):
        self.vie = newVie

    def get_degat(self):
        return self.degat

    def get_ceinture(self):
        return self.ceinture

    def set_ceinture(self, slot, item):
        self.ceinture[slot] = item

    def get_main(self):
        return self.main

    def set_main(self, glissement):
        negatif = False
        if glissement < 0:
            negatif = True
            glissement = -glissement
        while self.get_main() + glissement > 6:
            glissement -= 6
        self.main = (6 - glissement) if negatif else glissement

    def attaque(self, victime):
        if isinstance(self.ceinture[self.get_main()], Arme):
            victime.set_vie(victime.get_vie() - self.ceinture[self.get_main()].degat)
        else:
            victime.set_vie(victime.get_vie() - self.degat)

    def set_texture(self, canva):
        self.id = canva.create_image(self.x_debut, self.y_debut, image=self.texture, anchor="nw", tags=("bom",))


class Joueur(Entite):
    def __init__(self, coordonnees=(0,0), vie=100, degat=10, ceinture=list(), sac=list()):
        super().__init__(coordonnees, vie, degat, ceinture)
        self.sac = sac


class Arme:
    def __init__(self, degat, texture='./textures/missing.png'):
        self.degat = degat
        self.texture = texture


class Pioche:
    pass

# --------------------- BLOCK & ITEM ---------------------
class Block:
    def __init__(self, typpe, x_debut, y_debut, textur):
        self.type = typpe
        self.x_debut = x_debut
        self.y_debut = y_debut
        self.textur = textur

    def get_type(self):
        return self.type

    def texture(self, canva):
        self.id = canva.create_image(self.x_debut, self.y_debut, image=self.textur, anchor="nw", tags=("block",))

    def resistance(self):
        self.soliditer = 1


class Item:
    def __init__(self, nom, x, y, image):
        self.nom = nom
        self.x = x
        self.y = y
        self.image = image
        self.vy = -5
        self.ausol = False

    def texture(self, canva):
        self.id_item = canva.create_image(self.x, self.y, image=self.image, anchor="nw", tags=("items",))

    def physique_item(self, canva, gravite, chunk):
        self.vy += gravite
        canva.move(self.id_item, 0, self.vy)
        x1, y1 = canva.coords(self.id_item)
        x2, y2 = x1 + 20, y1 + 20
        collisions = False
        voisins = self.blocs_autour(x1, y1, chunk)
        for bloc in voisins:
            if bloc.get_type() in ("grass", "air", "flower"):
                continue
            bx1, by1 = bloc.x_debut, bloc.y_debut
            bx2, by2 = bx1 + 50, by1 + 50
            if not (x2 <= bx1 or x1 >= bx2 or y2 <= by1 or y1 >= by2):
                if self.vy > 0:
                    canva.move(self.id_item, 0, by1 - y2)
                    self.vy = 0
                    self.ausol = True
                elif self.vy < 0:
                    canva.move(self.id_item, 0, by2 - y1)
                    self.vy = 0
                collisions = True
                break
        if not collisions:
            self.ausol = False

    def blocs_autour(self, px, py, chunk):
        gx, gy = int(px // 50), int(py // 50)
        voisins = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                bloc = chunk.get((gx + dx, gy + dy))
                if bloc and bloc.type != "air":
                    voisins.append(bloc)
        return voisins

# --------------------- PYCRAFT ---------------------
class Python_Craft(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Craft")
        self.attributes("-fullscreen", True)
        self.monde, self.blocks, self.chunk, self.items = [], {}, {}, {}
        self.image_liste, self.image_liste_PIl = {}, {}
        self.long_world, self.large_world = 5000, 3000
        self.gravite, self.gravite_saut = 1.3, -20
        self.vitesse_joueur, self.vitesse_verticale = 5, 0
        self.ausol = False
        self.etat = {"droite": True, "marche": False, "mine": False}
        self.timing = time.time()
        self.delai_animation = 0.12
        self.anim_index = 0
        self.anim_index_m = 0
        self.loot_table = {
            "grass_block": [("dirt",1)],
            "dirt": [("dirt",1)],
            "rock": [("cobble",1)],
            "iron": [("iron_ore",1)],
            "coal": [("coal", randint(1,2))],
            "wood": [("wood", randint(1,3))],
            "leaves": [("leaves", randint(0,2))]
        }
        self.inventaire = [None]*9
        self.inventaire[0] = {"nom": "stone", "quantite":12, "image": None}
        self.inventaire[1] = {"nom": "wood", "quantite":5, "image": None}
        self.inventaire_ouvert = False
        self.item_en_main = None
        self.slot_depart = None
        self.ui_slots, self.ui_items, self.ui_texts = [], [], []

        # Images
        for fichier in os.listdir("texturing"):
            chemin = os.path.join("texturing", fichier)
            image = Image.open(chemin).convert("RGBA").resize((50,50))
            self.image_liste[os.path.splitext(fichier)[0]] = ImageTk.PhotoImage(image)
            self.image_liste_PIl[os.path.splitext(fichier)[0]] = image
        air_img = Image.new("RGBA",(50,50),(0,0,0,0))
        self.air = ImageTk.PhotoImage(air_img)

        # Canvas
        self.sw = tk.Canvas(self, width=self.long_world, height=self.large_world, bg="skyblue",
                            scrollregion=(0,0,self.long_world,self.large_world))
        self.sw.pack()
        self.joueur = self.sw.create_image(500,1300,image=self.image_liste["steeve"],anchor="nw")
        self.mouton = Entite(self.image_liste["sheep"],500,2500,20,1)
        self.mouton.set_texture(self.sw)

        self.create_world()
        self.charge_world()
        self.update()
        self.x_visible=self.winfo_width()
        self.y_visible=self.winfo_height()
        self.touches_presser={}
        self.delai_touche = 1.8
        self.casser_animation()
        self.deplacement_animation()

        # Bindings
        self.bind("<e>", self.toggle_inventaire)
        self.sw.bind("<Button-1>", self.click_slot)
        self.sw.bind("<B1-Motion>", self.drag_item)
        self.sw.bind("<ButtonRelease-1>", self.drop_item)
        self.sw.tag_bind("block", "<ButtonPress-1>", self.click_maintenue)
        self.sw.tag_bind("block", "<ButtonRelease-1>", self.click_lacher)
        self.sw.tag_bind("block", "<Button-3>", self.poser_block)
        self.bind_all("<KeyPress>", self.touche_appuyer, add="+")
        self.bind_all("<KeyRelease>", self.touche_relacher, add="+")
        self.bind("<Escape>", lambda e:self.destroy())
        self.bind("<FocusOut>", lambda e:self.touche_effacer())
        self.bind("<Configure>", lambda e:self.taille_visible(e))
        self.sw.focus_set()
        self.sw.focus_force()
        self.type_block_choisie="dirt"
        self.textur_block_choisie=self.image_liste["dirt"]

        self.after(16, self.jeu_a_jour)
        self.after(16, self.physique_a_jour)

    # ------------- WORLD -------------
    def create_world(self):
        coordonnes = self.long_world//50
        couche = self.large_world//50
        nb, taille_biome = 0, [15,20,17]
        for y in range(couche):
            for x in range(coordonnes):
                if y==60: self.monde.append(Block("bedrock", x*50, y*50, self.image_liste["bedrock"]))
                elif 45<=y<60:
                    d = randint(1,200)
                    if d==1: self.monde.append(Block("iron", x*50, y*50, self.image_liste["iron"]))
                    elif d in (2,3): self.monde.append(Block("coal", x*50, y*50, self.image_liste["coal"]))
                    else: self.monde.append(Block("rock", x*50, y*50, self.image_liste["stone"]))
                elif 30<=y<45: self.monde.append(Block("dirt", x*50, y*50, self.image_liste["dirt"]))
                elif 29<=y<30: self.monde.append(Block("grass_block", x*50, y*50, self.image_liste["grass_block"]))
                elif 28<=y<29:
                    if nb==0:
                        biomes=randint(1,2)
                        nb=taille_biome[randint(0,2)]
                    else: nb-=1
                    if biomes==1 and randint(1,3)==1: self.planter_arbre(x,y)
                    if biomes==2:
                        if randint(1,10) in (1,2,3,4):
                            if randint(1,10) in range(1,10):
                                self.monde.append(Block("grass", x*50, y*50, self.image_liste["g1"]))
                            else:
                                self.monde.append(Block("flower", x*50, y*50, self.image_liste["flower"]))
                        else: self.monde.append(Block("air", x*50, y*50, self.air))
                else: self.monde.append(Block("air", x*50, y*50, self.air))

    def planter_arbre(self,x,sol):
        hauteur = randint(3,5)
        for i in range(hauteur):
            self.monde.append(Block("wood", x*50, (sol-i)*50, self.image_liste["wood"]))
        sommet = sol - hauteur
        for dx in range(-2,3):
            for dy in range(-2,2):
                if abs(dx)+abs(dy)<=3:
                    self.monde.append(Block("leaves", (x+dx)*50, (sommet+dy)*50, self.image_liste["leaves"]))

    def charge_world(self):
        for bloc in self.monde:
            bloc.texture(self.sw)
            self.blocks[bloc.id] = bloc
            chunk = (bloc.x_debut//50, bloc.y_debut//50)
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

    def deplacement_joueur(self, dx, dy):
        """Déplace le joueur avec collision, gravité et centrage caméra"""
        self.sw.move(self.joueur, dx, dy)
        x1, y1 = self.sw.coords(self.joueur)
        x2, y2 = x1 + 50, y1 + 50
        collisions = False

        # Vérifie collisions avec les blocs autour
        for bloc in self.blocs_autour(x1, y1):
            if bloc.get_type() in ("air", "grass", "flower"):
                continue
            bx1, by1 = bloc.x_debut, bloc.y_debut
            bx2, by2 = bx1 + 50, by1 + 50
            if not (x2 <= bx1 or x1 >= bx2 or y2 <= by1 or y1 >= by2):
                if dy > 0 and y1 < by1:  # chute
                    self.sw.move(self.joueur, 0, by1 - y2)
                    self.vitesse_verticale = 0
                    self.ausol = True
                elif dy < 0 and y2 > by2:  # montée
                    self.sw.move(self.joueur, 0, by2 - y1)
                    self.vitesse_verticale = 0
                elif dx > 0 and x1 < bx1:  # droite
                    self.sw.move(self.joueur, bx1 - x2, 0)
                elif dx < 0 and x2 > bx2:  # gauche
                    self.sw.move(self.joueur, bx2 - x1, 0)
                collisions = True
                break

        if not collisions and dy >= 0:
            self.ausol = False

        # Limites du monde
        if x1 < 0:
            self.sw.move(self.joueur, -x1, 0)
        elif x2 > self.long_world:
            self.sw.move(self.joueur, self.long_world - x2, 0)
        if y2 > self.large_world:
            self.sw.move(self.joueur, 0, self.large_world - y2)
            self.vitesse_verticale = 0
            self.ausol = True

        # Centrage caméra
        self.camera_centrer(x1, x2, y1, y2)

    def camera_centrer(self,x1,x2,y1,y2):
        pos_x = (x1 + x2) / 2
        pos_y = (y1 + y2) / 2
        vue_x = (pos_x - self.x_visible / 2) / self.long_world
        vue_y = (pos_y - self.y_visible / 2) / self.large_world
        self.sw.xview_moveto(max(0, min(1, vue_x)))
        self.sw.yview_moveto(max(0, min(1, vue_y)))
        self.chunk_render()

    def physique_a_jour(self):
        """Applique gravité et met à jour les items flottants"""
        self.vitesse_verticale += self.gravite
        self.deplacement_joueur(0, self.vitesse_verticale)
        for item in self.items.values():
            item.physique_item(self.sw, self.gravite, self.chunk)
        self.ramassage_items()
        self.after(16, self.physique_a_jour)

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

    # --------------------- Inventaire toggle ---------------------
    def toggle_inventaire(self, event=None):
        """Ouvre ou ferme l'inventaire"""
        if self.inventaire_ouvert:
            self.cacher_inventaire()
            self.inventaire_ouvert = False
        else:
            self.redraw_inventaire()
            self.inventaire_ouvert = True


    def ramassage_items(self):
        """Vérifie les collisions joueur-item et les ajoute à l'inventaire"""
        px1, py1 = self.sw.coords(self.joueur)
        px2, py2 = px1 + 50, py1 + 50
        for item_id, item in list(self.items.items()):
            ix1, iy1 = self.sw.coords(item.id_item)
            ix2, iy2 = ix1 + 20, iy1 + 20
            if not (px2 < ix1 or px1 > ix2 or py2 < iy1 or py1 > iy2):
                self.ajouter_item(item.nom, 1)
                self.sw.delete(item.id_item)
                del self.items[item_id]

    def ajouter_item(self, nom, quantite=1):
        """Ajoute un item à l'inventaire avec empilement"""
        for slot in self.inventaire:
            if slot and slot["nom"] == nom:
                slot["quantite"] += quantite
                self.redraw_inventaire()
                return
        for i in range(len(self.inventaire)):
            if self.inventaire[i] is None:
                self.inventaire[i] = {"nom": nom, "quantite": quantite, "image": None}
                self.redraw_inventaire()
                return

    def afficher_inventaire(self):
        """Affiche la hotbar et l’inventaire à l’écran"""
        x0, y0 = 200, 200
        taille, padding = 50, 5
        for i, slot in enumerate(self.inventaire):
            x = x0 + i * (taille + padding)
            y = y0
            r = self.sw.create_rectangle(x, y, x+taille, y+taille, fill="#333", outline="white")
            self.ui_slots.append(r)
            if slot:
                t = self.sw.create_text(x+25, y+25, text=f"{slot['nom']}\n{slot['quantite']}", fill="white")
                self.ui_texts.append(t)

    def cacher_inventaire(self):
        for elem in self.ui_slots + self.ui_items + self.ui_texts:
            self.sw.delete(elem)
        self.ui_slots.clear()
        self.ui_items.clear()
        self.ui_texts.clear()

    def redraw_inventaire(self):
        self.cacher_inventaire()
        self.afficher_inventaire()

    # Drag & Drop inventaire
    def coord_to_slot(self, x, y):
        x0, y0 = 200, 200
        taille, padding = 50, 5
        if y < y0 or y > y0 + taille:
            return None
        index = (x - x0) // (taille + padding)
        if 0 <= index < len(self.inventaire):
            return int(index)
        return None

    def click_slot(self, event):
        if not self.inventaire_ouvert or self.item_en_main:
            return
        index = self.coord_to_slot(event.x, event.y)
        if index is None or self.inventaire[index] is None:
            return
        self.item_en_main = self.inventaire[index]
        self.slot_depart = index
        self.inventaire[index] = None
        self.image_flottante = self.sw.create_text(event.x, event.y, text=self.item_en_main['nom'], fill="yellow")
        self.redraw_inventaire()

    def drag_item(self, event):
        if self.image_flottante:
            self.sw.coords(self.image_flottante, event.x, event.y)

    def drop_item(self, event):
        if not self.item_en_main:
            return
        index = self.coord_to_slot(event.x, event.y)
        if index is None:
            self.inventaire[self.slot_depart] = self.item_en_main
        else:
            cible = self.inventaire[index]
            if cible is None:
                self.inventaire[index] = self.item_en_main
            elif cible['nom'] == self.item_en_main['nom']:
                cible['quantite'] += self.item_en_main['quantite']
            else:
                self.inventaire[self.slot_depart] = cible
                self.inventaire[index] = self.item_en_main
        self.sw.delete(self.image_flottante)
        self.image_flottante = None
        self.item_en_main = None
        self.slot_depart = None
        self.redraw_inventaire()

    def chunk_render(self):
        """Ne dessine que les blocs visibles autour du joueur"""
        for item in self.sw.find_withtag("render"):
            self.sw.delete(item)
        x1, y1 = self.sw.coords(self.joueur)
        chunkx, chunky = int(x1 // 50), int(y1 // 50)
        view_x, view_y = self.x_visible // 50 + 2, self.y_visible // 50 + 2
        for gy in range(chunky - view_y, chunky + view_y):
            for gx in range(chunkx - view_x, chunkx + view_x):
                block = self.chunk.get((gx, gy))
                if block:
                    block.id = self.sw.create_image(block.x_debut, block.y_debut,
                                                    image=block.textur, anchor="nw",
                                                    tags=("render", "block"))

    def blocs_autour(self, px, py):
        """Retourne les blocs autour d'une position (pour collisions)"""
        gx, gy = int(px // 50), int(py // 50)
        voisins = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                bloc = self.chunk.get((gx+dx, gy+dy))
                if bloc and bloc.get_type() != "air":
                    voisins.append(bloc)
        return voisins

    def deplacement_animation(self):
        self.delai_frame = time.time()
        self.walk_rightframe = [self.image_liste["steeve_walk1"],self.image_liste["steeve_walk2"],self.image_liste["steeve"]]
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

    def casser_block(self,event):
        clicked = self.sw.find_withtag("current")

        if clicked:
            block_id = clicked[0]
            block = self.blocks.get(block_id)
            block_type = block.type

            if block_type in self.loot_table:
                for item_nom, quantite in self.loot_table[block_type]:
                    for _ in range(quantite):
                        self.spawn_item(item_nom, block.x_debut, block.y_debut)

            if block_type != "air":
                self.sw.delete(block_id)

                del self.blocks[block_id]
                block.type = "air"
                block.textur = self.air
                block.texture(self.sw)
                self.blocks[block.id] = block
                self.click_gauche = False
                self.timing = 0

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

# ------------- MAIN -------------
if __name__ == "__main__":
    jeux = Python_Craft()
    jeux.mainloop()
