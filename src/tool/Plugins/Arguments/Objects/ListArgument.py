from Plugins.Arguments.Argument import Argument
from Plugins.Data.JSON.JSON import JSON
from pydantic import Field, computed_field

class ListArgument(Argument):
    orig: Argument = Field()

    def implementation(self):
        lists = []
        if type(self.current) == list:
            lists = self.current
        if type(self.current) == str:
            is_json = JSON(self.passed_value).isValid()
