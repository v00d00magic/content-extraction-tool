from Executables.responses.Response import Response

class ItemsResponse(Response):
    def check(self):
        assert type(self.data) == list, "not a list!!!"

    def items(self):
        return self.data

    def append(self, item):
        self.data.append(item)

    def display(self):
        _object = {
            "items": []
        }
        for item in self.items():
            _object["items"].append(item.getStructure())

        return _object
