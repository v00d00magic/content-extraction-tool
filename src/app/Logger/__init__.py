from colorama import init as ColoramaInit
from app.Logger.LogFile import LogFile
from app.Logger.LogMessage import LogMessage
from app.Logger.LogKind import LogKind
from app.Logger.LogSection import LogSection
from app.Logger.LogLimiter import LogLimiter
from utils.Data.JSON import JSON
from utils.Hookable import Hookable
from datetime import datetime
import traceback

class Logger(Hookable):
    events = ["log"]

    def __init__(self, config, storage):
        super().__init__()

        ColoramaInit()

        self._skip_file = config.get("logger.skip_file") == 1

        self.limiter = LogLimiter(config.get("logger.skip_categories"))
        self.storage = storage.get('logs')
        self.file = None
        self.setFile(self.newFile())

        def writeToConsoleHook(**kwargs):
            message = kwargs.get("message")
            if self.limiter.shouldBeDisplayed(message, "console") == True:
                message.print()

        def writeToFileHook(**kwargs):
            message = kwargs.get("message")
            if message.should("file") == True:
                return

            if self.logs == None:
                try:
                    self.logs = JSON(self.log_stream.read()).parse()
                except:
                    self.logs = []

            self.logs.append(message.data)

            self.file_stream.truncate(0)
            self.file_stream.seek(0)
            self.file_stream.write(JSON(self.logs).dump(indent=4))

        self.add_hook("log", writeToConsoleHook)
        #self.add_hook("log", write_to_file_hook)

    def newFile(self) -> LogFile:
        if self._skip_file == True:
            return None

        file = LogFile()
        file.create(0, self.storage)

        return file

    def setFile(self, file: LogFile):
        self.file = file

    def logMessage(self, msg: LogMessage):
        self.file.add(msg)
        self.trigger("log", message=msg)

    def log(self, message, section: str = "App", kind: str = "message", silent: bool = False, prefix: str = "", id: int = None):
        write_message = message
        if isinstance(message, BaseException):
            exc = traceback.format_exc()
            write_message = prefix + type(message).__name__ + " " + exc

        msg = LogMessage({
            "time": (datetime.now()).timestamp(),
            "message": write_message,
            "section": LogSection({"section": section}),
            "kind": LogKind({"kind": kind}),
            "id": id,
        })

        self.logMessage(msg)
