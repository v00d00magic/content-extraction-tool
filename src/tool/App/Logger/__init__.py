from colorama import init as ColoramaInit
from App.Logger.LogFile import LogFile

# Maybe its better to create LogPart class?
from App.Logger.LogMessage import LogMessage
from App.Logger.LogKind import LogKind
from App.Logger.LogSection import LogSection
from App.Logger.LogLimiter import LogLimiter

from Utils.Configurable import Configurable
from Utils.Data.JSON import JSON
from Utils.Hookable import Hookable
from datetime import datetime

from Declarable.Arguments import Argument, StringArgument, ClassArgument, CsvArgument, BooleanArgument
from App.Logger.LogSkipSection import LogSkipSection
from Declarable.Documentation import global_documentation

import traceback

class Logger(Hookable, Configurable):
    events = ["log"]

    def __init__(self, config, storage):
        super().__init__()

        ColoramaInit()

        self.__class__.updateConfig()
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

    def log(self, message, section: str = "App", kind: str = "message", silent: bool = False, prefix: str = "", id_prefix: int = None):
        write_message = message
        if isinstance(message, BaseException):
            exc = traceback.format_exc()
            write_message = prefix + type(message).__name__ + " " + exc

        msg = LogMessage({
            "time": (datetime.now()).timestamp(),
            "message": write_message,
            "section": LogSection({"section": section}),
            "kind": LogKind({"kind": kind}),
            "id_prefix": id_prefix,
        })

        self.logMessage(msg)

    @classmethod
    def declareSettings(cls):
        locale_keys = {
            "logger.skip_categories.name": {
                "en_US": "Ignored categories",
            },
            "logger.skip_categories.definition": {
                "en_US": "List of categories that will not be displayed from the logger",
            },
            "logger.skip_file.name": {
                "en_US": "Do not write logs into the file",
            },
        }
        global_documentation.loadKeys(locale_keys)

        items = {}
        items["logger.skip_categories"] = CsvArgument({
            "default": [
                LogSkipSection({
                    "name": ["Executables", "Initialization"],
                    "kinda": "message"
                }), 
                LogSkipSection({
                    "name": ["Executables", "Declaration"],
                    "kinda": "message",
                }),
                LogSkipSection({
                    "name": ["Saveable", "Container"],
                    "wildcard": False,
                })
            ],
            "orig": ClassArgument({
                "class": LogSkipSection
            }),
            "docs": {
                "name": global_documentation.get("logger.skip_categories.name"),
                "definition": global_documentation.get("logger.skip_categories.definition"),
            },
        })
        items["logger.skip_file"] = BooleanArgument({
            "default": 0,
            "docs": {
                "name": global_documentation.get("logger.skip_file.name"),
            },
        })

        return items
