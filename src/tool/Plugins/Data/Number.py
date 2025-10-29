from Plugins.App.Executables.Types.Representation import Representation
from Plugins.App.Arguments.ApplyArgumentList import ApplyArgumentList
from Plugins.App.Arguments.Types.IntArgument import IntArgument

class Number(Representation):
    class ContentUnit(Representation.ContentUnit):
        number: list | dict = None
