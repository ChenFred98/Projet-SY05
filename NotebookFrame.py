from tkinter import *
from tkinter import ttk
from SolverInterface import *
from AmortizerInterface import *

class NotebookFrame(Frame):

    def __init__(self, window):
        Frame.__init__(self, window)
        container = ttk.Frame(window)
        container.pack(in_=window, side='top',fill='both', expand='Y')
        self.mainView = ttk.Notebook(container, name='notebook')
        
        # Solver Tab
        solverTab = ttk.Frame(self.mainView)
        self.mainView.add(solverTab, text="Solver")
        self.mainView.pack(fill='both', expand=Y, side='top')
        SolverInterface(solverTab)

        # Simulator
        amortizerTab = ttk.Frame(self.mainView)
        self.mainView.add(amortizerTab, text="Amortizer")
        self.mainView.pack(fill='both', expand=Y, side='top')
        AmortizerInterface(amortizerTab)