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
from app.App import app

class Executable(Documentable, EnvContainable, RecursiveDeclarable, Progressable, Linkable, Runnable, Saveable, Sectionable, Submodulable, Hookable):
    def __init__(self, index: int = None):
        super().__init__()

        self.preStart(index)

    def preStart(self, index: int = None):
        self.index = index
        if self.index == None:
            self.index = app.getIndex()
