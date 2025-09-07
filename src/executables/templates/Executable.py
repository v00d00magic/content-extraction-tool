from executables.templates.Documentable import Documentable
from executables.templates.EnvContainable import EnvContainable
from executables.templates.RecursiveDeclarable import RecursiveDeclarable
from executables.templates.Runnable import Runnable
from executables.templates.Saveable import Saveable
from executables.templates.Linkable import Linkable
from executables.templates.Submodulable import Submodulable
from utils.Hookable import Hookable
from app.App import logger

class ProgressMessage():
    def __init__(self, message, percentage):
        self.message = message
        self.percentage = percentage

class Executable(Documentable, EnvContainable, RecursiveDeclarable, Linkable, Runnable, Saveable, Submodulable, Hookable):
    events = ["error", "progress"]
    section = "Executable"

    def __init__(self):
        super().__init__()

        def __progress_hook(message):
            self.trigger("progress", message=message)

        def __onerror(exception):
            logger.log(exception, section=self.section)

        self.add_hook("progress", __progress_hook)
        self.add_hook("error", __onerror)

    def notifyAboutProgress(self, message, percentage: float = 0.0):
        self.trigger("progress", message=ProgressMessage(message, percentage))
