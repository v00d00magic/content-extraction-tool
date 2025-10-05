from Executables.Templates.Executable import Executable
from Executables.Responses.ItemsResponse import ItemsResponse
from Executables.Variables.ResultsVariable import ResultsVariable

class Extractor(Executable):
    self_name: str = "Extractor"

    def getResult(self):
        return ItemsResponse(self.variable("items").get())

    def defineVariables(self):
        variables = {}
        variables["items"] = ResultsVariable()
        variables["collections"] = ResultsVariable()

        return variables
