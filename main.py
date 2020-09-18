from nim_gui import NimGui
from tkinter import *

if __name__ == "__main__":
    main = Tk()
    main.geometry("600x600")
    c = NimGui(main)
    main.mainloop()