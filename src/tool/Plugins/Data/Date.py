from datetime import datetime
from Plugins.App.Arguments.ApplyArgumentList import ApplyArgumentList
from Plugins.App.Arguments.Objects.ObjectArgument import ObjectArgument
from Plugins.App.Executables.Types.Representation import Representation

class Date(Representation):
    def setNow(self):
        return self.setSelf(datetime.now().timestamp())
