from nim_gui import NimGui
import tkinter as tk

if __name__ == "__main__":
    main = tk.Tk()
    main.geometry("1000x700")
    c = NimGui(main)
    main.mainloop()