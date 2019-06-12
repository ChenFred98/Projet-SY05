# Interface library
from tkinter import *

class NewFactoryWindow(Frame):
    def __init__(self, window, factoriesList, mainWindow, **kwargs):   
        window.title("Add a factory")
        self.mainWindow = mainWindow 
        self.factoriesList = factoriesList
        self.mainFrame = Frame(window, borderwidth=10)
        self.mainFrame.pack()
        self.parametersFrames = []
        self.labelFrames = []
        self.boxesFrames = []
        i = 0
        # Edit boxes
        for key,value in self.factoriesList[0].items():
            if i<7:
                self.parametersFrames.append(Frame(self.mainFrame, borderwidth=10))
                self.parametersFrames[i].pack(fill=X)
                self.labelFrames.append(Label(self.parametersFrames[i], text= str(key)+"  ", anchor='w'))
                self.labelFrames[i].pack(side="left")
                self.boxesFrames.append(Entry(self.parametersFrames[i], width=10))
                self.boxesFrames[i].pack(side="right")
            i += 1
        self.editButton = Button(self.mainFrame, text="Create !", command=self.create)
        self.editButton.pack(side="right")

    def create(self):
        i = 0
        factory = {}
        for key,value in self.factoriesList[0].items():
            if i<7 and self.boxesFrames[i].get() != "":
                try:
                    factory[key] = float(self.boxesFrames[i].get())
                except:
                    factory[key] = self.boxesFrames[i].get()
            i += 1
        self.factoriesList.append(factory)
        self.mainWindow.updateFactoryList()

