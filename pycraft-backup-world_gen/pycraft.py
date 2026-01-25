import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from random import *
import time
import os
from pathlib import Path
import winsound

class Entite:
    """
    une entité (joueur, animal, créature...)
    """
    def __init__(self,texture,x_debut, y_debut, vie:int=None, degat:int=None, ceinture:list=[], main:int=0,):
        """
        Constructeur de la classe Entité.
        * coordonnees (tuple) : coordonnees x / y de l'entité dans le monde
        * vie (int) : nombre de points de vie actuels (pas le maximum)
        * degat (int) : nombre de degats infligés par l'entité par défaut (sans arme en main)
        * ceinture (list) : liste de 6 'items' accessibles en main par l'entite
        """
        self.x_debut    = x_debut
        self.y_debut    = y_debut
        self.texture    = texture
        self.vie        = vie
        self.degat      = degat
        self.ceinture   = ceinture
        self.main       = 0

    def get_coordonnees(self):
        """ Retourne la valeur de l'attribut coordonnees de l'entité. """
        return self.coordonnees

    def set_coordonnees(self, newCoordonnees:tuple):
        """ Remplace la valeur de l'attribut coordonnees de l'entité. """
        self.coordonnees = newCoordonnees

    def get_vie(self):
        """ Retourne la valeur de l'attribut vie de l'entité. """
        return self.vie

    def set_vie(self, newVie:int):
        """ Remplace la valeur de l'attribut vie de l'entité. """
        self.vie = newVie

    def get_degat(self):
        """ Retourne la valeur de l'attribut degat de l'entité. """
        return self.degat

    # pas set_degat(self): car on ne change jamais les dégâts faits par l'entité
    # attaque() prend déjà en charge le port d'arme

    def get_ceinture(self):
        """ Retourne la valeur de l'attribut ceinture de l'entité. """
        return self.ceinture

    def set_ceinture(self, slot:int, item):
        """ Remplace l'item à l'emplacement d'index {slot} (de la ceinture) par {item}. """
        self.ceinture[slot] = item

    def get_main(self):
        """ Retourne la valeur de l'attribut main de l'entité. """
        return self.main

    def set_main(self, glissement:int):
        """ Remplace l'index de la ceinture actuellement en main. """
        # glissement = int(glissement) # si les scrolls de tkinter sont en floats
        if glissement < 0:
            negatif= True               #
            glissement= -1*glissement   # passe le glissement en positif pour le calcul

        while (self.get_main() + glissement) > 6:
            glissement -= 6

        if negatif:
            self.main = 6 - glissement
        else:
            self.main = glissement

    def attaque(self, victime):
        if isinstance(self.ceinture[self.get_main()], Arme):
            victime.set_vie(victime.get_vie() - self.ceinture[self.get_main()].degat)
        else:
            victime.set_vie(victime.get_vie() - self.degat)

    def set_texture(self,canva):
        self.id = canva.create_image(self.x_debut,self.y_debut,image = self.texture,anchor="nw",tags=("bom",))

    def deplacement_joueur(self,canva,deplacement_x, deplacement_y):
        canva.move(self.joueur,deplacement_x,deplacement_y)
        x1,y1 = canva.coords(self.joueur)
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
                    canva.move(self.joueur, 0, by1 - y2)
                    self.vitesse_verticale = 0
                    self.ausol = True
                elif deplacement_y < 0 and y2 > by2:
                    canva.move(self.joueur, 0, by2 - y1)
                    self.vitesse_verticale = 0
                elif deplacement_x > 0 and x1 < bx1:
                    canva.move(self.joueur, bx1 - x2, 0)
                elif deplacement_x < 0 and x2 > bx2:
                    canva.move(self.joueur, bx2 - x1, 0)
                collisions = True
                break

        if not collisions and deplacement_y >= 0:
            self.ausol = False

        if x1  <0:
            canva.move(self.joueur, -x1,0)
        elif x2 > self.long_world:
            canva.move(self.joueur,self.long_world - x2,0)
        if y2 > self.large_world:
            canva.move(self.joueur,0, self.large_world- y2)
            self.vitesse_verticale = 0
            self.ausol = True

