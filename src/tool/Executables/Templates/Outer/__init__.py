from Executables.Templates.Executable import Executable

class Outer(Executable):
    self_name = "Outer"

    # must not return anything
    def __init__(self, original):
        self.original = original
