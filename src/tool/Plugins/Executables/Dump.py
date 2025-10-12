from Objects.Object import Object
from Plugins.Executables.Types.Executable import Executable
from pydantic import Field

class Dump(Object):
    executable: Executable = Field()
    data: dict = Field()
