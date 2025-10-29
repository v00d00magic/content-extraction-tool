from datetime import datetime
from Plugins.App.Arguments.ApplyArgumentList import ApplyArgumentList
from Plugins.App.Arguments.Objects.ObjectArgument import ObjectArgument
from Plugins.App.Executables.Types.Representation import Representation

class Date(Representation):
    class Variables(Representation.Variables):
        items = ApplyArgumentList([
            ObjectArgument(
                name = "date",
                default = {}
            )
        ])

    def useAsClass(self, data: int = None):
        self.variables.get("date").current = int

    def setNow(self):
        return self.setSelf(datetime.now().timestamp())
