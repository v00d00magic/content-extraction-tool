from executables.templates.Runnable import Runnable
from executables.templates.Saveable import Saveable

class ThumbnailMethod(Runnable, Saveable):
    def __init__(self, outer):
        self.outer = outer

    def create(self, item, params)->list:
        pass
