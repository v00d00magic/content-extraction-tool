from Objects.Object import Object
from Plugins.App.Executables.Types.Executable import Executable
from pydantic import Field

class Dump(Object):
    executable: Executable = Field()
    data: dict = Field()
