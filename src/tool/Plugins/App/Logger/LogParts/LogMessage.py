from Objects.Object import Object
from . import LogKind, LogSection, LogPrefix
from pydantic import Field
from datetime import datetime

class LogMessage(Object):
    message: str = Field(default="No message passed")
    kind: LogKind.LogKind
    time: int = Field(default=lambda: (datetime.now()).timestamp())
    section: LogSection.LogSection = Field(default=["N/A"])
    prefix: LogPrefix.LogPrefix = Field(default=None)

    def toString(self):
        date = datetime.fromtimestamp(self.time)
        KIND_COLOR = self.kind.getColor()
        RESET = LogKind.ColorsEnum.reset.value

        parts = []
        parts.append(date.strftime("%H:%M:%S.%f"))        
        parts.append(LogKind.ColorsEnum.pink.value + self.section.toString() + RESET)
        if self.prefix != None:
            parts.append(LogKind.ColorsEnum.cyan.value + self.prefix.toString() + RESET)

        parts.append(KIND_COLOR + self.message + RESET)
        parts.append(RESET)

        return " ".join(parts).replace("\\n", "\n")
