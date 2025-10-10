from Plugins.Arguments.Argument import Argument
from Plugins.Data.JSON.JSON import JSON
from typing import Any
from Objects.Object import Object
from pydantic import Field, computed_field

class ObjectArgument(Argument):
    object: Any = Field()

    def implementation(self, i = {}):
        lists = []
        if type(self.value) == list:
            lists = self.current
        if type(self.value) == str:
            is_json = JSON(self.passed_value).isValid()
