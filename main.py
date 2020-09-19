from nim_gui import NimGui
<<<<<<< HEAD
import tkinter as tk

if __name__ == "__main__":
    main = tk.Tk()
    main.geometry("1000x700")
=======
from tkinter import *

if __name__ == "__main__":
    main = Tk()
    main.geometry("600x600")
>>>>>>> 6e65c48e97719b3ec4133a9cb3d37edbcffb721b
    c = NimGui(main)
    main.mainloop()