#class Nom(AutreClasse) fait hériter Nom de toutes les propriétés de AutreClasse
class Joueur(Entite):
    """
    le joueur
    """
    def __init__(self, coordonnees:tuple=(0,0), vie:int=100, degat:int=10, ceinture:list=[], sac:list=[]):
        """
        Constructeur de la classe Joueur.
        * coordonnees (tuple) : coordonnées x / y du joueur dans le monde
        * vie (int) : nombre de points de vie actuels (pas le maximum)
        * degat (int) : nombre de dégâts infligés par le joueur par défaut (sans arme en main)
        * ceinture (list) : liste de 6 'items' accessibles en main par le joueur
        * sac (list) : liste de tous les 'items' dans l'inventaire du joueur
        """
        # pour bien transmettre les paramètres passés dans Joueur dans ceux hérités de Entite
        super().__init__(coordonnees, vie, degat, ceinture)
        self.sac= sac

    def casser_bloc(self):
        # à voir si utile ou pas ?
        # peut être garder, selon la dureté des blocs pour faire une "pause" avant de le faire disparaitre
        if isinstance(self.ceinture[self.get_main()], Pioche):
            pass # faire 
        pass

    def poser_bloc(self):
        pass

    """def verification_ennemis(self, ennemis:list=[]):
        
        Retourne la liste de tous les ennemis qui voient le joueur, ou None si aucune.
        Fonction utilisée automatiquement à chaque déplacement du joueur.
        * ennemis (list) : liste de toutes les entités hostiles dans le monde
        
        # vérifier si blocks entre joueur et entité :
        #   si oui, passer à la suivante, sinon passer à la vérif suivante
        # vérifier si distance joueur-entité est 7 ou plus :
        #   si oui, passer à la suivante, sinon passer à la vérif suivante
        ennemis_proches = []

        for entite in ennemis:
            # si il n'y a pas de blocks entre le joueur et l'ennemi
            if not presence_block(self.coordonnees, entite.coordonnees):
                if distance(self.coordonnees, entite.coordonnees) <= 6:
                    ennemis_proches.append(entite)
        
        if len(ennemis_proches) <= 0:
            return None
        return ennemis_proches
"""

class Arme:
    """
    une arme
    """
    def __init__(self, degat:int, texture:str='./textures/missing.png'):
        """
        Constructeur de la classe Arme.
        * degat (int) : nombre de dégâts infligés par l'arme
        * texture (str) : chemin d'accès à la texture de l'arme
        """
        self.degat  = degat
        self.texture= texture


class Pioche:
    pass

"""
# Fonctions en dehors des classes

def presence_block(monde:dict, point_1:tuple, point_2:tuple):
    
    Retourne True si il y a des blocks entre les deux points donnés et False sinon.
    * monde (dict) : dictionnaire (coordonnees:tuple : block:Block) contenant tous les blocks du monde
    * point_1 (tuple) : coordonnees (x, y) du premier point
    * point_2 (tuple) : coordonnees (x, y) du deuxième point
    
    delta_x, delta_y= distance_directe(point_1, point2)
    deplacement_xb = None # par défaut car optionel selon les coordonnées
    deplacement_yb = None #

    if delta_x >= delta_y:
        if delta_y == 0:
            deplacement_x = delta_x
            deplacement_y = 0
        else:
            deplacement_x = delta_x // delta_y
            deplacement_y = 1
            if delta_x % delta_y != 0:
                deplacement_xb = deplacement_x + 1
    else:
        if delta_x == 0:
            deplacement_y = delta_y
            deplacement_x = 0
        else:
            deplacement_y = delat-y // delta_x
            deplacement_x = 1
            if delta_y % delta_x != 0:
                deplacement-yb = deplacement_y + 1
#                                                                                                             passage dans l'autre sens pour laisser la place au passage d'une entité
    if deplacement_curseur(point_1, point_2, deplacement_x, deplacement_y, deplacement_xb, deplacement_yb) or deplacement_curseur(point_2, point_1, 0-deplacement_x, 0-deplacement_y, 0-deplacement_xb, 0-deplacement_yb):
        return True
    return False

def deplacement_curseur(point_1, point_2, deplacement_x, deplacement_y, deplacement_xb, deplacement_yb):
    curseur = list(point_1)
    while curseur != point_2:
        curseur[0] += deplacement_x
        if get_block(curseur[0], curseur[1]).type != 'air':
            return True
        curseur[1] += deplacement_y
        if get_block(curseur[0], curseur[1]).type != 'air':
            return True
        if deplacement_xb:
            curseur[0] += deplacement_xb
            if get_block(curseur[0], curseur[1]).type != 'air':
                return True
        if deplacement_yb:
            curseur[1] += deplacement_yb
            if get_block(curseur[0], curseur[1]).type != 'air':
                return True
    return False
"""
"""
    
    deplacement_x   = int(delta_x/delta_y)
    if delta_x % delta_y != 0:
        deplacement_x_2 = int(delta_x/delta_y)+1
    else:
        deplacement_x_2 = None
    curseur = point_1

    while curseur != point2:
        curseur[0] += deplacement_x
        if curseur == point_2:
            break
        if get_bloc(curseur).type != 'air':
            return True

        curseur[1] += 1
        if curseur == point_2:
            break
        if get_bloc(curseur).type != 'air':
            return True

        if deplacement_x_2:
            pass
# A FINIR
"""
def distance(point_1:tuple, point_2:tuple):
    """
    Retourne sous forme de tuple la distance (horizontale puis verticale) entre deux points.
    * point_1 (tuple) : coordonnees (x, y) du premier point
    * point_2 (tuple) : coordonnees (x, y) du deuxième point
    """
    return abs(point_1[0] - point_2[0]), abs(point_1[1] - point_2[1])
    # théorème de Pythagore pour calculer distance

