
# Interface library
from tkinter import *
from Problem import *
from NewFactoryWindow import * 
from EditFactoryWindow import *

class HybridInterface(Frame):

    def __init__(self, parent, **kwargs):
        self.problem = Problem()
        Frame.__init__(self, parent, width=768, height=576, **kwargs)
        self.pack(fill=BOTH)
        
        # Widgets creation
        # Left side widgets (Factory info)
        self.factoriesListFrame = Frame(self, borderwidth=10)
        self.factoriesListFrame.pack(side="left", fill=Y)
        # Factories List
        self.variableLabel = Label(self.factoriesListFrame, text="Current factories")
        self.variableLabel.pack()
        self.variableList = Listbox(self.factoriesListFrame)
        self.variableList.pack(side = "bottom", fill=X)

        for factory in self.problem.factoriesData:
            self.variableList.insert(END, factory["FactoryName"])
        
        self.factoryButtonsFrame = Frame(self.factoriesListFrame)
        self.factoryButtonsFrame.pack(side="bottom", fill = X)
        # Factory management buttons
        self.viewButton = Button(self.factoryButtonsFrame, text="New", command=self.newFactory)
        self.viewButton.pack(side="left")
        self.editButton = Button(self.factoryButtonsFrame, text="Edit", command=self.editFactory)
        self.editButton.pack(side="left")
        self.deleteButton = Button(self.factoryButtonsFrame, text="Delete", command=self.deleteFactory)
        self.deleteButton.pack(side="left")

        # Right side widgets
        self.rightFrame = Frame(self, borderwidth=10)
        self.rightFrame.pack(side= "right", fill=Y)

        # Limit setter
        self.userParams = Frame(self.rightFrame, bd = 10)
        self.userParams.pack(side="top", fill=X)
        self.limitFrame = Frame(self.userParams, bd= 10)
        self.limitFrame.pack(side = "top", fill=X)
        self.limitLabel = Label(self.limitFrame, text = "Limit")
        self.limitLabel.pack(side="left")
        self.limitBox = Entry(self.limitFrame, width=10)
        self.limitBox.insert(END, str(self.problem.limit))
        self.limitBox.pack(side="right")
        self.varFrame = Frame(self.userParams, bd= 10)
        self.varFrame.pack(side = "top", fill=X)
        self.varLabel = Label(self.varFrame, text = "Deviation to ignore (%)")
        self.varLabel.pack(side="left")
        self.varBox = Entry(self.varFrame, width=10)
        self.varBox.insert(END, str(0))
        self.varBox.pack(side="right")

        # Model choice frame
        self.modelChoiceFrame = Frame(self.rightFrame, borderwidth=1)
        self.modelChoiceFrame.pack(side ="top", fill=X)
        # Model choice label
        self.prompt = Label(self.modelChoiceFrame, text="Modelling is hybrid.")
        self.prompt.pack()

        # Result display
        self.message = Label(self.rightFrame, text="No optimization has been launched yet.")
        self.message.pack()

        # Quit and optmize buttons      
        self.optimizeButton = Button(self.rightFrame, text="Start optimization",
                command=self.optimize)
        self.optimizeButton.pack()

    def optimize(self):
        self.problem.limit = float(self.limitBox.get())
        optimizationResult = self.problem.problemDefiner(True ,float(self.varBox.get()))
        self.message["text"] = optimizationResult

    def newFactory(self):
        newWindow = Tk()
        NewFactoryWindow(newWindow, self.problem.factoriesData, self)
        newWindow.mainloop()
        
    def editFactory(self):
        newWindow = Tk()
        selection = self.variableList.curselection()[0]
        EditWindow(newWindow, self.problem.factoriesData[selection], self)
        newWindow.mainloop()

    def deleteFactory(self):
        self.problem.factoriesData.pop(self.variableList.curselection()[0])
        self.updateFactoryList()

    def updateFactoryList(self):
        self.variableList.delete(0, END)  #clear listbox
        for factory in self.problem.factoriesData:
            self.variableList.insert(END, factory["FactoryName"])
