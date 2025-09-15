from app.App import logger, app

class ProgressMessage():
    def __init__(self, message, percentage, index):
        self.message = message
        self.percentage = percentage
        self.index = index

class Progressable:
    events = ["error", "progress"]
    index = 0

    def __init__(self):
        super().__init__()

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
