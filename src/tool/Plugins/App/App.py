from Objects.Object import Object
from Objects.Increment import Increment
from Objects.Hookable import Hookable
from Objects.Section import Section
from pathlib import Path
from typing import Any
import asyncio, sys
import os

from Plugins.Data.Text import Text

from pydantic import Field

class App(Object, Hookable, Section):
    context_name: str = Field(default = 'none')
    settings: dict = {}
    cwd: str = None
    src: str = None
    loop: Any = None

    Config: Any = None
    Env: Any = None
    Storage: Any = None
    Logger: Any = None
    Storage: Any = None
    DbConnection: Any = None
    DownloadManager: Any = None
    ExecutablesTable: Any = None

    _globals: Any = None
    argv: dict = None

    class Globals(Section):
        class ExecutablesTable(Section):
            def __init__(self):
                from .Index.PluginsList import PluginsList

                self.executable_index = Increment()
                self.list = PluginsList()
                self.list.load()
                self.calls = []

        def initConfig(self, outer):
            from Plugins.App.Config import Config

            outer.Config = Config.Config(
                path = outer.cwd.parent.joinpath("storage").joinpath("config")
            )
            outer.Config.comparer.compare = outer.settings

        def initEnv(self, outer):
            from Plugins.App.Env import Env
            
            outer.Env = Env.Env(
                path = outer.cwd.parent.joinpath("storage").joinpath("env"),
                name = "env.json"
            )

        def initLogger(self, outer):
            from Plugins.App.Logger import Logger
            from Plugins.App.Logger.LogLimiter import LogLimiter

            outer.Logger = Logger.Logger(
                skip_file = outer.Config.get("logger.output.to_file"),
                limiter = LogLimiter(skip_categories = outer.Config.get("logger.output.filters")),
            )

        def initStorage(self, outer):
            from Plugins.App.Storage import Storage

            outer.Storage = Storage.Storage()

            text = Text.use(
                text = outer.Config.get('storage.path')
            )
            text.replaceCwd()

            outer.Storage.common = Path(text.content.text)
            outer.Storage.register()

        def initDB(self, outer):
            from Plugins.App.DB.Connection import Connection

            outer.DbConnection = Connection(
                temp_db = outer.Config.get("db.temp.connection").getWrapper("temp"),
                db = outer.Config.get("db.content.connection").getWrapper("content"),
                instance_db = outer.Config.get("db.instance.connection").getWrapper("instance")
            )
            outer.DbConnection.createTables()

        def initDownloadManager(self, outer):
            from Plugins.Web.DownloadManager.DownloadManager import DownloadManager

            outer.DownloadManager = DownloadManager(
                max_concurrent_downloads = outer.Config.get("media.download_manager.max_concurrent_downloads"),
                max_kbps_speed = outer.Config.get("media.download_manager.max_kbps_speed"),
                connection_timeout = outer.Config.get("media.download_manager.connection_timeout"),
            )

        def initExecutablesTable(self, outer):
            outer.ExecutablesTable = self.ExecutablesTable()

        def __init__(self, outer):
            section_name = ["App", "Globals"]

            self.initExecutablesTable(outer)
            self.initConfig(outer)
            self.initEnv(outer)
            self.initLogger(outer)

            outer.Logger.log("Init app, loading globals", section = section_name)

            self.initStorage(outer)
            self.initDB(outer)
            self.initDownloadManager(outer)

            outer.Logger.log("Loaded globals", section = section_name)

    class HooksManager(Hookable.HooksManager):
        @property
        def events(self) -> list:
            return ["progress"]

    def _constructor(self):
        self.argv = self._parse_argv()
        self.cwd = Path(os.getcwd())
        self.src = self.cwd.parent
        self.loop = asyncio.get_event_loop()
        self._globals = self.Globals(self)

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
