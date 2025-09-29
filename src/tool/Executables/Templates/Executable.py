from Executables.Templates.Containable import Containable
from Executables.Templates.Documentable import Documentable
from Executables.Templates.EnvContainable import EnvContainable
from Executables.Templates.RecursiveDeclarable import RecursiveDeclarable
from Executables.Templates.Runnable import Runnable
from Executables.Templates.Saveable import Saveable
from Executables.Templates.Sectionable import Sectionable
from Executables.Templates.Submodulable import Submodulable

class Executable(Containable, Documentable, EnvContainable, RecursiveDeclarable, Runnable, Saveable, Sectionable, Submodulable):
    def defineWrapper(self, wrapper):
        self.call = wrapper

    @classmethod
    def makeSelfCall(cls):
        from Executables.ExecutableCall import ExecutableCall

        return ExecutableCall(executable=cls)
