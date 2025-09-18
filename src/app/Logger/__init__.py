from colorama import init as ColoramaInit
from app.Logger.LogFile import LogFile
from utils.Data.JSON import JSON
from utils.Data.List import List
from utils.Hookable import Hookable
import traceback

class Logger(Hookable):
    events = ["log"]

    KIND_SUCCESS = 'success'
    KIND_ERROR = 'error'
    KIND_DEPRECATED = 'deprecated'
    KIND_MESSAGE = 'message'

    SECTION_ACTS = 'Acts'
    SECTION_DB = 'DB'
    SECTION_EXECUTABLES = 'Executables'
    SECTION_EXTRACTORS = 'Extractors'
    SECTION_LINKAGE = 'Linkage'
    SECTION_SERVICES = 'Services'
    SECTION_SAVEABLE = 'Saveable'
    SECTION_WEB = 'Web'

    def __init__(self, config, storage):
        super().__init__()

        ColoramaInit()

        self.storage = storage.get('logs')
        self.file = None
        self.setFile()

        self.skip_categories = config.get("logger.skip_categories")
        self.skip_file = config.get("logger.skip_file") == 1

        def console_hook(**kwargs):
            message = kwargs.get("message")
            if message.should("cli") == True:
                message.print_self()

        def write_to_file_hook(**kwargs):
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

        self.add_hook("log", console_hook)
        self.add_hook("log", write_to_file_hook)

    def setFile(self):
        if self.skip_file == True:
            return None

        file = LogFile()
        file.create(0, self.storage)

        self.file = file

    def log(self, message, section: str = "App", kind: str = "message", silent: bool = False, prefix: str = "", id: int = None):
        write_message = message
        if isinstance(message, BaseException):
            __exp = traceback.format_exc()
            write_message = prefix + type(message).__name__ + " " + __exp

        return self.logObject({
            "message": write_message,
            "section": section,
            "kind": kind,
            "silent": silent,
            "id": id,
        })

    def logObject(self, data):
        should = {
            "web": True,
            "cli": data.get("silent") == False,
            "file": self.skip_file == False
        }

        message = LogMessage({
            "time": (datetime.now()).timestamp(),
            "section": data.get("section"),
            "message": data.get("message"),
            "kind": data.get("kind"),
            "id": data.get("id"),
            "should": should,
        })
        for item in self.skip_categories:
            category = LoggerCategory(item)
            should = category.check(message.getSection(), message.getKind())

        self.trigger("log", message=message)

        return message

    def __del__(self):
        try:
            self.save()
            self.log_stream.close()
        except AttributeError:
            pass

    def save(self):
        self.log_stream.flush()

class LoggerCategory():
    def __init__(self, data):
        if type(data) == str:
            self.data = {"name":data}
        else:
            self.data = data

    # TODO refactor
    def check(self, section, kind = None):
        name = self.data.get("name")
        wildcard = self.data.get("wildcard", False)
        kinda = self.data.get("kinda")
        where = self.data.get("where", "*")
        should_ = True

        should = {
            "web": True,
            "cli": True,
            "file": True
        }

        _name = ".".join(List(name).convert())
        _compare = ".".join(List(section).convert())
        if _name == _compare or (_compare.find(_name) != -1 and wildcard == True):
            should_ = False

        if should_ == False:
            if kinda != None:
                should_ = kind != kinda

        if where == "*":
            # ((
            should["web"] = should_
            should["cli"] = should_
            should["file"] = should_
        else:
            should[where] = should_

        return should

class LogMessage():
    def __init__(self, data):
        self.data = data

    def getKind(self):
        return self.data.get("kind")

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
        return self.data

    def print_self(self):
        section = self.data.get("section")
        message = self.data.get("message")
        kind = self.data.get("kind")
        id = self.data.get("id")
        date = datetime.fromtimestamp(self.data.get("time"))

        write_message = f"{date.strftime("%H:%M:%S.%f")} [{self.getSection(True)}] {message}"
        if id != None:
            write_message = f"ID->{id} " + write_message

        write_message += "\n"
        write_message = write_message.replace("\\n", "\n")
        write_colored_message = ""

        match(kind):
            case Logger.KIND_ERROR:
                write_colored_message = "\033[91m" + write_message + "\033[0m"
            case Logger.KIND_SUCCESS:
                write_colored_message = "\033[92m" + write_message + "\033[0m"
            case Logger.KIND_DEPRECATED:
                write_colored_message = "\033[93m" + write_message + "\033[0m"
            case _:
                write_colored_message = write_message

        print(write_colored_message, end='')

    def should(self, where):
        print(self.data.get("should"))
        return self.data.get("should").get(where) == True
