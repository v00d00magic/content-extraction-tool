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

        def initConfig(self, outer):
            from Plugins.App.Config import Config
            from Plugins.App.Env import Env

            outer.Config = Config.Config(
                path = outer.cwd.parent.joinpath("storage").joinpath("config")
            )
            outer.Config.comparer.compare = outer.settings
            outer.Env = Env.Env(
                path = outer.cwd.parent
            )

        def initLogger(self, outer):
            from Plugins.App.Logger import Logger
            from Plugins.App.Logger.LogParts.LogLimiter import LogLimiter

            outer.Logger = Logger.Logger(
                skip_file = outer.Config.get("logger.output.to_file"),
                limiter = LogLimiter(skip_categories = outer.Config.get("logger.output.filters")),
            )
            outer.Logger.constructor()

        def initStorage(self, outer):
            from Plugins.App.Storage import Storage

            outer.Storage = Storage.Storage()

            texts = Text(outer.Config.get("storage.path"))
            _common = texts.cwdReplacement()

            outer.Storage.common = Path(_common)
            outer.Storage.register()

        def initDB(self, outer):
            from Plugins.DB.Connection import Connection

            outer.DbConnection = Connection(
                temp_db = outer.Config.get("db.temp.connection").getWrapper("temp"),
                db = outer.Config.get("db.content.connection").getWrapper("content"),
                instance_db = outer.Config.get("db.instance.connection").getWrapper("instance")
            )
            outer.DbConnection.createTables()

        def __init__(self, outer):
            self.initConfig(outer)
            self.initLogger(outer)
            outer.Logger.log("Init app, loading globals", section = self.section_name)

            self.initStorage(outer)
            #self.initDB(outer)

            #from Utils.Web.DownloadManager import DownloadManager

            #outer.DownloadManager = DownloadManager(max_concurrent_downloads = 2)

    def __init__(self, context_name = "None"):
        super().__init__()

        self.context = context_name

    def consturctor(self):
        self.cwd = Path(os.getcwd())
        self.src = self.cwd.parent
        self.loop = asyncio.get_event_loop()
        self.globals = self.Globals(self)
        self.executables = self.ExecutablesTable()
        self.argv = self._parse_argv()

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
