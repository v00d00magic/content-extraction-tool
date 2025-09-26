from Executables.templates.Executable import Executable


class Outer(Executable):
    # must not return anything
    def __init__(self, original):
        self.original = original
