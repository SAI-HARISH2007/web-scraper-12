import customtkinter as ctk
from PIL import Image, ImageTk
import time
import threading
import subprocess

def close():
    root.destroy()

def run_subprocess():
    subprocess.Popen(['python', 'LOGIN_PAGE.py'])

def open_file():
    threading.Thread(target=run_subprocess).start()

def INITIALIZING_PAGE():
    D_W = root.winfo_screenwidth()
    D_H = root.winfo_screenheight()
    x = (D_W // 2) - (600 // 2)
    y = (D_H // 2) - (325 // 2)
    root.geometry(f"{600}x{370}+{x}+{y}")
    root.overrideredirect(True)

    image = Image.open(r"PICS\intro page.png")
    image = image.resize((580, 320), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    image_label = ctk.CTkLabel(root, image=photo, text="")
    image_label.place(x=10, y=10)

    threading.Thread(target=PROGRESS).start()

def PROGRESS():
    progress = ctk.CTkProgressBar(root, width=300)
    progress.pack(side='bottom', pady=20)
    progress.set(0)
    PROG_LOAD = ctk.CTkLabel(root, text=f"LOADING {0} %",
                              font=("Agency FB", 20))
    PROG_LOAD.place(x=260, y=305)

    for i in range(101):
        time.sleep(0.02)
        PROG_LOAD.configure(text=f"LOADING {i} %")
        progress.set(i / 100)
    open_file()  

ctk.set_appearance_mode("Dark")
root = ctk.CTk()
INITIALIZING_PAGE()
root.mainloop()
