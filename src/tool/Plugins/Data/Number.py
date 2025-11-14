from Plugins.App.Executables.Types.Representation import Representation
from Plugins.App.Arguments.ApplyArgumentList import ApplyArgumentList
from Plugins.App.Arguments.Types.IntArgument import IntArgument

class Number(Representation):
    @classmethod
    def define_data(cls):
        class NewContent(Representation.ContentUnit):
            class Data(Representation.ContentUnit.Data):
                number: int = None

            content: Data

        return NewContent
