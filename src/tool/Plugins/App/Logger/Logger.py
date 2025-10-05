from .LogParts import LogMessage, LogKind, LogSection, LogLimiter, LogFile, LogSkipSection
from Plugins.Arguments.ArgumentList import ArgumentList

from Objects.Configurable import Configurable
from Plugins.Data.JSON.JSON import JSON
from Objects.Hookable import Hookable
from datetime import datetime

from pydantic import Field
from Objects.Object import Object

import traceback

class Logger(Object, Hookable, Configurable):
    skip_file: int = Field(default=False)
    limiter: LogLimiter = LogLimiter()
    file: LogFile = Field(default=None)

    events: list = ["log"]

    def constructor(self):
        super().__init__()

        self.file = None
        self.setFile(self.newFile())

        def hook_WriteToConsole(**kwargs):
            message = kwargs.get("message")
            if self.limiter.shouldBeDisplayed(message, "console") == True:
                message.print()

        def hook_WriteToFile(**kwargs):
            return
            message = kwargs.get("message")
            if message.should("file") == True:
                return

            self.file_stream.truncate(0)
            self.file_stream.seek(0)
            self.file_stream.write(JSON(self.logs).dump(indent=4))

        self.addHook("log", hook_WriteToConsole)
        #self.addHook("log", hook_WriteToFile)

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

    @property
    def options() -> ArgumentList:
        return ArgumentList([
            BooleanArgument(
                name = "logger.external_watching.allow",
                default = True
            ),
            ListArgument(
                name = "logger.skip_categories",
                default = [
                    LogSkipSection({
                        "name": ["Executables", "Initialization"],
                        "kinda": "message",
                        "wildcard": True,
                    }), 
                    LogSkipSection({
                        "name": ["Executables", "Declaration"],
                        "kinda": "message",
                        "wildcard": True,
                    }),
                    LogSkipSection({
                        "name": ["Saveable", "Container"],
                        "wildcard": False,
                    })
                ],
                orig = ClassArgument(
                    wrap = LogSkipSection
                )
            ),
            BooleanArgument(
                name = "logger.skip_file"
                default = 0,
            )
        ])

    def setFile(self, file: LogFile):
        self.file = file

    def newFile(self) -> LogFile:
        if self.skip_file == True:
            return None

        file = LogFile()
        file.create(0, self.storage)

        return file
