from tkinter import *

class EditWindow(Frame):

    def __init__(self, window, factoryData,mainWindow, **kwargs):   
        window.title("Edit Factory")
        self.mainWindow = mainWindow
        self.factoryData = factoryData
        self.mainFrame = Frame(window, borderwidth=10)
        self.mainFrame.pack()
        self.parametersFrames = []
        self.labelFrames = [] 
        self.currentValuesFrames = []
        self.boxesFrames = []
        i = 0
        # Edit boxes
        for key,value in self.factoryData.items():
            if i < 7:
                self.parametersFrames.append(Frame(self.mainFrame, borderwidth=10))
                self.parametersFrames[i].pack(fill=X)
                self.labelFrames.append(Label(self.parametersFrames[i], text= str(key)+"  ", anchor='w'))
                self.labelFrames[i].pack(side="left")
                self.boxesFrames.append(Entry(self.parametersFrames[i], width=10))
                self.boxesFrames[i].pack(side="right")
                self.currentValuesFrames.append(Label(self.parametersFrames[i], text="   " + str(value), anchor='w'))
                self.currentValuesFrames[i].pack(side="right")
            i += 1
        self.finishedButton = Button(self.mainFrame, text="Finished !", command=window.destroy)
        self.finishedButton.pack(side="left")
        self.editButton = Button(self.mainFrame, text="Edit", command=self.edit)
        self.editButton.pack(side="right")

    def edit(self):
        i = 0
        for key,value in self.factoryData.items():
            if i<7 and self.boxesFrames[i].get() != "":
                try:
                    self.factoryData[key] = float(self.boxesFrames[i].get())
                except:
                    self.factoryData[key] = self.boxesFrames[i].get()
                self.currentValuesFrames[i]["text"] ="   " + str(self.factoryData[key])
            i += 1
        self.mainWindow.updateFactoryList()
