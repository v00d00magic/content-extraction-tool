from Executables.Variables.ExecutableVariable import ExecutableVariable

class ListVariable(ExecutableVariable):
    def __init__(self):
        self.content = []

    def append(self, item):
        self.content.append(item)
