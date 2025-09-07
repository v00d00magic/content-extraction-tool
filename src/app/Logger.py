from colorama import init as ColoramaInit
from utils.MainUtils import parse_json, dump_json
from pathlib import Path
from datetime import datetime
from utils.Hookable import Hookable
import traceback

class Logger(Hookable):
    '''
    Module for logging of messages and printing them to terminal
    '''

    events = ["log"]
    file_checked = False
    current_json = None

    # CONSTS

    KIND_SUCCESS = 'success'
    KIND_ERROR = 'error'
    KIND_DEPRECATED = 'deprecated'
    KIND_MESSAGE = 'message'

    MODE_PER_DAY = 0
    MODE_PER_STARTUP = 1

    SECTION_SERVICES = 'Services'
    SECTION_DB = 'DB'
    SECTION_LINKAGE = 'Linkage'
    SECTION_EXECUTABLES = 'Executables'
    SECTION_SAVEABLE = 'Saveable'
    SECTION_EXTRACTORS = 'Extractors'
    SECTION_ACTS = 'Acts'
    SECTION_WEB = 'Web'

    def log(self, message, section: str = "App", kind: str = "message", silent: bool = False, prefix: str = ""):
        write_message = message
        if isinstance(message, BaseException):
            __exp = traceback.format_exc()
            write_message = prefix + type(message).__name__ + " " + __exp

        return self.log_({
            "message": write_message,
            "section": section,
            "kind": kind,
            "silent": silent
        })

    def log_(self, data):
        should = {
            "web": True,
            "cli": data.get("silent") == False,
            "file": self.skip_file == False
        }

        for item in self.skip_categories:
            category = LoggerCategory(item)
            should = category.check(data.get("section"), data.get("kind"))

        message = LogMessage({
            "time": (datetime.now()).timestamp(),
            "section": data.get("section"),
            "message": data.get("message"),
            "kind": data.get("kind"),
            "should": should,
        })
        self.__log_file_check()
        self.__console_hook(message=message) # not a hook cuz its uses async and prints wrong

        self.trigger("log", message=message)

        return message

    def __init__(self, config, storage):
        super().__init__() # for hookable

        ColoramaInit()

        self.write_mode = self.MODE_PER_STARTUP
        self.logs_storage = storage.sub('logs')
        self.skip_categories = config.get("logger.skip_categories")
        self.skip_file = config.get("logger.skip_file") == 1

        self.add_hook("log", self.__write_to_file_hook)

    def __console_hook(self, **kwargs):
        message = kwargs.get("message")
        if message.should("cli") == True:
            message.print_self()

    def __write_to_file_hook(self, **kwargs):
        if self.skip_file == True:
            return False

        message = kwargs.get("message")
        if message.should("file") == True:
            return

        if self.current_json == None:
            try:
                self.current_json = parse_json(self.log_stream.read())
            except:
                self.current_json = []

        self.current_json.append(message.data)

        self.log_stream.truncate(0)
        self.log_stream.seek(0)
        self.log_stream.write(dump_json(self.current_json, indent=4))

    def __del__(self):
        try:
            self.save()
            self.log_stream.close()
        except AttributeError:
            pass

    def __log_file_check(self):
        if self.skip_file == True:
            return True
        if self.file_checked == True:
            return True

        now = datetime.now()
        match(self.write_mode):
            case self.MODE_PER_STARTUP:
                self.path = Path(f"{self.logs_storage.dir}/{now.strftime('%Y-%m-%d_%H-%M-%S')}.json")
            case self.MODE_PER_DAY:
                self.path = Path(f"{self.logs_storage.dir}/{now.strftime('%Y-%m-%d')}.json")

        if self.path.exists() == False:
            _not_exists = open(self.path, 'w', encoding='utf-8')
            _not_exists.close()

        self.log_stream = open(str(self.path), 'r+', encoding='utf-8')
        self.file_checked = True

        return True

    def save(self):
        self.log_stream.flush()

class LoggerCategory():
    def __init__(self, data):
        if type(data) == str:
            self.data = {"name":data}
        else:
            self.data = data

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

        if name == section:
            should_ = False
        else:
            if section.find(name) != -1 and wildcard == True:
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

    def out(self):
        return self.data

    def print_self(self):
        section = self.data.get("section")
        message = self.data.get("message")
        kind = self.data.get("kind")
        date = datetime.fromtimestamp(self.data.get("time"))

        write_message = f"{date.strftime("%Y-%m-%d %H:%M:%S")} [{section}] {message}\n"
        write_message = write_message.replace("\\n", "\n")
        write_colored_message = ""

        if kind == Logger.KIND_ERROR:
            write_colored_message = "\033[91m" + write_message + "\033[0m"
        elif kind == Logger.KIND_SUCCESS:
            write_colored_message = "\033[92m" + write_message + "\033[0m"
        elif kind == Logger.KIND_DEPRECATED:
            write_colored_message = "\033[93m" + write_message + "\033[0m"
        else:
            write_colored_message = write_message

        print(write_colored_message, end='')

    def should(self, where):
        return self.data.get("should").get(where) == True
