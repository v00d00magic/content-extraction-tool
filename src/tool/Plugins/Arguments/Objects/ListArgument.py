from Plugins.Arguments.Argument import Argument
from Plugins.Data.JSON.JSON import JSON
from pydantic import Field, computed_field

class ListArgument(Argument):
    orig: Argument = Field()
    total_count: int = Field()

    def implementation(self):
        lists = []
        if type(self.value) == list:
            lists = self.value
        if type(self.value) == str:
            is_json = JSON(self.passed_value).isValid()

        return []

    def getCount(self):
        return len(self.value)

    def getCompleteness(self):
        return self.getCount() / self.total_count

    def append(self, item):
        self.value.append(item)
