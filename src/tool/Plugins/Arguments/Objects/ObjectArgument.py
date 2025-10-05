from Plugins.Arguments.Argument import Argument
from Plugins.Data.JSON.JSON import JSON
from typing import Any
from Objects.Object import Object
from pydantic import Field, computed_field

class ObjectArgument(Argument):
    object: Any = Field()

    def implementation(self):
        lists = []
        if type(self.current) == list:
            lists = self.current
        if type(self.current) == str:
            is_json = JSON(self.passed_value).isValid()
