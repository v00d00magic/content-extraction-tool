from executables.templates.Executable import Executable
from executables.responses.ItemsResponse import ItemsResponse

class Extractor(Executable):
    self_name = "Extractor"

    def getResult(self):
        return ItemsResponse(self.variable("items").get())
