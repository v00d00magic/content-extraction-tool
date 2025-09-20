from executables.templates.Executable import Executable
from app.App import logger

class Outer(Executable):
    # must not return anything
    def __init__(self, original):
        self.original = original
