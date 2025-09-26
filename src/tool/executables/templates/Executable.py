from executables.templates.Containable import Containable
from executables.templates.Documentable import Documentable
from executables.templates.EnvContainable import EnvContainable
from executables.templates.RecursiveDeclarable import RecursiveDeclarable
from executables.templates.Runnable import Runnable
from executables.templates.Saveable import Saveable
from executables.templates.Sectionable import Sectionable
from executables.templates.Submodulable import Submodulable

class Executable(Containable, Documentable, EnvContainable, RecursiveDeclarable, Runnable, Saveable, Sectionable, Submodulable):
    def defineWrapper(self, wrapper):
        self.call = wrapper
