from Plugins.App.Executables.Response.Response import Response
from Plugins.App.Executables.Response.ModelsResponse import ModelsResponse

class RunQueueResults():
    items: dict = {}
    iterator: int = 0

    def get(self, index: int) -> dict:
        if index < 0:
            return self.items[len(self.items.keys()) + index]

        return self.items[index]

    def set(self, iterator: int, item: dict):
        self.items[iterator] = item

    def getResults(self, iterator: int | str) -> Response:
        if type(iterator) == int:
            return self.get(iterator)
        elif iterator == 'join':
            response = ModelsResponse()

            for key, value in self.items.items():
                response.data.append(value)

            return response
