from .LogParts import LogMessage, LogKind, LogSection, LogLimiter, LogFile, LogSkipSection
from Plugins.Arguments.ArgumentList import ArgumentList

from Objects.Configurable import Configurable
from Objects.Hookable import Hookable
from Objects.classproperty import classproperty
from datetime import datetime

from pydantic import Field
from Objects.Object import Object

import traceback

class Logger(Object, Hookable, Configurable):
    skip_file: bool = Field(default=False)
    limiter: LogLimiter.LogLimiter = Field(default=None)
    file: LogFile.LogFile = Field(default=None)

    def logMessage(self, msg: LogMessage):
        #self.file.add(msg)
        self.trigger("log", message=msg)

    def log(self, message, section: str = "App", kind: str = "message", silent: bool = False, prefix: str = "", id_prefix: int = None):
        print(message)
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
    def events() -> list:
        return ["log"]

    def constructor(self):
        super().__init__()

        if self.skip_file != True:
            self.file = LogFile.LogFile.new()

        self.addHooks()

    def addHooks(self):
        def hook_WriteToConsole(**kwargs):
            message: LogMessage = kwargs.get("message")
            if self.limiter.shouldBeDisplayed(message, "console") == True:
                print(message.toString(), end='\n')

        def hook_WriteToFile(**kwargs):
            return
            #from Plugins.Data.JSON.JSON import JSON

            message = kwargs.get("message")
            if message.should("file") == True:
                return

            self.file_stream.truncate(0)
            self.file_stream.seek(0)
            self.file_stream.write(JSON(self.logs).dump(indent=4))

        self.addHook("log", hook_WriteToConsole)

    @classproperty
    def options(cls) -> ArgumentList:
        from Plugins.Arguments.Types.BooleanArgument import BooleanArgument
        from Plugins.Arguments.Objects.ListArgument import ListArgument
        from Plugins.Arguments.Objects.ObjectArgument import ObjectArgument

        return ArgumentList([
            BooleanArgument(
                name = "logger.external_watching.allow",
                default = True
            ),
            ListArgument(
                name = "logger.skip_categories",
                default = [
                    LogSkipSection.LogSkipSection(
                        name = ["Executables", "Initialization"],
                        kinda = ["message"],
                        wildcard = True
                    ), 
                    LogSkipSection.LogSkipSection(
                        name = ["Executables", "Declaration"],
                        kinda = ["message"],
                        wildcard = True
                    ),
                    LogSkipSection.LogSkipSection(
                        name = ["Saveable", "Container"],
                        kinda = ["message"],
                    )
                ],
                orig = ObjectArgument(
                    name = "skip_category",
                    object = LogSkipSection.LogSkipSection
                )
            ),
            BooleanArgument(
                name = "logger.skip_file",
                default = 0,
            )
        ])
