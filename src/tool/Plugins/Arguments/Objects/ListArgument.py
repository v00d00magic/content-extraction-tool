from Plugins.Arguments.Argument import Argument
from Plugins.Data.JSON.JSON import JSON
from pydantic import Field, computed_field

class ListArgument(Argument):
    orig: Argument = Field()
    total_count: int = Field(default=0)

    def implementation(self, i = {}):
        lists = []
        value = self.inputs

        if type(value) == list:
            lists = value
        if type(value) == str:
            is_json = JSON(value).isValid()

        return value

    def getCount(self):
        return len(self.current)

    def getCompleteness(self):
        return self.getCount() / self.total_count

    def append(self, item):
        self.current.append(item)
