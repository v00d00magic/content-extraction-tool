from Utils.Wrap import Wrap
from App.Logger.LogKind import LogKind
from App.Logger.LogSection import LogSection
from datetime import datetime

class LogMessage(Wrap):
    message: str = None
    kind: LogKind = None
    time: int = None
    section: LogSection = None
    id_prefix: int = None

    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "white": "\033[0m",
        "cyan": "\u001b[36m",
        "pink": "\u001b[35m"
    }

    def out(self):
        return {
            "message": self.message,
            "kind": self.kind.kind,
            "time": self.time,
            "section": self.section,
            "id_prefix": self.id_prefix,
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
