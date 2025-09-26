from Executables.templates.Containable import Containable
from Executables.templates.Documentable import Documentable
from Executables.templates.EnvContainable import EnvContainable
from Executables.templates.RecursiveDeclarable import RecursiveDeclarable
from Executables.templates.Runnable import Runnable
from Executables.templates.Saveable import Saveable
from Executables.templates.Sectionable import Sectionable
from Executables.templates.Submodulable import Submodulable

class Executable(Containable, Documentable, EnvContainable, RecursiveDeclarable, Runnable, Saveable, Sectionable, Submodulable):
    def defineWrapper(self, wrapper):
        self.call = wrapper
