from executables.templates.Documentable import Documentable
from executables.templates.EnvContainable import EnvContainable
from executables.templates.RecursiveDeclarable import RecursiveDeclarable
from executables.templates.Runnable import Runnable
from executables.templates.Saveable import Saveable
from executables.templates.Progressable import Progressable
from executables.templates.Linkable import Linkable
from executables.templates.Sectionable import Sectionable
from executables.templates.Submodulable import Submodulable
from utils.Hookable import Hookable

class Executable(Documentable, EnvContainable, RecursiveDeclarable, Progressable, Linkable, Runnable, Saveable, Sectionable, Submodulable, Hookable):
    def defineWrapper(self, wrapper):
        self.call = wrapper
