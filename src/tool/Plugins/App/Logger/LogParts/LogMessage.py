from Objects.Object import Object
from Plugins.App.Logger.LogParts.LogKind import LogKind
from Plugins.App.Logger.LogParts.LogSection import LogSection
from pydantic import Field
from datetime import datetime

class LogMessage(Object):
    message: str = Field(default="No message passed")
    kind: LogKind = Field(default=LogKind.KIND_MESSAGE)
    time: int = Field(default=lambda: (datetime.now()).timestamp())
    section: LogSection = Field(default=["Not passed!"])
    prefix: str = Field(default="0")

    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "white": "\033[0m",
        "cyan": "\u001b[36m",
        "pink": "\u001b[35m"
    }

    def print(self):
        date = datetime.fromtimestamp(self.time)
        color = ""

        match(self.kind.kind):
            case LogKind.KIND_ERROR:
                color = self.colors.get('red')
            case LogKind.KIND_SUCCESS:
                color = self.colors.get('green')
            case LogKind.KIND_DEPRECATED:
                color = self.colors.get('yellow')
            case LogKind.KIND_HIGHLIGHT:
                color = self.colors.get('pink')

        print_parts = []

        print_parts.append(date.strftime("%H:%M:%S.%f"))        
        print_parts.append(self.colors.get("pink") + "[" + self.section.str() + "]" + self.colors.get('white'))

        if self.id_prefix != None:
            print_parts.append(self.colors.get('cyan') + self.id_prefix + self.colors.get('white'))

        print_parts.append(color + self.message + self.colors.get('white'))
        #print_parts.append("\n")
        print_parts.append(self.colors.get('white'))

        write_message = " ".join(print_parts)
        write_message = write_message.replace("\\n", "\n")

        print(write_message, end='\n')
