# GENERE PAR IA POUR TEST
# GENERE PAR IA POUR TEST
# GENERE PAR IA POUR TEST

import tkinter as tk
from PIL import Image, ImageTk

class SpriteApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sprite Movement")
        self.master.geometry("800x600")

        self.canvas = tk.Canvas(master, width=800, height=600)
        self.canvas.pack()

        # Load image with a safe fallback if file or a Pillow resampling attribute is missing
        try:
            img = Image.open('./textures/missing.png')
            try:
                resample = Image.Resampling.LANCZOS
            except AttributeError:
                resample = Image.ANTIALIAS
            img = img.resize((50, 50), resample)
        except Exception:
            # create a visible magenta placeholder if the texture is missing
            img = Image.new('RGBA', (50, 50), (255, 0, 255, 255))

        self.sprite_image = img
        self.sprite = ImageTk.PhotoImage(self.sprite_image)

        self.sprite_id = self.canvas.create_image(400, 300, image=self.sprite)

        self.master.bind('<KeyPress-q>', self.move_left)
        self.master.bind('<KeyPress-d>', self.move_right)

        # Ensure the window has keyboard focus so key presses are received
        self.master.focus_set()

    def move_left(self, event=None):
        self.canvas.move(self.sprite_id, -10, 0)

    def move_right(self, event=None):
        self.canvas.move(self.sprite_id, 10, 0)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpriteApp(root)
    root.mainloop()