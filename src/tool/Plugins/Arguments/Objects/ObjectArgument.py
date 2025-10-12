from Plugins.Arguments.Argument import Argument
from typing import Any
from pydantic import Field, computed_field

class ObjectArgument(Argument):
    object: Any = Field(default = None)

    def implementation(self, i = {}):
        if self.object == None:
            return self.inputs
        
        _item = self.object
        _item.model_validate(self.inputs)

        return _item(**self.inputs)
