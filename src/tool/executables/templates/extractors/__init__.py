from Executables.templates.Executable import Executable
from Executables.responses.ItemsResponse import ItemsResponse

class Extractor(Executable):
    self_name = "Extractor"

    def getResult(self):
        return ItemsResponse(self.variable("items").get())
