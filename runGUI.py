from doinkGUI import MainGUI
from tkinter import Tk

if __name__=="__main__":
    root = Tk()
    app = MainGUI(master=root)
    root.title("Doink Calculator")
    root.mainloop()