from ..Templates.Containable import Containable
from ..Templates.EnvContainable import EnvContainable
from ..Templates.RecursiveDeclarable import RecursiveDeclarable
from ..Templates.Runnable import Runnable
from ..Templates.Submodulable import Submodulable
from Objects.Object import Object
from Objects.Namespace import Namespace

class Executable(Object, Namespace, Containable, EnvContainable, RecursiveDeclarable, Runnable, Submodulable):
    self_name: str = "None"

    @classmethod
    def makeSelfCall(cls):
        from ..ExecutableCall import ExecutableCall

        return ExecutableCall(executable=cls)