from math import sqrt
def distance_directe(point_1:tuple, point_2:tuple):
    """
    Retourne un float correspondant à la distance directe entre deux points.
    * point_1 (tuple) : coordonnees (x, y) du premier point
    * point_2 (tuple) : coordonnees (x, y) du deuxième point
    """
    distance_indirecte= distance(point_1, point_2)
    return sqrt( distance_indirecte[0]**2 + distance_indirecte[1]) + 1


################################################################################

"""joueur  = Joueur((0, 0), 100, 5, ['air' for _ in range(0, 6)])
monstre = Entite((0,0), 50, 10, [Arme(20)])
epee    = Arme(20)"""



class Block():
    """
    Un block standard
    """
    def __init__(self, typpe, x_debut, y_debut,textur):
        """
        Consrtucteur de la classe Block.
        * type (str) : le type de block
        * debut (tuple) : les coordonnes (x, y) de début du block
        * texture (str) : envoie la texture du block associer
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

class Item:
    def __init__(self, nom, x, y, image):
        self.nom = nom
        self.x = x
        self.y = y
        self.image = image
        self.vy = 0
        self.ausol = False

    def texture(self,canva):
        self.id_item = canva.create_image(self.x , self.y, image = self.image, anchor = "center", tags=("items",))

    def physique_item(self, canva, gravite, chunk):
        self.vy += gravite
        canva.move(self.id_item, 0, self.vy)

        x1, y1 = canva.coords(self.id_item)
        x2 = x1 + 20
        y2 = y1 + 20

        collisions = False
        voisins = self.blocs_autour(x1, y1, chunk)

        for bloc in voisins:
            if bloc.get_type() in ("grass", "air", "flower"):
                continue

            bx1, by1 = bloc.x_debut, bloc.y_debut
            bx2, by2 = bx1 + 50, by1 + 50

            if not (x2 <= bx1 or x1 >= bx2 or y2 <= by1 or y1 >= by2):

                if self.vy > 0:  # chute
                    canva.move(self.id_item, 0, by1 - y2)
                    self.vy = 0
                    self.ausol = True

                elif self.vy < 0:  # montée
                    canva.move(self.id_item, 0, by2 - y1)
                    self.vy = 0

                collisions = True
                break

        if not collisions:
            self.ausol = False



    def blocs_autour(self, px, py, chunk):
        gx = int(px // 50)
        gy = int(py // 50)

        voisins = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                bloc = chunk.get((gx + dx, gy + dy))
                if bloc and bloc.type != "air":
                    voisins.append(bloc)
        return voisins 


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
        self.large_world= 3000

        self.items = {}
        self.timing_animation = time.time()

        self.gravite = 1.3
        self.gravite_saut = -20
        self.vitesse_joueur = 8
        self.vitesse_verticale = 0
        self.ausol = False

        self.etat = {"droite": True,"marche": False,"mine":False}
        self.timing = time.time()
        self.delai_animation  = 0.12
        self.anim_index = 0
        self.anim_index_m = 0

        self.loot_table = {
                            "grass_block": [("dirt"     ,         1   )],
                            "dirt"       : [("dirt"     ,         1   )],
                            "rock"       : [("stone"    ,         1   )],
                            "iron"       : [("iron"     ,         1   )],
                            "coal"       : [("coal"     , randint(1,2))],
                            "wood"       : [("wood"     , randint(1,3))],
                            "leaves"     : [("leaves"   , randint(0,2))]
                           }
        
        self.inventaire = [None] * 9
        self.inventaire[0] = {"nom": "stone", "quantite": 12, "image": None}
        self.inventaire[1] = {"nom": "wood", "quantite": 5, "image": None}

        """import toutes les images du dossier /texture"""
        for fichier in os.listdir("texturing"):
            chemin_complet = os.path.join("texturing", fichier)
            image = Image.open(chemin_complet).convert("RGBA")
            image = image.resize((50, 50))
            self.image_liste[os.path.splitext(fichier)[0]] = ImageTk.PhotoImage(image)
            self.image_liste_PIl[os.path.splitext(fichier)[0]] = image
        
        """creer une image transparente"""
        air_img = Image.new("RGBA",(50,50),(0,0,0,0))
        self.air = ImageTk.PhotoImage(air_img)

        """creation et modification du canva"""
        self.sw = tk.Canvas(self,width=self.long_world,height = self.large_world,bg="skyblue",
                            scrollregion=(0,0,self.long_world,self.large_world))
        self.sw.pack()
        """creation du sprite d'un joueur"""
        self.joueur = self.sw.create_image(500, 1300, image = self.image_liste["steeve"],anchor="nw")
        self.mouton = Entite(self.image_liste["sheep"],500,2500,20,1)
        self.mouton.set_texture(self.sw)

        """creer un monde et l'update""" #ajouter le chargement de mode dynamique.
        self.create_world()
        self.charge_world()
        self.update()

        """prend les info de la taille de l'écran"""
        self.x_visible=self.winfo_width()
        self.y_visible=self.winfo_height()

        """variable pour régler des problème de touche"""
        self.touches_presser={}
        self.delai_touche =1.8

        """lance les animation en boucle"""
        self.casser_animation()
        self.deplacement_animation()

        """permet de lancer la fonction qui pose et casse des blocks"""
        self.sw.tag_bind("block", "<ButtonPress-1>", self.click_maintenue)
        self.sw.tag_bind("block", "<ButtonRelease-1>", self.click_lacher)
        self.sw.tag_bind("block","<Button-3>",self.poser_block)

        """fonctions pour les problème de touches"""
        self.bind_all("<KeyPress>", self.touche_appuyer, add="+")
        self.bind_all("<KeyRelease>", self.touche_relacher, add="+")
        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<FocusOut>", lambda e: self.touche_effacer())

        """lance une fonction qui s'occupe le réagenssement des fenetres"""
        self.bind("<Configure>", lambda e: self.taille_visible(e))

        """gère et remet le focus sur le canevas"""
        self.sw.focus_set()
        self.sw.focus_force()

        """définti quelle block pose la fonction poser_block"""
        self.type_block_choisie = "dirt"
        self.textur_block_choisie= self.image_liste["dirt"]

        """fonctionnement du monde"""
        self.after(16, self.jeu_a_jour)
        self.after(16, self.physique_a_jour)
        #self.after(500, self.touche_nettoyer)

    """génère tout les blocks du monde dans la liste monde"""
    def create_world(self):
        """on utilise self.long_world, self.large_world pour la grille"""

        coordonnes= self.long_world // 50 
        couche = self.large_world // 50 

        self.nb = 0
        self.taille_biome = [15,20,17]
        self.choix = 0

        for y in range(couche):

            for x in range(coordonnes):

                if y == 60:
                    self.monde.append(Block("bedrock", x*50, y*50, self.image_liste["bedrock"]))

                elif 45 <= y < 60 :
                    d = randint(1,200)

                    if d == 1 :
                        self.monde.append(Block("iron", x*50, y*50, self.image_liste["iron"]))

                    elif d == 2 or d ==3 :
                        self.monde.append(Block("coal", x*50, y*50, self.image_liste["coal"]))

                    else:
                        self.monde.append(Block("rock", x*50, y*50, self.image_liste["stone"]))

                elif 30 <= y < 45:
                    self.monde.append(Block("dirt", x*50, y*50, self.image_liste["dirt"]))

                elif 29 <= y < 30:
                    self.monde.append(Block("grass_block", x*50, y*50, self.image_liste["grass_block"]))

                elif 28 <= y < 29:

                    if self.nb == 0:
                        self.biomes = randint(1,2) 
                        self.nb = self.taille_biome[randint(0,2)]
                        print(self.biomes, self.nb)

                    else:
                        self.nb -= 1

                        if self.biomes == 1:

                            if randint(1, 3) == 1:
                                self.planter_arbre(x, y)
                    
                        if self.biomes == 2:
                            if randint(1,10) in (1,2,3,4):
                
                                if randint(1,10) in (1,2,3,4,5,6,7,8,9):

                                    if randint(1,2) == 1:
                                        self.monde.append(Block("grass", x*50, y*50, self.image_liste["g1"]))

                                    else:
                                        self.monde.append(Block("grass", x*50, y*50, self.image_liste["g1s"]))
                                else:
                                    self.monde.append(Block("flower", x*50, y*50, self.image_liste["flower"]))
                            else:
                                self.monde.append(Block("air", x*50, y*50, self.air))
                else:
                    self.monde.append(Block("air", x*50, y*50, self.air))

    
    def planter_arbre(self, x, sol):
        hauteur = randint(3, 5)

        # Tronc
        for i in range(hauteur):
            self.monde.append(
                Block("wood", x*50, (sol - i) *50, self.image_liste["wood"])
            )

        # Feuilles
        sommet = sol - hauteur

        for dx in range(-2, 3):
            for dy in range(-2, 2):
                if abs(dx) + abs(dy) <= 3:
                    self.monde.append(
                        Block("leaves", (x + dx)*50, (sommet + dy)*50, self.image_liste["leaves"]
                        )
                    )
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
        self.after(33, self.jeu_a_jour)

    def physique_a_jour(self):
        self.vitesse_verticale += self.gravite
        self.deplacement_joueur(0,self.vitesse_verticale)
        for item in self.items.values():
            item.physique_item(self.sw, self.gravite, self.chunk)
        self.ramassage_items()
        #self.mouton.deplacement
        self.after(33,self.physique_a_jour)

    def deplacement_joueur(self,deplacement_x, deplacement_y):
        self.sw.move(self.joueur,deplacement_x,deplacement_y)
        x1,y1 =self.sw.coords(self.joueur)
        x2 = x1 + 50
        y2 = y1 + 50
        collisions = False

        voisins = self.blocs_autour(x1, y1)
        for bloc in voisins:
            if bloc.get_type() in ("grass","air","flower"):
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

        if x1  <0:
            self.sw.move(self.joueur, -x1,0)
        elif x2 > self.long_world:
            self.sw.move(self.joueur,self.long_world - x2,0)
        if y2 > self.large_world:
            self.sw.move(self.joueur,0, self.large_world- y2)
            self.vitesse_verticale = 0
            self.ausol = True
        self.camera_centrer(x1,x2,y1,y2)

    def camera_centrer(self,x1,x2,y1,y2):
        pos_x = (x1 + x2) / 2
        pos_y = (y1 + y2) / 2
        vue_x = (pos_x - self.x_visible / 2) / self.long_world
        vue_y = (pos_y - self.y_visible / 2) / self.large_world
        self.sw.xview_moveto(max(0, min(1, vue_x)))
        self.sw.yview_moveto(max(0, min(1, vue_y)))
        self.chunk_render()


