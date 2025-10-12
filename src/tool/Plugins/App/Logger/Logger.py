from . import LogLimiter
from .LogParts import LogMessage, LogKind, LogSection, LogFile, LogSkipSection, LogPrefix
from Plugins.Data.NameDictList import NameDictList

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
        self.hooks.trigger("log", logger = self, message = msg)

    def log(self, 
            message: str, 
            section: str = ["App"], 
            kind: str = "message",
            exception_prefix: str = "",
            prefix: LogPrefix.LogPrefix = None):

        write_message = message
        if isinstance(message, BaseException):
            exc = traceback.format_exc()
            write_message = exception_prefix + type(message).__name__ + " " + exc

        _dict = {}
        _dict["message"] = write_message
        _dict["kind"] = LogKind.LogKind(
            kind = kind
        )
        _dict["section"] = LogSection.LogSection(
            section = section
        )

        if prefix != None:
            _dict["prefix"] = prefix

        msg = LogMessage.LogMessage(**_dict)

        self.logMessage(msg)

    def constructor(self):
        if self.skip_file != True:
            self.file = LogFile.LogFile.new()

        self.hooks.register()

    @classproperty
    def options(cls) -> NameDictList:
        from Plugins.Arguments.Types.BooleanArgument import BooleanArgument
        from Plugins.Arguments.Objects.ListArgument import ListArgument
        from Plugins.Arguments.Objects.ObjectArgument import ObjectArgument

        return NameDictList([
            BooleanArgument(
                name = "logger.editing.allow",
                default = True
            ),
            ListArgument(
                name = "logger.output.filters",
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
                name = "logger.output.to_file",
                default = True,
            )
        ])

    class HooksManager(Hookable.HooksManager):
        @property
        def events(self) -> list:
            return ["log"]

        def register(self):
            def hook_WriteToConsole(**kwargs):
                message: LogMessage = kwargs.get("message")
                logger = kwargs.get("logger")

                if logger.limiter.shouldBeDisplayed(message, "console") == True:
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

            self.add("log", hook_WriteToConsole)
