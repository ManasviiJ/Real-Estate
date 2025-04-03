import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def upload_images():
    file_paths = filedialog.askopenfilenames(title="Select Images", 
                                             filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    if file_paths:
        for widget in frame.winfo_children():
            widget.destroy()  # Clear previous images
        
        images.clear()
        
        for path in file_paths:
            img = Image.open(path)
            img.thumbnail((150, 150))  # Resize for display
            img_tk = ImageTk.PhotoImage(img)
            images.append(img_tk)  # Store reference to prevent garbage collection
            
            label = tk.Label(frame, image=img_tk)
            label.pack(side=tk.LEFT, padx=5, pady=5)

root = tk.Tk()
root.title("Multiple Image Uploader")

btn = tk.Button(root, text="Upload Images", command=upload_images)
btn.pack()

frame = tk.Frame(root)
frame.pack()

images = []  # Store image references

root.mainloop()
