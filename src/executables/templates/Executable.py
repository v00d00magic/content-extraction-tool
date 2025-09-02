from executables.templates.Documentable import Documentable
from executables.templates.EnvContainable import EnvContainable
from executables.templates.RecursiveDeclarable import RecursiveDeclarable
from executables.templates.Runnable import Runnable
from executables.templates.Saveable import Saveable
from executables.templates.Submodulable import Submodulable
from utils.Hookable import Hookable
from app.App import logger

class Executable(Documentable, EnvContainable, RecursiveDeclarable, Runnable, Saveable, Submodulable, Hookable):
    '''
    Class that contains all other abstract classes
    '''
    def __init__(self):
        super().__init__()

        def __onerror(exception):
            logger.logException(exception, section=logger.SECTION_EXECUTABLES)

        self.add_hook("error", __onerror)
