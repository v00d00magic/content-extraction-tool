from ..Argument import Argument
from pydantic import Field
from App import app

class ExecutableArgument(Argument):
    str_type: str = Field(default = None)

    def implementation(self, i = {}):
        return app.ExecutablesTable.list.find(key = self.inputs)
