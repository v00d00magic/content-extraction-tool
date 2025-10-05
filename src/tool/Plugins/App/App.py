from Objects.Increment import Increment
from Objects.Namespace import Namespace
from Objects.Hookable import Hookable
from Objects.Section import Section
from pathlib import Path
import asyncio, sys
import os

from Plugins.Data.Text.Text import Text

class App(Hookable, Namespace):
    events = ["progress"]

    class ExecutablesTable(Section):
        section_name = ["App", "Executables"]

        def __init__(self):
            self.executable_index = Increment()
            self.list = []
            self.calls = []

        def loadList(self):
            from Executables.ExecutableList import ExecutableList

            self.log("Loading list")

            self.list = ExecutableList()

    class Globals(Section):
        section_name = ["App", "Globals"]

        def __init__(self, outer):
            from Plugins.App.Config import Config
            from Plugins.App.Env import Env
            from Plugins.App.Logger import Logger
            from Plugins.App.Logger.LogParts.LogLimiter import LogLimiter
            from DB.DbConnection import DbConnection
            from Plugins.App.Storage import Storage

            outer.Config = Config.Config(
                path = outer.cwd.parent.joinpath("storage").joinpath("config")
            )
            outer.Config.comparer.compare = outer.options
            outer.Env = Env.Env(
                path = self.cwd.parent
            )

            texts = Text()
            _common = texts.NTFSNormalizer(outer.Config.get("storage.path"))
            _common = texts.cwdReplacement(_common)
            _common = texts.cwdReplacement(_common)

            outer.Storage = Storage.Storage(
                common = _common
            )
            outer.Logger = Logger.Logger(
                skip_file = False,
                skip_categories = LogLimiter(outer.Config.get("logger.skip_categories")),
            )
            outer.Logger.constructor()
            outer.Logger.log("Loading globals", section = self.section_name)

            outer.DbConnection = DbConnection()
            outer.DbConnection.attachDbs(self.Config, self.Env)
            outer.DbConnection.createTables()

            #from Utils.Web.DownloadManager import DownloadManager

            #outer.DownloadManager = DownloadManager(max_concurrent_downloads = 2)

    def __init__(self, context_name = "None"):
        super().__init__()

        self.context = context_name
        self.globals = self.Globals(self)
        self.executables = self.ExecutablesTable()
        self.argv = self._parse_argv()
        self.loop = asyncio.get_event_loop()
        self.cwd = Path(os.getcwd())
        self.src = self.cwd.parent

    def _parse_argv(self):
        # didn't changed since sep.2024
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
