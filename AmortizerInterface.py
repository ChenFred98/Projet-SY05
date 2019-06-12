# Interface library
from tkinter import *
from Problem import *
from NewFactoryWindow import * 
from EditFactoryWindow import *
import matplotlib.pyplot as plt

class AmortizerInterface(Frame):
    def __init__(self, parent, **kwargs):
        self.currentProblem = Problem()
        self.targetProblem = Problem()
        Frame.__init__(self, parent, width=768, height=576, **kwargs)
        self.pack(fill=BOTH)
        
        # Widgets creation
        # Left side widgets (Factory info)
        self.leftFrame = Frame(self, borderwidth=10)
        self.leftFrame.pack(side= "left", fill=Y)
        self.currentFactoriesListFrame = Frame(self.leftFrame, borderwidth=10)
        self.currentFactoriesListFrame.pack(side="left", fill=Y)
        self.targetFactoriesListFrame = Frame(self.leftFrame, borderwidth=10)
        self.targetFactoriesListFrame.pack(side="left", fill=Y)

        # Current Factories List
        self.currentVariableLabel = Label(self.currentFactoriesListFrame, text="Current factories")
        self.currentVariableLabel.pack()
        self.currentVariableList = Listbox(self.currentFactoriesListFrame)
        self.currentVariableList.pack(side = "bottom", fill=X)

        for factory in self.currentProblem.factoriesData:
            self.currentVariableList.insert(END, factory["FactoryName"])
        
        self.currentFactoryButtonsFrame = Frame(self.currentFactoriesListFrame)
        self.currentFactoryButtonsFrame.pack(side="bottom", fill = X)
        # Factory management buttons
        self.currentViewButton = Button(self.currentFactoryButtonsFrame, text="New", command=self.newCurrentFactory)
        self.currentViewButton.pack(side="left")
        self.currentEditButton = Button(self.currentFactoryButtonsFrame, text="Edit", command=self.editCurrentFactory)
        self.currentEditButton.pack(side="left")
        self.currentDeleteButton = Button(self.currentFactoryButtonsFrame, text="Delete", command=self.deleteCurrentFactory)
        self.currentDeleteButton.pack(side="left")
        
        # Target Factories List
        self.targetVariableLabel = Label(self.targetFactoriesListFrame, text="Modified factories")
        self.targetVariableLabel.pack()
        self.targetVariableList = Listbox(self.targetFactoriesListFrame)
        self.targetVariableList.pack(side = "bottom", fill=X)

        for factory in self.targetProblem.factoriesData:
            self.targetVariableList.insert(END, factory["FactoryName"])
        
        self.targetFactoryButtonsFrame = Frame(self.targetFactoriesListFrame)
        self.targetFactoryButtonsFrame.pack(side="bottom", fill = X)
        # Factory management buttons
        self.targetViewButton = Button(self.targetFactoryButtonsFrame, text="New", command=self.newTargetFactory)
        self.targetViewButton.pack(side="left")
        self.targetEditButton = Button(self.targetFactoryButtonsFrame, text="Edit", command=self.editTargetFactory)
        self.targetEditButton.pack(side="left")
        self.targetDeleteButton = Button(self.targetFactoryButtonsFrame, text="Delete", command=self.deleteTargetFactory)
        self.targetDeleteButton.pack(side="left")

        # Right side widgets
        self.rightFrame = Frame(self, borderwidth=10)
        self.rightFrame.pack(side= "right", fill=Y)

        # Limit setter
        self.limitSetter = Frame(self.rightFrame, bd = 10)
        self.limitSetter.pack(side="top", fill=X)
        self.limitLabel = Label(self.limitSetter, text = "Limit")
        self.limitLabel.pack(side="left")
        self.limitBox = Entry(self.limitSetter, width=10)
        self.limitBox.insert(END, str(self.currentProblem.limit))
        self.limitBox.pack(side="right")
        
        # Modification Cost setter
        self.costSetter = Frame(self.rightFrame, bd = 10)
        self.costSetter.pack(side="top", fill=X)
        self.costLabel = Label(self.costSetter, text = "Modifications Cost")
        self.costLabel.pack(side="left")
        self.costBox = Entry(self.costSetter, width=10)
        self.costBox.insert(END, str(0))
        self.costBox.pack(side="right")
        
        # Model choice frame
        self.modelChoiceFrame = Frame(self.rightFrame, borderwidth=1)
        self.modelChoiceFrame.pack(side ="top", fill=X)
        # Model choice label
        self.prompt = Label(self.modelChoiceFrame, text="Modeling will be robust.")
        self.prompt.pack()

        # Result display
        self.message = Label(self.rightFrame, text="No optimization has been launched yet.")
        self.message.pack()

        # Quit and optmize buttons      
        self.displayButton = Button(self.rightFrame, text="Display graph", state=DISABLED,
                command=self.displayAmortizationGraph)
        self.optimizeButton = Button(self.rightFrame, text="Start simulation",
                command=self.optimize)
        self.displayButton.pack(side = "left")
        self.optimizeButton.pack(side = "right")

    def optimize(self):
        self.displayButton['state'] = 'normal'
        self.currentProblem.limit = float(self.limitBox.get())
        self.targetProblem.limit = float(self.limitBox.get())
        self.currentProblem.problemDefiner("robust")
        self.targetProblem.problemDefiner("robust")
        self.gainPerDay = round(value(self.currentProblem.Cost),2)-round(value(self.targetProblem.Cost),2)
        self.days = float(self.costBox.get())/self.gainPerDay
        self.message["text"] = "Potential gain is $"+ str(round(self.gainPerDay,2)) +" per day.\nModifications will be amortized in " + str(int(self.days)) + " days." 

    def displayAmortizationGraph(self):
        days = [0, 1.5*int(self.days)]
        self.potentialCosts = [float(self.costBox.get())+(day*round(value(self.targetProblem.Cost),2)) for day in days]
        self.currentCosts = [round(value(self.currentProblem.Cost),2)*day for day in days]
        self.costDifference = [(float(self.costBox.get())+(day*round(value(self.targetProblem.Cost),2)))-(round(value(self.currentProblem.Cost),2)*day) for day in days]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,6))
        ax1.set_title('Total cost throughout amortization phase')
        ax2.set_title('Cost difference throughout amortization phase')
        ax1.plot(days, self.potentialCosts, c="blue")
        ax1.plot(days, self.currentCosts, c="red")
        ax2.plot(days, self.costDifference)
        
        #Ajout des axes
        ax1.plot([0,days[1]],[0,0],color='silver',linestyle='-',linewidth=1)
        ax1.plot([0,0],[0,self.currentCosts[1]],color='silver',linestyle='-',linewidth=1)
        ax2.plot([0,0],[self.costDifference[0],self.costDifference[1]], color='silver',linestyle='-',linewidth=1)
        ax2.plot([0,days[1]],[0,0],color='silver',linestyle='-',linewidth=1)

        #Affichage
        plt.show()


    def newCurrentFactory(self):
        newWindow = Tk()
        NewFactoryWindow(newWindow, self.currentProblem.factoriesData, self)
        newWindow.mainloop()
        
    def editCurrentFactory(self):
        newWindow = Tk()
        selection = self.currentVariableList.curselection()[0]
        EditWindow(newWindow, self.currentProblem.factoriesData[selection], self)
        newWindow.mainloop()

    def deleteCurrentFactory(self):
        self.currentProblem.factoriesData.pop(self.currentVariableList.curselection()[0])
        self.updateFactoryList()

    def newTargetFactory(self):
        newWindow = Tk()
        NewFactoryWindow(newWindow, self.targetProblem.factoriesData, self)
        newWindow.mainloop()
        
    def editTargetFactory(self):
        newWindow = Tk()
        selection = self.targetVariableList.curselection()[0]
        EditWindow(newWindow, self.targetProblem.factoriesData[selection], self)
        newWindow.mainloop()

    def deleteTargetFactory(self):
        self.targetProblem.factoriesData.pop(self.targetVariableList.curselection()[0])
        self.updateFactoryList()

    def updateFactoryList(self):
        self.currentVariableList.delete(0, END)  #clear listbox
        for factory in self.currentProblem.factoriesData:
            self.currentVariableList.insert(END, factory["FactoryName"])
        self.targetVariableList.delete(0, END)  #clear listbox
        for factory in self.targetProblem.factoriesData:
            self.targetVariableList.insert(END, factory["FactoryName"])
