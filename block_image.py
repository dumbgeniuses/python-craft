import tkinter as tk
from PIL import Image, ImageTk

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Scaled Image Viewer")

    # Load the image
    original_image = Image.open("./textures/missing.png")
    
    # Scale the image (e.g., 40x larger)
    scale_factor = 40
    scaled_size = (original_image.width * scale_factor, 
                  original_image.height * scale_factor)
    scaled_image = original_image.resize(scaled_size, Image.Resampling.NEAREST)
    
    # Convert to PhotoImage for Tkinter
    photo = ImageTk.PhotoImage(scaled_image)
    
    # Create a label to display the image
    label = tk.Label(root, image=photo)
    label.image = photo  # Keep a reference!
    label.pack(padx=10, pady=10)

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()