from Plugins.Executables.Types.Representation import Representation
from Plugins.Arguments.Objects.ObjectArgument import ObjectArgument
from Plugins.Arguments.ApplyArgumentList import ApplyArgumentList
import json

class JSON(Representation):
    class Variables(Representation.Variables):
        items = ApplyArgumentList([
            ObjectArgument(
                name = "json",
                default = {}
            )
        ])

    def useAsClass(self, text: str):
        self.variables.get("json").current = text

    def getSelf(self) -> str:
        return self.variables.items.get("json").current

    def setSelf(self, new: str) -> str:
        self.variables.items.get("json").current = new

        return self.getSelf()

    def parse(self, data: dict):
        if type(data) == str:
            return json.loads(data)

        return data

    def dump(self, data: dict, indent = None):
        return json.dumps(data, ensure_ascii = False, indent = indent)

    def isValid(self, data: dict):
        try:
            return data != None and type(data) != int and type(data) != str
        except json.JSONDecodeError:
            return False
        except TypeError:
            return False
