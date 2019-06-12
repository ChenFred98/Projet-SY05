# Interface library
from tkinter import Tk
from NotebookFrame import *
        
if __name__ == "__main__":
    window = Tk()
    window.title("Interface - Projet SY05")
    interface = NotebookFrame(window)
    window.mainloop()
    window.destroy()