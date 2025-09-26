class Containable():
    # or better Variableble

    def defineVariables(self):
        pass

    def __init__(self):
        self.variables = self.defineVariables()

    def variable(self, name):
        return self.variables.get(name)

    def getResult(self):
        pass
