# Import the Linear programming library
from pulp import *

class Problem():
    def __init__(self):
        # Variable definition.
        self.factoriesData = [
            {
                "FactoryName": "Dairy",
                "C": 400,    # $/ton
                "B": 850,    # mg/L (ton^-6/m^3)
                "S": 0.56,   # $/m^3
                "E": 0.9,    # Efficiency
                "Ed" : 0.05, # variable drift
                "W": 1200    # m^3/d
            },
            {
                "FactoryName": "Beverage",
                "C": 500,   # $/ton
                "B": 400,   # mg/L (ton^-6/m^3)
                "S": 0.25,  # $/m^3
                "E": 0.95,  # Efficiency
                "Ed": 0.02,  # Variable drift
                "W": 4000   # m^3/d
            }
        ]
        self.limit = 170 # kg (ton^-3)

    def problemDefiner(self, isRobust=False):
        # Problem definition
        self.wasteManagement = LpProblem('Waste management', LpMinimize)

        # Define our decision variables
        for factory in self.factoriesData:
            factory["x"] = LpVariable(factory["FactoryName"]+' x', 0, factory["W"])     # m^3
            factory["y"] = LpVariable(factory["FactoryName"]+' y', 0, None)             # m^3

        # Cost definition
        self.Cost = LpVariable('Total cost', 0)
        self.wasteManagement += self.Cost == sum(factory["C"] * (1/1000000) * factory["B"] * factory["x"] + factory["S"] * factory["y"] for factory in self.factoriesData)
        self.wasteManagement.setObjective(self.Cost)


        # Define constraints
        
        # Allow the model to manage cases where there is deviation
        if isRobust: 
            self.wasteManagement += sum((1/1000000) * factory["B"] * (1-factory["E"]*(1-factory["Ed"])) * factory["x"] for factory in self.factoriesData) <= self.limit/1000           
        else:
            self.wasteManagement += sum((1/1000000) * factory["B"] * (1-factory["E"]) * factory["x"] for factory in self.factoriesData) <= self.limit/1000
        
        for factory in self.factoriesData:
            self.wasteManagement += factory["y"] == factory["W"] - factory["x"]

        # Solve the model
        self.status = self.wasteManagement.solve()
        assert self.status == LpStatusOptimal
        
        message = "Optimal point found.\nCost: $"+ str(round(value(self.Cost),2))+" \n" 
        for i in range(len(self.factoriesData)):
            message += "X" + str(i+1) + ": " + str(round(value(self.factoriesData[i]["x"]),2)) + "m^3 , "
            message += "Y" + str(i+1)+ ": " + str(round(value(self.factoriesData[i]["y"]),2)) + "m^3\n"
        
        return message

