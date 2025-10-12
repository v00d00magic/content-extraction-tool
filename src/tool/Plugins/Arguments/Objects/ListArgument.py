from Plugins.Arguments.Argument import Argument
from Plugins.Data.JSON.JSON import JSON
from pydantic import Field, computed_field

class ListArgument(Argument):
    orig: Argument = Field()
    total_count: int = Field(default=0)

    def implementation(self, i = {}):
        results: list = []
        value: list = self.inputs

        if type(value) == str:
            _json = JSON(value)
            if _json.isValid() == True:
                value = _json.getSelf()

        if self.orig == None:
            return value

        for item in value:
            _orig = self.orig
            _orig.setInput(item)

            results.append(_orig.getValue())

        return results

    def getCount(self):
        return len(self.current)

    def getCompleteness(self):
        return self.getCount() / self.total_count

    def append(self, item):
        self.current.append(item)