#prend l'id des block et les supprimes et delete leur texture en prennant le click souris
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
                
    def spawn_item(self, nom, x, y):


        image    = self.image_liste_PIl[nom]
        image    = image.resize((20,20))
        image_tk = ImageTk.PhotoImage(image)

        item = Item(nom, x + randint(-5,5), y, image_tk)
        item.texture(self.sw)
        self.items[item.id_item] = item

    def ramassage_items(self):
        px1, py1,  = self.sw.coords(self.joueur)
        px2 = px1 + 50
        py2 = py1 + 50
        for item_id, item in list(self.items.items()):
            ix1, iy1 = self.sw.coords(item.id_item)
            ix2 = ix1 + 20
            iy2 = iy1 + 20

            # Collision AABB
            if not (px2 < ix1 or px1 > ix2 or py2 < iy1 or py1 > iy2):
                self.ajouter_item(item.nom, 1)

                # Supprimer l'item
                self.sw.delete(item.id_item)
                del self.items[item_id]

    def ajouter_item(self, nom, quantite=1):

        for slot in self.inventaire:
            if slot and slot["nom"] == nom:
                slot["quantite"] += quantite
                return self.inventaire

        for i in range(len(self.inventaire)):
            if self.inventaire[i] is None:
                self.inventaire[i] = {
                    "nom": nom,
                    "quantite": quantite,
                    "image": None
                }
                return


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



if __name__ == "__main__":
    jeux = Python_Craft()
    jeux.mainloop()