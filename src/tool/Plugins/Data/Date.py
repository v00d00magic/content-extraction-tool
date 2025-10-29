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

        @property
        def common_variable(self):
            return "date"

    def setNow(self):
        return self.setSelf(datetime.now().timestamp())
