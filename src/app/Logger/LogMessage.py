from utils.Wrap import Wrap
from app.Logger.LogKind import LogKind
from app.Logger.LogSection import LogSection
from datetime import datetime

class LogMessage(Wrap):
    message: str
    kind: LogKind
    time: int
    section: LogSection
    time: int
    id: int

    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "white": "\033[0m",
        "cyan": "\u001b[36m",
        "pink": "\u001b[35m"
    }

    def getSection(self, as_string = False):
        _section = self.data.get("section")
        _section_list = _section

        if type(_section) == str:
            _section_list = _section.split("!")

        if as_string == True:
            return "!".join(_section_list)
        else:
            return _section_list

    def out(self):
        return {
            "message": self.message,
            "kind": self.kind.kind,
            "time": self.time,
            "section": self.section,
            "id": self.id,
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

        print_parts = []

        print_parts.append(date.strftime("%H:%M:%S.%f"))        
        print_parts.append(self.colors.get("pink") + "[" + self.section.str() + "]" + self.colors.get('white'))

        if self.id != None:
            print_parts.append(self.colors.get('cyan') + f"ID->{self.id}" + self.colors.get('white'))

        print_parts.append(self.message)
        #print_parts.append("\n")
        print_parts.append(self.colors.get('white'))

        write_message = color + " ".join(print_parts) + self.colors.get('white')
        write_message = write_message.replace("\\n", "\n")

        print(write_message, end='\n')

    def should(self, where):
        return True
