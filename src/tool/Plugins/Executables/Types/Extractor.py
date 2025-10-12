from Plugins.Executables.Types.Executable import Executable

class Extractor(Executable):
    self_name: str = "Extractor"

    def getResult(self):
        return ItemsResponse(self.variable("items").get())

    def defineVariables(self):
        variables = {}
        variables["items"] = ResultsVariable()
        variables["collections"] = ResultsVariable()

        return variables
