from executables.templates.Runnable import Runnable
from executables.templates.Documentable import Documentable
from executables.templates.Saveable import Saveable
from executables.templates.RecursiveDeclarable import RecursiveDeclarable
from utils.Hookable import Hookable
from app.App import logger

class Executable(Runnable, Documentable, Saveable, RecursiveDeclarable, Hookable):
    def __init__(self):
        super().__init__()

        def __onerror(exception):
            logger.logException(exception, section=logger.SECTION_EXECUTABLES)

        self.add_hook("error", __onerror)
