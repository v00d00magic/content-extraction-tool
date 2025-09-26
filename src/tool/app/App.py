from utils.Hookable import Hookable
from utils.Increment import Increment

from pathlib import Path
import asyncio, sys
import platform, os

class App(Hookable):
    incremental_executable_index = 0
    context = "cli"
    events = ["progress"]

    def _parse_argv(self):
        args = sys.argv
        parsed_args = {}
        key = None
        for arg in args[1:]:
            if arg.startswith('--'):
                if key:
                    parsed_args[key] = True
                key = arg[2:]
                parsed_args[key] = True
            else:
                if key:
                    parsed_args[key] = arg
                    key = None
                else:
                    pass

        return parsed_args

    def __init__(self):
        super().__init__()

        self.argv = self._parse_argv()
        self.loop = asyncio.get_event_loop()
        self.executable_index = Increment()
        self.setConsts()

    def setConsts(self):
        self.consts = {}
        self.cwd = Path(os.getcwd())
        self.src = self.cwd.parent
        self.consts["os.name"] = platform.system()
        self.consts["pc.name"] = os.getenv("COMPUTERNAME", "NoName-PC")
        self.consts["pc.user"] = os.getlogin()
        self.consts["pc.fullname"] = self.consts["pc.name"] + ", " + self.consts["pc.user"]

    def setup(self):
        from executables.ExecutableMap import ExecutableMap

        self.indexated_scripts = ExecutableMap()

app = App()
