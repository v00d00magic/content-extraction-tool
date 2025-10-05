class Containable():
    def defineVariables(self):
        pass

    def variable(self, name):
        if getattr(self, "variables", None) == None:
            self.variables = self.defineVariables()

        if self.variables == None:
            return None

        return self.variables.get(name)

    def getResult(self):
        '''
        If nothing returned at implementation(), we calling that function to check variables
        '''

        pass
