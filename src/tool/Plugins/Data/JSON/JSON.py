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

    def useAsClass(self, data: dict):
        self.variables.get("json").current = data

    def getSelf(self) -> str:
        return self.variables.items.get("json").current

    def setSelf(self, new: str) -> str:
        self.variables.items.get("json").current = new

        return self.getSelf()

    def parse(self) -> dict:
        if type(self.getSelf()) == str:
            return self.setSelf(json.loads(self.getSelf()))

        return self.getSelf()

    def dump(self, indent = None) -> str:
        return json.dumps(self.getSelf(), ensure_ascii = False, indent = indent)

    def isValid(self):
        try:
            return self.getSelf() != None and type(self.getSelf()) != int and type(self.getSelf()) != str
        except json.JSONDecodeError:
            return False
        except TypeError:
            return False
