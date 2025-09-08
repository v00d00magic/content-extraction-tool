from executables.templates.Documentable import Documentable
from executables.templates.EnvContainable import EnvContainable
from executables.templates.RecursiveDeclarable import RecursiveDeclarable
from executables.templates.Runnable import Runnable
from executables.templates.Saveable import Saveable
from executables.templates.Linkable import Linkable
from executables.templates.Submodulable import Submodulable
from utils.Hookable import Hookable
from utils.MainUtils import random_int
from app.App import logger, app

class ProgressMessage():
    def __init__(self, message, percentage, index):
        self.message = message
        self.percentage = percentage
        self.index = index

class Executable(Documentable, EnvContainable, RecursiveDeclarable, Linkable, Runnable, Saveable, Submodulable, Hookable):
    events = ["error", "progress"]
    index = 0
    section = "Executable"

    def __init__(self, executable_index = None):
        super().__init__()
        self.index = executable_index
        if self.index == None:
            self.index = random_int(0, 10000)

        # it doesnt makes sense to trigger submodules so we calling app
        def __progress_hook(message):
            app.trigger("progress", message=message)

        def __onerror(exception):
            logger.log(exception, section=self.section)

        # doesnt makes sense to trigger on executable
        # cuz it will probaly be submodule
        self.add_hook("progress", __progress_hook)
        self.add_hook("error", __onerror)

    def notifyAboutProgress(self, message, percentage: float = 0.0):
        self.trigger("progress", message=ProgressMessage(message, percentage, self.index))
